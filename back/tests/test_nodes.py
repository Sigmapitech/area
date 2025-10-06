def test_add_nodes(client, auth_headers, workflow):
    wf_id = workflow["id"]

    foo_payload = {
        "name": "foo",
        "description": "foo node",
        "node_type": "receive",
    }
    resp = client.post(
        f"/api/workflow/{wf_id}", json=foo_payload, headers=auth_headers
    )
    assert resp.status_code == 201
    foo = resp.json()

    assert foo["id"] == 1

    bar_payload = {
        "name": "bar",
        "description": "bar node",
        "node_type": "send",
    }
    resp = client.post(
        f"/api/workflow/{wf_id}", json=bar_payload, headers=auth_headers
    )
    assert resp.status_code == 201
    bar = resp.json()

    assert bar["id"] == 2


def test_connect_nodes(client, auth_headers, workflow):
    wf_id = workflow["id"]

    foo_payload = {
        "name": "foo",
        "description": "foo node",
        "node_type": "receive",
    }
    foo = client.post(
        f"/api/workflow/{wf_id}", json=foo_payload, headers=auth_headers
    ).json()

    bar_payload = {
        "name": "bar",
        "description": "bar node",
        "node_type": "send",
    }
    bar = client.post(
        f"/api/workflow/{wf_id}", json=bar_payload, headers=auth_headers
    ).json()

    patch_payload = {"parent_id": foo["id"]}
    resp = client.patch(
        f"/api/workflow/{wf_id}/{bar['id']}",
        json=patch_payload,
        headers=auth_headers,
    )

    assert resp.status_code == 200
    connected = resp.json()
    assert connected.get("parent_id") == foo["id"]
