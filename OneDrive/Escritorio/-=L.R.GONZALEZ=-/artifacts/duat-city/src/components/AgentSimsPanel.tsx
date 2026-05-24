import type { CityState } from "../core/types";
import { selectAgentSimsView } from "../gameModes/agentSimsMode";

export function AgentSimsPanel({ state, selectedAgentId }: { state: CityState; selectedAgentId?: string }) {
  const view = selectAgentSimsView(state, selectedAgentId);
  return (
    <div className="section">
      <div className="section-title">Agent Sims</div>
      <div className="stat-row"><span className="stat-key">Agent</span><span className="stat-val">{view.agent?.name ?? "none"}</span></div>
      <div className="stat-row"><span className="stat-key">Gate</span><span className="stat-val">{view.agent?.gate ?? "REVIEW"}</span></div>
      <p className="mini-copy">{view.decisionSuggestion}</p>
    </div>
  );
}
