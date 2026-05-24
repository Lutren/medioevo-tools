import type { CityState } from "../core/types";
import type { RPGAudioGameFeelProfile, RPGArtDirectionProfile, RPGDistrict, RPGGraphicsProfile, RPGMapTile, RPGPhysicsProfile, RPGQuaternaryProfile, RPGWorld, RPGLocation, RPGNPC, RPGQuest, RPGVisualSceneProfile, RPGPixelPhysicsProfile } from "./rpgTypes";
import { generateFactions } from "./factionGenerator";
import { generateQuests } from "./questGenerator";
import { generateEncounters } from "./encounterGenerator";
import { getLoreTag, getRarityLabel } from "./loreTags";
import { generateHandoff } from "../core/handoff";
import { playableSceneRpgProfile } from "../scene/sceneState";
import { compileNarrativeLens, generateQuestTone, PUBLIC_BOUNDARY_NOTE } from "../artDirection/narrativeLenses";
import { generateSymbolicObjects } from "../artDirection/symbolicObjectGrammar";
import type { NarrativeLensId } from "../artDirection/artDirectionTypes";
import { DEFAULT_DUAT_STYLE_TOKENS } from "../style/styleTokens";
import { createGameModeState } from "../gameModes/gameModeState";
import { createBrainRuntime } from "../brain/brainRuntime";
import { computeLanguageMetrics } from "../language/languageMetrics";
import { generateNpcUtterance } from "../language/npcSpeechEngine";
import { compileInWorldCosmology } from "../lore/medioevoCosmology";
import { createRpgModeBridge } from "./rpgModeBridge";
import { createAudioGameFeelSnapshot } from "../audio/gameFeelAdapter";
import type { AudioGameFeelSnapshot } from "../audio/audioTypes";
import { compileOSITFormulaProfile } from "../osit/ositIntegration";

