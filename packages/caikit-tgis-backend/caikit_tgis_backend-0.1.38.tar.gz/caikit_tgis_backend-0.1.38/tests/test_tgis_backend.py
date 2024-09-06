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
"""
Unit tests for TGIS backend
"""

# Standard
from copy import deepcopy
from dataclasses import asdict
from typing import Any, Dict, Optional, Sequence, Tuple, Union
from unittest import mock
import os
import tempfile
import time

# Third Party
import fastapi
import grpc
import pytest
import tls_test_tools

# First Party
import caikit

# Local
from caikit_tgis_backend import TGISBackend
from caikit_tgis_backend.protobufs import generation_pb2
from caikit_tgis_backend.tgis_connection import TGISConnection
from tests.tgis_mock import tgis_mock_insecure  # noqa
from tests.tgis_mock import tgis_mock_insecure_health_delay  # noqa
from tests.tgis_mock import tgis_mock_mtls  # noqa
from tests.tgis_mock import tgis_mock_tls  # noqa
from tests.tgis_mock import TGISMock

## Helpers #####################################################################


# for convenience in managing the multiple parts of the fixture
class MockTGISFixture:
    def __init__(
        self,
        mock_popen: mock.MagicMock,
        mock_proc: mock.Mock,
        mock_tgis_server: TGISMock,
    ):
        self.mock_poppen = mock_popen
        self.mock_proc = mock_proc
        self.mock_tgis_server = mock_tgis_server
        self._configure_mock_proc()

    def server_launched(self) -> bool:
        return self.mock_poppen.called

    def set_poll_return(self, poll_return):
        self._configure_mock_proc(poll_return)

    def _configure_mock_proc(self, poll_return=None):
        self.mock_proc.configure_mock(
            **{
                "poll.return_value": poll_return,
                # calls to terminate stop the mock server
                # NOTE: return value of terminate is not used
                "terminate.side_effect": self.mock_tgis_server.stop,
            }
        )


def _launch_mock_tgis_proc_as_side_effect(mock_tgis_server: TGISMock):
    # function is passed the same args as the mock
    def side_effect(*args, **kwargs):
        mock_tgis_server.start()
        return mock.DEFAULT

    return side_effect


@pytest.fixture
def mock_tgis_fixture():
    mock_tgis = TGISMock(tls=False, mtls=False)
    with mock.patch("subprocess.Popen") as mock_popen_func:
        # when called, launch the mock_tgis server
        mock_popen_func.side_effect = _launch_mock_tgis_proc_as_side_effect(mock_tgis)
        process_mock = mock.Mock()
        mock_popen_func.return_value = process_mock
        yield MockTGISFixture(mock_popen_func, process_mock, mock_tgis)
    mock_tgis.stop()


class TestServicerContext(grpc.ServicerContext):
    """
    A dummy class for mimicking ServicerContext invocation metadata storage.
    """

    def __init__(self, metadata: Dict[str, Union[str, bytes]]):
        self.metadata = metadata

    def invocation_metadata(self) -> Sequence[Tuple[str, Union[str, bytes]]]:
        # https://grpc.github.io/grpc/python/glossary.html#term-metadata
        return list(self.metadata.items())

    def is_active(self):
        raise NotImplementedError

    def time_remaining(self):
        raise NotImplementedError

    def cancel(self):
        raise NotImplementedError

    def add_callback(self, callback):
        raise NotImplementedError

    def peer(self):
        raise NotImplementedError

    def peer_identities(self):
        raise NotImplementedError

    def peer_identity_key(self):
        raise NotImplementedError

    def auth_context(self):
        raise NotImplementedError

    def send_initial_metadata(self, initial_metadata):
        raise NotImplementedError

    def set_trailing_metadata(self, trailing_metadata):
        raise NotImplementedError

    def abort(self, code, details):
        raise NotImplementedError

    def abort_with_status(self, status):
        raise NotImplementedError

    def set_code(self, code):
        raise NotImplementedError

    def set_details(self, details):
        raise NotImplementedError


