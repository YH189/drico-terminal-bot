import os
import shutil
import tempfile

import pytest


@pytest.fixture
def drico_home(monkeypatch):
    path = tempfile.mkdtemp(prefix="drico-test-")
    monkeypatch.setenv("DRICO_HOME", path)
    yield path
    shutil.rmtree(path, ignore_errors=True)
