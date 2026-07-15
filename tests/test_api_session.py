import re
from unittest.mock import patch, MagicMock

import pytest

from core.api import APISession


def make_session(token="test-token-abcde"):
    """Construct an APISession bypassing token resolution and requests.session()."""
    with patch("requests.session") as mock_session_factory:
        mock_http = MagicMock()
        mock_session_factory.return_value = mock_http
        s = APISession.__new__(APISession)
        s.token = token
        s.session = s._create_session()
        return s, mock_http


def test_user_agent_header_is_set():
    _, mock_http = make_session()
    assert "User-Agent" in mock_http.headers


def test_user_agent_starts_with_origin_python_sdk():
    _, mock_http = make_session()
    assert mock_http.headers["User-Agent"].startswith("origin-python-sdk/")


def test_user_agent_includes_version_number():
    _, mock_http = make_session()
    user_agent = mock_http.headers["User-Agent"]
    # version segment must look like a PEP 440 version, e.g. "0.30.1"
    version_part = user_agent.split("/", 1)[1]
    assert re.match(r"^\d+\.\d+", version_part), (
        f"Expected a version number after 'origin-python-sdk/', got: {version_part!r}"
    )


def test_user_agent_version_matches_installed_package():
    from importlib.metadata import version

    expected = f"origin-python-sdk/{version('aurora_origin_sdk')}"
    _, mock_http = make_session()
    assert mock_http.headers["User-Agent"] == expected


def test_user_agent_not_overridden_by_different_token():
    """User-Agent must be the same regardless of which token is used."""
    _, http1 = make_session(token="token-aaaaa")
    _, http2 = make_session(token="token-bbbbb")
    assert http1.headers["User-Agent"] == http2.headers["User-Agent"]


def test_existing_auth_headers_still_set():
    _, mock_http = make_session(token="mytoken12345")
    assert mock_http.headers["Private-Token"] == "mytoken12345"
    assert mock_http.headers["EOS-Cookie"] == "mytoken12345"
    assert mock_http.headers["Content-Type"] == "application/json"