## Conn Config #################################################################


def test_tgis_backend_is_registered():
    """Make sure that the TGIS backend is correctly registered with caikit"""
    assert hasattr(caikit.core.module_backends.backend_types, TGISBackend.backend_type)


def test_tgis_backend_config_valid_insecure(tgis_mock_insecure):
    """Make sure that the TGIS backend can be configured with a valid config
    blob for an insecure server
    """
    tgis_be = TGISBackend({"connection": {"hostname": tgis_mock_insecure.hostname}})
    model_id = "test-model"
    tgis_be.get_client(model_id).Generate(
        generation_pb2.BatchedGenerationRequest(
            requests=[
                generation_pb2.GenerationRequest(text="Hello world"),
            ],
        ),
    )
    assert tgis_be.is_started
    conn = tgis_be.get_connection(model_id)
    assert conn
    assert not conn.tls_enabled
    assert not conn.mtls_enabled


def test_tgis_backend_config_valid_tls(tgis_mock_tls):
    """Make sure that the TGIS backend can be configured with a valid config
    blob for a TLS server
    """
    tgis_be = TGISBackend(
        {
            "connection": {
                "hostname": tgis_mock_tls.hostname,
                "ca_cert_file": tgis_mock_tls.ca_cert_file,
            },
        }
    )
    model_id = "test-model"
    tgis_be.get_client(model_id).Generate(
        generation_pb2.BatchedGenerationRequest(
            requests=[
                generation_pb2.GenerationRequest(text="Hello world"),
            ],
        ),
    )
    assert tgis_be.is_started
    conn = tgis_be.get_connection(model_id)
    assert conn
    assert conn.tls_enabled
    assert not conn.mtls_enabled


def test_tgis_backend_tls_hn_override(tgis_mock_tls):
    hn_override = "foo.com"
    tgis_be = TGISBackend(
        {
            "connection": {
                "hostname": tgis_mock_tls.hostname,
                "ca_cert_file": tgis_mock_tls.ca_cert_file,
                "hostname_override": hn_override,
            },
        }
    )
    model_id = "test-model"
    # This should fail- foo.com not in cert
    with pytest.raises(grpc.RpcError):
        tgis_be.get_client(model_id).Generate(
            generation_pb2.BatchedGenerationRequest(
                requests=[
                    generation_pb2.GenerationRequest(text="Hello world"),
                ],
            ),
        )

    # Now make a new mock with "foo.com" in the SAN list and make sure it does work
    with TGISMock(tls=True, san_list=[hn_override]) as foo_com_mock:
        tgis_be = TGISBackend(
            {
                "connection": {
                    "hostname": foo_com_mock.hostname,
                    "ca_cert_file": foo_com_mock.ca_cert_file,
                    "hostname_override": hn_override,
                },
            }
        )
        model_id = "test-model"
        tgis_be.get_client(model_id).Generate(
            generation_pb2.BatchedGenerationRequest(
                requests=[
                    generation_pb2.GenerationRequest(text="Hello world"),
                ],
            ),
        )
        assert tgis_be.is_started
        conn = tgis_be.get_connection(model_id)
        assert conn
        assert conn.tls_enabled
        assert not conn.mtls_enabled


def test_tgis_backend_config_valid_mtls(tgis_mock_mtls):
    """Make sure that the TGIS backend can be configured with a valid config
    blob for an mTLS server
    """
    tgis_be = TGISBackend(
        {
            "connection": {
                "hostname": tgis_mock_mtls.hostname,
                "ca_cert_file": tgis_mock_mtls.ca_cert_file,
                "client_cert_file": tgis_mock_mtls.client_cert_file,
                "client_key_file": tgis_mock_mtls.client_key_file,
            },
        }
    )
    model_id = "test-model"
    tgis_be.get_client(model_id).Generate(
        generation_pb2.BatchedGenerationRequest(
            requests=[
                generation_pb2.GenerationRequest(text="Hello world"),
            ],
        ),
    )
    assert tgis_be.is_started
    conn = tgis_be.get_connection(model_id)
    assert conn
    assert conn.tls_enabled
    assert conn.mtls_enabled


