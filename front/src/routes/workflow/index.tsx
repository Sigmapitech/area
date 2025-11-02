import {
  addEdge,
  Background,
  type Connection,
  Controls,
  Position,
  ReactFlow,
  ReactFlowProvider,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";
import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router";
import "@xyflow/react/dist/style.css";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

import "./style.scss";

const nodeDefaults = {
  sourcePosition: Position.Right,
  targetPosition: Position.Left,
};

export default function GraphPage() {
  const { token } = useAuth();
  const navigate = useNavigate();

  const { workflowId } = useParams<{ workflowId: string }>();

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);

  const onConnect = useCallback(
    async (params: Connection) => {
      setEdges((els) => addEdge(params, els));

      if (!workflowId || !token) return;

      try {
        const targetNodeId = params.target;
        const sourceNodeId = params.source;

        const res = await fetch(
          `${API_BASE_URL}/workflow/${workflowId}/nodes/${targetNodeId}`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ parent_id: sourceNodeId }),
          }
        );

        if (!res.ok) {
          console.error("Failed to update node parent:", res.statusText);
          return;
        }

        const updatedNode = await res.json();
        setNodes((nds) =>
          nds.map((n) =>
            n.id === updatedNode.id.toString()
              ? {
                  ...n,
                  data: {
                    label: `Node ${updatedNode.id}`,
                  },
                }
              : n
          )
        );
      } catch (err) {
        console.error("Error updating node parent:", err);
      }
    },
    [setEdges, setNodes, workflowId, token]
  );

  useEffect(() => {
    const fetchNodes = async () => {
      if (!workflowId || !token) return;
      setLoading(true);

      try {
        const res = await fetch(`${API_BASE_URL}/workflow/${workflowId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const data = await res.json();
        if (res.status === 404 && data.detail === "Workflow not found") {
          navigate("/workflow", { replace: true });
          return;
        }

        // Map nodes
        const fetchedNodes = data.nodes.map((node: any, index: number) => ({
          id: node.id.toString(),
          data: { label: `Node ${node.id}` },
          position: { x: (node.config?.parent_id ?? 0) * 200, y: index * 120 },
          ...nodeDefaults,
        }));

        // Create edges if node.config contains parent info
        const fetchedEdges = data.nodes
          .filter((n: any) => n.config?.parent_id)
          .map((n: any) => ({
            id: `e${n.config.parent_id}-${n.id}`,
            source: n.config.parent_id.toString(),
            target: n.id.toString(),
            animated: true,
          }));

        setNodes(fetchedNodes);
        setEdges(fetchedEdges);
      } catch (err) {
        console.error("Error loading workflow:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchNodes();
  }, [workflowId, token, setNodes, setEdges]);

  const handleAddNode = useCallback(async () => {
    if (!workflowId || !token) return;

    const newNodeId = nodes.length + 1;
    const newNode = {
      id: newNodeId,
      data: { label: `Node ${newNodeId}` },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      ...nodeDefaults,
    };

    try {
      const res = await fetch(`${API_BASE_URL}/workflow/${workflowId}/nodes`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ workflow_id: workflowId }),
      });

      if (!res.ok) {
        console.error("Failed to add node:", res.statusText);
        return;
      }

      const savedNode = await res.json();
      setNodes((nds) => [
        ...nds,
        {
          ...newNode,
          id: savedNode.id.toString(),
          data: { label: `Node ${savedNode.id}` },
        },
      ]);
    } catch (err) {
      console.error("Error adding node:", err);
    }
  }, [nodes, setNodes, workflowId, token]);

  if (loading) return <div className="info-loading">Loading workflow...</div>;

  return (
    <main className="workflow-editor">
      <ReactFlowProvider>
        <ReactFlow
          colorMode="system"
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </ReactFlowProvider>
      <button
        type="button"
        className="btn add-node-btn"
        onClick={handleAddNode}
      >
        Add Node
      </button>
    </main>
  );
}
