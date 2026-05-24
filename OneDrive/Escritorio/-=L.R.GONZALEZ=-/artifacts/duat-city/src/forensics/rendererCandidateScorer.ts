export type RendererCandidateType =
  | "three"
  | "react_three_fiber"
  | "drei"
  | "canvas"
  | "css_3d"
  | "isometric_grid"
  | "camera_controls"
  | "lighting"
  | "shadow"
  | "postprocess"
  | "billboard_sprite"
  | "tile_map"
  | "scene_graph"
  | "ui_panel"
  | "i18n_asset"
  | "visual_bible"
  | "duat_component"
  | "unknown";

export interface RendererScoreInput {
  path: string;
  size?: number;
  sourceZip?: string;
}

export interface RendererCandidateScore {
  types: RendererCandidateType[];
  stackDetected: string[];
  usefulFor: string[];
  risk: "low" | "medium" | "high";
  recommendation: "adopt" | "adapt" | "reference_only" | "reject";
  reason: string;
  requiresDependency: boolean;
}

const KEYWORDS: Array<[RendererCandidateType, RegExp, string]> = [
  ["three", /(^|[/\\])(three|threejs|webgl|glb|gltf)|@react-three/i, "3d shell reference"],
  ["react_three_fiber", /@react-three[/\\]fiber|react[-_ ]three[-_ ]fiber|r3f/i, "React 3D renderer reference"],
  ["drei", /@react-three[/\\]drei|orbitcontrols|camera-controls|drei/i, "camera and helper reference"],
  ["canvas", /canvas|ctx\.|getContext|CanvasRenderingContext2D/i, "Canvas renderer reference"],
  ["css_3d", /css3d|preserve-3d|perspective|transform-style/i, "CSS 3D reference"],
  ["isometric_grid", /isometric|iso[-_ ]?grid|tilemap|tile-map|grid/i, "isometric layout reference"],
  ["camera_controls", /camera|orbit|zoom|pan|controls/i, "camera controls reference"],
  ["lighting", /light|illumination|shadow|ambient|directional|pointlight|spotlight/i, "lighting reference"],
  ["shadow", /shadow|drop-shadow|castShadow|receiveShadow/i, "shadow reference"],
  ["postprocess", /postprocess|bloom|composer|outlinepass|fxaa|tone/i, "postprocess reference"],
  ["billboard_sprite", /sprite|billboard|plane|character|agent/i, "2D population reference"],
  ["tile_map", /tileset|tilemap|map\.json|atlas/i, "tile map reference"],
  ["scene_graph", /scene|entity|node|graph|world/i, "scene graph reference"],
  ["ui_panel", /component|panel|toolbar|hud|dashboard|tsx$/i, "UI panel reference"],
  ["i18n_asset", /i18n|locale|translation|lang|es\.json|en\.json/i, "i18n reference"],
  ["visual_bible", /visual[-_ ]?bible|style[-_ ]?guide|palette|moodboard|reference/i, "visual bible reference"],
  ["duat_component", /duat|osit|wabi|medioevo|fibmob/i, "DUAT component reference"],
];

export function scoreRendererCandidate(input: RendererScoreInput): RendererCandidateScore {
  const path = input.path.replace(/\\/g, "/");
  const lower = path.toLowerCase();
  const matched = KEYWORDS.filter(([, pattern]) => pattern.test(path));
  const types = unique(matched.map(([type]) => type));
  const stackDetected = unique(matched.map(([, , stack]) => stack));
  const extension = lower.slice(lower.lastIndexOf(".") + 1);
  const isRuntimeCode = ["ts", "tsx", "js", "jsx", "mjs", "cjs", "vue", "svelte"].includes(extension);
  const isManifest = ["json", "md", "css", "html"].includes(extension);
  const requiresDependency = /@react-three|three|drei|postprocess|composer|webgl/i.test(path);
  const usefulFor = unique([
    ...types.map(typeToUse),
    ...(lower.includes("lovable") ? ["lovable renderer comparison"] : []),
    ...(lower.includes("visual") || lower.includes("palette") ? ["art direction"] : []),
  ]).filter(Boolean);
  const risk: RendererCandidateScore["risk"] = isRuntimeCode ? "high" : requiresDependency ? "medium" : "low";
  const recommendation: RendererCandidateScore["recommendation"] =
    types.includes("react_three_fiber") || types.includes("three") || types.includes("isometric_grid")
      ? "adapt"
      : isManifest || types.includes("visual_bible") || types.includes("i18n_asset")
        ? "reference_only"
        : types.length > 0
          ? "reference_only"
          : "reject";
  const reason = types.length
    ? `Matched ${types.join(", ")}; use as architecture reference only unless reviewed.`
    : "No renderer-relevant keywords found.";

  return {
    types: types.length ? types : ["unknown"],
    stackDetected: stackDetected.length ? stackDetected : ["unknown"],
    usefulFor: usefulFor.length ? usefulFor : ["unknown"],
    risk,
    recommendation,
    reason,
    requiresDependency,
  };
}

function typeToUse(type: RendererCandidateType): string {
  switch (type) {
    case "three":
    case "react_three_fiber":
    case "drei":
    case "css_3d":
      return "iso3d shell";
    case "canvas":
      return "canvas fallback";
    case "isometric_grid":
    case "tile_map":
      return "isometric city routing";
    case "lighting":
    case "shadow":
    case "postprocess":
      return "light/render behavior";
    case "billboard_sprite":
      return "2d pixel population";
    case "ui_panel":
    case "i18n_asset":
      return "ui";
    case "visual_bible":
      return "art direction";
    case "duat_component":
      return "DUAT integration";
    default:
      return "unknown";
  }
}

function unique<T>(values: T[]): T[] {
  return Array.from(new Set(values));
}
