from http import HTTPStatus


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
    assert resp.status_code == HTTPStatus.CREATED
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
    assert resp.status_code == HTTPStatus.CREATED
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

    assert resp.status_code == HTTPStatus.OK
    connected = resp.json()
    assert connected.get("parent_id") == foo["id"]


def test_delete_node(client, auth_headers, workflow):
    wf_id = workflow["id"]

    node_payload = {
        "name": "temp_node",
        "description": "temporary node",
        "node_type": "receive",
    }
    resp = client.post(
        f"/api/workflow/{wf_id}", json=node_payload, headers=auth_headers
    )
    assert resp.status_code == HTTPStatus.CREATED
    node = resp.json()
    node_id = node["id"]

    resp = client.delete(
        f"/api/workflow/{wf_id}/{node_id}", headers=auth_headers
    )
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = client.get(f"/api/workflow/{wf_id}/{node_id}", headers=auth_headers)
    assert resp.status_code == HTTPStatus.NOT_FOUND
