import type { CompiledNarrativeLens, NarrativeLens, NarrativeLensId } from "./artDirectionTypes";

export const PUBLIC_BOUNDARY_NOTE = "Original MEDIOEVO narrative lens. Conceptual influences are transformed into safe internal tokens; no characters, worlds, scenes or protected text are copied.";

export const NARRATIVE_LENSES: Record<NarrativeLensId, NarrativeLens> = {
  systems_logic_lens: lens("systems_logic_lens", "systems_future_protocol", ["causality", "protocol", "city-machine"], ["agents", "protocols", "machine cities"]),
  moral_conflict_lens: lens("moral_conflict_lens", "moral_responsibility_trial", ["guilt", "choice", "responsibility"], ["personal quests", "witness judgement"]),
  stoic_duty_lens: lens("stoic_duty_lens", "disciplined_gate_duty", ["duty", "inner control", "acceptance"], ["gatekeepers", "guardians", "missions"]),
  surveillance_dystopia_lens: lens("surveillance_dystopia_lens", "surveillance_control_language", ["propaganda", "obedience", "language control"], ["authoritarian city", "DUAT panels", "factions"]),
  perception_break_lens: lens("perception_break_lens", "perception_anomaly", ["false memory", "simulacrum", "paranoia"], ["anomalies", "Q states", "ruins", "dream logs"]),
  mythic_archive_lens: lens("mythic_archive_lens", "archive_symbol_memory", ["lineage", "memory", "sacred objects"], ["archives", "relics", "RPG lore", "source cards"]),
  absurd_trial_lens: lens("absurd_trial_lens", "recursive_gate_review", ["bureaucracy", "labyrinth", "blocked judgement"], ["gates", "blocked workflows", "corrupted districts"]),
  will_and_void_lens: lens("will_and_void_lens", "will_under_void_pressure", ["will", "nihilism", "desire", "suffering"], ["high-risk agents", "ruins", "decisions under R"]),
  knowledge_dialogue_lens: lens("knowledge_dialogue_lens", "question_definition_audit", ["questions", "method", "definition"], ["tutorials", "Socratic agents", "claim audit"]),
  power_knowledge_lens: lens("power_knowledge_lens", "power_knowledge_structure", ["classification", "observation", "decision power"], ["factions", "surveillance", "archive politics"]),
};

export function compileNarrativeLens(sceneState: unknown, selectedLens: NarrativeLensId | string): CompiledNarrativeLens {
  const lensProfile = NARRATIVE_LENSES[selectedLens as NarrativeLensId] ?? NARRATIVE_LENSES.mythic_archive_lens;
  const stateTags = extractStateTags(sceneState);
  return {
    id: lensProfile.id,
    internalToken: lensProfile.internalToken,
    moodTags: Array.from(new Set([lensProfile.internalToken, ...lensProfile.themes, ...stateTags])).slice(0, 12),
    questTone: generateQuestTone(lensProfile.id, sceneState),
    publicBoundaryNote: PUBLIC_BOUNDARY_NOTE,
  };
}

export function generateQuestTone(lensId: NarrativeLensId | string, cityState: unknown): string {
  const lensProfile = NARRATIVE_LENSES[lensId as NarrativeLensId] ?? NARRATIVE_LENSES.mythic_archive_lens;
  const R = extractNumber(cityState, "R");
  const urgency = R > 0.45 ? "high residue" : "controlled residue";
  const tones: Record<NarrativeLensId, string> = {
    systems_logic_lens: `Trace a failing protocol through the city-machine under ${urgency}.`,
    moral_conflict_lens: `Force a witness decision where guilt and repair both cost something under ${urgency}.`,
    stoic_duty_lens: `Hold a gate with discipline while collapse pressure rises under ${urgency}.`,
    surveillance_dystopia_lens: `Decode a control signal and decide who is allowed to classify truth under ${urgency}.`,
    perception_break_lens: `Verify which memory is real before an anomaly rewrites the route under ${urgency}.`,
    mythic_archive_lens: `Recover a memory relic and bind it to a living archive under ${urgency}.`,
    absurd_trial_lens: `Escape a recursive gate review without pretending the bureaucracy is rational under ${urgency}.`,
    will_and_void_lens: `Choose an action when desire, loss and void pressure point in different directions under ${urgency}.`,
    knowledge_dialogue_lens: `Ask the question that breaks a false definition under ${urgency}.`,
    power_knowledge_lens: `Expose who benefits from the taxonomy that governs the district under ${urgency}.`,
  };
  return tones[lensProfile.id];
}

export function generateAgentConflict(lensId: NarrativeLensId | string, agents: Array<{ id?: string; name?: string; role?: string; R?: number }> = []): string {
  const lensProfile = NARRATIVE_LENSES[lensId as NarrativeLensId] ?? NARRATIVE_LENSES.mythic_archive_lens;
  const agent = agents[0];
  const subject = agent?.name ?? agent?.role ?? "an unnamed agent";
  return `${subject} is pulled into ${lensProfile.internalToken} without leaving MEDIOEVO-original boundaries.`;
}

export function generateSceneText(lensId: NarrativeLensId | string, location = "district"): string {
  const lensProfile = NARRATIVE_LENSES[lensId as NarrativeLensId] ?? NARRATIVE_LENSES.mythic_archive_lens;
  return `The ${location} reads as ${lensProfile.internalToken}: symbols, gates and material evidence create an original MEDIOEVO scene.`;
}

function lens(id: NarrativeLensId, internalToken: string, themes: string[], uses: string[]): NarrativeLens {
  return { id, internalToken, themes, uses, publicBoundaryNote: PUBLIC_BOUNDARY_NOTE };
}

function extractStateTags(sceneState: unknown): string[] {
  if (!sceneState || typeof sceneState !== "object") return [];
  const maybe = sceneState as { regime?: unknown; gate?: unknown };
  return [maybe.regime, maybe.gate].filter((value): value is string => typeof value === "string").map(value => value.toLowerCase());
}

function extractNumber(value: unknown, key: string): number {
  if (!value || typeof value !== "object") return 0;
  const raw = (value as Record<string, unknown>)[key];
  return typeof raw === "number" && Number.isFinite(raw) ? raw : 0;
}
