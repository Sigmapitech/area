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
        const res = await fetch(
          `${API_BASE_URL}/workflow/${workflowId}/edges`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              from_node_id: params.source,
              to_node_id: params.target,
            }),
          }
        );

        if (!res.ok) {
          console.error("Failed to create edge:", res.statusText);
          return;
        }

        const savedEdge = await res.json();
        setEdges((eds) => [
          ...eds,
          {
            id: `e${savedEdge.from_node_id}-${savedEdge.to_node_id}`,
            source: savedEdge.from_node_id.toString(),
            target: savedEdge.to_node_id.toString(),
            animated: true,
          },
        ]);
      } catch (err) {
        console.error("Error creating edge:", err);
      }
    },
    [workflowId, token, setEdges]
  );

  useEffect(() => {
    const fetchWorkflow = async () => {
      if (!workflowId || !token) return;
      setLoading(true);

      try {
        const resNodes = await fetch(`${API_BASE_URL}/workflow/${workflowId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const dataNodes = await resNodes.json();

        if (
          resNodes.status === 404 &&
          dataNodes.detail === "Workflow not found"
        ) {
          navigate("/workflow", { replace: true });
          return;
        }

        const fetchedNodes = dataNodes.nodes.map((node, index: number) => ({
          id: node.id.toString(),
          data: { label: `Node ${node.id}` },
          position: {
            x: (node.config?.parent_id ?? 0) * 200,
            y: index * 120,
          },
          ...nodeDefaults,
        }));
        setNodes(fetchedNodes);

        const resEdges = await fetch(
          `${API_BASE_URL}/workflow/${workflowId}/edges`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const dataEdges = await resEdges.json();

        const fetchedEdges = dataEdges.map((edge) => ({
          id: `e${edge.from_node_id}-${edge.to_node_id}`,
          source: edge.from_node_id.toString(),
          target: edge.to_node_id.toString(),
          animated: true,
        }));
        setEdges(fetchedEdges);
      } catch (err) {
        console.error("Error loading workflow:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchWorkflow();
  }, [workflowId, token, setNodes, setEdges, navigate]);

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
