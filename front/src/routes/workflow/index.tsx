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
import { useCallback } from "react";
import "@xyflow/react/dist/style.css";

import "./style.scss";

const nodeDefaults = {
  sourcePosition: Position.Right,
  targetPosition: Position.Left,
};

export default function GraphPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const onConnect = useCallback(
    (params: Connection) => setEdges((els) => addEdge(params, els)),
    [setEdges]
  );

  const handleAddNode = useCallback(() => {
    const newId = (nodes.length + 1).toString();
    const newNode = {
      id: newId,
      data: { label: `New Node (${newId})` },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      ...nodeDefaults,
    };
    setNodes((nds) => [...nds, newNode]);
  }, [nodes, setNodes]);

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
      <button type="button" className="add-node-btn" onClick={handleAddNode}>
        Add Node
      </button>
    </main>
  );
}
