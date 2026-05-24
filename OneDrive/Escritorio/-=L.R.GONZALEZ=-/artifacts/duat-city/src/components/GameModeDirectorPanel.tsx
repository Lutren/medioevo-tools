import { useMemo, useState } from "react";
import type { CityState } from "../core/types";
import type { EraId, GameModeId } from "../gameModes/gameModeTypes";
import { createGameModeState } from "../gameModes/gameModeState";
import { listGameModes, switchGameMode } from "../gameModes/gameModeRouter";
import { AgentSimsPanel } from "./AgentSimsPanel";
import { BrainRuntimePanel } from "./BrainRuntimePanel";
import { CityPresidentPanel } from "./CityPresidentPanel";
import { EraProgressionPanel } from "./EraProgressionPanel";
import { HormigueroPanel } from "./HormigueroPanel";
import { LanguageCortexPanel } from "./LanguageCortexPanel";
import { OSITIntegrationPanel } from "./OSITIntegrationPanel";
import { RpgModePanel } from "./RpgModePanel";
import { VsArenaPanel } from "./VsArenaPanel";

export function GameModeDirectorPanel({ state }: { state: CityState }) {
  const [modeState, setModeState] = useState(() => createGameModeState(readInitialGameMode()));
  const modes = useMemo(() => listGameModes(), []);
  function setMode(nextMode: GameModeId) {
    setModeState(prev => switchGameMode(prev, nextMode, state));
  }
  function setEra(era: EraId) {
    setModeState(prev => ({ ...prev, activeEra: era, notes: [...prev.notes, `Era set to ${era}`].slice(-12) }));
  }
  return (
    <div className="section">
      <div className="section-title">Game OS Director</div>
      <select value={modeState.activeMode} onChange={event => setMode(event.target.value as GameModeId)} className="select-input">
        {modes.map(mode => <option key={mode.id} value={mode.id}>{mode.label}</option>)}
      </select>
      <div className="stat-row"><span className="stat-key">Zoom</span><span className="stat-val">{modeState.zoom.toFixed(2)}</span></div>
      <div className="stat-row"><span className="stat-key">Observer</span><span className="stat-val">{String(modeState.observerOnly)}</span></div>
      {modeState.activeMode === "hormiguero" && <HormigueroPanel state={state} />}
      {modeState.activeMode === "agent_sims" && <AgentSimsPanel state={state} selectedAgentId={modeState.selectedAgentId} />}
      {modeState.activeMode === "city_president" && <CityPresidentPanel state={state} />}
      {modeState.activeMode === "era_progression" && <EraProgressionPanel era={modeState.activeEra} secretUnlocked={modeState.eraSecretUnlocked} onEra={setEra} />}
      {modeState.activeMode === "vs_arena" && <VsArenaPanel state={state} />}
      {modeState.activeMode === "rpg" && <RpgModePanel state={state} />}
      {modeState.activeMode === "metroidvania" && <div className="stat-row"><span className="stat-key">Layer</span><span className="stat-val">side-view</span></div>}
      <LanguageCortexPanel state={state} />
      <OSITIntegrationPanel state={state} />
      <BrainRuntimePanel state={state} />
    </div>
  );
}

function readInitialGameMode(): GameModeId {
  if (typeof window === "undefined") return "duat_interface";
  const raw = new URLSearchParams(window.location.search).get("gameMode");
  return raw && listGameModes().some(mode => mode.id === raw) ? raw as GameModeId : "duat_interface";
}