def test_stop():
    """Make sure that a working backend instance can be stopped"""
    tgis_be = TGISBackend({"connection": {"hostname": "foo.bar.{model_id}:12345"}})
    assert not tgis_be.is_started

    # Add two models with get_client
    model_id1 = "foo"
    model_id2 = "bar"
    tgis_be.get_client(model_id1)
    tgis_be.get_client(model_id2)
    assert tgis_be.is_started
    assert tgis_be.get_connection(model_id1, False)
    assert tgis_be.get_connection(model_id2, False)

    # Stop the backend and make sure both models get removed
    tgis_be.stop()
    assert not tgis_be.is_started
    assert not tgis_be.get_connection(model_id1, False)
    assert not tgis_be.get_connection(model_id2, False)


def test_lazy_start_remote_model():
    """Make sure that an entry in the remote_models config can be respected even
    if it is invalid at instantiation and test_connections is enabled
    """
    # Set up a TGIS connection that will not be valid yet
    port = tls_test_tools.open_port()
    model_name = "some-model"
    cfg = {
        "remote_models": {model_name: {"hostname": f"localhost:{port}"}},
        "test_connections": True,
    }

    # Initialize the backend and make sure getting the model's connection
    # returns None
    tgis_be = TGISBackend(cfg)
    assert tgis_be.get_connection(model_name) is None

    # Now boot the TGIS instance and try again
    with TGISMock(grpc_port=port):
        max_time = 5
        start_time = time.time()
        conn = None
        while time.time() - start_time < max_time:
            conn = tgis_be.get_connection(model_name)
            if conn:
                break
            time.sleep(0.1)
        assert conn


## Local Subprocess ############################################################


def test_construct_run_local():
    """Make sure that when constructed without a connection, it runs in TGIS
    local mode
    """
    assert TGISBackend({}).local_tgis
    assert TGISBackend({"connection": {}}).local_tgis
    assert TGISBackend({"remote_models": {}}).local_tgis

    # When setting the connection to empty via the env, this is what it looks
    # like, so we want to make sure this doesn't error
    assert TGISBackend({"connection": ""}).local_tgis


def test_local_tgis_run(mock_tgis_fixture: MockTGISFixture):
    """Test that a "local tgis" (mocked) can be booted and maintained"""
    mock_tgis_server: TGISMock = mock_tgis_fixture.mock_tgis_server
    tgis_be = TGISBackend(
        {
            "local": {
                "grpc_port": int(mock_tgis_server.hostname.split(":")[-1]),
                "http_port": mock_tgis_server.http_port,
                "health_poll_delay": 0.1,
            },
        }
    )
    assert tgis_be.local_tgis
    assert not mock_tgis_fixture.server_launched()

    # Get a client handle and make sure that the server has launched
    tgis_be.get_client("").Generate(
        generation_pb2.BatchedGenerationRequest(
            requests=[
                generation_pb2.GenerationRequest(text="Hello world"),
            ],
        ),
    )
    assert mock_tgis_fixture.server_launched()


def test_local_tgis_unload(mock_tgis_fixture: MockTGISFixture):
    """Test that a "local tgis" (mocked) can unload and reload itself"""
    mock_tgis_server: TGISMock = mock_tgis_fixture.mock_tgis_server
    tgis_be = TGISBackend(
        {
            "local": {
                "grpc_port": int(mock_tgis_server.hostname.split(":")[-1]),
                "http_port": mock_tgis_server.http_port,
            },
        }
    )
    assert tgis_be.local_tgis
    assert not mock_tgis_fixture.server_launched()

    # Boot up the client
    model_id = "foobar"
    tgis_be.get_client(model_id)
    assert mock_tgis_fixture.server_launched()
    assert tgis_be.model_loaded

    # Unload the model
    tgis_be.unload_model(model_id)
    assert tgis_be.local_tgis
    assert not tgis_be.model_loaded

    # Load the model again by getting the client
    tgis_be.get_client(model_id)
    assert tgis_be.local_tgis
    assert tgis_be.model_loaded


