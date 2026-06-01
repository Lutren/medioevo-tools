import type { PlaneType } from "../core/geoConfig";

export interface CelestialState {
  sunPosition: { x: number; y: number };
  moonPhase: number; // 0.0 - 1.0
  season: "spring" | "summer" | "autumn" | "winter";
}

/**
 * CelestialEngine manages plane-specific celestial motion.
 */
export function updateCelestialState(plane: PlaneType, tick: number): CelestialState {
  if (plane === "astral") {
    // Fixed cardinal seasons
    // North: Winter, West: Autumn, East: Spring, South: Summer
    return { sunPosition: { x: 0, y: 0 }, moonPhase: 0, season: "winter" }; // Placeholder logic
  }

  // Base/Medio: Rotation/Translation
  const angle = tick * 0.01;
  return {
    sunPosition: { x: Math.cos(angle) * 100, y: Math.sin(angle) * 100 },
    moonPhase: (tick / 1000) % 1,
    season: "summer",
  };
}
