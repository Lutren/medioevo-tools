import type { LightCanonName, NarrativeLensId, SceneMoodCompileResult } from "./artDirectionTypes";
import { getLightCanonProfile } from "./lightCanon";
import { PUBLIC_BOUNDARY_NOTE } from "./narrativeLenses";

const DEFAULT_LENS: NarrativeLensId = "mythic_archive_lens";

export function compileSceneMood(prompt: string): SceneMoodCompileResult {
  const text = normalize(prompt);
  const lightCanon = inferLightCanon(text);
  const narrativeLenses = inferNarrativeLenses(text);
  const directCopyWarning = detectsDirectCopyRequest(text)
    ? ["COPY_BOUNDARY: se compilan principios/tokens originales MEDIOEVO; no se copia obra, autor, mundo, escena, personaje ni frase."]
    : [];
  const profile = getLightCanonProfile(lightCanon);
  const moodTags = Array.from(new Set([
    profile.publicToken,
    ...narrativeLenses.map(lensToToken),
    ...inferMoodTags(text),
  ]));
  return {
    lightCanon,
    lightToken: profile.publicToken,
    narrativeLenses,
    narrativeTokens: narrativeLenses.map(lensToToken),
    moodTags,
    materialDetailProfile: lightCanon === "van_eyck_detail_light" ? "micro_material_detail" : "medioevo_material_detail",
    warnings: directCopyWarning,
    parsedIntent: [
      `light:${profile.publicToken}`,
      ...narrativeLenses.map(lens => `lens:${lens}`),
      ...moodTags.map(tag => `tag:${tag}`),
    ],
    publicBoundaryNote: PUBLIC_BOUNDARY_NOTE,
  };
}

export function lensToToken(lens: NarrativeLensId): string {
  const tokens: Record<NarrativeLensId, string> = {
    systems_logic_lens: "systems_future_protocol",
    moral_conflict_lens: "moral_absurd_trial",
    stoic_duty_lens: "disciplined_gate_duty",
    surveillance_dystopia_lens: "surveillance_control_language",
    perception_break_lens: "perception_anomaly",
    mythic_archive_lens: "archive_symbol_memory",
    absurd_trial_lens: "recursive_gate_review",
    will_and_void_lens: "will_under_void_pressure",
    knowledge_dialogue_lens: "question_definition_audit",
    power_knowledge_lens: "power_knowledge_structure",
  };
  return tokens[lens];
}

function inferLightCanon(text: string): LightCanonName {
  if (has(text, ["caravaggio", "claroscuro", "chiaroscuro", "dramatic light", "revelacion"])) return "caravaggio_chiaroscuro";
  if (has(text, ["vermeer", "ventana", "interior suave", "luz interior"])) return "vermeer_interior_light";
  if (has(text, ["van eyck", "van_eyck", "microdetalle", "micro detalle", "detalle material"])) return "van_eyck_detail_light";
  return "balanced_medioevo";
}

function inferNarrativeLenses(text: string): NarrativeLensId[] {
  const lenses = new Set<NarrativeLensId>();
  if (has(text, ["vigilancia", "orwell", "huxley", "propaganda", "control de lenguaje"])) lenses.add("surveillance_dystopia_lens");
  if (has(text, ["archivo mitico", "archivo mítico", "borges", "jung", "memoria", "mitico", "mythic", "tolkien"])) lenses.add("mythic_archive_lens");
  if (has(text, ["absurdo", "kafka", "kafkiano", "juicio", "burocracia"])) lenses.add("absurd_trial_lens");
  if (has(text, ["culpa", "dostoyevski", "kierkegaard", "camus", "moral"])) lenses.add("moral_conflict_lens");
  if (has(text, ["deber estoico", "estoico", "guardian", "hold the gate"])) lenses.add("stoic_duty_lens");
  if (has(text, ["percepcion rota", "percepción rota", "pkd", "serling", "simulacro", "paranoia"])) lenses.add("perception_break_lens");
  if (has(text, ["asimov", "wells", "sistemas", "robotica", "protocolo"])) lenses.add("systems_logic_lens");
  if (has(text, ["foucault", "poder", "clasifica", "quien observa", "quien decide"])) lenses.add("power_knowledge_lens");
  if (has(text, ["dialogo", "socratic", "socratico", "metodo", "definicion"])) lenses.add("knowledge_dialogue_lens");
  if (has(text, ["voluntad", "nihilismo", "vacio", "sufrimiento"])) lenses.add("will_and_void_lens");
  if (lenses.size === 0) lenses.add(DEFAULT_LENS);
  return Array.from(lenses);
}

function inferMoodTags(text: string): string[] {
  const tags: string[] = [];
  if (has(text, ["mercado cyberpunk", "cyberpunk", "neon"])) tags.push("underground_market_neon");
  if (has(text, ["ruina sagrada", "sagrada", "ritual"])) tags.push("sacred_ruin");
  if (has(text, ["niebla", "fog", "humo"])) tags.push("atmosphere_scatter");
  if (has(text, ["agua", "reflejo", "wet", "lluvia"])) tags.push("wet_reflection");
  return tags;
}

function detectsDirectCopyRequest(text: string): boolean {
  return has(text, ["copia", "copiar", "imitacion exacta", "imitación exacta", "igual que", "personaje de", "frase de", "escena de", "mundo de"]);
}

function normalize(value: string): string {
  return value
    .toLowerCase()
    .replace(/[áà]/g, "a")
    .replace(/[éè]/g, "e")
    .replace(/[íì]/g, "i")
    .replace(/[óò]/g, "o")
    .replace(/[úùü]/g, "u");
}

function has(text: string, words: string[]): boolean {
  return words.some(word => text.includes(normalize(word)));
}
