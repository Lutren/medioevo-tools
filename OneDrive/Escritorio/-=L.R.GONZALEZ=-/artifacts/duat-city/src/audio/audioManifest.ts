import type { AudioCueKind, AudioManifest } from "./audioTypes";

export const AUDIO_CUE_KINDS: AudioCueKind[] = [
  "material_water",
  "material_fire",
  "material_smoke",
  "material_stone",
  "material_wood",
  "material_neon",
  "light_torch",
  "light_window",
  "light_neon",
  "light_fire",
  "light_magic",
  "light_signal",
  "light_ruin_anomaly",
  "agent_need",
  "agent_task",
  "gate_approve",
  "gate_review",
  "gate_block",
  "language_certeza",
  "language_inferencia",
  "language_incognita",
  "language_bloqueo",
  "cosmology_fire_event",
  "rpg_transition",
  "ui_confirm",
  "ui_warning",
];

export function createAudioGameFeelManifest(generatedAt = new Date().toISOString()): AudioManifest {
  return {
    schema: "duat/audio-gamefeel-manifest/v1.3.1",
    fingerprint: "DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY",
    generatedAt,
    boundary: {
      ownerProvidedInternalProtectedIp: true,
      proceduralOnly: true,
      externalSamplesCopied: false,
      publicationAllowed: false,
      noCloud: true,
      requiresUserGesture: true,
      wabiExecutionAllowed: false,
    },
    cueKinds: AUDIO_CUE_KINDS,
    synthesisPolicy: "Local deterministic WebAudio tone plans only; browser synthesis is off until local user gesture.",
    manifests: [
      "/asset-manifest/audio_zip_manifest_v1_3.json",
      "/asset-manifest/audio_gamefeel_manifest_v1_3_1.json",
      "/asset-manifest/agents_gamefeel_manifest_v1_3_1.json",
    ],
  };
}