def test_local_tgis_fail_start(mock_tgis_fixture: MockTGISFixture):
    """Test that when tgis fails to boot, an exception is raised"""
    tgis_be = TGISBackend({})
    mock_tgis_fixture.set_poll_return(1)
    with pytest.raises(RuntimeError):
        tgis_be.get_client("")


def test_local_tgis_load_timeout(mock_tgis_fixture: MockTGISFixture):
    """Test that if a local tgis model takes too long to load, it fails
    gracefully
    """
    mock_tgis_server: TGISMock = mock_tgis_fixture.mock_tgis_server
    # increase the health poll delay to greater than the load timeout
    mock_tgis_server.health_delay = 1
    tgis_be = TGISBackend(
        {
            "local": {
                "grpc_port": int(mock_tgis_server.hostname.split(":")[-1]),
                "http_port": mock_tgis_server.http_port,
                "health_poll_delay": 0.1,
                "load_timeout": 0.05,
            },
        }
    )
    assert tgis_be.local_tgis
    assert not mock_tgis_fixture.server_launched()

    # TODO: health check for coverage?
    # # (For coverage!) make sure the health probe doesn't actually run
    # assert not tgis_be._tgis_health_check()

    # Get a client handle and make sure that the server has launched
    with pytest.raises(TimeoutError):
        tgis_be.get_client("")
    assert mock_tgis_fixture.server_launched()
    assert tgis_be.local_tgis
    assert not tgis_be.model_loaded


def test_local_tgis_autorecovery(mock_tgis_fixture: MockTGISFixture):
    """Test that the backend can automatically restart the TGIS subprocess if it
    crashes
    """
    # mock the subprocess to be our mock server and to come up working
    mock_tgis_server: TGISMock = mock_tgis_fixture.mock_tgis_server
    tgis_be = TGISBackend(
        {
            "local": {
                "grpc_port": int(mock_tgis_server.hostname.split(":")[-1]),
                "http_port": mock_tgis_server.http_port,
                "health_poll_delay": 0.1,
                "health_poll_timeout": 1,
            },
        }
    )
    assert tgis_be.local_tgis

    # Get a client handle and make sure that the server has launched
    tgis_client = tgis_be.get_client("")

    assert mock_tgis_fixture.server_launched()

    # requests should succeed
    tgis_client.Generate(
        generation_pb2.BatchedGenerationRequest(
            requests=[
                generation_pb2.GenerationRequest(text="Hello world"),
            ],
        ),
    )

    # "kill" the mock server
    mock_tgis_server.stop()

    # request should fail, which triggers the auto-recovery
    with pytest.raises(grpc.RpcError):
        tgis_client.Generate(
            generation_pb2.BatchedGenerationRequest(
                requests=[
                    generation_pb2.GenerationRequest(text="Hello world"),
                ],
            ),
        )

    # wait for the server to reboot
    # pause this thread to allow the reboot thread to start
    time.sleep(0.5)
    tgis_be._managed_tgis.wait_until_ready()

    # request should succeed without recreating the client
    tgis_client.Generate(
        generation_pb2.BatchedGenerationRequest(
            requests=[
                generation_pb2.GenerationRequest(text="Hello world"),
            ],
        ),
    )


