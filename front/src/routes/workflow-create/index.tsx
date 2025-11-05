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
  const [newWorkflow, setNewWorkflow] = useState({ name: "", description: "" });
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingData, setEditingData] = useState({ name: "", description: "" });

  const createNewWorkflow = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWorkflow.name.trim()) return;

    try {
      const response = await fetch(`${API_BASE_URL}/workflow`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newWorkflow),
      });

      if (!response.ok) throw new Error("Failed to create workflow");

      const data = await response.json();
      setWorkflows((prev) => [...prev, data]);
      setNewWorkflow({ name: "", description: "" });
    } catch (error) {
      console.error(error);
      alert("Error creating workflow");
    }
  };

  const deleteWorkflow = async (id: number) => {
    if (!confirm("Delete this workflow?")) return;

    try {
      const response = await fetch(`${API_BASE_URL}/workflow/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        setWorkflows((prev) => prev.filter((w) => w.id !== id));
      }
    } catch (error) {
      console.error(error);
      alert("Failed to delete workflow");
    }
  };

  const startEditing = (workflow: Workflow) => {
    setEditingId(workflow.id);
    setEditingData({
      name: workflow.name,
      description: workflow.description || "",
    });
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditingData({ name: "", description: "" });
  };

  const saveEditing = async (id: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/workflow/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(editingData),
      });
      if (!response.ok) throw new Error("Failed to update workflow");

      const updated = await response.json();
      setWorkflows((prev) => prev.map((w) => (w.id === id ? updated : w)));
      cancelEditing();
    } catch (error) {
      console.error(error);
      alert("Failed to update workflow");
    }
  };

  useEffect(() => {
    fetch(`${API_BASE_URL}/workflow`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        setWorkflows(data);
        setLoading(false);
      })
      .catch((e) => console.error(e));
  }, [token]);

  if (loading) return <div className="workflow-list__loading">Loading...</div>;

  return (
    <div className="workflow-wrapper">
      <div className="workflow-list">
        <h1>Workflows</h1>

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
            placeholder="Description"
            value={newWorkflow.description}
            onChange={(e) =>
              setNewWorkflow((f) => ({ ...f, description: e.target.value }))
            }
          />
          <button className="btn" type="submit">
            ＋ Create Workflow
          </button>
        </form>

        <ul className="workflow-items">
          {workflows.map((workflow) => (
            <li className="workflow-card" key={workflow.id}>
              <div className="workflow-card__main">
                {editingId === workflow.id ? (
                  <>
                    <input
                      type="text"
                      value={editingData.name}
                      onChange={(e) =>
                        setEditingData((d) => ({ ...d, name: e.target.value }))
                      }
                    />
                    <input
                      type="text"
                      value={editingData.description}
                      onChange={(e) =>
                        setEditingData((d) => ({
                          ...d,
                          description: e.target.value,
                        }))
                      }
                    />
                  </>
                ) : (
                  <>
                    <h3>{workflow.name}</h3>
                    <p>{workflow.description || "No description"}</p>
                  </>
                )}
              </div>
              <div className="workflow-card__actions">
                {editingId === workflow.id ? (
                  <>
                    <button
                      type="button"
                      className="btn save-btn"
                      onClick={() => saveEditing(workflow.id)}
                    >
                      Save
                    </button>
                    <button
                      type="button"
                      className="btn cancel-btn"
                      onClick={cancelEditing}
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <>
                    <Link
                      to={`/workflow/${workflow.id}`}
                      className="btn view-btn"
                    >
                      View
                    </Link>
                    <button
                      type="button"
                      className="btn edit-btn"
                      onClick={() => startEditing(workflow)}
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      className="btn delete-btn"
                      onClick={() => deleteWorkflow(workflow.id)}
                    >
                      Delete
                    </button>
                  </>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
