import type { CityState, Agent } from "../core/types";
import { AGENT_ROLE_COLORS, GATE_COLORS, rColor } from "../render/palette";
import { ResourcePanel } from "./ResourcePanel";
import { qStateColor } from "../quaternary/qstate";
import { AgentLifeDashboardPanel } from "./AgentLifeDashboardPanel";

interface AgentInspectorProps {
  state: CityState;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}

const NEED_BARS: { key: keyof Agent["needs"]; cls: string; label: string }[] = [
  { key: "energy", cls: "bar-energy", label: "Energy" },
  { key: "hunger", cls: "bar-hunger", label: "Hunger" },
  { key: "social", cls: "bar-social", label: "Social" },
  { key: "purpose", cls: "bar-purpose", label: "Purpose" },
  { key: "safety", cls: "bar-safety", label: "Safety" },
  { key: "curiosity", cls: "bar-curiosity", label: "Curious" },
];

function AgentCard({ agent, state }: { agent: Agent; state: CityState }) {
  const color = AGENT_ROLE_COLORS[agent.role] ?? "#ffffff";
  const gateColor = GATE_COLORS[agent.gate];
  const activeTask = agent.currentTaskId ? "Working..." : "Idle";
  const qEval = state.quaternary?.recent.find(evaluation => evaluation.sourceId === `agent:${agent.id}`);

  return (
    <div style={{ padding: "6px 0" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4 }}>
        <div style={{ width: 10, height: 10, borderRadius: "50%", background: color, flexShrink: 0 }} />
        <strong style={{ color }}>{agent.name}</strong>
        <span style={{ color: "#6e7681", fontSize: 10 }}>[{agent.role}]</span>
        <span className={`agent-gate-tag gate-${agent.gate}`} style={{ marginLeft: "auto" }}>{agent.gate}</span>
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 4 }}>
        <div className="stat-row" style={{ flex: 1 }}>
          <span className="stat-key">R</span>
          <span className="stat-val" style={{ color: rColor(agent.R) }}>{agent.R.toFixed(3)}</span>
        </div>
        <div className="stat-row" style={{ flex: 1 }}>
          <span className="stat-key">Φ_eff</span>
          <span className="stat-val" style={{ color: rColor(1 - agent.Phi_eff) }}>{agent.Phi_eff.toFixed(3)}</span>
        </div>
      </div>
      <div className="stat-row">
        <span className="stat-key">Mood</span>
        <span className="stat-val">{(agent.mood * 100).toFixed(0)}%</span>
        <span className="stat-key" style={{ marginLeft: 8 }}>Trust</span>
        <span className="stat-val">{(agent.trust * 100).toFixed(0)}%</span>
      </div>
      <div className="stat-row">
        <span className="stat-key">Status</span>
        <span className="stat-val" style={{ color: "#7bc8f6" }}>{activeTask}</span>
      </div>
      {qEval && (
        <div className="stat-row">
          <span className="stat-key">Q state</span>
          <span className="stat-val" style={{ color: qStateColor(qEval.state) }}>{qEval.state} · dwell {qEval.timing.dwellTicks} · f {qEval.timing.frequency.toFixed(2)} · s {qEval.timing.stability.toFixed(2)}</span>
        </div>
      )}

      <div style={{ marginTop: 4 }}>
        {NEED_BARS.map(({ key, cls, label }) => (
          <div key={key} className="need-row">
            <span className="need-label">{label}</span>
            <div className="need-bar-wrap">
              <div className="progress-bar">
                <div className={`progress-fill ${cls}`} style={{ width: `${agent.needs[key] * 100}%` }} />
              </div>
            </div>
            <span className="stat-val" style={{ minWidth: 28, textAlign: "right", fontSize: 10 }}>
              {(agent.needs[key] * 100).toFixed(0)}
            </span>
          </div>
        ))}
      </div>

      {agent.memory.length > 0 && (
        <div style={{ marginTop: 4 }}>
          <div className="section-title">Memory</div>
          {agent.memory.slice(-3).map((m, i) => (
            <div key={i} className="memory-item">{m}</div>
          ))}
        </div>
      )}
    </div>
  );
}

export function AgentInspector({ state, selectedId, onSelect }: AgentInspectorProps) {
  const selected = state.agents.find(a => a.id === selectedId);

  return (
    <div className="panel-right">
      <AgentLifeDashboardPanel state={state} selectedId={selectedId} onSelect={onSelect} />
      {selected ? (
        <div className="section">
          <div className="section-title">
            Agent Inspector
            <button style={{ float: "right", background: "none", border: "none", color: "#6e7681", cursor: "pointer" }} onClick={() => onSelect(null)}>✕</button>
          </div>
          <AgentCard agent={selected} state={state} />
        </div>
      ) : (
        <div className="section">
          <div className="section-title">Agents ({state.agents.length})</div>
          {state.agents.map(agent => {
            const color = AGENT_ROLE_COLORS[agent.role] ?? "#fff";
            return (
              <div
                key={agent.id}
                className={`agent-item ${selectedId === agent.id ? "selected" : ""}`}
                onClick={() => onSelect(agent.id)}
              >
                <div className="agent-dot" style={{ background: color }} />
                <span className="agent-name" style={{ color }}>{agent.name}</span>
                <span className="stat-val" style={{ color: rColor(agent.R), fontSize: 10 }}>R{agent.R.toFixed(2)}</span>
                <span className={`agent-gate-tag gate-${agent.gate}`}>{agent.gate.slice(0, 3)}</span>
              </div>
            );
          })}
        </div>
      )}
      <ResourcePanel state={state} />
    </div>
  );
}
