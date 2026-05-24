import type { AssetManifestEntryV12, AssetManifestV12, DuatStyleTokens } from "./styleTypes";
import { mergeStyleTokens } from "./styleTokens";

export function analyzeStyleFromManifest(manifest: Pick<AssetManifestV12, "assets" | "asset_count">): DuatStyleTokens {
  const assets = manifest.assets ?? [];
  const kindCounts = countBy(assets, asset => asset.kind);
  const imageCount = assets.filter(asset => ["png", "jpg", "jpeg", "webp", "gif"].includes(asset.extension)).length;
  const avgScore = average(assets.map(asset => asset.visual_score));
  const hasUi = (kindCounts.ui_component ?? 0) > 0;
  const sceneRefs = kindCounts.scene_reference ?? 0;
  return mergeStyleTokens({
    generatedAt: new Date(0).toISOString(),
    sourceAssetCount: manifest.asset_count ?? assets.length,
    contrastProfile: avgScore >= 4 ? "high" : avgScore >= 2.5 ? "medium" : "low",
    edgeDetailDensity: finite01(0.45 + avgScore * 0.09 + Math.min(0.18, imageCount * 0.002)),
    uiFrameStyle: hasUi ? "asset-informed diegetic terminal frame" : "procedural diegetic terminal frame",
    sceneMoodTags: sceneRefs > 0
      ? ["asset-board-reference", "archeopunk", "cinematic-light", "material-rich"]
      : ["procedural-fallback", "archeopunk", "cinematic-light"],
  });
}

export function inferStyleProfileFromPrompt(prompt: string): string {
  const text = prompt.toLowerCase();
  if (text.includes("archivo")) return "forbidden_archive";
  if (text.includes("forja") || text.includes("forge") || text.includes("fuego")) return "central_forge";
  if (text.includes("jardin") || text.includes("garden") || text.includes("biomecan")) return "biomechanical_garden";
  if (text.includes("mercado") || text.includes("market")) return "underground_market";
  if (text.includes("lluv") || text.includes("neon")) return "neon_rain_street";
  if (text.includes("taberna") || text.includes("interior")) return "warm_interior_tavern";
  if (text.includes("debug") || text.includes("qstate")) return "qstate_debug_glyphs";
  return "archeopunk_city_rain";
}

function countBy<T>(items: T[], keyFn: (item: T) => string): Record<string, number> {
  return items.reduce<Record<string, number>>((acc, item) => {
    const key = keyFn(item);
    acc[key] = (acc[key] ?? 0) + 1;
    return acc;
  }, {});
}

function average(values: number[]): number {
  const finite = values.filter(Number.isFinite);
  return finite.length ? finite.reduce((sum, value) => sum + value, 0) / finite.length : 0;
}

function finite01(value: number): number {
  return Math.max(0, Math.min(1, Number.isFinite(value) ? Number(value.toFixed(3)) : 0));
}
