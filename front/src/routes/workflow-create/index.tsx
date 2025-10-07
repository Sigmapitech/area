import { useEffect, useState } from "react";
import { Link } from "react-router";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

import "./style.scss";

interface Workflow {
  id: number;
  name: string;
  description: string;
}

export default function WorkflowList() {
  const { token } = useAuth();

  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [newWorkflow, setNewWorkflow] = useState<Workflow>({
    name: "",
    description: "",
    id: 0,
  });

  const createNewWorkflow = (info: React.FormEvent) => {
    info.preventDefault();

    fetch(`${API_BASE_URL}/api/workflow`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: newWorkflow.name,
        description: newWorkflow.description,
      }),
    })
      .then((response) => response.json())
      .then((data) => setWorkflows([...workflows, data]));
  };

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/workflow`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => setWorkflows(data))
      .catch((e) => console.error(e));
    console.table(workflows);
  }, [workflows, token]);

  return (
    <>
      <Link to="/">Back to home</Link>
      <form className="workflow-create-form" onSubmit={createNewWorkflow}>
        <input
          type="text"
          placeholder="Name"
          value={newWorkflow.name}
          onChange={(e) =>
            setNewWorkflow((f) => ({ ...f, name: e.target.value }))
          }
          required
        />
        <input
          type="text"
          placeholder="description"
          value={newWorkflow.description}
          onChange={(e) =>
            setNewWorkflow((f) => ({ ...f, description: e.target.value }))
          }
        />
        <button type="submit">Create new workflow</button>
      </form>
      <ul>
        {workflows.map((workflow) => (
          <li className="workflow" key={workflow.id}>
            <p>{workflow.id}</p>
            <p>{workflow.name}</p>
            <p key={workflow.id}>{workflow.description}</p>
          </li>
        ))}
      </ul>
    </>
  );
}
