import pytest
from debuff.main import api
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_app():
    client = TestClient(api)
    yield client
