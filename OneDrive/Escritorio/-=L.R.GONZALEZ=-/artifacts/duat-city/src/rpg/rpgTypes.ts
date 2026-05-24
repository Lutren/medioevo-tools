export interface RPGLocation {
  id: string;
  name: string;
  type: string;
  description: string;
  lore_tags: string[];
  R: number;
  is_risk_zone: boolean;
}

export interface RPGFaction {
  id: string;
  name: string;
  alignment: "order" | "conflict" | "neutral" | "void";
  description: string;
  controlled_locations: string[];
  resources: string[];
  reputation: number;
}

export interface RPGNPC {
  id: string;
  name: string;
  role: string;
  faction?: string;
  description: string;
  R: number;
  gate: string;
  quest_giver: boolean;
  schedule?: Array<{ phase: string; location_id?: string; activity: string }>;
}

export interface RPGQuest {
  id: string;
  title: string;
  type: "investigation" | "resource" | "social" | "exploration" | "anomaly";
  hook: string;
  location_id?: string;
  reward: string;
  R_required: number;
  difficulty: "easy" | "medium" | "hard" | "legendary";
}

export interface RPGEncounter {
  id: string;
  type: string;
  title: string;
  description: string;
  outcome_approve: string;
  outcome_block: string;
  R_delta: number;
}

export interface RPGPhysicsProfile {
  walkable_routes: string[];
  blocked_zones: string[];
  collision_heavy_areas: string[];
  agent_flow_corridors: string[];
}

export interface RPGGraphicsProfile {
  visual_rarity: Record<string, number>;
  fibmob_polarity_map: Record<string, string>;
  anomaly_overlays: string[];
  render_mood: string;
  visual_style_profile?: {
    projection: "isometric-2.5d";
    palette: string[];
    identity: string;
    overlays: string[];
  };
  tile_atlas_refs?: Record<string, string>;
  agent_icon_refs?: Record<string, string>;
  light_profile?: {
    ambient: string;
    point_lights: number;
    flicker_source: string;
  };
  reviewed_asset_refs?: string[];
  screenshot_paths?: string[];
}

export interface RPGQuaternaryProfile {
  counts: Record<string, number>;
  anomaly_zones: string[];
  stable_zones: string[];
  event_zones: string[];
  unstable_agents: string[];
  suggested_quests: string[];
}

export interface RPGVisualSceneProfile {
  palette: string;
  light_profile: string;
  weather: string;
  material_map: Record<string, string>;
  mood: string;
  visual_tags: string[];
  placed_materials?: Array<{ id: string; x: number; y: number; material: string }>;
  placed_lights?: Array<{ id: string; x: number; y: number; kind: string; color: string }>;
  vibe_config?: object;
}

export interface RPGPixelPhysicsProfile {
  water_zones: string[];
  fire_zones: string[];
  smoke_zones: string[];
  reflective_zones: string[];
  danger_materials: string[];
  anomaly_materials: string[];
}

export interface RPGArtDirectionProfile {
  light_canon: string;
  material_detail_profile: string;
  narrative_lenses: string[];
  symbolic_objects: Array<{ id: string; label: string; material: string; meaning: string; placement: string }>;
  mood_tags: string[];
  public_boundary_note: string;
}

export interface RPGAudioGameFeelProfile {
  schema: "duat/rpg-audio-gamefeel/v1.3.1";
  procedural_only: true;
  requires_user_gesture: true;
  external_samples_copied: false;
  publication_allowed: false;
  cue_count: number;
  cue_tags: string[];
  R_audio: number;
  Phi_audio: number;
  material_cues: number;
  light_cues: number;
  agent_cues: number;
  manifest_refs: string[];
}

export interface RPGMapTile {
  id: number;
  x: number;
  y: number;
  type: string;
  R: number;
  Phi_eff: number;
  asset_ref: string;
}

export interface RPGDistrict {
  id: string;
  name: string;
  zoning: string;
  growth: number;
  risk: number;
}

export interface RPGWorld {
  schema: string;
  name: string;
  seed: number;
  tick: number;
  locations: RPGLocation[];
  factions: RPGFaction[];
  npcs: RPGNPC[];
  quests: RPGQuest[];
  encounters: RPGEncounter[];
  resources: Record<string, number>;
  map_tiles?: RPGMapTile[];
  districts?: RPGDistrict[];
  landmarks?: string[];
  faction_control?: Record<string, string[]>;
  danger_zones?: string[];
  light_zones?: string[];
  environmental_hazards?: string[];
  visual_asset_manifest_refs?: string[];
  reviewed_asset_refs?: string[];
  visual_style_profile?: object;
  tile_atlas_refs?: Record<string, string>;
  agent_icon_refs?: Record<string, string>;
  light_profile?: object;
  screenshot_paths?: string[];
  physics_field_summary?: object;
  suggested_scenes?: string[];
  lore_tags: string[];
  risk_zones: string[];
  physics_profile: RPGPhysicsProfile;
  graphics_profile: RPGGraphicsProfile;
  quaternary_profile?: RPGQuaternaryProfile;
  visual_scene_profile?: RPGVisualSceneProfile;
  pixel_physics_profile?: RPGPixelPhysicsProfile;
  art_direction_profile?: RPGArtDirectionProfile;
  audio_gamefeel_profile?: RPGAudioGameFeelProfile;
  style_tokens?: object;
  asset_references?: string[];
  procedural_generation_seeds?: Record<string, number>;
  material_field_summary?: object;
  light_field_summary?: object;
  vibe_command_history?: string[];
  agent_routes?: string[];
  interaction_points?: string[];
  playable_scene_profile?: object;
  game_os_profile?: object;
  language_profile?: object;
  brain_runtime_profile?: object;
  cosmology_profile?: object;
  osit_formula_profile?: object;
  rpg_metroidvania_bridge?: object;
  handoff: object;
}
