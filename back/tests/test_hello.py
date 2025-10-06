def test_hello(client):
    resp = client.get("/api/hello")
    assert resp.status_code == 200
    data = resp.json()
    assert "hello" in str(data).lower()
