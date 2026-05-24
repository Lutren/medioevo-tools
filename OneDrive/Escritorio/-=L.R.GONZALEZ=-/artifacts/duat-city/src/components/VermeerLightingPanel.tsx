import { createVermeerLightProfile } from "../artDirection/vermeerLightProfile";

export function VermeerLightingPanel() {
  const profile = createVermeerLightProfile();
  return (
    <div className="section" data-qa="vermeer-lighting-panel">
      <div className="section-title">Vermeer Light</div>
      <div className="stat-row"><span className="stat-key">Token</span><span className="stat-val">{profile.publicToken}</span></div>
      <div className="stat-row"><span className="stat-key">Side light</span><span className="stat-val">{profile.sideLight.toFixed(2)}</span></div>
      <div className="stat-row"><span className="stat-key">Window</span><span className="stat-val">{profile.windowSourceClarity.toFixed(2)}</span></div>
      <div className="stat-row"><span className="stat-key">Shadow</span><span className="stat-val">{profile.shadowControl.toFixed(2)}</span></div>
      <div className="stat-row"><span className="stat-key">Bloom</span><span className="stat-val">disciplined {profile.bloomDiscipline.toFixed(2)}</span></div>
      <div className="panel-note">Soft interior window light, controlled shadows, warm/cold balance, no physical-exact claim.</div>
    </div>
  );
}