export function exportRPGWorld(state: CityState): RPGWorld {
  const physicsProfile = buildPhysicsProfile(state);
  const graphicsProfile = buildGraphicsProfile(state);
  const quaternaryProfile = buildQuaternaryProfile(state);
  const visualSceneProfile = buildVisualSceneProfile(state);
  const pixelPhysicsProfile = buildPixelPhysicsProfile(state);
  const artDirectionProfile = buildArtDirectionProfile(state);
  const audioGameFeel = createAudioGameFeelSnapshot(state);
  const audioGameFeelProfile = buildAudioGameFeelProfile(audioGameFeel);
  const ositFormulaProfile = compileOSITFormulaProfile(state);
  const gameModeState = createGameModeState("rpg");
  const languageStatements = state.agents.slice(0, 4).map(agent => generateNpcUtterance(agent, state, "rpg_export"));
  const languageMetrics = computeLanguageMetrics(languageStatements);
  const brainRuntime = createBrainRuntime({ city: state, gameMode: gameModeState, languageMetrics, audioGameFeel });
  const cosmologyProfile = compileInWorldCosmology();
  const reviewedAssetRefs = ["/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json", "/reviewed-assets/v1_2/REVIEWED_ASSETS_MANIFEST.json"];
  const screenshotPaths = [
    "docs/screenshots/v0_7/city-operational.png",
    "docs/screenshots/v0_7/osit-debug-pixel-field.png",
  ];
  const factions = generateFactions(state);
  const quests = [
    ...generateQuests(state, physicsProfile),
    ...buildQuaternaryQuests(state, quaternaryProfile),
    ...buildPixelRealismQuests(state, pixelPhysicsProfile),
    ...buildArtDirectionQuests(state, artDirectionProfile),
  ];
  const encounters = generateEncounters(state);

  const locations: RPGLocation[] = state.buildings.map(b => {
    const tile = state.tiles.find(t => t.x === b.x && t.y === b.y);
    const loreTag = tile ? getLoreTag(tile) : "unknown";
    return {
      id: b.id,
      name: b.name,
      type: b.type,
      description: `A ${b.type} at (${b.x},${b.y}). R=${b.R.toFixed(2)} Phi=${b.Phi_eff.toFixed(2)}.`,
      lore_tags: [loreTag, getRarityLabel(tile?.fibmob.rarity ?? 0.5)],
      R: b.R,
      is_risk_zone: b.R > 0.5 || b.type === "ruin",
    };
  });

  const npcs: RPGNPC[] = state.agents.map(agent => {
    const faction = factions.find(f => f.name.toLowerCase().includes(agent.role.toLowerCase()));
    return {
      id: agent.id,
      name: agent.name,
      role: agent.role,
      faction: faction?.name,
      description: `${agent.role} with R=${agent.R.toFixed(2)}, gate=${agent.gate}. Memory: ${agent.memory.slice(-1)[0] ?? "none"}.`,
      R: agent.R,
      gate: agent.gate,
      quest_giver: agent.role === "Observer" || agent.role === "Archivist" || agent.role === "Storykeeper",
      schedule: [
        { phase: "morning_work", location_id: agent.workplaceId, activity: "work or evidence task" },
        { phase: "midday_social", location_id: state.buildings.find(b => b.type === "market" || b.type === "plaza")?.id, activity: "eat/social" },
        { phase: "evening_home", location_id: agent.homeId, activity: "rest/home" },
      ],
    };
  });

  const loreTags = [
    ...new Set([
      ...state.tiles
        .filter(t => t.type !== "empty" && t.type !== "road")
        .map(t => getLoreTag(t))
        .slice(0, 20),
    ]),
  ];

  const riskZones = locations.filter(l => l.is_risk_zone).map(l => l.name);
  const mapTiles: RPGMapTile[] = state.tiles
    .filter(t => t.type !== "empty")
    .slice(0, 240)
    .map(t => ({
      id: t.id,
      x: t.x,
      y: t.y,
      type: t.type,
      R: t.R,
      Phi_eff: t.Phi_eff,
      asset_ref: `tile/${t.type}`,
    }));
  const districts: RPGDistrict[] = (state.districts ?? []).map(d => ({
    id: d.id,
    name: d.name,
    zoning: d.zoning,
    growth: d.growth,
    risk: d.risk,
  }));
  const environmentalHazards = [
    ...(state.fieldSummary?.hazards ?? []),
    ...state.tiles.filter(t => t.type === "water").slice(0, 3).map(t => `flood:${t.x},${t.y}`),
    ...state.buildings.filter(b => b.type === "ruin").slice(0, 4).map(b => `ruin_anomaly:${b.name}`),
  ];
  const factionControl = Object.fromEntries(factions.map(f => [f.name, f.controlled_locations]));

  return {
    schema: "medioevo-rpg/world/v3",
    name: "Generated MEDIOEVO City",
    seed: state.tick * 31337 % 999999,
    tick: state.tick,
    locations,
    factions,
    npcs,
    quests,
    encounters,
    resources: { ...state.resources },
    map_tiles: mapTiles,
    districts,
    landmarks: locations.filter(l => ["observatory", "archive", "temple", "ruin", "gatehouse"].includes(l.type)).map(l => l.name),
    faction_control: factionControl,
    danger_zones: [...riskZones, ...environmentalHazards],
    light_zones: state.buildings
      .filter(b => ["observatory", "market", "clinic", "temple", "archive"].includes(b.type))
      .map(b => `${b.name}:${b.x},${b.y}`),
    environmental_hazards: environmentalHazards,
    visual_asset_manifest_refs: [
      "/asset-manifest/visual_assets_manifest_v0_6.json",
      "/asset-manifest/code_candidates_manifest_v0_6.json",
      "/asset-manifest/duat_variants_manifest_v0_6.json",
      "/asset-manifest/asset_allowlist_v0_7.json",
      "/asset-manifest/assets_du_wabi_manifest_v1_2.json",
      "/asset-manifest/style_tokens_v1_2.json",
      "/asset-manifest/asset_allowlist_v1_2.json",
      "/asset-manifest/audio_gamefeel_manifest_v1_3_1.json",
      "/asset-manifest/agents_gamefeel_manifest_v1_3_1.json",
      "/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json",
      "/reviewed-assets/v1_2/REVIEWED_ASSETS_MANIFEST.json",
    ],
    reviewed_asset_refs: reviewedAssetRefs,
    visual_style_profile: graphicsProfile.visual_style_profile,
    tile_atlas_refs: graphicsProfile.tile_atlas_refs,
    agent_icon_refs: graphicsProfile.agent_icon_refs,
    light_profile: graphicsProfile.light_profile,
    screenshot_paths: screenshotPaths,
    physics_field_summary: state.fieldSummary ?? { hazards: [], R_field: 0, Phi_field: 1 },
    suggested_scenes: [
      state.regime === "SATURADO" ? "handoff closure at archive" : "morning market route",
      environmentalHazards.length > 0 ? "district hazard response" : "observatory signal scan",
    ],
    lore_tags: loreTags,
    risk_zones: riskZones,
    physics_profile: physicsProfile,
    graphics_profile: graphicsProfile,
    quaternary_profile: quaternaryProfile,
    visual_scene_profile: visualSceneProfile,
    pixel_physics_profile: pixelPhysicsProfile,
    art_direction_profile: artDirectionProfile,
    audio_gamefeel_profile: audioGameFeelProfile,
    style_tokens: DEFAULT_DUAT_STYLE_TOKENS,
    asset_references: reviewedAssetRefs,
    procedural_generation_seeds: {
      tiles: 1209,
      buildings: 1202,
      props: 1206,
      ui: 1201,
      agents: 1210,
    },
    material_field_summary: {
      active_cells: state.playableScene?.metrics.activeMaterialCells ?? state.fieldMetrics?.activeCells ?? 0,
      skipped_cells: state.fieldMetrics?.skippedCells ?? 0,
      hazards: pixelPhysicsProfile.danger_materials,
    },
    light_field_summary: {
      active_light_cells: state.pixelRealism?.activeLightCells ?? 0,
      R_light: state.pixelRealism?.R_light ?? 0,
      Phi_light: state.pixelRealism?.Phi_light ?? 1,
      light_profile: visualSceneProfile.light_profile,
    },
    vibe_command_history: state.playableScene?.lastIntent ?? [],
    agent_routes: state.agents.slice(0, 12).map(agent => `${agent.name}:${Math.round(agent.x)},${Math.round(agent.y)}`),
    interaction_points: [
      ...(visualSceneProfile.placed_materials?.slice(0, 8).map(cell => `${cell.material}:${cell.x},${cell.y}`) ?? []),
      ...(visualSceneProfile.placed_lights?.slice(0, 8).map(light => `${light.kind}:${light.x},${light.y}`) ?? []),
    ],
    playable_scene_profile: state.playableScene ? playableSceneRpgProfile(state.playableScene) : undefined,
    game_os_profile: {
      active_mode: gameModeState.activeMode,
      supported_modes: ["duat_interface", "hormiguero", "agent_sims", "city_president", "era_progression", "vs_arena", "rpg", "metroidvania"],
      direct_agent_control_default: false,
    },
    language_profile: {
      metrics: languageMetrics,
      sample_dialogue: languageStatements.map(statement => ({ classification: statement.classification, text: statement.text, gate: statement.gate })),
    },
    brain_runtime_profile: {
      schema: brainRuntime.schema,
      executionAllowed: brainRuntime.executionAllowed,
      systems: Object.fromEntries(Object.entries(brainRuntime.systems).map(([key, value]) => [key, { R: value.R, Phi_eff: value.Phi_eff, gate: value.gate }])),
    },
    osit_formula_profile: {
      schema: ositFormulaProfile.schema,
      formulaCount: ositFormulaProfile.formulaCount,
      gate: ositFormulaProfile.gate,
      R_formula: ositFormulaProfile.R_formula,
      Phi_formula: ositFormulaProfile.Phi_formula,
      modules: ositFormulaProfile.modules,
      boundary: ositFormulaProfile.boundary,
    },
    cosmology_profile: {
      boundary: "IN_WORLD_COSMOLOGY",
      publicClaimAllowed: cosmologyProfile.publicClaimAllowed,
      concepts: cosmologyProfile.concepts.map(concept => concept.id),
      scienceBoundaryNote: cosmologyProfile.scienceBoundaryNote,
    },
    rpg_metroidvania_bridge: createRpgModeBridge(state),
    handoff: generateHandoff(state),
  };
}