def test_local_tgis_with_prompt_dir(mock_tgis_fixture: MockTGISFixture):
    """Test that a "local tgis" (mocked) can manage prompts"""
    mock_tgis_server: TGISMock = mock_tgis_fixture.mock_tgis_server
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            tgis_be = TGISBackend(
                {
                    "local": {
                        "grpc_port": int(mock_tgis_server.hostname.split(":")[-1]),
                        "http_port": mock_tgis_server.http_port,
                        "health_poll_delay": 0.1,
                        "prompt_dir": prompt_dir,
                    },
                }
            )
            assert tgis_be.local_tgis
            assert not mock_tgis_fixture.server_launched()
            local_model_id = "local_model"
            tgis_be.get_client(local_model_id)

            prompt_id = "some-prompt"
            artifact_fname = "artifact.pt"
            source_fname = os.path.join(source_dir, artifact_fname)
            with open(source_fname, "w") as handle:
                handle.write("stub")
            tgis_be.load_prompt_artifacts(local_model_id, prompt_id, source_fname)
            assert os.path.exists(os.path.join(prompt_dir, prompt_id, artifact_fname))


## Remote Models ###############################################################


def test_tgis_backend_config_remote_models_only():
    """Make sure that config works with only remote models"""
    tgis_be = TGISBackend(
        {
            "remote_models": {
                "foo": {"hostname": "foo:123"},
                "bar": {"hostname": "bar:123"},
            },
        }
    )
    assert not tgis_be.local_tgis
    assert tgis_be.get_connection("foo")
    assert tgis_be.get_connection("bar")
    assert not tgis_be.get_connection("baz")


def test_tgis_backend_config_remote_models_with_connection():
    """Make sure thatconfig works with only remote models and a connection
    template
    """
    tgis_be = TGISBackend(
        {
            "connection": {"hostname": "foobar.{model_id}:123"},
            "remote_models": {
                "foo": {"hostname": "foo:123"},
                "bar": {"hostname": "bar:123"},
            },
        }
    )
    assert not tgis_be.local_tgis
    assert tgis_be.get_connection("foo")
    assert tgis_be.get_connection("bar")
    baz_conn = tgis_be.get_connection("baz")
    assert baz_conn
    assert baz_conn.hostname == "foobar.baz:123"


def test_tgis_multi_model_client():
    """Make sure that TGISBackend can manage multiple simultaneous client
    objects to different running TGIS servers
    """
    prompt = "hello"
    with TGISMock(prompt_responses={prompt: "foo"}) as tgis_foo:
        with TGISMock(prompt_responses={prompt: "bar"}) as tgis_bar:
            tgis_be = TGISBackend(
                {
                    "remote_models": {
                        "foo": {"hostname": f"localhost:{tgis_foo.grpc_port}"},
                        "bar": {"hostname": f"localhost:{tgis_bar.grpc_port}"},
                    },
                }
            )
            assert not tgis_be.local_tgis
            assert tgis_be.get_connection("foo")
            assert tgis_be.get_connection("bar")
            foo_client = tgis_be.get_client("foo")
            bar_client = tgis_be.get_client("bar")
            for client, exp_res in [(foo_client, "foo"), (bar_client, "bar")]:
                resp = client.Generate(
                    generation_pb2.BatchedGenerationRequest(
                        requests=[
                            generation_pb2.GenerationRequest(text=prompt),
                        ],
                    ),
                )
                assert len(resp.responses) == 1
                assert resp.responses[0].text == exp_res


def test_tgis_backend_unload_multi_connection():
    """Make sure that connections can be unloaded individually"""
    tgis_be = TGISBackend(
        {
            "connection": {"hostname": "foobar.{model_id}:123"},
            "remote_models": {
                "foo": {"hostname": "foo:123"},
                "bar": {"hostname": "bar:123"},
            },
        }
    )
    assert tgis_be.get_connection("foo")
    assert tgis_be.get_connection("bar")
    tgis_be.unload_model("foo")
    assert not tgis_be.get_connection("foo", False)
    assert tgis_be.get_connection("bar", False)
    tgis_be.unload_model("bar")
    assert not tgis_be.get_connection("foo", False)
    assert not tgis_be.get_connection("bar", False)


