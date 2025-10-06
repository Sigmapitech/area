import { API_BASE_URL } from "@/api_url";
import { useEffect, useState } from "react";
import { Link } from "react-router";

interface Workflow {
  id: number;
  name: string;
  description: string;
}

const WorkflowList = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>();
  const [newWorkflow, setNewWorkflow] = useState<Workflow>({
    name: "",
    description: "",
    id: 0,
  });

  const createNewWorkflow = (info: React.FormEvent) => {
    info.preventDefault();
    const formData = new FormData();
    formData.append("name", newWorkflow.name);
    formData.append("description", newWorkflow.description);

    fetch(`${API_BASE_URL}/api/workflow`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: formData,
    });
  };

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/workflow`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((response) => response.json())
      .then((data) => setWorkflows(data))
      .catch((e) => console.error(e));
  }, []);

  console.table(workflows);
  return (
    <>
      <Link to="/">Back to home</Link>
      <form className="Create new Workflow" onSubmit={createNewWorkflow}>
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
        <button type="submit">test</button>
      </form>
    </>
  );
};

export default WorkflowList;