export function buildPhysicsProfile(state: CityState): RPGPhysicsProfile {
  const roads = state.tiles.filter(t => t.type === "road").slice(0, 12);
  const blocked = state.tiles.filter(t => t.buildingId && t.type !== "plaza" && t.type !== "garden").slice(0, 12);
  const collisionHeavy = state.physicsMetrics && state.physicsMetrics.unresolvedCollisions + state.physicsMetrics.resolvedCollisions > 0
    ? state.buildings.slice(0, 3).map(b => b.name)
    : [];
  return {
    walkable_routes: roads.map(t => `road:${t.x},${t.y}`),
    blocked_zones: blocked.map(t => `${t.type}:${t.x},${t.y}`),
    collision_heavy_areas: collisionHeavy,
    agent_flow_corridors: roads.filter((_, i) => i % 3 === 0).map(t => `corridor:${t.x},${t.y}`),
  };
}

export function buildGraphicsProfile(state: CityState): RPGGraphicsProfile {
  const visual_rarity: Record<string, number> = {};
  const fibmob_polarity_map: Record<string, string> = {};
  const anomaly_overlays: string[] = [];
  for (const tile of state.tiles.filter(t => t.type !== "empty").slice(0, 40)) {
    visual_rarity[String(tile.id)] = tile.fibmob.rarity;
    fibmob_polarity_map[String(tile.id)] = tile.fibmob.polarity;
    if (tile.type === "ruin" || tile.fibmob.polarity === "void") anomaly_overlays.push(`tile:${tile.id}:${tile.type}`);
  }
  return {
    visual_rarity,
    fibmob_polarity_map,
    anomaly_overlays,
    render_mood: state.regime === "SATURADO" ? "compressed-alert" : state.Phi_eff > 0.75 ? "clear-signal" : "working-field",
    visual_style_profile: {
      projection: "isometric-2.5d",
      palette: ["obsidian", "bronze", "operational-cyan", "alert-amber", "ritual-stone"],
      identity: "MEDIOEVO archeopunk city-builder with OSIT overlays",
      overlays: ["R", "Phi_eff", "gate", "FibMob", "pixel-field"],
    },
    tile_atlas_refs: {
      road: "tile/road",
      ruin: "tile/ruin",
      market: "tile/market",
      archive: "tile/archive",
    },
    agent_icon_refs: {
      default: "agent/default",
      Archivist: "agent/Archivist",
      Observer: "ui/witness",
    },
    light_profile: {
      ambient: state.tick % 240 < 120 ? "day" : "night",
      point_lights: state.buildings.filter(b => ["observatory", "market", "clinic", "temple", "archive"].includes(b.type)).length,
      flicker_source: "FibMob deterministic tick",
    },
    reviewed_asset_refs: ["/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json"],
    screenshot_paths: [
      "docs/screenshots/v0_7/city-operational.png",
      "docs/screenshots/v0_7/osit-debug-pixel-field.png",
    ],
  };
}