def test_tgis_backend_config_load_prompt_artifacts():
    """Make sure that loading prompt artifacts behaves as expected"""
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            # Make some source files
            source_fnames = ["prompt1.pt", "prompt2.pt"]
            source_files = [os.path.join(source_dir, fname) for fname in source_fnames]
            for source_file in source_files:
                with open(source_file, "w") as handle:
                    handle.write("stub")

            # Set up a separate prompt dir for foo and bar
            foo_prompt_dir = os.path.join(prompt_dir, "foo")
            bar_prompt_dir = os.path.join(prompt_dir, "bar")
            os.makedirs(foo_prompt_dir)
            os.makedirs(bar_prompt_dir)

            # Make the backend with two remotes that support prompts and one
            # that does not
            tgis_be = TGISBackend(
                {
                    "remote_models": {
                        "foo": {"hostname": "foo:123", "prompt_dir": foo_prompt_dir},
                        "bar": {"hostname": "bar:123", "prompt_dir": bar_prompt_dir},
                        "baz": {"hostname": "bar:123"},
                    },
                }
            )

            # Make sure loading prompts lands on the right model and prompt
            prompt_id1 = "prompt-one"
            prompt_id2 = "prompt-two"
            tgis_be.load_prompt_artifacts("foo", prompt_id1, source_files[0])
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert not os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id2, source_fnames[1])
            )
            assert not os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert not os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id2, source_fnames[1])
            )
            tgis_be.load_prompt_artifacts("foo", prompt_id2, source_files[1])
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id2, source_fnames[1])
            )
            assert not os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert not os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id2, source_fnames[1])
            )
            tgis_be.load_prompt_artifacts("bar", prompt_id1, source_files[0])
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id2, source_fnames[1])
            )
            assert os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert not os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id2, source_fnames[1])
            )
            tgis_be.load_prompt_artifacts("bar", prompt_id2, source_files[1])
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id2, source_fnames[1])
            )
            assert os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id2, source_fnames[1])
            )

            # piggy-back to test unloading prompt artifacts
            tgis_be.unload_prompt_artifacts("bar", prompt_id1, prompt_id2)
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert os.path.exists(
                os.path.join(foo_prompt_dir, prompt_id2, source_fnames[1])
            )
            assert not os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id1, source_fnames[0])
            )
            assert not os.path.exists(
                os.path.join(bar_prompt_dir, prompt_id2, source_fnames[1])
            )

            # Make sure non-prompt models raise
            with pytest.raises(ValueError):
                tgis_be.load_prompt_artifacts("baz", prompt_id1, source_files[0])

            # Make sure unknown model raises
            with pytest.raises(ValueError):
                tgis_be.load_prompt_artifacts("buz", prompt_id1, source_files[0])


@pytest.mark.parametrize(
    argnames=["model_id", "conn_cfg", "fill", "expected_conn_cfg"],
    argvalues=[
        (
            "model1",
            None,
            False,
            {
                "hostname": "localhost:1234",
                "model_id": "model1",
                "lb_policy": "abc",
            },
        ),
        (
            "model1",
            None,
            True,
            {
                "hostname": "localhost:1234",
                "model_id": "model1",
                "lb_policy": "abc",
            },
        ),
        (
            "model1",
            {"hostname": "myhost"},
            False,
            {"hostname": "myhost", "model_id": "model1"},
        ),
        (
            "model1",
            {"hostname": "myhost"},
            True,
            {"hostname": "myhost", "model_id": "model1", "lb_policy": "abc"},
        ),
    ],
)
def test_tgis_backend_register_model_connection(
    model_id: str,
    conn_cfg: Optional[dict],
    fill: bool,
    expected_conn_cfg: Dict[str, Any],
):
    """Test that register_model_connection correctly adds a TGISConnection to the _model_connections dictionary"""
    tgis_be = TGISBackend(
        {
            "connection": {"hostname": "localhost:1234", "grpc_lb_policy_name": "abc"},
            "remote_models": {},
        }
    )

    # Assert new model is not in backend
    assert model_id not in tgis_be._remote_models_cfg
    assert model_id not in tgis_be._model_connections
    backup_base_cfg = deepcopy(tgis_be._base_connection_cfg)

    # Register model
    tgis_be.register_model_connection(model_id, conn_cfg, fill_with_defaults=fill)
    assert model_id in tgis_be._remote_models_cfg
    assert model_id in tgis_be._model_connections
    assert isinstance(tgis_be._model_connections[model_id], TGISConnection)
    assert {
        k: v
        for k, v in asdict(tgis_be._model_connections[model_id]).items()
        if v is not None
    } == expected_conn_cfg

    # Re-register -> no change to existing model
    tgis_be.register_model_connection(model_id, {"hostname": "{model_id}.mycluster"})
    assert {
        k: v
        for k, v in asdict(tgis_be._model_connections[model_id]).items()
        if v is not None
    } == expected_conn_cfg

    # Confirm get_connection works
    conn = tgis_be.get_connection(model_id, create=False)
    assert isinstance(conn, TGISConnection)
    assert {
        k: v
        for k, v in asdict(tgis_be._model_connections[model_id]).items()
        if v is not None
    } == expected_conn_cfg

    # Confirm that the source _base_connection_cfg wasn't mutated
    assert tgis_be._base_connection_cfg == backup_base_cfg


