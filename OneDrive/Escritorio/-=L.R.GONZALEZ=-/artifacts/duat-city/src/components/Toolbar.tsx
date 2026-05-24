import type { CityState, Mode, TileType } from "../core/types";
import type { ViewMode } from "../graphics/types";
import type { PixelRealismConfig } from "../pixelRealism/renderPasses";
import type { VibeSceneConfig } from "../vibecoding/vibeTypes";
import type { PlayableLightKind, PlayableMaterial, PlayableSceneState, SceneInteractionTool } from "../scene/sceneTypes";
import { TILE_ICONS } from "../render/palette";
import { ModeTabs } from "./ModeTabs";
import { VisualEnginePanel } from "./VisualEnginePanel";
import { VibeCodingPanel } from "./VibeCodingPanel";
import { SceneInteractionPanel } from "./SceneInteractionPanel";
import { AssetLibraryPanel } from "./AssetLibraryPanel";
import { StyleTokenPanel } from "./StyleTokenPanel";
import { VibeGameAuthoringPanel } from "./VibeGameAuthoringPanel";
import { PixelEnginePanel } from "./PixelEnginePanel";
import { GameModeDirectorPanel } from "./GameModeDirectorPanel";
import { AudioGameFeelPanel } from "./AudioGameFeelPanel";
import { IsoRendererPanel } from "./IsoRendererPanel";
import { VermeerLightingPanel } from "./VermeerLightingPanel";

const BUILD_TOOLS: { type: TileType | "select" | "erase"; label: string }[] = [
  { type: "select",      label: "✦ Select" },
  { type: "road",        label: "Road" },
  { type: "residential", label: `${TILE_ICONS.residential} Res` },
  { type: "workshop",    label: `${TILE_ICONS.workshop} Work` },
  { type: "archive",     label: `${TILE_ICONS.archive} Archive` },
  { type: "observatory", label: `${TILE_ICONS.observatory} Obs` },
  { type: "market",      label: `${TILE_ICONS.market} Market` },
  { type: "clinic",      label: `${TILE_ICONS.clinic} Clinic` },
  { type: "academy",     label: `${TILE_ICONS.academy} Acad` },
  { type: "theater",     label: `${TILE_ICONS.theater} Theater` },
  { type: "garden",      label: `${TILE_ICONS.garden} Garden` },
  { type: "plaza",       label: `${TILE_ICONS.plaza} Plaza` },
  { type: "ruin",        label: `${TILE_ICONS.ruin} Ruin` },
  { type: "water",       label: `${TILE_ICONS.water} Water` },
  { type: "forest",      label: `${TILE_ICONS.forest} Forest` },
  { type: "wall",        label: `${TILE_ICONS.wall} Wall` },
  { type: "erase",       label: "✕ Erase" },
];

interface ToolbarProps {
  mode: Mode;
  onMode: (m: Mode) => void;
  tool: TileType | "select" | "erase";
  onTool: (t: TileType | "select" | "erase") => void;
  animate: boolean;
  onAnimate: (v: boolean) => void;
  speed: number;
  onSpeed: (v: number) => void;
  onReset: () => void;
  onSave: () => void;
  onLoad: () => void;
  onResetCamera: () => void;
  onFollowCriticalAgent: () => void;
  onCinematic: () => void;
  physicsEnabled: boolean;
  onPhysicsEnabled: (v: boolean) => void;
  showPhysicsDebug: boolean;
  onShowPhysicsDebug: (v: boolean) => void;
  showChunkDebug: boolean;
  onShowChunkDebug: (v: boolean) => void;
  viewMode: ViewMode;
  onViewMode: (v: ViewMode) => void;
  state: CityState;
  visualConfig: PixelRealismConfig;
  onVisualConfig: (config: PixelRealismConfig) => void;
  activeVibeScene?: VibeSceneConfig;
  onApplyVibeScene: (scene: VibeSceneConfig) => void;
  onUndoVibeScene: () => void;
  canUndoVibeScene: boolean;
  playableScene: PlayableSceneState;
  sceneTool: SceneInteractionTool;
  onSceneTool: (tool: SceneInteractionTool) => void;
  sceneMaterial: PlayableMaterial;
  onSceneMaterial: (material: PlayableMaterial) => void;
  sceneLightKind: PlayableLightKind;
  onSceneLightKind: (kind: PlayableLightKind) => void;
  onToggleScenePause: () => void;
  onStepScene: () => void;
  onSceneTimeOfDay: (time: PlayableSceneState["timeOfDay"]) => void;
  onSceneWeather: (weather: PlayableSceneState["weather"]) => void;
  onApplySceneVibePreset: (preset: string) => void;
  onSaveScene: () => void;
  onLoadScene: (json: string) => void;
  onExportRpgScene: () => void;
  onRunPlayableQa: () => void;
  onApplyVibeGameCommand: (command: string) => void;
  playableQaSummary?: string;
}

