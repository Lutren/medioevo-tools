import type { FrequencyType } from "./gameTypes";

export const FREQUENCIES: Record<string, FrequencyType> = {
  // 26Hz: Ambient stability (from Voynich/Nexus)
  ambientStability: {
    name: "26Hz",
    hz: 26,
    effect: "Stabilizes atmospheric tension; minor Ψ regeneration.",
    costPsi: 0.1,
  },
  // 432Hz: Resonance opening (from Voynich/RPG Agent)
  resonanceOpening: {
    name: "432Hz",
    hz: 432,
    effect: "Opens resonance-locked gates/doors.",
    costPsi: 0.2,
  },
  // 0.12Hz: Stealth/Dampening (from Voynich/Nexus)
  archonDampening: {
    name: "0.12Hz",
    hz: 0.12,
    effect: "Annulla detección de ARCHON por 1 sección.",
    costPsi: 0.3,
  },
  // 963Hz: Destructive/High Intensity (from RPG Agent)
  highIntensityResonance: {
    name: "963Hz",
    hz: 963,
    effect: "Daño masivo a estructuras/entidades.",
    costPsi: 0.5,
  },
};
