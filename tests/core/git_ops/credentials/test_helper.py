# tests/core/git_ops/credentials/test_helper.py

"""Tests for the bounded Git credential protocol helper."""

import io
from types import SimpleNamespace

from app.core.git_ops.credentials import CredentialProvider, CredentialSource, helper


def test_get_outputs_only_git_protocol_fields(monkeypatch):
    material = SimpleNamespace(
        provider=CredentialProvider.GITHUB,
        source=CredentialSource.FILE,
        username="x-access-token",
        token="secret",
    )
    service = SimpleNamespace(material_for_helper=lambda remote_url: material)
    monkeypatch.setattr(helper, "CredentialService", lambda: service)
    monkeypatch.setattr(
        helper.sys,
        "stdin",
        io.StringIO("protocol=https\nhost=github.com\npath=org/repo.git\n\n"),
    )
    output = io.StringIO()
    monkeypatch.setattr(helper.sys, "stdout", output)
    assert helper.run("get") == 0
    assert output.getvalue() == "username=x-access-token\npassword=secret\n\n"


def test_store_and_erase_are_intentional_noops(monkeypatch):
    monkeypatch.setattr(helper.sys, "stdin", io.StringIO("\n"))
    assert helper.run("store") == 0
    monkeypatch.setattr(helper.sys, "stdin", io.StringIO("\n"))
    assert helper.run("erase") == 0
