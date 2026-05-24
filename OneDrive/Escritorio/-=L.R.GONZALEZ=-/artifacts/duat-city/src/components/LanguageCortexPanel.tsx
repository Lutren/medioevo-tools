import type { CityState } from "../core/types";
import { computeLanguageMetrics } from "../language/languageMetrics";
import { generateNpcUtterance } from "../language/npcSpeechEngine";

export function LanguageCortexPanel({ state }: { state: CityState }) {
  const utterances = state.agents.slice(0, 3).map(agent => generateNpcUtterance(agent, state, "panel"));
  const metrics = computeLanguageMetrics(utterances);
  return (
    <div className="section">
      <div className="section-title">Language Cortex</div>
      <div className="stat-row"><span className="stat-key">R_lang</span><span className="stat-val">{metrics.R_language.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Phi_lang</span><span className="stat-val">{metrics.Phi_language.toFixed(3)}</span></div>
      <p className="mini-copy">{utterances[0]?.classification}: {utterances[0]?.text ?? "No NPC speech"}</p>
    </div>
  );
}