export function buildQuaternaryProfile(state: CityState): RPGQuaternaryProfile {
  const q = state.quaternary;
  const recent = q?.recent ?? [];
  const anomaly_zones = recent
    .filter(e => e.state === "01" && (e.sourceKind === "tile" || e.sourceKind === "building" || e.sourceKind === "render_chunk"))
    .map(e => e.sourceId)
    .slice(0, 8);
  const stable_zones = recent
    .filter(e => e.state === "10" && (e.sourceKind === "tile" || e.sourceKind === "building"))
    .map(e => e.sourceId)
    .slice(0, 8);
  const event_zones = recent
    .filter(e => e.state === "11" && e.timing.stability >= 0.35)
    .map(e => e.sourceId)
    .slice(0, 8);
  const unstable_agents = recent
    .filter(e => e.sourceKind === "agent" && e.timing.frequency > 0.35)
    .map(e => e.sourceId.replace("agent:", ""))
    .slice(0, 8);
  const suggested_quests: string[] = [];
  if (anomaly_zones.some(zone => zone.includes("ruin") || zone.includes("gatehouse")) || (q?.counts["01"] ?? 0) > 0) {
    suggested_quests.push("Investigate missing signal");
  }
  if (recent.some(e => e.sourceId.includes("market") && e.timing.frequency > 0.25)) {
    suggested_quests.push("Stabilize market oscillation");
  }
  if (stable_zones.some(zone => zone.includes("archive"))) {
    suggested_quests.push("Recover stable knowledge");
  }
  if (event_zones.some(zone => zone.includes("observatory")) || (q?.counts["11"] ?? 0) > 3) {
    suggested_quests.push("Follow active anomaly");
  }

  return {
    counts: q?.counts ?? { "00": 0, "01": 0, "10": 0, "11": 0 },
    anomaly_zones,
    stable_zones,
    event_zones,
    unstable_agents,
    suggested_quests,
  };
}

