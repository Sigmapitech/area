from http import HTTPStatus


def test_hello(client):
    resp = client.get("/hello")
    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert "hello" in str(data).lower()
