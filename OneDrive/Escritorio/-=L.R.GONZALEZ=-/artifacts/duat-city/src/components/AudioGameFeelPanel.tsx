import { useEffect, useMemo, useRef, useState } from "react";
import type { CityState } from "../core/types";
import { createAudioGameFeelSnapshot, createMutedAudioGameFeelConfig } from "../audio/gameFeelAdapter";
import { createWorldAudioAdapter, DEFAULT_AUDIO_GAMEFEEL_CONFIG } from "../audio/worldAudioAdapter";
import { computeGameFeelRenderBudget } from "../pixelRealism/gameFeelPerformance";
import type { RenderQualityPreset } from "../pixelRealism/renderPasses";

interface AudioGameFeelPanelProps {
  state: CityState;
  qualityPreset: RenderQualityPreset;
}

export function AudioGameFeelPanel({ state, qualityPreset }: AudioGameFeelPanelProps) {
  const [enabled, setEnabled] = useState(false);
  const [volume, setVolume] = useState(DEFAULT_AUDIO_GAMEFEEL_CONFIG.masterGain);
  const [lastPreview, setLastPreview] = useState("not run");
  const adapterRef = useRef(createWorldAudioAdapter({ maxCues: 24, masterGain: volume }));
  const config = useMemo(() => createMutedAudioGameFeelConfig({
    enabled,
    masterGain: volume,
    maxCues: 24,
    mode: enabled ? "runtime" : "off",
  }), [enabled, volume]);
  const snapshot = useMemo(() => createAudioGameFeelSnapshot(state, config), [config, state]);
  const budget = useMemo(() => computeGameFeelRenderBudget(qualityPreset, snapshot), [qualityPreset, snapshot]);
  const topCues = snapshot.cues.slice(0, 5);

  useEffect(() => {
    if (typeof window === "undefined") return;
    (window as unknown as { __DUAT_AUDIO_QA__?: object }).__DUAT_AUDIO_QA__ = {
      schema: "duat/audio-gamefeel-headed-qa/v1.4",
      enabled,
      lastPreview,
      cueCount: snapshot.cues.length,
      topCueKinds: topCues.map(cue => cue.kind),
      browserAudioAvailable: adapterRef.current.isAvailable(),
      audioOffByDefault: !enabled,
      noCloud: true,
      noSamples: true,
    };
  }, [enabled, lastPreview, snapshot.cues.length, topCues]);

  const handleEnable = async () => {
    adapterRef.current = createWorldAudioAdapter({ maxCues: 24, masterGain: volume, enabled: false });
    const ok = await adapterRef.current.enable();
    setEnabled(ok);
    setLastPreview(ok ? "browser audio enabled by local gesture" : "AudioContext not available");
  };

  const handlePreview = () => {
    const played = adapterRef.current.preview(state);
    setLastPreview(played > 0 ? `previewed ${played} procedural cues` : "enable audio first");
  };

  return (
    <div className="section" data-qa="audio-gamefeel-panel">
      <div className="section-title">Audio / Game Feel</div>
      <div className="stat-row"><span className="stat-key">State</span><span className="stat-val">{enabled ? "enabled" : "off by default"}</span></div>
      <div className="stat-row"><span className="stat-key">Cue budget</span><span className="stat-val">{snapshot.cues.length}/{budget.maxAudioCues}</span></div>
      <div className="stat-row"><span className="stat-key">R_audio</span><span className="stat-val">{snapshot.metrics.R_audio.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Phi_audio</span><span className="stat-val">{snapshot.metrics.Phi_audio.toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Pulse</span><span className="stat-val">L{snapshot.gameFeel.lightPulse.toFixed(2)} S{snapshot.gameFeel.screenShake.toFixed(2)}</span></div>
      <label className="field-label">Master gain</label>
      <input
        className="range-input"
        type="range"
        min={0}
        max={0.8}
        step={0.01}
        value={volume}
        onChange={event => setVolume(Number(event.currentTarget.value))}
      />
      <div className="ctrl-row compact">
        <button className={`ctrl-btn ${enabled ? "primary" : ""}`} onClick={() => { void handleEnable(); }}>Enable</button>
        <button className="ctrl-btn" onClick={handlePreview}>Preview</button>
      </div>
      <div className="audio-cue-list">
        {topCues.map(cue => (
          <div key={cue.id} className="audio-cue-pill">
            <span>{cue.kind}</span>
            <b>{cue.frequencyHz.toFixed(0)}Hz</b>
          </div>
        ))}
      </div>
      <div className="panel-note">
        {lastPreview}. Local deterministic synthesis only; no samples, no cloud, Wabi execution false.
      </div>
    </div>
  );
}