export function buildVisualSceneProfile(state: CityState): RPGVisualSceneProfile {
  const pixel = state.pixelRealism;
  const materialMap: Record<string, string> = {};
  for (const tile of state.tiles.filter(t => t.type !== "empty").slice(0, 60)) {
    materialMap[`${tile.x},${tile.y}`] = tile.type === "water"
      ? "water"
      : tile.type === "forest" || tile.type === "garden"
        ? "grass"
        : tile.type === "ruin"
          ? "ruinMatter"
          : tile.type === "road"
            ? "wet-stone"
            : "brick";
  }
  for (const cell of state.playableScene?.materials ?? []) {
    materialMap[`${cell.x},${cell.y}`] = cell.material;
  }
  const visualTags = [
    "pixel-art-realism",
    "isometric-2.5d",
    pixel?.qualityPreset ?? "MEDIUM",
    pixel?.vibePreset ?? "no-vibe",
  ];
  return {
    palette: pixel?.palette ?? "medioevo_archeopunk",
    light_profile: pixel?.lightProfile ?? "operational-balanced",
    weather: state.playableScene?.weather ?? (pixel?.vibePreset?.includes("rain") ? "rain" : "local-simulated"),
    material_map: materialMap,
    mood: state.playableScene?.activeVibe?.mood ?? pixel?.vibePreset ?? (state.regime === "SATURADO" ? "compressed-alert" : "working-field"),
    visual_tags: visualTags,
    placed_materials: state.playableScene?.materials.map(cell => ({ id: cell.id, x: cell.x, y: cell.y, material: cell.material })),
    placed_lights: state.playableScene?.lights.map(light => ({ id: light.id, x: light.x, y: light.y, kind: light.kind, color: light.color })),
    vibe_config: state.playableScene?.activeVibe,
  };
}

export function buildPixelPhysicsProfile(state: CityState): RPGPixelPhysicsProfile {
  const sceneMaterials = state.playableScene?.materials ?? [];
  const water = [
    ...state.tiles.filter(t => t.type === "water").map(t => `water:${t.x},${t.y}`),
    ...sceneMaterials.filter(cell => cell.material === "water").map(cell => `water:${cell.x},${cell.y}`),
  ].slice(0, 16);
  const ruins = state.buildings.filter(b => b.type === "ruin").map(b => `${b.name}:${b.x},${b.y}`).slice(0, 8);
  const reflective = [
    ...water,
    ...state.tiles.filter(t => t.type === "road").slice(0, 8).map(t => `wet-road:${t.x},${t.y}`),
  ];
  const fire = [
    ...state.buildings.filter(b => ["market", "temple"].includes(b.type)).map(b => `warm-source:${b.x},${b.y}`),
    ...sceneMaterials.filter(cell => cell.material === "fire" || cell.material === "neon").map(cell => `${cell.material}:${cell.x},${cell.y}`),
  ].slice(0, 12);
  const smoke = [
    ...state.buildings.filter(b => ["market", "workshop", "ruin"].includes(b.type)).map(b => `smoke:${b.x},${b.y}`),
    ...sceneMaterials.filter(cell => cell.material === "smoke").map(cell => `smoke:${cell.x},${cell.y}`),
  ].slice(0, 12);
  return {
    water_zones: water,
    fire_zones: fire,
    smoke_zones: smoke,
    reflective_zones: reflective,
    danger_materials: ["fire", "smoke", "ruinMatter"],
    anomaly_materials: ruins.length > 0 ? ["ruinMatter", "crystal", ...ruins] : ["ruinMatter", "crystal"],
  };
}

export function buildAudioGameFeelProfile(snapshot: AudioGameFeelSnapshot): RPGAudioGameFeelProfile {
  return {
    schema: "duat/rpg-audio-gamefeel/v1.3.1",
    procedural_only: true,
    requires_user_gesture: true,
    external_samples_copied: false,
    publication_allowed: false,
    cue_count: snapshot.metrics.cueCount,
    cue_tags: Array.from(new Set(snapshot.cues.flatMap(cue => cue.tags))).slice(0, 24),
    R_audio: snapshot.metrics.R_audio,
    Phi_audio: snapshot.metrics.Phi_audio,
    material_cues: snapshot.metrics.materialCues,
    light_cues: snapshot.metrics.lightCues,
    agent_cues: snapshot.metrics.agentCues,
    manifest_refs: [
      "/asset-manifest/audio_gamefeel_manifest_v1_3_1.json",
      "/asset-manifest/audio_zip_manifest_v1_3.json",
    ],
  };
}

