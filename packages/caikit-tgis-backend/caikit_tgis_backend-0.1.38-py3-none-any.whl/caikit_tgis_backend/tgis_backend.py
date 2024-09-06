# Copyright The Caikit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module implements a TGIS backend configuration"""

# Standard
from copy import deepcopy
from threading import Lock
from typing import Any, Dict, Optional, Tuple, Union

# Third Party
import grpc

# Since fastapi is optional in caikit, it may not be available
try:
    # Third Party
    import fastapi

    HAVE_FASTAPI = True
except ImportError:
    HAVE_FASTAPI = False
    fastapi = None

# First Party
from caikit.core.exceptions import error_handler
from caikit.core.module_backends.backend_types import register_backend_type
from caikit.core.module_backends.base import BackendBase
from caikit.interfaces.runtime.data_model import RuntimeServerContextType
import alog

# Local
from .managed_tgis_subprocess import ManagedTGISSubprocess
from .protobufs import generation_pb2_grpc
from .tgis_connection import TGISConnection

log = alog.use_channel("TGISBKND")
error = error_handler.get(log)


# pylint: disable=too-many-instance-attributes
class TGISBackend(BackendBase):
    """Caikit backend with a connection to the TGIS server. If no connection
    details are given, this backend will manage an instance of the TGIS as a
    subprocess for the lifecycle of the model that needs it.

    NOTE: Currently TGIS does not support multiple models, so when running TGIS
        locally, calls to get a client for a model _other_ than the first one
        will fail!

    TODO: To handle multi-model TGIS, we can maintain an independent process for
        each model. To do this, we'd need to dynamically generate the port and
        then yield the right client connection when a given model is requested.
    """

    TGIS_LOCAL_GRPC_PORT = 50055
    TGIS_LOCAL_HTTP_PORT = 3000

    # HTTP Header / gRPC Metadata key used to identify a route override in an
    # inbound request context
    ROUTE_INFO_HEADER_KEY = "x-route-info"

    ## Backend Interface ##

    backend_type = "TGIS"

    # TODO: consider potential refactor with TGIS connection class for
    # the many instance attributes
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)

        # NOTE: Needs to be set before any possible errors since it's used in
        #   the destructor
        self._mutex = Lock()
        self._local_tgis = None
        self._managed_tgis = None
        self._model_connections: Dict[str, TGISConnection] = {}
        self._test_connections = self.config.get("test_connections", False)
        self._connect_timeout = self.config.get("connect_timeout", None)

        # Parse the config to see if we're managing a connection to a remote
        # TGIS instance or running a local copy
        connection_cfg = self.config.get("connection") or {}
        error.type_check("<TGB20235229E>", dict, connection=connection_cfg)
        self._remote_models_cfg: Dict[str, dict] = (
            self.config.get("remote_models") or {}
        )
        error.type_check("<TGB20235338E>", dict, connection=self._remote_models_cfg)
        local_cfg = self.config.get("local") or {}
        error.type_check("<TGB20235225E>", dict, local=local_cfg)

        # The base connection config is valid IFF there's a hostname
        conn_hname = connection_cfg.get("hostname")
        self._base_connection_cfg = connection_cfg if conn_hname else None
        error.value_check(
            "<TGB20235231E>",
            not conn_hname or ":" in self._base_connection_cfg.get("hostname", ""),
            "Invalid base configuration: {}",
            self._base_connection_cfg,
        )
        error.value_check(
            "<TGB45582311E>",
            self._base_connection_cfg is None
            or TGISConnection.from_config("__TEST__", self._base_connection_cfg)
            is not None,
            "Invalid base connection: {}",
            self._base_connection_cfg,
        )

        # Parse connection objects for all model-specific connections
        for model_id, model_conn_cfg in self._remote_models_cfg.items():
            model_conn = TGISConnection.from_config(model_id, model_conn_cfg)

            log.debug(
                "model connection config and model_id are set to the following: %s , %s",
                model_conn_cfg,
                model_id,
            )
            error.value_check(
                "<TGB90377847E>",
                model_conn is not None,
                "Invalid connection config for {}",
                model_id,
            )
            if self._test_connections:
                model_conn = self._test_connection(model_conn, self._connect_timeout)
            if model_conn is not None:
                self._safely_update_state(model_id, model_conn)

        # We manage a local TGIS instance if there are no remote connections
        # specified as either a valid base connection or remote_connections
        self._local_tgis = not self._base_connection_cfg and not self._remote_models_cfg
        log.info("Running %s TGIS backend", "LOCAL" if self._local_tgis else "REMOTE")

        if self._local_tgis:
            log.info("<TGB20235227I>", "Managing local TGIS instance")
            self._managed_tgis = ManagedTGISSubprocess(
                grpc_port=local_cfg.get("grpc_port") or self.TGIS_LOCAL_GRPC_PORT,
                http_port=local_cfg.get("http_port") or self.TGIS_LOCAL_HTTP_PORT,
                bootup_poll_delay=local_cfg.get("health_poll_delay", 1.0),
                health_poll_timeout=local_cfg.get("health_poll_timeout", 10),
                load_timeout=local_cfg.get("load_timeout", 30),
                num_gpus=local_cfg.get("num_gpus", 1),
                prompt_dir=local_cfg.get("prompt_dir"),
            )

    def __del__(self):
        # TODO: When adding multi-model support, we'll need to call this for
        #   each loaded model
        self.unload_model("")

    # pylint: disable=unused-argument
    def register_config(self, config: Dict) -> None:
        """Function to merge configs with existing configurations"""
        error(
            "<TGB20236213E>",
            AssertionError(
                f"{self.backend_type} backend does not support this operation"
            ),
        )

    def start(self):
        """Start backend, initializing the client"""
        self._started = True

    def stop(self):
        """Stop backend and unload all models"""
        self._started = False
        for model_id in list(self._model_connections.keys()):
            log.debug("Unloading model %s on stop", model_id)
            self.unload_model(model_id)

    def handle_runtime_context(
        self,
        model_id: str,
        runtime_context: RuntimeServerContextType,
    ):
        """Handle the runtime context for a request for the given model"""
        if route_info := self.get_route_info(runtime_context):
            log.debug(
                "<TGB10705560D> Registering remote model connection with context "
                "override: 'hostname: %s'",
                route_info,
            )
            self.register_model_connection(
                model_id,
                {"hostname": route_info},
                fill_with_defaults=True,
            )
        else:
            log.debug(
                "<TGB32948346D> No %s context override found",
                self.ROUTE_INFO_HEADER_KEY,
            )

    ## Backend user interface ##

    def get_connection(
        self, model_id: str, create: bool = True
    ) -> Optional[TGISConnection]:
        """Get the TGISConnection object for the given model"""
        model_conn = self._model_connections.get(model_id)
        conn_cfg = self._remote_models_cfg.get(model_id, self._base_connection_cfg)
        if not model_conn and create and not self.local_tgis and conn_cfg:
            model_conn = TGISConnection.from_config(model_id, conn_cfg)
            if self._test_connections:
                model_conn = self._test_connection(model_conn)
            if model_conn is not None:
                self._safely_update_state(model_id, model_conn)

        return model_conn

    def register_model_connection(
        self,
        model_id: str,
        conn_cfg: Optional[Dict[str, Any]] = None,
        fill_with_defaults: bool = True,
    ) -> None:
        """
        Register a remote model connection.

        If a local TGIS instance is maintained, do nothing.

        If the model connection is already registered, do nothing.

        Otherwise create and register the model connection using the TGISBackend's
        config connection, or the `conn_cfg` if provided.

        If `fill_with_defaults == True`, missing keys in `conn_cfg` will be populated
        with defaults from the TGISBackend's config connection.
        """
        # Don't attempt registering a remote model if running local TGIS instance
        if self.local_tgis:
            log.debug(
                "<TGB99277346D> Running a local TGIS instance... won't register a "
                "remote model connection"
            )
            return

        if model_id in self._model_connections:
            log.debug(
                "<TGB08621956D> remote model connection for model %s already exists... "
                "nothing to register",
                model_id,
            )
            return  # Model connection exists --> do nothing

        # Craft new connection config
        new_conn_cfg = {}
        if conn_cfg is None:
            new_conn_cfg = deepcopy(self._base_connection_cfg)
        else:
            if fill_with_defaults:
                new_conn_cfg = deepcopy(self._base_connection_cfg)
            new_conn_cfg.update(conn_cfg)

        # Create model connection
        error.value_check(
            "<TGB17891341E>", new_conn_cfg, "TGISConnection config is empty"
        )

        model_conn = TGISConnection.from_config(model_id, new_conn_cfg)

        error.value_check("<TGB81270235E>", model_conn is not None)

        # Register model connection
        if self._test_connections:
            model_conn = self._test_connection(model_conn)
        if model_conn is not None:
            log.debug(
                "<TGB16640078D> Registering new remote model connection for %s",
                model_id,
            )
            self._safely_update_state(model_id, model_conn, new_conn_cfg)

    def get_client(self, model_id: str) -> generation_pb2_grpc.GenerationServiceStub:
        model_conn = self.get_connection(model_id)
        if model_conn is None and self.local_tgis:
            with self._mutex:
                log.debug2("Launching TGIS subprocess")
                self._managed_tgis.launch(model_id)

            log.debug2("Waiting for TGIS subprocess to become ready")
            self._managed_tgis.wait_until_ready()
            model_conn = self._managed_tgis.get_connection()
            self._model_connections[model_id] = model_conn
        error.value_check(
            "<TGB09142406E>",
            model_conn is not None,
            "Unknown model_id: {}",
            model_id,
        )

        # Mark the backend as started
        self.start()

        # Return the client to the server
        return model_conn.get_client()

    def unload_model(self, model_id: str):
        """Unload the model from TGIS"""
        # If running locally, shut down the managed instance
        if self.local_tgis:
            with self._mutex:
                if self._managed_tgis:
                    self._managed_tgis.terminate()

        # Remove the connection for this model
        self._model_connections.pop(model_id, None)

    def load_prompt_artifacts(self, model_id: str, prompt_id: str, *prompt_artifacts):
        """Load the given prompt artifacts for the given prompt against the base
        model
        """
        conn = self.get_connection(model_id)
        error.value_check(
            "<TGB00822514E>", conn is not None, "Unknown model {}", model_id
        )
        conn.load_prompt_artifacts(prompt_id, *prompt_artifacts)

    def unload_prompt_artifacts(self, model_id: str, *prompt_ids: str):
        """Unload all the artifacts for the prompt ids provided with base model model_id"""
        conn = self.get_connection(model_id)
        error.value_check(
            "<TGB99822514E>", conn is not None, "Unknown model {}", model_id
        )
        log.debug3(
            "Unloading prompt artifacts for model: %s, prompts: %s",
            model_id,
            prompt_ids,
        )
        conn.unload_prompt_artifacts(*prompt_ids)

    @property
    def local_tgis(self) -> bool:
        return self._local_tgis

    @property
    def model_loaded(self) -> bool:
        return not self.local_tgis or (
            self._managed_tgis is not None and self._managed_tgis.is_ready()
        )

    @classmethod
    def get_route_info(
        cls,
        context: Optional[RuntimeServerContextType],
    ) -> Optional[str]:
        """Get the string value of the x-route-info header/metadata if present
        in a case insensitive manner.

        Args:
            context (Optional[RuntimeServerContextType]): The grpc or fastapi
                request context

        Returns:
            route_info (Optional[str]): The header/metadata value if present,
                otherwise None
        """
        if context is None:
            return context
        if isinstance(context, grpc.ServicerContext):
            return TGISBackend._request_metadata_get(
                context.invocation_metadata(), cls.ROUTE_INFO_HEADER_KEY
            )

        if HAVE_FASTAPI and isinstance(context, fastapi.Request):
            return TGISBackend._request_header_get(context, cls.ROUTE_INFO_HEADER_KEY)
        error.log_raise(
            "<TGB92615097E>",
            TypeError(f"context is of an unsupported type: {type(context)}"),
        )

    ## Implementation Details ##

    def _test_connection(
        self, model_conn: Optional[TGISConnection], timeout: Optional[float] = None
    ) -> Optional[TGISConnection]:
        """
        Returns the TGISConnection if successful, else returns None.
        """
        if model_conn is None:
            return

        try:
            model_conn.test_connection(timeout)
        except grpc.RpcError as err:
            log.warning(
                "<TGB10601575W>",
                "Unable to connect to model %s: %s",
                model_conn.model_id,
                err,
                exc_info=True,
            )
            model_conn = None

        return model_conn

    def _safely_update_state(
        self,
        model_id: str,
        model_connections: Optional[TGISConnection] = None,
        remote_models_cfg: Optional[Dict[str, Any]] = None,
    ):
        """
        Update the `_model_connections` and `_remote_models_cfg` state dictionaries in a
        thread safe manner.
        """
        # NOTE: setdefault used here to avoid the need to hold the mutex
        #   when running the connection test. It's possible that two
        #   threads would stimulate the creation of the connection
        #   concurrently, so just keep whichever dict update lands first
        if model_connections:
            self._model_connections.setdefault(model_id, model_connections)
        if remote_models_cfg:
            self._remote_models_cfg.setdefault(model_id, remote_models_cfg)

    @classmethod
    def _request_header_get(cls, request: fastapi.Request, key: str) -> Optional[str]:
        """
        Returns the first matching value for the header key (case insensitive).
        If no matching header was found return None.
        """
        # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/datastructures.py#L543
        items: list[Tuple[str, str]] = request.headers.items()
        get_header_key = key.lower()

        for header_key, header_value in items:
            if header_key.lower() == get_header_key:
                return header_value

    @classmethod
    def _request_metadata_get(
        cls, metadata: Tuple[str, Union[str, bytes]], key: str
    ) -> Optional[str]:
        """
        Returns the first matching value for the metadata key (case insensitive).
        If no matching metadata was found return None.
        """
        # https://grpc.github.io/grpc/python/glossary.html#term-metadatum
        get_metadata_key = key.lower()

        for metadata_key, metadata_value in metadata:
            if str(metadata_key).lower() == get_metadata_key:
                if isinstance(metadata_value, str):
                    return metadata_value
                if isinstance(metadata_value, bytes):
                    return metadata_value.decode()


# Register local backend
register_backend_type(TGISBackend)
