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
Unit tests for the TGISConnection class
"""

# Standard
from contextlib import contextmanager
from pathlib import Path
import os
import tempfile

# Third Party
import grpc
import pytest
import tls_test_tools

# Local
from caikit_tgis_backend.tgis_connection import TGISConnection
from tests.tgis_mock import tgis_mock_insecure  # noqa


@contextmanager
def temp_file():
    with tempfile.NamedTemporaryFile(mode="w") as handle:
        handle.write("stub")
        yield handle.name


@pytest.fixture
def temp_ca_cert():
    with temp_file() as fname:
        yield fname


@pytest.fixture
def temp_client_cert():
    with temp_file() as fname:
        yield fname


@pytest.fixture
def temp_client_key():
    with temp_file() as fname:
        yield fname


## Happy Paths #################################################################


def test_happy_path_no_tls():
    conn = TGISConnection.from_config("", {TGISConnection.HOSTNAME_KEY: "foo.bar:1234"})
    assert conn.hostname == "foo.bar:1234"
    assert conn.ca_cert_file is None
    assert conn.client_tls is None


def test_happy_path_template():
    template_piece = "{{{}}}".format(TGISConnection.HOSTNAME_TEMPLATE_MODEL_ID)
    template = f"foo.{template_piece}.bar.{template_piece}"
    model_id = "some/model"
    conn = TGISConnection.from_config(
        model_id,
        {TGISConnection.HOSTNAME_KEY: template},
    )
    assert conn.hostname == template.format(
        **{TGISConnection.HOSTNAME_TEMPLATE_MODEL_ID: model_id}
    )


def test_happy_path_tls(temp_ca_cert):
    conn = TGISConnection.from_config(
        "",
        {
            TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
            TGISConnection.CA_CERT_FILE_KEY: temp_ca_cert,
        },
    )
    assert conn.hostname == "foo.bar:1234"
    assert conn.ca_cert_file is temp_ca_cert
    assert conn.client_tls is None


def test_happy_path_mtls(temp_ca_cert, temp_client_cert, temp_client_key):
    conn = TGISConnection.from_config(
        "",
        {
            TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
            TGISConnection.CA_CERT_FILE_KEY: temp_ca_cert,
            TGISConnection.CLIENT_CERT_FILE_KEY: temp_client_cert,
            TGISConnection.CLIENT_KEY_FILE_KEY: temp_client_key,
        },
    )
    assert conn.hostname == "foo.bar:1234"
    assert conn.ca_cert_file is temp_ca_cert
    assert conn.client_tls
    assert conn.client_tls.cert_file is temp_client_cert
    assert conn.client_tls.key_file is temp_client_key


def test_load_prompt_artifacts_ok():
    """Make sure that prompt artifacts are correctly copied to the prompt dir"""
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            # Make some source files
            source_fnames = ["foo.pt", "bar.pt"]
            source_files = [os.path.join(source_dir, fname) for fname in source_fnames]
            for source_file in source_files:
                with open(source_file, "w") as handle:
                    handle.write("stub")

            # Make the connection with the prompt dir
            conn = TGISConnection.from_config(
                "",
                {
                    TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
                    TGISConnection.PROMPT_DIR_KEY: prompt_dir,
                },
            )

            # Copy the artifacts over
            prompt_id = "some-prompt-id"
            conn.load_prompt_artifacts(prompt_id, *source_files)

            # Make sure the artifacts are available
            for fname in source_fnames:
                assert os.path.exists(os.path.join(prompt_dir, prompt_id, fname))


def test_load_prompt_artifacts_bad_source_file():
    """Make sure an error is raised if the source file doesn't exist or is a
    directory
    """
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            # Make the connection with the prompt dir
            conn = TGISConnection.from_config(
                "",
                {
                    TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
                    TGISConnection.PROMPT_DIR_KEY: prompt_dir,
                },
            )
            prompt_id = "some-prompt-id"
            with pytest.raises(FileNotFoundError):
                conn.load_prompt_artifacts(prompt_id, source_dir)
            with pytest.raises(FileNotFoundError):
                conn.load_prompt_artifacts(
                    prompt_id, os.path.join(source_dir, "does-not-exist.pt")
                )


def test_load_prompt_artifacts_no_prompt_dir():
    """Make sure an error is raised if the the connection does not support a
    prompt dir
    """
    with tempfile.TemporaryDirectory() as source_dir:
        # Make some source files
        source_fnames = ["foo.pt", "bar.pt"]
        source_files = [os.path.join(source_dir, fname) for fname in source_fnames]
        for source_file in source_files:
            with open(source_file, "w") as handle:
                handle.write("stub")

        # Make the connection with the prompt dir
        conn = TGISConnection.from_config(
            "",
            {TGISConnection.HOSTNAME_KEY: "foo.bar:1234"},
        )

        # Copy the artifacts over
        prompt_id = "some-prompt-id"
        with pytest.raises(ValueError):
            conn.load_prompt_artifacts(prompt_id, *source_files)


def tests_load_prompt_artifacts_dont_copy_existing_files():
    """Make sure that only files which doesn't exist in the prompt dir is copied"""
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            prompt_id = "some-prompt-id"

            # Make some source files and prompt files
            fnames = ["foo.pt", "bar.pt"]
            source_files = [os.path.join(source_dir, fname) for fname in fnames]
            for fname in source_files:
                with open(fname, "w", encoding="utf8") as f:
                    f.write("new stub")

            # Make some source files and prompt files
            # Output path: prompt_dir / prompt_id / prompt_file.pt
            os.mkdir(os.path.join(prompt_dir, prompt_id))
            prompt_files = [
                os.path.join(prompt_dir, prompt_id, fname) for fname in fnames
            ]
            for fname in prompt_files:
                with open(fname, "w", encoding="utf8") as f:
                    f.write("old stub")

            # Make the connection with the prompt dir
            conn = TGISConnection.from_config(
                "",
                {
                    TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
                    TGISConnection.PROMPT_DIR_KEY: prompt_dir,
                },
            )

            # Copy the artifacts over
            conn.load_prompt_artifacts(prompt_id, *source_files)

            # Make sure the artifacts are available
            for fname in prompt_files:
                assert os.path.exists(fname)
                with open(fname, "r", encoding="utf8") as f:
                    assert f.read() == "old stub"


