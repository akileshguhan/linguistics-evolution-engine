"use client";

import { useEffect, useState, useCallback } from 'react';
import { ReactFlow, Background, Controls, Node, Edge, NodeMouseHandler } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { fetchTreeData, fetchEpochState } from '../lib/api';
import { useSimulationStore } from '../lib/store';

interface TreeRow {
  source: string;
  source_epoch: number;
  root: string;
  target: string | null;
  target_epoch: number | null;
  event: string;
  isolation: number;
  density: number;
}

export default function PhylogeneticTree() {
  const { currentEpoch, setActiveWords, setEpoch } = useSimulationStore();
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    const loadGraph = async () => {
      try {
        const response = await fetchTreeData();
        const rawData = response.data;
        
        const newNodes: Node[] = [];
        const newEdges: Edge[] = [];
        const addedNodeIds = new Set<string>();

        // Process Neo4j rows into React Flow layout
        rawData.forEach((row: TreeRow, index: number) => {
          // Add Source Node (Parent)
          const sourceId = `${row.source}-${row.source_epoch}`;
          if (!addedNodeIds.has(sourceId)) {
            newNodes.push({
              id: sourceId,
              data: { label: `${row.source} (Ep: ${row.source_epoch})`, epoch: row.source_epoch },
              position: { x: row.source_epoch * 300, y: (index % 5) * 100 },
              className: 'bg-black/60 backdrop-blur-md border border-white/20 text-blue-100 rounded-xl p-3 font-mono text-sm shadow-[0_0_15px_rgba(59,130,246,0.2)] cursor-pointer hover:border-blue-400 hover:shadow-[0_0_20px_rgba(59,130,246,0.5)] transition-all',
            });
            addedNodeIds.add(sourceId);
          }

          // Add Target Node & Edge (Child)
          if (row.target && row.target_epoch !== null) {
            const targetId = `${row.target}-${row.target_epoch}`;
            if (!addedNodeIds.has(targetId)) {
              newNodes.push({
                id: targetId,
                data: { label: `${row.target} (Ep: ${row.target_epoch})`, epoch: row.target_epoch },
                position: { x: row.target_epoch * 300, y: (index % 5) * 100 },
                className: 'bg-black/60 backdrop-blur-md border border-purple-500/50 text-purple-100 rounded-xl p-3 font-mono text-sm shadow-[0_0_15px_rgba(168,85,247,0.2)] cursor-pointer hover:border-purple-400 hover:shadow-[0_0_20px_rgba(168,85,247,0.5)] transition-all',
              });
              addedNodeIds.add(targetId);
            }

            // Connect them
            newEdges.push({
              id: `e-${sourceId}-${targetId}-${index}`,
              source: sourceId,
              target: targetId,
              animated: true,
              label: row.event !== 'none' ? row.event : '',
              style: { stroke: 'rgba(255,255,255,0.3)', strokeWidth: 2 },
              labelStyle: { fill: '#9ca3af', fontWeight: 600, fontSize: 10 },
              labelBgStyle: { fill: 'rgba(0,0,0,0.7)', padding: 4 }
            });
          }
        });

        setNodes(newNodes);
        setEdges(newEdges);
      } catch (error) {
        console.error("Error fetching tree data:", error);
      }
    };

    if (currentEpoch >= 0) {
      loadGraph();
    }
  }, [currentEpoch]);

  const onNodeClick: NodeMouseHandler = useCallback(async (event, node) => {
    try {
      const epochToLoad = node.data.epoch as number;
      const response = await fetchEpochState(epochToLoad);
      if (response.status === 'success') {
        setActiveWords(response.words);
        setEpoch(epochToLoad);
      }
    } catch (err) {
      console.error("Failed to load historical state", err);
    }
  }, [setActiveWords, setEpoch]);

  return (
    <div className="flex-grow bg-black/20 backdrop-blur-3xl border border-white/10 rounded-2xl overflow-hidden shadow-2xl relative h-[600px] md:h-auto">
      <ReactFlow 
        nodes={nodes} 
        edges={edges} 
        fitView 
        colorMode="dark"
        onNodeClick={onNodeClick}
      >
        <Background color="rgba(255,255,255,0.05)" />
        <Controls className="bg-black/50 border border-white/10 fill-white" />
      </ReactFlow>
      <div className="absolute top-4 left-4 bg-black/60 backdrop-blur-md px-4 py-2 rounded-full text-xs font-semibold text-blue-200 border border-white/10 shadow-lg tracking-wider uppercase">
        Live Phylogenetic Trajectory
      </div>
      <div className="absolute bottom-4 left-4 bg-black/60 backdrop-blur-md px-4 py-2 rounded-lg text-xs font-medium text-gray-300 border border-white/10 shadow-lg pointer-events-none">
        Click any node to rewind time and branch a new timeline.
      </div>
    </div>
  );
}