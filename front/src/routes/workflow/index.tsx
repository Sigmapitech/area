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
  const [selectedEdge, setSelectedEdge] = useState<any | null>(null);
  const [deleteButtonPos, setDeleteButtonPos] = useState<{ x: number; y: number } | null>(null);

  const onConnect = useCallback(
    async (params: Connection) => {
      if (!workflowId || !token) return;

      try {
        const res = await fetch(`${API_BASE_URL}/workflow/${workflowId}/edges`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            from_node_id: params.source,
            to_node_id: params.target,
          }),
        });

        if (!res.ok) {
          console.error("Failed to create edge:", res.statusText);
          return;
        }

        const savedEdge = await res.json();
        setEdges((eds) => [
          ...eds,
          {
            id: savedEdge.id,
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

  const onEdgeClick = useCallback(
    (event, edge) => {
      event.stopPropagation();
      setSelectedEdge(edge);

      const edgePath = event.target.getBoundingClientRect();
      setDeleteButtonPos({
        x: edgePath.left + edgePath.width / 2,
        y: edgePath.top + edgePath.height / 2,
      });
    },
    []
  );

  const handleDeleteEdge = useCallback(async () => {
    if (!selectedEdge || !token) return;

    try {
      const edgeId = selectedEdge.id;

      const res = await fetch(`${API_BASE_URL}/workflow/edges/${edgeId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        console.error("Failed to delete edge:", res.statusText);
        return;
      }

      setEdges((eds) => eds.filter((e) => e.id !== selectedEdge.id));
      setSelectedEdge(null);
      setDeleteButtonPos(null);
    } catch (err) {
      console.error("Error deleting edge:", err);
    }
  }, [selectedEdge, token, setEdges]);

  const onPaneClick = useCallback(() => {
    setSelectedEdge(null);
    setDeleteButtonPos(null);
  }, []);

  useEffect(() => {
    const fetchWorkflow = async () => {
      if (!workflowId || !token) return;
      setLoading(true);

      try {
        const resNodes = await fetch(`${API_BASE_URL}/workflow/${workflowId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const dataNodes = await resNodes.json();

        if (resNodes.status === 404 && dataNodes.detail === "Workflow not found") {
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

        const resEdges = await fetch(`${API_BASE_URL}/workflow/${workflowId}/edges`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const dataEdges = await resEdges.json();

        const fetchedEdges = dataEdges.map((edge) => ({
          id: edge.id,
          source: edge.from_node_id,
          target: edge.to_node_id,
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
          id: savedNode.id,
          data: { label: `Node ${savedNode.id}` },
        },
      ]);
    } catch (err) {
      console.error("Error adding node:", err);
    }
  }, [nodes, setNodes, workflowId, token]);

  if (loading) return <div className="info-loading">Loading workflow...</div>;

  return (
    <main className="workflow-editor" onClick={onPaneClick}>
      <ReactFlowProvider>
        <ReactFlow
          colorMode="system"
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onEdgeClick={onEdgeClick}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </ReactFlowProvider>

      {deleteButtonPos && (
        <button
          className="delete-edge-btn"
          style={{
            position: "absolute",
            top: deleteButtonPos.y - 20,
            left: deleteButtonPos.x - 20,
          }}
          onClick={(e) => {
            e.stopPropagation();
            handleDeleteEdge();
          }}
        >
          🗑️
        </button>
      )}

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