def test_tgis_backend_register_model_connection_local():
    tgis_be = TGISBackend()

    # Confirm marked as local TGIS instance with no base connection config
    assert tgis_be.local_tgis
    assert not tgis_be._base_connection_cfg
    assert not tgis_be._model_connections
    assert not tgis_be._remote_models_cfg

    # Register action should do nothing
    tgis_be.register_model_connection("should do nothing")

    # Confirm nothing was done
    assert not tgis_be._base_connection_cfg
    assert not tgis_be._model_connections
    assert not tgis_be._remote_models_cfg


## Failure Tests ###############################################################


def test_no_updated_config():
    """Make sure that the config for a TGISBackend cannot be updated"""
    tgis_be = TGISBackend({"connection": {"hostname": "localhost:12345"}})
    with pytest.raises(AssertionError):
        tgis_be.register_config({"connection": {"hostname": "localhost:54321"}})


@pytest.mark.parametrize(
    "params",
    [
        ("not a dict", TypeError),
        ({"hostname": "localhost"}, ValueError),
        ({"hostname": "foo:123", "ca_cert_file": 1}, TypeError),
        # Missing TLS Files
        ({"hostname": "foo:123", "ca_cert_file": "not there"}, ValueError),
        (
            {
                "hostname": "foo:123",
                "ca_cert_file": __file__,
                "client_cert_file": "not there",
                "client_key_file": __file__,
            },
            ValueError,
        ),
        (
            {
                "hostname": "foo:123",
                "ca_cert_file": __file__,
                "client_cert_file": __file__,
                "client_key_file": "not there",
            },
            ValueError,
        ),
        # TLS Files as dirs
        (
            {"hostname": "foo:123", "ca_cert_file": os.path.dirname(__file__)},
            ValueError,
        ),
        (
            {
                "hostname": "foo:123",
                "ca_cert_file": __file__,
                "client_cert_file": os.path.dirname(__file__),
                "client_key_file": __file__,
            },
            ValueError,
        ),
        (
            {
                "hostname": "foo:123",
                "ca_cert_file": __file__,
                "client_cert_file": __file__,
                "client_key_file": os.path.dirname(__file__),
            },
            ValueError,
        ),
        # Bad TLS File combos
        (
            {
                "hostname": "foo:123",
                "ca_cert_file": __file__,
                "client_cert_file": __file__,
            },
            ValueError,
        ),
        (
            {
                "hostname": "foo:123",
                "ca_cert_file": __file__,
                "client_key_file": __file__,
            },
            ValueError,
        ),
        (
            {
                "hostname": "foo:123",
                "client_cert_file": __file__,
                "client_key_file": __file__,
            },
            ValueError,
        ),
    ],
)
def test_invalid_connection(params):
    """Make sure that invalid connections cause errors"""
    conn, error_type = params
    with pytest.raises(error_type):
        TGISBackend({"connection": conn})


