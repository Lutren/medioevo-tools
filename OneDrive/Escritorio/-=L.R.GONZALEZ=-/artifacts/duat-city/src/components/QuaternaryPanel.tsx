import type { CityState } from "../core/types";
import type { QState } from "../quaternary/types";
import { qStateColor, qStateLabel } from "../quaternary/qstate";
import { downloadJson } from "../core/persistence";
import { GATE_COLORS, rColor } from "../render/palette";

interface QuaternaryPanelProps {
  state: CityState;
}

const STATES: QState[] = ["00", "01", "10", "11"];

export function QuaternaryPanel({ state }: QuaternaryPanelProps) {
  const q = state.quaternary;
  if (!q) {
    return (
      <div className="section">
        <div className="section-title">Quaternary Timing</div>
        <span className="stat-key">Waiting for first simulation tick</span>
      </div>
    );
  }

  const handoff = {
    schema: "duat/quaternary-timing/v0.9",
    R_quaternary: q.R,
    Phi_quaternary: q.Phi_eff,
    gate: q.gate,
    counts: q.counts,
    top_anomalies: q.topAnomalies,
    top_unstable: q.topUnstable,
    next_action: q.next_action,
  };

  const copyJson = () => {
    const json = JSON.stringify(handoff, null, 2);
    if (navigator.clipboard?.writeText) {
      void navigator.clipboard.writeText(json).catch(() => {
        downloadJson(`duat-quaternary-handoff-t${state.tick}.json`, json);
      });
    } else {
      downloadJson(`duat-quaternary-handoff-t${state.tick}.json`, json);
    }
  };

  return (
    <div className="section">
      <div className="section-title">Quaternary Timing v0.9</div>
      <div className="stat-row">
        <span className="stat-key">Gate</span>
        <span className="stat-val" style={{ color: GATE_COLORS[q.gate] }}>{q.gate}</span>
      </div>
      <div className="need-row" style={{ marginTop: 4 }}>
        <span className="need-label">R_Q</span>
        <div className="need-bar-wrap"><div className="progress-bar"><div className="progress-fill bar-r" style={{ width: `${q.R * 100}%` }} /></div></div>
        <span className="stat-val" style={{ color: rColor(q.R), minWidth: 36 }}>{q.R.toFixed(3)}</span>
      </div>
      <div className="need-row">
        <span className="need-label">Phi_Q</span>
        <div className="need-bar-wrap"><div className="progress-bar"><div className="progress-fill bar-phi" style={{ width: `${q.Phi_eff * 100}%` }} /></div></div>
        <span className="stat-val" style={{ color: rColor(1 - q.Phi_eff), minWidth: 36 }}>{q.Phi_eff.toFixed(3)}</span>
      </div>
      <div className="q-count-grid">
        {STATES.map(stateKey => (
          <div key={stateKey} className="q-count-cell" style={{ borderColor: qStateColor(stateKey) }}>
            <span className="q-bit" style={{ color: qStateColor(stateKey) }}>{stateKey}</span>
            <span className="q-label">{qStateLabel(stateKey)}</span>
            <span className="q-total">{q.counts[stateKey]}</span>
          </div>
        ))}
      </div>
      <div className="stat-row"><span className="stat-key">Avg frequency</span><span className="stat-val">{q.avgFrequency.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Avg permanence</span><span className="stat-val">{q.avgPermanence.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Avg stability</span><span className="stat-val">{q.avgStability.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Combined R</span><span className="stat-val" style={{ color: rColor(q.combinedR) }}>{q.combinedR.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Combined Phi</span><span className="stat-val">{q.combinedPhi.toFixed(3)}</span></div>
      {q.topAnomalies.length > 0 && (
        <div className="q-mini-list">
          <span className="stat-key">Top anomalies</span>
          {q.topAnomalies.slice(0, 3).map(item => <span key={item} className="q-mini-item">{item}</span>)}
        </div>
      )}
      {q.topUnstable.length > 0 && (
        <div className="q-mini-list">
          <span className="stat-key">Top unstable</span>
          {q.topUnstable.slice(0, 3).map(item => <span key={item} className="q-mini-item">{item}</span>)}
        </div>
      )}
      <div style={{ color: "#8cb7c9", fontSize: 11, lineHeight: 1.35, marginTop: 8 }}>
        00 silence/cache · 01 missing signal/review · 10 stable presence/LOD · 11 active event/full detail
      </div>
      <button className="ctrl-btn" style={{ marginTop: 8 }} onClick={copyJson}>Copy Q Handoff JSON</button>
    </div>
  );
}

