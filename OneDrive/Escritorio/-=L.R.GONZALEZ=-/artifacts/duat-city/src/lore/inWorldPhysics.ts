export function blockPublicCosmologyClaim(statement: string) {
  const risky = /real physics|science proves|actual universe|physical law/i.test(statement);
  return {
    statement,
    publicAllowed: false as const,
    gate: risky ? "BLOCK" as const : "REVIEW" as const,
    boundary: "IN_WORLD_COSMOLOGY",
    note: "Use as fictional/in-world mechanic only.",
  };
}

export function fireEventLoreMechanic() {
  return {
    id: "fire_event",
    visual: "bloom/heat/smoke",
    audio: "crackle plus energy release",
    osit: "R_light up, Phi_light recovers when stabilized",
    lore: "visible materia-energy conversion in MEDIOEVO fiction",
    boundary: "fictional/in-world mechanic",
  };
}
