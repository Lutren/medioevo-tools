import type { CityState } from "../core/types";
import { compileOSITFormulaProfile } from "../osit/ositIntegration";

export function OSITIntegrationPanel({ state }: { state: CityState }) {
  const profile = compileOSITFormulaProfile(state);
  const top = profile.formulas.slice(0, 4);
  return (
    <div className="section" data-qa="osit-integration-panel">
      <div className="section-title">OSIT Formula Lab</div>
      <div className="stat-row"><span className="stat-key">Gate</span><span className="stat-val">{profile.gate}</span></div>
      <div className="stat-row"><span className="stat-key">R_formula</span><span className="stat-val">{profile.R_formula.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Phi_formula</span><span className="stat-val">{profile.Phi_formula.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Operators</span><span className="stat-val">{profile.formulaCount}</span></div>
      <div className="audio-cue-list">
        {top.map(formula => (
          <div key={formula.id} className="audio-cue-pill" title={formula.notes}>
            <span>{formula.historicalReference}</span>
            <b>{formula.boundary.replaceAll("_", " ")}</b>
          </div>
        ))}
      </div>
      <div className="panel-note">Formal-lab mappings only. ScienceClaimGate blocks exact/public physics claims.</div>
    </div>
  );
}
