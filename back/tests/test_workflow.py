from http import HTTPStatus


def test_create_workflow(client, auth_headers):
    wf_payload = {
        "name": "pytest workflow",
        "description": "Created by pytest",
    }
    resp = client.post("/api/workflow", json=wf_payload, headers=auth_headers)
    assert resp.status_code == HTTPStatus.CREATED
    wf = resp.json()
    assert wf["name"] == "pytest workflow"
    assert "id" in wf


def test_update_workflow_name(client, auth_headers):
    wf_payload = {
        "name": "original name",
        "description": "workflow to update",
    }
    resp = client.post("/api/workflow", json=wf_payload, headers=auth_headers)
    assert resp.status_code == HTTPStatus.CREATED
    wf = resp.json()
    wf_id = wf["id"]

    update_payload = {"name": "updated name"}
    resp = client.patch(
        f"/api/workflow/{wf_id}", json=update_payload, headers=auth_headers
    )
    assert resp.status_code == HTTPStatus.OK
    updated_wf = resp.json()

    assert updated_wf["name"] == "updated name"
    assert updated_wf["id"] == wf_id


def test_delete_workflow(client, auth_headers):
    wf_payload = {
        "name": "temp workflow",
        "description": "To be deleted",
    }
    resp = client.post("/api/workflow", json=wf_payload, headers=auth_headers)
    assert resp.status_code == HTTPStatus.CREATED
    wf = resp.json()
    wf_id = wf["id"]

    resp = client.delete(f"/api/workflow/{wf_id}", headers=auth_headers)
    assert resp.status_code == HTTPStatus.NO_CONTENT

    resp = client.get(f"/api/workflow/{wf_id}", headers=auth_headers)
    assert resp.status_code == HTTPStatus.NOT_FOUND
