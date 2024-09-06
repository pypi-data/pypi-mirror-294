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
"""Encapsulate the creation of a TGIS Connection"""

# Future
from __future__ import annotations

# Standard
from collections.abc import Container
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional
import os
import shutil

# Third Party
import grpc

# First Party
from caikit.core.exceptions import error_handler
import alog

# Local
from .load_balancing_proxy import GRPCLoadBalancerProxy
from .protobufs import generation_pb2, generation_pb2_grpc

if TYPE_CHECKING:
    # Third Party
    from _typeshed import StrPath

log = alog.use_channel("TGCONN")
error = error_handler.get(log)


@dataclass
class TLSFilePair:
    cert_file: str
    key_file: str


# pylint: disable=too-many-instance-attributes
@dataclass
class TGISConnection:
    #################
    # Class members #
    #################

    # The URL (with port) for the connection
    hostname: str
    # The model_id associated with this connection
    model_id: str
    # Path to CA cert when TGIS is running with TLS
    ca_cert_file: Optional[str] = None
    # Paths to client key/cert pair when TGIS requires mTLS
    client_tls: Optional[TLSFilePair] = None
    # TLS HN override
    tls_hostname_override: Optional[str] = None
    # Mounted directory where TGIS will look for prompt vector artifacts
    prompt_dir: Optional[str] = None
    # Load balancing policy
    lb_policy: Optional[str] = None
    # DNS poll interval (seconds) for LB updates
    lb_poll_interval_s: Optional[float] = None
    # Private member to hold the client once created
    _client: Optional[generation_pb2_grpc.GenerationServiceStub] = None

    ###################
    # Class constants #
    ###################

    HOSTNAME_KEY = "hostname"
    HOSTNAME_TEMPLATE_MODEL_ID = "model_id"
    CA_CERT_FILE_KEY = "ca_cert_file"
    CLIENT_CERT_FILE_KEY = "client_cert_file"
    CLIENT_KEY_FILE_KEY = "client_key_file"
    PROMPT_DIR_KEY = "prompt_dir"
    LB_POLICY_KEY = "grpc_lb_policy_name"
    LB_POLL_INTERVAL_KEY = "grpc_lb_poll_interval_s"
    TLS_HN_OVERRIDE_KEY = "hostname_override"

    @classmethod
    def from_config(
        cls, model_id: str, config: Dict[str, Any]
    ) -> Optional["TGISConnection"]:
        """Create an instance from a connection template and a model_id"""
        hostname = config.get(cls.HOSTNAME_KEY)
        if hostname:
            error.type_check("<TGB57775870E>", str, hostname=hostname)

            hostname = hostname.format_map(
                {
                    cls.HOSTNAME_TEMPLATE_MODEL_ID: model_id,
                }
            )
            log.debug("Resolved hostname [%s] for model %s", hostname, model_id)

            tls_hostname_override = config.get(cls.TLS_HN_OVERRIDE_KEY)
            lb_policy = config.get(cls.LB_POLICY_KEY) or None
            error.type_check(
                "<TGB17223790E>",
                str,
                allow_none=True,
                **{cls.LB_POLICY_KEY: lb_policy},
            )

            lb_poll_interval_s = config.get(cls.LB_POLL_INTERVAL_KEY) or None
            error.type_check(
                "<TGB17223790E>",
                float,
                int,
                allow_none=True,
                **{cls.LB_POLL_INTERVAL_KEY: lb_poll_interval_s},
            )

            # Look for the prompt dir
            prompt_dir = config.get(cls.PROMPT_DIR_KEY) or None
            error.type_check(
                "<TGB17909870E>",
                str,
                allow_none=True,
                **{cls.PROMPT_DIR_KEY: prompt_dir},
            )
            if prompt_dir:
                error.dir_check("<RGB69837665E>", prompt_dir)

            # Pull out the TLS info
            ca_cert = config.get(cls.CA_CERT_FILE_KEY) or None
            client_cert = config.get(cls.CLIENT_CERT_FILE_KEY) or None
            client_key = config.get(cls.CLIENT_KEY_FILE_KEY) or None
            log.debug2("CA Cert File: %s", ca_cert)
            log.debug2("Client Cert File: %s", client_cert)
            log.debug2("Client Key File: %s", client_key)
            error.type_check(
                "<TGB73210861E>",
                str,
                allow_none=True,
                **{cls.CA_CERT_FILE_KEY: ca_cert},
            )
            error.type_check(
                "<TGB73210862E>",
                str,
                allow_none=True,
                **{cls.CLIENT_CERT_FILE_KEY: client_cert},
            )
            error.type_check(
                "<TGB73210863E>",
                str,
                allow_none=True,
                **{cls.CLIENT_KEY_FILE_KEY: client_key},
            )
            error.value_check(
                "<TGB73210864E>", ca_cert is None or os.path.isfile(ca_cert)
            )
            error.value_check(
                "<TGB73210865E>", client_cert is None or os.path.isfile(client_cert)
            )
            error.value_check(
                "<TGB73210866E>", client_key is None or os.path.isfile(client_key)
            )
            error.value_check(
                "<TGB79518571E>",
                ca_cert or (not client_cert and not client_key),
                "Cannot set client TLS ({}/{}) without CA ({})",
                cls.CLIENT_CERT_FILE_KEY,
                cls.CLIENT_KEY_FILE_KEY,
                cls.CA_CERT_FILE_KEY,
            )
            error.value_check(
                "<TGB79518572E>",
                (client_cert and client_key) or (not client_cert and not client_key),
                "Must set both {} and {} or neither",
                cls.CLIENT_CERT_FILE_KEY,
                cls.CLIENT_KEY_FILE_KEY,
            )
            client_tls = (
                TLSFilePair(cert_file=client_cert, key_file=client_key)
                if client_cert
                else None
            )
            return cls(
                hostname=hostname,
                model_id=model_id,
                ca_cert_file=ca_cert,
                client_tls=client_tls,
                tls_hostname_override=tls_hostname_override,
                prompt_dir=prompt_dir,
                lb_policy=lb_policy,
                lb_poll_interval_s=lb_poll_interval_s,
            )

    @property
    def tls_enabled(self) -> bool:
        return self.ca_cert_file is not None

    @property
    def mtls_enabled(self) -> bool:
        return None not in [self.ca_cert_file, self.client_tls]

    def load_prompt_artifacts(self, prompt_id: str, *artifact_paths: str):
        """Load the given artifact paths to this TGIS connection

        As implemented, this is a simple copy to the TGIS instance's prompt dir,
        but it could extend to API interactions in the future.

        TODO: If two copies of the runtime attempt to perform the same copy at
            the same time, it could race and cause errors with the mounted
            directory system.

        Args:
            prompt_id (str): The ID that this prompt should use
            *artifact_paths (Tuple[str]): The paths to the artifacts to load
        """
        error.value_check(
            "<TGB07970356E>",
            self.prompt_dir is not None,
            "No prompt_dir configured for {}",
            self.hostname,
        )
        error.type_check_all(
            "<TGB23973965E>",
            str,
            artifact_paths=artifact_paths,
        )

        target_dir = Path(self.prompt_dir) / prompt_id
        os.makedirs(target_dir, exist_ok=True)

        # Don't copy files which are already in the target_dir
        existing_artifact_names = {f.name for f in target_dir.iterdir()}
        new_artifacts = {
            Path(f)
            for f in artifact_paths
            if file_or_swp_not_in_listing(Path(f).name, existing_artifact_names)
        }

        for artifact_path in new_artifacts:
            error.file_check("<TGB14818050E>", artifact_path)
            target_file = target_dir / artifact_path.name
            swp_file = target_file.with_name(target_file.name + ".swp")

            # Copy file as a swap file
            log.debug3("Copying %s -> %s", artifact_path, target_file)
            shutil.copyfile(artifact_path, swp_file)

            # Rename on completion of copy using replace
            # Replace silently overrides the destination irrespective of OS
            os.replace(swp_file, target_file)

    def unload_prompt_artifacts(self, *prompt_ids: str):
        """Unload the given prompts from TGIS

        As implemented, this simply removes the prompt artifacts for these IDs
        and does not explicitly unload them from the TGIS in-memory cache.

        NOTE: This intentionally ignores all errors. It's very likely that
            multiple replicas of the runtime will attempt to unload the same
            prompt, so we need to let the first one win and the rest quietly
            accept that it's already deleted.

        Args:
            *prompt_ids (str): The IDs to unload
        """
        error.value_check(
            "<TGB07970365E>",
            self.prompt_dir is not None,
            "No prompt_dir configured for {}",
            self.hostname,
        )
        error.type_check_all(
            "<TGB41380075E>",
            str,
            prompt_ids=prompt_ids,
        )
        for prompt_id in prompt_ids:
            prompt_id_dir = os.path.join(self.prompt_dir, prompt_id)
            log.debug3(
                "Unloading prompt artifact %s at path %s", prompt_id, prompt_id_dir
            )
            shutil.rmtree(prompt_id_dir, ignore_errors=True)

    def get_client(self) -> generation_pb2_grpc.GenerationServiceStub:
        """Get a grpc client for the connection"""
        load_balancer_kwargs = {}
        if self._client is None:
            log.info(
                "<TGB20236231I>",
                "Initializing TGIS connection to [%s]. TLS enabled? %s. mTLS Enabled? %s",
                self.hostname,
                self.tls_enabled,
                self.mtls_enabled,
            )
            if not self.tls_enabled:
                log.debug("Connecting to TGIS at [%s] INSECURE", self.hostname)
            else:
                log.debug("Connecting to TGIS at [%s] SECURE", self.hostname)
                creds_kwargs = {
                    "root_certificates": self._load_tls_file(self.ca_cert_file)
                }
                if self.mtls_enabled:
                    log.debug("Enabling mTLS for TGIS connection")
                    creds_kwargs["certificate_chain"] = self._load_tls_file(
                        self.client_tls.cert_file
                    )
                    creds_kwargs["private_key"] = self._load_tls_file(
                        self.client_tls.key_file
                    )
                credentials = grpc.ssl_channel_credentials(**creds_kwargs)
                load_balancer_kwargs["credentials"] = credentials

                if self.tls_hostname_override:
                    # using a list for the opts so that they can be appended to later if necessary
                    channel_opts = [
                        (
                            "grpc.ssl_target_name_override",
                            self.tls_hostname_override,
                        )
                    ]
                    # kwarg name for the GRPCLoadBalancerProxy init
                    load_balancer_kwargs["channel_options"] = channel_opts

            # Override the lb policy, if configured.
            # The load balancer will always provide a default if we don't pass one.
            if self.lb_policy:
                load_balancer_kwargs["policy"] = self.lb_policy

            if self.lb_poll_interval_s:
                load_balancer_kwargs["poll_interval_s"] = self.lb_poll_interval_s

            load_balancer = GRPCLoadBalancerProxy(
                client_class=generation_pb2_grpc.GenerationServiceStub,
                target=self.hostname,
                **load_balancer_kwargs,
            )
            self._client = load_balancer.client
        return self._client

    def test_connection(self, timeout: Optional[float] = None):
        """Test whether the connection is valid. If not valid, an appropriate
        grpc.RpcError will be raised
        """
        client = self.get_client()
        client.ModelInfo(
            generation_pb2.ModelInfoRequest(model_id=self.model_id),
            timeout=timeout,
        )

    @staticmethod
    def _load_tls_file(file_path: Optional[str]) -> Optional[bytes]:
        error.type_check(
            "<TGB20235227E>",
            str,
            allow_none=True,
            file_path=file_path,
        )
        if file_path is not None:
            error.value_check(
                "<TGB20235228E>",
                os.path.isfile(file_path),
                "Invalid TLS file path: {}",
                file_path,
            )
            with open(file_path, "rb") as handle:
                return handle.read()


def file_or_swp_not_in_listing(
    filename: "StrPath", file_listing: Container[str], swap_extension: str = ".swp"
) -> bool:
    """Determine if the file, or its swap variant, is in the file listing."""
    file = Path(filename)

    return (
        file.name not in file_listing
        and file.with_suffix(swap_extension).name not in file_listing
    )
