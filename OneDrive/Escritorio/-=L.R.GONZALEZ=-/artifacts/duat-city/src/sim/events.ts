import type { CityState, CityEvent, Gate } from "../core/types";
import { computeGate } from "../core/metrics";
import { uid, pick, seededRandom, type RandomSource } from "../core/math";

export function makeEvent(
  tick: number,
  type: CityEvent["type"],
  title: string,
  detail: string,
  R_delta: number,
  gate: Gate,
  rng?: RandomSource
): CityEvent {
  return { id: uid(rng), tick, type, title, detail, R_delta, gate };
}

export function generateTickEvents(state: CityState, rng?: RandomSource): CityEvent[] {
  const events: CityEvent[] = [];
  const { tick, resources, buildings, agents, R } = state;
  const gate = computeGate(R);
  const random = rng ?? seededRandom(`events:${tick}:${resources.food}:${resources.trust}:${buildings.length}:${agents.length}:${R.toFixed(6)}`);

  // Resource events
  if (resources.food < 15) {
    events.push(makeEvent(tick, "resource", "Food Shortage", "Food reserves critically low", 0.05, "BLOCK", random));
  }
  if (resources.trust < 10) {
    events.push(makeEvent(tick, "resource", "Trust Crisis", "Community trust collapsing", 0.08, "BLOCK", random));
  }
  if (resources.knowledge > 120) {
    events.push(makeEvent(tick, "rpg", "Knowledge Surge", "Archive overflow - quest hook generated", -0.03, "APPROVE", random));
  }
  if (resources.signal > 70) {
    events.push(makeEvent(tick, "rpg", "Signal Anomaly", "Observatory detected anomaly - follow the signal", -0.02, "APPROVE", random));
  }

  // Ruin events
  const ruins = buildings.filter(b => b.type === "ruin");
  if (ruins.length > 0 && random() < 0.05) {
    events.push(makeEvent(tick, "risk", "Ruin Anomaly", `${ruins[0].name} emanates strange signals`, 0.04, "REVIEW", random));
  }

  // Agent events
  const blocked = agents.filter(a => a.gate === "BLOCK");
  if (blocked.length >= 3 && random() < 0.08) {
    events.push(makeEvent(tick, "risk", "Agent Crisis", `${blocked.length} agents blocked - city stress rising`, 0.06, "BLOCK", random));
  }

  // Random positive events
  if (R < 0.2 && random() < 0.04) {
    const positives = [
      "City thriving — Phi_eff peak",
      "Cultural festival emerges",
      "Trade routes optimized",
      "Archive milestone reached",
    ];
    events.push(makeEvent(tick, "system", "Prosperity", pick(positives, random), -0.02, gate, random));
  }

  // RPG events
  if (tick % 50 === 0 && buildings.length > 3) {
    events.push(makeEvent(tick, "rpg", "RPG Hook", "A new quest opportunity emerged", 0, gate, random));
  }

  return events;
}