def tests_load_prompt_artifacts_exclude_swp_files():
    """Make sure that swp files in the prompt_dir causes the source file to be excluded.
    This assumes another process is by copying other files."""
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            prompt_id = "some-prompt-id"

            # Make some source files and prompt files
            fnames = ["foo.pt", "bar.pt"]
            source_files = [os.path.join(source_dir, fname) for fname in fnames]
            for fname in source_files:
                with open(fname, "w", encoding="utf8") as f:
                    f.write("new stub")

            # Make some source files and prompt files
            # Output path: prompt_dir / prompt_id / prompt_file.pt
            target_dir = Path(prompt_dir) / prompt_id
            os.mkdir(target_dir)
            swp_file = os.path.join(prompt_dir, prompt_id, "bar.swp")
            with open(swp_file, "w", encoding="utf8") as f:
                f.write("in progress")

            # Make the connection with the prompt dir
            conn = TGISConnection.from_config(
                "",
                {
                    TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
                    TGISConnection.PROMPT_DIR_KEY: prompt_dir,
                },
            )

            # Copy the artifacts over
            conn.load_prompt_artifacts(prompt_id, *source_files)

            # Make sure the correct artifacts are available
            expected_prompt_files = {"foo.pt", "bar.swp"}
            assert {
                f.name for f in Path(target_dir).iterdir()
            } == expected_prompt_files, "Incorrect files were copied"
            with open(target_dir / "foo.pt", "r", encoding="utf8") as f:
                assert f.read() == "new stub", "File was not copied to prompt_dir"
            with open(target_dir / "bar.swp", "r", encoding="utf8") as f:
                assert f.read() == "in progress", "Swap file should not be overwritten"


def test_unload_prompt_artifacts_ok():
    """Make sure that prompt artifacts can be unloaded cleanly"""
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            # Make some source files
            source_fnames = ["foo.pt", "bar.pt"]
            source_files = [os.path.join(source_dir, fname) for fname in source_fnames]
            for source_file in source_files:
                with open(source_file, "w") as handle:
                    handle.write("stub")

            # Make the connection with the prompt dir
            conn = TGISConnection.from_config(
                "",
                {
                    TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
                    TGISConnection.PROMPT_DIR_KEY: prompt_dir,
                },
            )

            # Copy the artifacts over
            prompt_id = "some-prompt-id"
            conn.load_prompt_artifacts(prompt_id, *source_files)

            # Make sure the artifacts are available
            for fname in source_fnames:
                assert os.path.exists(os.path.join(prompt_dir, prompt_id, fname))

            # Unload all of the prompts and make sure they're gone
            conn.unload_prompt_artifacts(prompt_id)
            assert not os.path.exists(os.path.join(prompt_dir, prompt_id))


def test_unload_prompt_artifacts_bad_prompt_id():
    """Make sure that unloading a bad prompt ID is a no-op"""
    with tempfile.TemporaryDirectory() as source_dir:
        with tempfile.TemporaryDirectory() as prompt_dir:
            conn = TGISConnection.from_config(
                "",
                {
                    TGISConnection.HOSTNAME_KEY: "foo.bar:1234",
                    TGISConnection.PROMPT_DIR_KEY: prompt_dir,
                },
            )

            # Unload all of the prompts and make sure they're gone
            prompt_id = "some-prompt-id"
            conn.unload_prompt_artifacts(prompt_id)
            assert not os.path.exists(os.path.join(prompt_dir, prompt_id))


def test_connection_valid_endpoint(tgis_mock_insecure):
    """Make sure that a connection test works with a valid server"""
    conn = TGISConnection(hostname=tgis_mock_insecure.hostname, model_id="asdf")
    conn.test_connection()


def test_connection_invalid_endpoint():
    """Make sure that a connection test works with a valid server"""
    hostname = f"localhost:{tls_test_tools.open_port()}"
    conn = TGISConnection(hostname=hostname, model_id="foobar")
    with pytest.raises(grpc.RpcError):
        conn.test_connection()


# NOTE: All failure cases are exercised by test_invalid_connection in
#   test_tgis_backend.py
