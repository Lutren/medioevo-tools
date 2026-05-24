import { listStyleProfiles } from "../style/styleProfiles";
import { DEFAULT_DUAT_STYLE_TOKENS } from "../style/styleTokens";

interface StyleTokenPanelProps {
  selectedProfile?: string;
  onProfile?: (profile: string) => void;
}

export function StyleTokenPanel({ selectedProfile = "archeopunk_city_rain", onProfile }: StyleTokenPanelProps) {
  return (
    <div className="section">
      <div className="section-title">Style Tokens</div>
      <select className="select-input" value={selectedProfile} onChange={event => onProfile?.(event.target.value)}>
        {listStyleProfiles().map(profile => <option key={profile.id} value={profile.id}>{profile.id}</option>)}
      </select>
      <div className="scene-preview">
        <div><b>Palette:</b> {DEFAULT_DUAT_STYLE_TOKENS.paletteTokens.join(", ")}</div>
        <div><b>Glow:</b> {DEFAULT_DUAT_STYLE_TOKENS.glowColorTendencies.join(", ")}</div>
        <div><b>Frame:</b> {DEFAULT_DUAT_STYLE_TOKENS.uiFrameStyle}</div>
      </div>
    </div>
  );
}
