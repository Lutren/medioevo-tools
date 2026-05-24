import type { CityEvent } from "../core/types";
import type { SourceCard } from "./languageTypes";

export function compileSourceCardFromEvent(event: CityEvent): SourceCard {
  return {
    schema: "duat/source-card/v1.3",
    id: `source:${event.id}`,
    title: event.title,
    eventType: event.type,
    evidence: [event.detail],
    R: finite(Math.max(0, event.R_delta)),
    Phi_eff: finite(1 - Math.max(0, event.R_delta)),
    gate: event.gate,
  };
}

function finite(value: number): number {
  return Number.isFinite(value) ? Number(value.toFixed(3)) : 0;
}
