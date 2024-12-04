import pytest

from semver_check import app


@pytest.fixture()
def app_test():
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app_test):
    return app_test.test_client()


@pytest.fixture()
def runner(app_test):
    return app_test.test_cli_runner()


def test_request_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!doctype html>" in response.data
    assert b"<title>" in response.data
    assert b"<body>" in response.data


def test_request_validate_valid(client):
    response = client.post("/validate", data="1.0.0")
    assert response.status_code == 200
    assert response.json["valid"]
    assert response.json["version"] == "1.0.0"


def test_request_validate_non_valid(client):
    response = client.post("/validate", data="1.0.0+")
    assert response.status_code == 400
    assert not response.json["valid"]
    assert response.json["version"] == "1.0.0+"


def test_request_validate_no_data(client):
    response = client.post("/validate")
    assert response.status_code == 400
    assert response.data == b"Version string missing in the request body"
