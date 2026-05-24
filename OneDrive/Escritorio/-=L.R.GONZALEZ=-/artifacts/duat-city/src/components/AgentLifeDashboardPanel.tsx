import { useMemo } from "react";
import type { CityState } from "../core/types";
import { buildAgentRelationshipGraph } from "../agents/agentRelationshipGraph";
import { AGENT_ROLE_COLORS, rColor } from "../render/palette";

interface AgentLifeDashboardPanelProps {
  state: CityState;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}

export function AgentLifeDashboardPanel({ state, selectedId, onSelect }: AgentLifeDashboardPanelProps) {
  const graph = useMemo(() => buildAgentRelationshipGraph(state, selectedId), [selectedId, state]);
  const points = useMemo(() => layoutNodes(graph.nodes.length), [graph.nodes.length]);

  return (
    <div className="section" data-qa="agent-life-dashboard">
      <div className="section-title">Agent Life Graph</div>
      <svg className="agent-life-graph" viewBox="0 0 220 128" role="img" aria-label="Agent relationship graph">
        {graph.edges.map(edge => {
          const from = graph.nodes.findIndex(node => node.id === edge.from);
          const to = graph.nodes.findIndex(node => node.id === edge.to);
          if (from < 0 || to < 0) return null;
          const a = points[from];
          const b = points[to];
          return (
            <line
              key={`${edge.from}-${edge.to}-${edge.kind}`}
              x1={a.x}
              y1={a.y}
              x2={b.x}
              y2={b.y}
              stroke={edge.weight >= 0 ? "#2f9d78" : "#b85b5b"}
              strokeOpacity={0.22 + Math.min(0.6, Math.abs(edge.weight))}
              strokeWidth={edge.kind === "declared" ? 1.6 : 0.8}
            />
          );
        })}
        {graph.nodes.map((node, index) => {
          const point = points[index];
          const color = AGENT_ROLE_COLORS[node.role] ?? "#7cb9ff";
          return (
            <g key={node.id} onClick={() => onSelect(node.id)} className="agent-life-node">
              <circle
                cx={point.x}
                cy={point.y}
                r={node.selected ? 6 : 4.5}
                fill={color}
                stroke={node.selected ? "#ffffff" : rColor(node.R)}
                strokeWidth={node.selected ? 1.5 : 0.8}
              />
              <title>{node.name} R={node.R.toFixed(2)} Phi={node.Phi_eff.toFixed(2)}</title>
            </g>
          );
        })}
      </svg>
      <div className="mini-panel">
        <div className="stat-row"><span className="stat-key">Selected</span><span className="stat-val">{graph.dashboard.selectedAgentName ?? "none"}</span></div>
        <div className="stat-row"><span className="stat-key">Task</span><span className="stat-val">{graph.dashboard.task}</span></div>
        <div className="stat-row"><span className="stat-key">Weak need</span><span className="stat-val">{graph.dashboard.weakestNeed} {(graph.dashboard.weakestNeedValue * 100).toFixed(0)}%</span></div>
        <div className="stat-row"><span className="stat-key">Mood audio</span><span className="stat-val">{graph.dashboard.audioMoodTag}</span></div>
        <div className="stat-row"><span className="stat-key">Graph</span><span className="stat-val">{graph.metrics.nodeCount} nodes / {graph.metrics.edgeCount} links</span></div>
      </div>
      {graph.dashboard.memory.length > 0 && (
        <div className="agent-life-memory">
          {graph.dashboard.memory.map((memory, index) => <div key={index} className="memory-item">{memory}</div>)}
        </div>
      )}
    </div>
  );
}

function layoutNodes(count: number): Array<{ x: number; y: number }> {
  if (count <= 0) return [];
  const points: Array<{ x: number; y: number }> = [];
  const cx = 110;
  const cy = 64;
  const rx = 82;
  const ry = 43;
  for (let i = 0; i < count; i++) {
    const angle = -Math.PI / 2 + (i / count) * Math.PI * 2;
    points.push({
      x: Number((cx + Math.cos(angle) * rx).toFixed(2)),
      y: Number((cy + Math.sin(angle) * ry).toFixed(2)),
    });
  }
  return points;
}
