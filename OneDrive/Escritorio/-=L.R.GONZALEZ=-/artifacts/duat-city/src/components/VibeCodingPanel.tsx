import { useMemo, useState } from "react";
import type { VibeSceneConfig } from "../vibecoding/vibeTypes";
import { compileVibeScene } from "../vibecoding/vibeSceneCompiler";
import { VIBE_PRESETS } from "../vibecoding/vibePresets";
import { noCloudSafetyNote } from "../vibecoding/vibeSafety";
import type { LightCanonName, NarrativeLensId } from "../artDirection/artDirectionTypes";
import { compileSceneMood } from "../artDirection/sceneMoodCompiler";
import { NARRATIVE_LENSES } from "../artDirection/narrativeLenses";

interface VibeCodingPanelProps {
  activeScene?: VibeSceneConfig;
  onApply: (scene: VibeSceneConfig) => void;
  onUndo?: () => void;
  canUndo?: boolean;
}

export function VibeCodingPanel({ activeScene, onApply, onUndo, canUndo }: VibeCodingPanelProps) {
  const [prompt, setPrompt] = useState("haz una calle lluviosa de noche con luces neon cian y ambar, charcos reflectantes, humo saliendo del mercado, agentes caminando lento");
  const [preset, setPreset] = useState(activeScene?.id ?? "neon_rain_street");
  const [compiled, setCompiled] = useState(() => compileVibeScene("neon_rain_street", "preset"));
  const [lightCanon, setLightCanon] = useState<LightCanonName>("balanced_medioevo");
  const [narrativeLens, setNarrativeLens] = useState<NarrativeLensId>("mythic_archive_lens");
  const [detailDensity, setDetailDensity] = useState(0.66);
  const [symbolicObjectDensity, setSymbolicObjectDensity] = useState(0.62);
  const [shadowStrength, setShadowStrength] = useState(0.58);
  const [materialReflection, setMaterialReflection] = useState(0.62);
  const [atmosphere, setAtmosphere] = useState(0.42);
  const compiledArt = useMemo(() => compileSceneMood(`${prompt} ${lightCanon} ${narrativeLens}`), [lightCanon, narrativeLens, prompt]);
  const sceneWithArt = useMemo(() => ({
    ...compiled.config,
    artDirection: {
      lightCanon,
      lightToken: compiledArt.lightToken,
      narrativeLenses: Array.from(new Set([narrativeLens, ...compiledArt.narrativeLenses])),
      narrativeTokens: Array.from(new Set([narrativeLens, ...compiledArt.narrativeLenses])).map(lens => NARRATIVE_LENSES[lens].internalToken),
      materialDetailProfile: compiledArt.materialDetailProfile,
      moodTags: Array.from(new Set([...compiledArt.moodTags, `detail_${detailDensity.toFixed(2)}`, `symbols_${symbolicObjectDensity.toFixed(2)}`, `shadow_${shadowStrength.toFixed(2)}`, `reflection_${materialReflection.toFixed(2)}`, `atmosphere_${atmosphere.toFixed(2)}`])),
      publicBoundaryNote: compiledArt.publicBoundaryNote,
    },
    visualTags: Array.from(new Set([...compiled.config.visualTags, ...compiledArt.moodTags, "medioevo-original-output"])),
  }), [atmosphere, compiled.config, compiledArt, detailDensity, lightCanon, materialReflection, narrativeLens, shadowStrength, symbolicObjectDensity]);
  const json = useMemo(() => JSON.stringify(sceneWithArt, null, 2), [sceneWithArt]);

  const compilePrompt = () => setCompiled(compileVibeScene(prompt, "prompt"));
  const compilePreset = (id: string) => {
    setPreset(id);
    setCompiled(compileVibeScene(id, "preset"));
  };
  const copyJson = () => {
    if (navigator.clipboard?.writeText) void navigator.clipboard.writeText(json);
  };

  return (
    <div className="section vibe-panel">
      <div className="section-title">VibeCoding Scene</div>
      <select className="select-input" value={preset} onChange={event => compilePreset(event.target.value)}>
        {Object.keys(VIBE_PRESETS).map(id => <option key={id} value={id}>{id}</option>)}
      </select>
      <textarea className="vibe-textarea" value={prompt} onChange={event => setPrompt(event.target.value)} />
      <div className="ctrl-row compact">
        <button className="ctrl-btn" onClick={compilePrompt}>Compile</button>
        <button className="ctrl-btn primary" onClick={() => onApply(sceneWithArt)}>Apply</button>
      </div>
      <div className="ctrl-row compact">
        <button className="ctrl-btn" onClick={copyJson}>Copy JSON</button>
        <button className="ctrl-btn" onClick={onUndo} disabled={!canUndo}>Undo Vibe</button>
      </div>
      <div className="scene-preview">
        <div><b>Preview:</b> {compiled.config.timeOfDay} · {compiled.config.weather} · {compiled.config.lightProfile}</div>
        <div><b>Intent:</b> {compiled.parsedIntent.join(", ")}</div>
      </div>
      <div className="section-title">Art Direction</div>
      <select className="select-input" value={lightCanon} onChange={event => setLightCanon(event.target.value as LightCanonName)}>
        <option value="balanced_medioevo">Balanced MEDIOEVO</option>
        <option value="caravaggio_chiaroscuro">Caravaggio</option>
        <option value="vermeer_interior_light">Vermeer</option>
        <option value="van_eyck_detail_light">van Eyck</option>
      </select>
      <select className="select-input" value={narrativeLens} onChange={event => setNarrativeLens(event.target.value as NarrativeLensId)}>
        {Object.keys(NARRATIVE_LENSES).map(id => <option key={id} value={id}>{id}</option>)}
      </select>
      <label className="mini-label">Detail Density <input type="range" min="0" max="1" step="0.01" value={detailDensity} onChange={event => setDetailDensity(Number(event.target.value))} /></label>
      <label className="mini-label">Symbol Density <input type="range" min="0" max="1" step="0.01" value={symbolicObjectDensity} onChange={event => setSymbolicObjectDensity(Number(event.target.value))} /></label>
      <label className="mini-label">Shadow Strength <input type="range" min="0" max="1" step="0.01" value={shadowStrength} onChange={event => setShadowStrength(Number(event.target.value))} /></label>
      <label className="mini-label">Material Reflection <input type="range" min="0" max="1" step="0.01" value={materialReflection} onChange={event => setMaterialReflection(Number(event.target.value))} /></label>
      <label className="mini-label">Atmosphere / Fog / Rain <input type="range" min="0" max="1" step="0.01" value={atmosphere} onChange={event => setAtmosphere(Number(event.target.value))} /></label>
      <div className="scene-preview">
        <div><b>Parsed art:</b> {sceneWithArt.artDirection.lightToken}</div>
        <div><b>Lens:</b> {sceneWithArt.artDirection.narrativeTokens.join(", ")}</div>
        <div><b>Output:</b> MEDIOEVO-original scene tokens, no copied work.</div>
      </div>
      <div className="panel-note">{noCloudSafetyNote()}</div>
      {[...compiled.warnings, ...compiledArt.warnings].length > 0 && <div className="panel-note warn">{[...compiled.warnings, ...compiledArt.warnings].join(" ")}</div>}
    </div>
  );
}