function buildQuaternaryQuests(state: CityState, profile: RPGQuaternaryProfile): RPGQuest[] {
  return profile.suggested_quests.slice(0, 4).map((title, index) => {
    const type: RPGQuest["type"] = title.toLowerCase().includes("signal") || title.toLowerCase().includes("anomaly")
      ? "anomaly"
      : title.toLowerCase().includes("market")
        ? "social"
        : "investigation";
    return {
      id: `q-quaternary-${state.tick}-${index}`,
      title,
      type,
      hook: `Quaternary timing profile suggests: ${title}. Gate=${state.quaternary?.gate ?? "APPROVE"}.`,
      location_id: state.buildings.find(b => title.toLowerCase().includes(b.type))?.id,
      reward: "R_quaternary -0.04, Phi_quaternary +0.04, new evidence marker",
      R_required: state.quaternary?.R ?? 0,
      difficulty: (state.quaternary?.gate === "BLOCK" ? "hard" : state.quaternary?.gate === "REVIEW" ? "medium" : "easy"),
    };
  });
}

function buildPixelRealismQuests(state: CityState, profile: RPGPixelPhysicsProfile): RPGQuest[] {
  const hooks = [
    ["restore broken light source", "Restore broken light source"],
    ["investigate impossible shadow", "Investigate impossible shadow"],
    ["drain flooded passage", "Drain flooded passage"],
    ["repair neon market", "Repair neon market"],
    ["stabilize ruin crystal", "Stabilize ruin crystal"],
    ["follow reflection anomaly", "Follow reflection anomaly"],
  ] as const;
  return hooks.map(([id, title], index) => ({
    id: `q-visual-${state.tick}-${index}-${id.replace(/\s+/g, "-")}`,
    title,
    type: title.includes("shadow") || title.includes("anomaly") || title.includes("crystal") ? "anomaly" : title.includes("flooded") ? "exploration" : "investigation",
    hook: `Pixel realism profile suggests: ${title}. Active light cells=${state.pixelRealism?.activeLightCells ?? 0}.`,
    location_id: state.buildings[index % Math.max(1, state.buildings.length)]?.id,
    reward: "R_light -0.03, Phi_light +0.04, visual scene evidence",
    R_required: state.pixelRealism?.R_light ?? 0,
    difficulty: (profile.anomaly_materials.length > 2 || (state.pixelRealism?.R_light ?? 0) > 0.3) ? "medium" : "easy",
  }));
}

export function buildArtDirectionProfile(state: CityState): RPGArtDirectionProfile {
  const art = state.playableScene?.activeVibe?.artDirection;
  const lenses = (art?.narrativeLenses?.length ? art.narrativeLenses : ["mythic_archive_lens"]) as NarrativeLensId[];
  const compiled = lenses.map(lens => compileNarrativeLens(state, lens));
  return {
    light_canon: art?.lightCanon ?? "balanced_medioevo",
    material_detail_profile: art?.materialDetailProfile ?? "medioevo_material_detail",
    narrative_lenses: lenses,
    symbolic_objects: generateSymbolicObjects(lenses, 13).map(obj => ({
      id: obj.id,
      label: obj.label,
      material: obj.material,
      meaning: obj.meaning,
      placement: obj.placement,
    })),
    mood_tags: Array.from(new Set([...(art?.moodTags ?? []), ...compiled.flatMap(lens => lens.moodTags)])).slice(0, 24),
    public_boundary_note: PUBLIC_BOUNDARY_NOTE,
  };
}

function buildArtDirectionQuests(state: CityState, profile: RPGArtDirectionProfile): RPGQuest[] {
  const hooks: Record<string, string> = {
    surveillance_dystopia_lens: "decode propaganda signal",
    moral_conflict_lens: "judge a sealed witness",
    mythic_archive_lens: "recover memory relic",
    perception_break_lens: "verify which memory is real",
    absurd_trial_lens: "escape recursive gate review",
    stoic_duty_lens: "hold the gate during collapse",
  };
  return profile.narrative_lenses
    .filter(lens => hooks[lens])
    .slice(0, 6)
    .map((lens, index) => ({
      id: `q-art-${state.tick}-${index}-${lens}`,
      title: hooks[lens],
      type: lens === "surveillance_dystopia_lens" || lens === "mythic_archive_lens" ? "investigation" : "anomaly",
      hook: generateQuestTone(lens, state),
      location_id: state.buildings[index % Math.max(1, state.buildings.length)]?.id,
      reward: "art_direction_profile +1, MEDIOEVO-original lore hook",
      R_required: state.R,
      difficulty: state.R > 0.45 ? "hard" : "medium",
    }));
}
