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

  const createNewWorkflow = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/api/workflow`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: newWorkflow.name,
          description: newWorkflow.description,
        }),
      });
      const data = await response.json();

      setWorkflows((prev) => [...prev, data]);
      setNewWorkflow({ id: 0, name: "", description: "" });
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/workflow`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setWorkflows(data);
      })
      .catch((e) => console.error(e));
  }, [token]);

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
