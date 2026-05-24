import type { AgentLineage, AgentLineagePerson } from "../core/types";
import { pick, type RandomSource, seededRandom } from "../core/math";

const PROFESSIONS = [
  "Archivist", "Bridge mason", "Field medic", "Signal keeper", "Market runner",
  "Water engineer", "Story printer", "Gate surveyor", "Garden planner", "Forge tuner",
];

const ERAS = [
  "prehistoria", "agricultura", "ciudad_antigua", "medieval", "industrial",
  "cyber_archeopunk", "duat_epoch",
];

const EVENTS = [
  "survived a gate failure",
  "rebuilt a district after flood",
  "guarded a forbidden archive",
  "mapped a broken road network",
  "taught a city during famine",
  "decoded a civic signal",
  "kept a clinic open through saturation",
  "negotiated a market truce",
];

const NAME_ROOTS = ["Ari", "Bel", "Cai", "Dara", "Elo", "Fio", "Iria", "Kao", "Luma", "Nox", "Oro", "Vera"];

export function generateAgentLineage(role: string, rng: RandomSource = seededRandom(`lineage:${role}`)): AgentLineage {
  const grandparents = [
    generateLineagePerson("grandparent", role, rng),
    generateLineagePerson("grandparent", role, rng),
  ] as [AgentLineagePerson, AgentLineagePerson];
  const parents = [
    generateLineagePerson("parent", role, rng),
    generateLineagePerson("parent", role, rng),
  ] as [AgentLineagePerson, AgentLineagePerson];
  return { schema: "duat.agent-lineage.v1", grandparents, parents };
}

export function generateOriginStory(role: string, lineage: AgentLineage): string {
  const parent = lineage.parents[0];
  const grandparent = lineage.grandparents[0];
  return `${role} arrived after ${parent.formativeEvent}, carrying ${grandparent.profession.toLowerCase()} discipline from ${parent.originEra}.`;
}

function generateLineagePerson(generation: "grandparent" | "parent", role: string, rng: RandomSource): AgentLineagePerson {
  const name = `${pick(NAME_ROOTS, rng)}-${Math.floor(rng() * 90 + 10)}`;
  const profession = pick(PROFESSIONS, rng);
  const originEra = pick(ERAS, rng);
  const formativeEvent = pick(EVENTS, rng);
  return {
    name,
    profession: generation === "parent" && role === "Psychologist" ? "Civic psychologist" : profession,
    originEra,
    formativeEvent,
  };
}
