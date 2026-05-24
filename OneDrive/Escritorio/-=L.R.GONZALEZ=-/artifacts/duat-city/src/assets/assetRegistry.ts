import type { AssetDomain, AssetRef } from "./assetTypes";

const DOMAINS: AssetDomain[] = ["tile", "building", "prop", "agent", "material", "ui", "effect"];

export function createProceduralAssetRef(domain: AssetDomain, type: string, styleProfile = "archeopunk_city_rain"): AssetRef {
  return {
    key: `${domain}/${type}`,
    domain,
    mode: "procedural",
    fallbackKey: `procedural/${styleProfile}/${domain}/${type}`,
    provenance: { publication_allowed: false, boundary: "PROCEDURAL_FALLBACK" },
  };
}

export function createDefaultAssetRegistry(styleProfile = "archeopunk_city_rain"): Record<string, AssetRef> {
  const types = {
    tile: ["wet_street", "canal_edge", "bridge_segment", "water", "stone"],
    building: ["archive", "forge", "garden", "market", "rooftop_module"],
    prop: ["bronze_lamp_post", "pipe_cluster", "drainage_grate", "archive_door"],
    agent: ["small_agent_silhouette", "archivist", "observer"],
    material: ["wet_stone", "aged_brass", "obsidian_glass", "neon"],
    ui: ["terminal_frame", "r_phi_gauge", "tube_meter", "action_gate_icons", "q_state_glyphs"],
    effect: ["fire", "smoke", "rain", "neon_glow"],
  } as const;
  const registry: Record<string, AssetRef> = {};
  for (const domain of DOMAINS) {
    for (const type of types[domain]) registry[`${domain}/${type}`] = createProceduralAssetRef(domain, type, styleProfile);
  }
  return registry;
}
