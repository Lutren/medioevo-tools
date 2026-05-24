import type { CityState } from "../core/types";
import type { RPGPhysicsProfile, RPGQuest } from "./rpgTypes";
import { uid } from "../core/math";

export function generateQuests(state: CityState, physicsProfile?: RPGPhysicsProfile): RPGQuest[] {
  const quests: RPGQuest[] = [];
  const { resources, buildings, R, Phi_eff } = state;

  const ruins = buildings.filter(b => b.type === "ruin");
  if (ruins.length > 0 && R > 0.3) {
    quests.push({
      id: uid(), type: "investigation",
      title: "Investigate the Ruin",
      hook: `A void anomaly detected at ${ruins[0].name}. R=${R.toFixed(2)}. Archivists request investigation.`,
      location_id: ruins[0].id,
      reward: "Reduce R by 0.08, gain knowledge +15",
      R_required: 0.3,
      difficulty: R > 0.6 ? "hard" : "medium",
    });
  }

  if ((physicsProfile?.collision_heavy_areas.length ?? 0) > 0) {
    quests.push({
      id: uid(), type: "resource",
      title: "Clear the Blocked Route",
      hook: `Agent flow is congested near ${physicsProfile!.collision_heavy_areas[0]}. Couriers request a safe route.`,
      reward: "materials +10, R -0.04, route stability improved",
      R_required: 0.2,
      difficulty: "medium",
    });
  }

  if (state.fieldSummary?.hazards.includes("fire")) {
    quests.push({
      id: uid(), type: "resource",
      title: "Contain the Fire Outbreak",
      hook: "The pixel field reports active fire cells. Medics and builders need a containment route.",
      reward: "R -0.05, safety +12, damaged objects repaired",
      R_required: 0.25,
      difficulty: "hard",
    });
  }

  if (state.fieldSummary?.hazards.includes("flooding") || state.tiles.some(t => t.type === "water")) {
    quests.push({
      id: uid(), type: "resource",
      title: "Drain the Flooded District",
      hook: "Water cells are blocking low-friction routes. Engineers need to restore road flow.",
      reward: "materials +8, route friction reduced, R -0.03",
      R_required: 0.2,
      difficulty: "medium",
    });
  }

  const voidRuin = state.tiles.find(t => t.type === "ruin" && t.fibmob.polarity === "void");
  if (voidRuin) {
    quests.push({
      id: uid(), type: "anomaly",
      title: "Stabilize the Ruin Anomaly",
      hook: `A FibMob void appeared at ruin tile ${voidRuin.id}. Archivists need containment evidence.`,
      reward: "signal +12, knowledge +8, anomaly overlay reduced",
      R_required: 0.25,
      difficulty: "hard",
    });
  }

  if (resources.food < 30) {
    quests.push({
      id: uid(), type: "resource",
      title: "Restore the Gardens",
      hook: "Food reserves critically low. The Gardeners need help reviving cultivation zones.",
      reward: "food +40, culture +10",
      R_required: 0.1,
      difficulty: "easy",
    });
  }

  if (resources.knowledge > 120) {
    quests.push({
      id: uid(), type: "exploration",
      title: "Open the Grand Archive",
      hook: "Knowledge overflow — a new archive wing can be opened. Archivists request builders.",
      reward: "knowledge +20, trust +15, new archive building",
      R_required: 0.0,
      difficulty: "medium",
    });
  }

  if (resources.trust < 15) {
    quests.push({
      id: uid(), type: "social",
      title: "Mediate the Conflict",
      hook: "Trust has collapsed. Market Circle and Ruin Seekers are in dispute. A mediator is needed.",
      reward: "trust +25, relationships improved",
      R_required: 0.2,
      difficulty: "hard",
    });
  }

  if (resources.signal > 70) {
    quests.push({
      id: uid(), type: "anomaly",
      title: "Follow the Signal Anomaly",
      hook: "The Observatory detected an unusual signal pattern. Follow it before it disperses.",
      reward: "signal +10, rare lore discovery",
      R_required: 0.15,
      difficulty: "medium",
    });
  }

  if (Phi_eff > 0.8 && quests.length < 2) {
    quests.push({
      id: uid(), type: "exploration",
      title: "Expand the City",
      hook: "Phi_eff is high. The city can grow. Scout new districts and establish outposts.",
      reward: "new district zone, materials +20",
      R_required: 0.0,
      difficulty: "easy",
    });
  }

  return quests;
}
