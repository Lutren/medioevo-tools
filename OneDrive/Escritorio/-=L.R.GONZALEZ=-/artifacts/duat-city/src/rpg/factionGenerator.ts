import type { CityState } from "../core/types";
import type { RPGFaction } from "./rpgTypes";
import { uid } from "../core/math";

const BASE_FACTIONS: Omit<RPGFaction, "id" | "controlled_locations" | "reputation">[] = [
  { name: "Archivists", alignment: "order", description: "Keepers of knowledge and evidence. Seek truth through documentation.", resources: ["knowledge", "signal"] },
  { name: "Builders", alignment: "neutral", description: "Pragmatic engineers who shape the city infrastructure.", resources: ["materials", "energy"] },
  { name: "Market Circle", alignment: "neutral", description: "A trade network controlling resource flows and trust.", resources: ["food", "trust"] },
  { name: "Observers", alignment: "order", description: "Watchers who monitor anomalies and report to the DUAT layer.", resources: ["signal", "knowledge"] },
  { name: "Gardeners", alignment: "order", description: "Cultivators of food and culture. City sustainers.", resources: ["food", "culture"] },
  { name: "Ruin Seekers", alignment: "conflict", description: "Explorers drawn to ruins and void anomalies. High R, high reward.", resources: ["signal"] },
];

export function generateFactions(state: CityState): RPGFaction[] {
  return BASE_FACTIONS.map(f => {
    const controlled: string[] = [];
    state.buildings.forEach(b => {
      if (f.name === "Archivists" && (b.type === "archive" || b.type === "academy")) controlled.push(b.id);
      if (f.name === "Builders" && b.type === "workshop") controlled.push(b.id);
      if (f.name === "Market Circle" && b.type === "market") controlled.push(b.id);
      if (f.name === "Observers" && b.type === "observatory") controlled.push(b.id);
      if (f.name === "Gardeners" && b.type === "garden") controlled.push(b.id);
      if (f.name === "Ruin Seekers" && b.type === "ruin") controlled.push(b.id);
    });

    const rep = f.alignment === "conflict" ? 0.3 + state.R * 0.5 : 0.6 + state.Phi_eff * 0.3;

    return {
      id: uid(),
      ...f,
      controlled_locations: controlled,
      reputation: Math.min(1, rep),
    };
  });
}
