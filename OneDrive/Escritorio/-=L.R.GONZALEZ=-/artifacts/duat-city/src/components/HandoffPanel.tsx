import { useState } from "react";
import type { CityState } from "../core/types";
import { generateHandoff } from "../core/handoff";
import { downloadJson } from "../core/persistence";
import { GATE_COLORS, rColor } from "../render/palette";

interface HandoffPanelProps { state: CityState; }

export function HandoffPanel({ state }: HandoffPanelProps) {
  const [copied, setCopied] = useState(false);
  const handoff = generateHandoff(state);
  const json = JSON.stringify(handoff, null, 2);

  function copy() {
    navigator.clipboard.writeText(json).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  function download() {
    downloadJson(`duat-handoff-tick${state.tick}.json`, json);
  }

  return (
    <div className="section">
      <div className="section-title">Handoff JSON</div>
      <div style={{ display: "flex", gap: 4, marginBottom: 6 }}>
        <button className="copy-btn" onClick={copy}>{copied ? "✓ Copied!" : "Copy JSON"}</button>
        <button className="copy-btn" onClick={download}>Download</button>
      </div>
      <div className="stat-row">
        <span className="stat-key">Gate</span>
        <span className="stat-val" style={{ color: GATE_COLORS[handoff.gate] }}>{handoff.gate}</span>
      </div>
      <div className="stat-row">
        <span className="stat-key">R</span>
        <span className="stat-val" style={{ color: rColor(handoff.R) }}>{handoff.R.toFixed(3)}</span>
      </div>
      {handoff.risks.length > 0 && (
        <div style={{ marginTop: 4 }}>
          <div className="section-title">Risks</div>
          {handoff.risks.map((r, i) => (
            <div key={i} style={{ color: "#ff6b35", fontSize: 10, padding: "1px 0" }}>⚠ {r}</div>
          ))}
        </div>
      )}
      <div className="json-box" style={{ marginTop: 6 }}>{json}</div>
    </div>
  );
}