export function Toolbar({
  mode, onMode, tool, onTool, animate, onAnimate, speed, onSpeed, onReset, onSave, onLoad,
  onResetCamera, onFollowCriticalAgent, onCinematic,
  physicsEnabled, onPhysicsEnabled, showPhysicsDebug, onShowPhysicsDebug, showChunkDebug, onShowChunkDebug,
  viewMode, onViewMode,
  state, visualConfig, onVisualConfig, activeVibeScene, onApplyVibeScene,
  onUndoVibeScene, canUndoVibeScene,
  playableScene, sceneTool, onSceneTool, sceneMaterial, onSceneMaterial, sceneLightKind, onSceneLightKind,
  onToggleScenePause, onStepScene, onSceneTimeOfDay, onSceneWeather, onApplySceneVibePreset,
  onSaveScene, onLoadScene, onExportRpgScene, onRunPlayableQa, playableQaSummary,
  onApplyVibeGameCommand,
}: ToolbarProps) {
  return (
    <div className="panel-left">
      <ModeTabs mode={mode} onMode={onMode} />

      {mode === "CITY" && (
        <div className="section">
          <div className="section-title">Build Tool</div>
          <div className="tool-grid">
            {BUILD_TOOLS.map(t => (
              <button
                key={t.type}
                className={`tool-btn ${tool === t.type ? "active" : ""}`}
                onClick={() => onTool(t.type as TileType | "select" | "erase")}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>
      )}

      <GameModeDirectorPanel state={state} />

      <div className="section">
        <div className="section-title">Simulation</div>
        <div className="ctrl-row">
          <button className={`ctrl-btn ${animate ? "primary" : ""}`} onClick={() => onAnimate(!animate)}>
            {animate ? "⏸ Pause" : "▶ Play"}
          </button>
        </div>
        <div className="speed-row">
          {[1, 2, 4].map(s => (
            <button key={s} className={`speed-btn ${speed === s ? "active" : ""}`} onClick={() => onSpeed(s)}>
              {s}x
            </button>
          ))}
        </div>
      </div>

      <div className="section">
        <div className="section-title">City</div>
        <div className="ctrl-row">
          <button className="ctrl-btn danger" onClick={onReset}>Reset</button>
        </div>
        <div className="ctrl-row">
          <button className="ctrl-btn" onClick={onSave}>💾 Save</button>
          <button className="ctrl-btn" onClick={onLoad}>📂 Load</button>
        </div>
      </div>

      <div className="section">
        <div className="section-title">View Mode</div>
        <div className="speed-row">
          {(["OPERATIONAL", "BEAUTIFUL", "DEBUG"] as ViewMode[]).map(v => (
            <button key={v} className={`speed-btn ${viewMode === v ? "active" : ""}`} onClick={() => onViewMode(v)}>
              {v === "OPERATIONAL" ? "Ops" : v === "BEAUTIFUL" ? "Beauty" : "Debug"}
            </button>
          ))}
        </div>
        <div className="ctrl-row">
          <button className="ctrl-btn" onClick={onResetCamera}>Reset Camera</button>
        </div>
        <div className="ctrl-row">
          <button className="ctrl-btn" onClick={onFollowCriticalAgent}>Follow Critical</button>
        </div>
        <div className="ctrl-row">
          <button className="ctrl-btn" onClick={onCinematic}>Hide UI</button>
        </div>
      </div>

      <div className="section">
        <div className="section-title">Physics</div>
        <div className="ctrl-row">
          <button className={`ctrl-btn ${physicsEnabled ? "primary" : ""}`} onClick={() => onPhysicsEnabled(!physicsEnabled)}>
            {physicsEnabled ? "Physics On" : "Physics Off"}
          </button>
        </div>
        <div className="ctrl-row">
          <button className={`ctrl-btn ${showPhysicsDebug ? "primary" : ""}`} onClick={() => onShowPhysicsDebug(!showPhysicsDebug)}>Debug</button>
          <button className={`ctrl-btn ${showChunkDebug ? "primary" : ""}`} onClick={() => onShowChunkDebug(!showChunkDebug)}>Chunks</button>
        </div>
      </div>

      <SceneInteractionPanel
        scene={playableScene}
        tool={sceneTool}
        material={sceneMaterial}
        lightKind={sceneLightKind}
        onTool={onSceneTool}
        onMaterial={onSceneMaterial}
        onLightKind={onSceneLightKind}
        onTogglePause={onToggleScenePause}
        onStep={onStepScene}
        onTimeOfDay={onSceneTimeOfDay}
        onWeather={onSceneWeather}
        onApplyVibePreset={onApplySceneVibePreset}
        onSaveScene={onSaveScene}
        onLoadScene={onLoadScene}
        onExportRpgScene={onExportRpgScene}
        onRunPlayableQa={onRunPlayableQa}
        qaSummary={playableQaSummary}
      />
      <IsoRendererPanel state={state} mode={mode} viewMode={viewMode} />
      <VermeerLightingPanel />
      <AudioGameFeelPanel state={state} qualityPreset={visualConfig.qualityPreset} />
      <VibeCodingPanel activeScene={activeVibeScene} onApply={onApplyVibeScene} onUndo={onUndoVibeScene} canUndo={canUndoVibeScene} />
      <VibeGameAuthoringPanel onApplyCommand={onApplyVibeGameCommand} />
      <StyleTokenPanel selectedProfile={visualConfig.paletteProfile} onProfile={profile => onVisualConfig({ ...visualConfig, paletteProfile: profile })} />
      <AssetLibraryPanel />
      <VisualEnginePanel state={state} config={visualConfig} onConfig={onVisualConfig} />
      <PixelEnginePanel state={state} config={visualConfig} />
    </div>
  );
}
