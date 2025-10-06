def test_create_workflow(client, auth_headers):
    wf_payload = {
        "name": "pytest workflow",
        "description": "Created by pytest",
    }
    resp = client.post("/api/workflow", json=wf_payload, headers=auth_headers)
    assert resp.status_code == 201
    wf = resp.json()
    assert wf["name"] == "pytest workflow"
    assert "id" in wf
