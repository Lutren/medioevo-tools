import type { CityState } from "../core/types";
import { createBrainRuntime } from "../brain/brainRuntime";

export function BrainRuntimePanel({ state }: { state: CityState }) {
  const runtime = createBrainRuntime({ city: state });
  return (
    <div className="section">
      <div className="section-title">Brain Runtime</div>
      <div className="stat-row"><span className="stat-key">Exec</span><span className="stat-val">{String(runtime.executionAllowed)}</span></div>
      <div className="stat-row"><span className="stat-key">Prefrontal</span><span className="stat-val">{runtime.systems.prefrontal.gate}</span></div>
      <div className="stat-row"><span className="stat-key">TruthGate</span><span className="stat-val">{runtime.systems.truthGate.gate}</span></div>
      <div className="stat-row"><span className="stat-key">Audio</span><span className="stat-val">{runtime.systems.audioGameFeel.gate} · {runtime.audioGameFeel?.metrics.cueCount ?? 0} cues</span></div>
      <div className="stat-row"><span className="stat-key">OSIT Lab</span><span className="stat-val">{runtime.systems.ositFormulaLab.gate} · {runtime.ositFormulaProfile?.formulaCount ?? 0} ops</span></div>
    </div>
  );
}