def test_tgis_backend_conn_testing_enabled(tgis_mock_insecure):
    """Make sure that the TGIS backend can be configured with a valid config
    blob for an insecure server and connection testing enabled
    """
    tgis_be = TGISBackend(
        {
            "connection": {"hostname": tgis_mock_insecure.hostname},
            "test_connections": True,
        }
    )
    model_id = "test-model"
    tgis_be.get_client(model_id).Generate(
        generation_pb2.BatchedGenerationRequest(
            requests=[
                generation_pb2.GenerationRequest(text="Hello world"),
            ],
        ),
    )
    assert tgis_be.is_started
    conn = tgis_be.get_connection(model_id)
    conn.test_connection()
    conn.test_connection(timeout=1)


@pytest.mark.parametrize(
    argnames=["context", "route_info"],
    argvalues=[
        (
            fastapi.Request(
                {
                    "type": "http",
                    "headers": [
                        (
                            TGISBackend.ROUTE_INFO_HEADER_KEY.encode("latin-1"),
                            "http exact".encode("latin-1"),
                        )
                    ],
                }
            ),
            "http exact",
        ),
        (
            fastapi.Request(
                {
                    "type": "http",
                    "headers": [
                        (
                            TGISBackend.ROUTE_INFO_HEADER_KEY.upper().encode("latin-1"),
                            "http upper-case".encode("latin-1"),
                        )
                    ],
                }
            ),
            "http upper-case",
        ),
        (
            fastapi.Request(
                {
                    "type": "http",
                    "headers": [
                        (
                            TGISBackend.ROUTE_INFO_HEADER_KEY.title().encode("latin-1"),
                            "http title-case".encode("latin-1"),
                        )
                    ],
                }
            ),
            "http title-case",
        ),
        (
            fastapi.Request(
                {
                    "type": "http",
                    "headers": [
                        (
                            "route-info".encode("latin-1"),
                            "http not-found".encode("latin-1"),
                        )
                    ],
                }
            ),
            None,
        ),
        (
            TestServicerContext({TGISBackend.ROUTE_INFO_HEADER_KEY: "grpc exact"}),
            "grpc exact",
        ),
        (
            TestServicerContext(
                {TGISBackend.ROUTE_INFO_HEADER_KEY.upper(): "grpc upper-case"}
            ),
            "grpc upper-case",
        ),
        (
            TestServicerContext(
                {TGISBackend.ROUTE_INFO_HEADER_KEY.title(): "grpc title-case"}
            ),
            "grpc title-case",
        ),
        (
            TestServicerContext({"route-info": "grpc not found"}),
            None,
        ),
        ("should raise TypeError", TypeError()),
        (None, None),
    ],
)
def test_get_route_info(context, route_info: Union[str, None, Exception]):
    if isinstance(route_info, Exception):
        with pytest.raises(type(route_info)):
            TGISBackend.get_route_info(context)
    else:
        actual_route_info = TGISBackend.get_route_info(context)
        assert actual_route_info == route_info


def test_handle_runtime_context_with_route_info():
    """Test that with route info present, handle_runtime_context updates the
    model connection
    """
    route_info = "sometext"
    context = fastapi.Request(
        {
            "type": "http",
            "headers": [
                (
                    TGISBackend.ROUTE_INFO_HEADER_KEY.encode("latin-1"),
                    route_info.encode("latin-1"),
                )
            ],
        }
    )

    tgis_be = TGISBackend(
        {
            "connection": {"hostname": "foobar:1234"},
            "test_connections": False,
        }
    )
    assert not tgis_be._model_connections

    # Handle the connection and make sure model_connections is updated
    model_id = "my-model"
    tgis_be.handle_runtime_context(model_id, context)
    assert model_id in tgis_be._model_connections
    assert (conn := tgis_be.get_connection(model_id)) and conn.hostname == route_info
