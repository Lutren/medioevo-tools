import { useState } from "react";
import type { CityState } from "../core/types";
import type { RPGWorld } from "../rpg/rpgTypes";
import { exportRPGWorld } from "../rpg/worldExport";
import { generateQuests } from "../rpg/questGenerator";
import { generateFactions } from "../rpg/factionGenerator";
import { generateEncounters } from "../rpg/encounterGenerator";
import { downloadJson } from "../core/persistence";

interface RPGBuilderPanelProps { state: CityState; }

export function RPGBuilderPanel({ state }: RPGBuilderPanelProps) {
  const [world, setWorld] = useState<RPGWorld | null>(null);
  const [tab, setTab] = useState<"quests" | "factions" | "encounters">("quests");

  const quests = generateQuests(state);
  const factions = generateFactions(state);
  const encounters = generateEncounters(state);

  function generate() {
    setWorld(exportRPGWorld(state));
  }

  function download() {
    if (!world) return;
    downloadJson(`duat-rpg-world-tick${state.tick}.json`, JSON.stringify(world, null, 2));
  }

  return (
    <div className="panel-right">
      <div className="section">
        <div className="section-title">⚔️ RPG World Builder</div>
        <div className="ctrl-row">
          <button className="ctrl-btn primary" onClick={generate}>Generate World</button>
          <button className="ctrl-btn" onClick={download} disabled={!world}>Download JSON</button>
        </div>
        {world && (
          <div style={{ marginTop: 4 }}>
            <div className="stat-row"><span className="stat-key">Locations</span><span className="stat-val">{world.locations.length}</span></div>
            <div className="stat-row"><span className="stat-key">NPCs</span><span className="stat-val">{world.npcs.length}</span></div>
            <div className="stat-row"><span className="stat-key">Factions</span><span className="stat-val">{world.factions.length}</span></div>
            <div className="stat-row"><span className="stat-key">Risk Zones</span><span className="stat-val" style={{ color: "#ff4444" }}>{world.risk_zones.length}</span></div>
          </div>
        )}
      </div>

      <div className="section">
        <div style={{ display: "flex", gap: 4, marginBottom: 6 }}>
          {(["quests", "factions", "encounters"] as const).map(t => (
            <button key={t} className={`ctrl-btn ${tab === t ? "primary" : ""}`} onClick={() => setTab(t)} style={{ padding: "2px 6px" }}>{t}</button>
          ))}
        </div>

        {tab === "quests" && (
          <>
            {quests.length === 0 && <span className="stat-key">No quests available yet</span>}
            {quests.map(q => (
              <div key={q.id} className="quest-item">
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span className="quest-title">{q.title}</span>
                  <span className={`quest-diff diff-${q.difficulty}`}>{q.difficulty}</span>
                </div>
                <div className="quest-hook">{q.hook}</div>
                <div className="quest-reward">⭐ {q.reward}</div>
              </div>
            ))}
          </>
        )}

        {tab === "factions" && (
          <>
            {factions.map(f => (
              <div key={f.id} className="quest-item">
                <div className="quest-title">{f.name} <span style={{ color: "#6e7681", fontSize: 10 }}>[{f.alignment}]</span></div>
                <div className="quest-hook">{f.description}</div>
                <div className="quest-reward">Rep: {(f.reputation * 100).toFixed(0)}% | Locations: {f.controlled_locations.length}</div>
              </div>
            ))}
          </>
        )}

        {tab === "encounters" && (
          <>
            {encounters.map(e => (
              <div key={e.id} className="quest-item">
                <div className="quest-title">{e.title}</div>
                <div className="quest-hook">{e.description}</div>
                <div style={{ color: "#00ff9d", fontSize: 10 }}>✓ {e.outcome_approve}</div>
                <div style={{ color: "#ff4444", fontSize: 10 }}>✗ {e.outcome_block}</div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}
