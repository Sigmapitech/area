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
import { useParams } from "react-router";
import "@xyflow/react/dist/style.css";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

import "./style.scss";

interface WorkflowNode {
  id: number;
  node_id: number | null;
  key: string;
  value?: string;
}

interface WorkflowDetail {
  id: number;
  workflow_id: number;
  config: WorkflowNode[];
}

const nodeDefaults = {
  sourcePosition: Position.Right,
  targetPosition: Position.Left,
};

export default function GraphPage() {
  const { token } = useAuth();
  const { workflowId } = useParams<{ workflowId: string }>();

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const [_indivNode, _setNode] = useState<WorkflowNode>({
    id: 0,
    node_id: null,
    key: "",
    value: "",
  });

  const [loading, setLoading] = useState(true);

  const onConnect = useCallback(
    async (params: Connection) => {
      setEdges((els) => addEdge(params, els));

      if (!workflowId || !token) return;

      try {
        const targetNodeId = params.target;
        const sourceNodeId = params.source;

        const res = await fetch(
          `${API_BASE_URL}/workflow/${workflowId}/${targetNodeId}`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              parent_id: sourceNodeId,
            }),
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
                    label: `${updatedNode.key} (${updatedNode.id})`,
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
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE_URL}/workflow/${workflowId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) {
          console.error("Failed to fetch workflow:", res.statusText);
          return;
        }

        const data: WorkflowDetail = await res.json();

        const fetchedNodes = data.config.map((node, index) => ({
          id: node.id.toString(),
          data: { label: `${node.key} (${node.id})` },
          position: {
            x: (node.node_id ?? 0) * 200,
            y: index * 120,
          },
          ...nodeDefaults,
        }));

        const fetchedEdges = data.config
          .filter((n) => n.node_id)
          .map((n) => ({
            id: `e${n.node_id}-${n.id}`,
            source: n.node_id?.toString(),
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

    const newId = nodes.length + 1;
    const newNode = {
      id: newId,
      data: { label: `New Node (${newId})` },
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
        body: JSON.stringify({
          id: newNode.id,
          node_id: null,
          key: "send",
          value: {},
        }),
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
          data: { label: `${savedNode.key} (${savedNode.id})` },
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
