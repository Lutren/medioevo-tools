import type { ForensicKind, IntegrationRecommendation, UsefulFor } from "./forensicTypes";

export function classifyUsefulFor(path: string): UsefulFor[] {
  const p = path.toLowerCase();
  const useful = new Set<UsefulFor>();
  if (/(audio|sound|synth|worklet|mixer|music)/.test(p)) useful.add("audio");
  if (/(physic|field|material|collision|grid)/.test(p)) useful.add("physics");
  if (/(light|shadow|lut|bloom|reflection)/.test(p)) useful.add("light");
  if (/(brain|hippocampus|prefrontal|cortex|truth|ghost|handoff)/.test(p)) useful.add("brain_os");
  if (/(language|dialog|speech|lore|claim|source)/.test(p)) useful.add("language");
  if (/(agent|npc|actor)/.test(p)) useful.add("agents");
  if (/(ui|panel|hud|glyph|terminal)/.test(p)) useful.add("ui");
  if (/(rpg|quest|world|metroid)/.test(p)) useful.add("rpg");
  if (/\.(png|jpg|jpeg|webp|gif|svg|aseprite|psd)$/i.test(p)) useful.add("assets");
  return useful.size > 0 ? Array.from(useful) : ["unknown"];
}

export function classifyForensicKind(path: string): ForensicKind {
  const p = path.toLowerCase();
  if (/\.(ts|tsx|js|jsx|mjs|cjs)$/.test(p)) return "code";
  if (/\.(md|txt|pdf|docx?)$/.test(p)) return "document";
  if (/(audio|sound|synth|worklet|mixer)/.test(p)) return "audio";
  if (/(physic|collision|field)/.test(p)) return "physics";
  if (/(light|shadow|bloom|reflection|lut)/.test(p)) return "light";
  if (/(brain|cortex|hippocampus|prefrontal|truth|ghost)/.test(p)) return "brain_os";
  if (/(dialog|language|speech|lore)/.test(p)) return "language";
  if (/(tile|tileset|terrain|road|water)/.test(p)) return "tile";
  if (/(building|facade|roof|tower|market|archive)/.test(p)) return "building";
  if (/(agent|npc|character|sprite)/.test(p)) return "agent";
  if (/(prop|lamp|pipe|door|bridge)/.test(p)) return "prop";
  if (/(material|swatch|stone|metal|wood|glass)/.test(p)) return "material";
  if (/(scene|board|reference|mood)/.test(p)) return "scene_reference";
  if (/(particle|smoke|rain|fire|fog)/.test(p)) return "particle";
  if (/(glyph|icon|symbol)/.test(p)) return "glyph";
  if (/(ui|panel|button|frame|terminal)/.test(p)) return "ui_component";
  return "unknown";
}

export function scoreIntegrationCandidate(input: {
  path: string;
  extension: string;
  size: number;
  kind?: ForensicKind;
  licenseKnown?: boolean;
}): { recommendation: IntegrationRecommendation; risk: "low" | "medium" | "high"; notes: string } {
  const extension = input.extension.toLowerCase();
  const kind = input.kind ?? classifyForensicKind(input.path);
  const isCode = ["ts", "tsx", "js", "jsx", "mjs", "cjs"].includes(extension.replace(".", ""));
  const isDoc = ["md", "json", "txt"].includes(extension.replace(".", ""));
  const isBinaryAsset = ["png", "jpg", "jpeg", "webp", "gif", "psd", "aseprite"].includes(extension.replace(".", ""));
  if (!input.licenseKnown && isBinaryAsset) {
    return { recommendation: "review_required", risk: "medium", notes: "Binary asset has unknown license; inventory only." };
  }
  if (isCode && input.size > 250_000) {
    return { recommendation: "reference_only", risk: "high", notes: "Large unknown code candidate; do not execute or import wholesale." };
  }
  if (isCode && ["audio", "physics", "light", "brain_os", "language", "code"].includes(kind)) {
    return { recommendation: "adapt", risk: "medium", notes: "Review as design source; selectively adapt typed logic with tests." };
  }
  if (isDoc || extension === ".json") {
    return { recommendation: "reference_only", risk: "low", notes: "Safe for read-only metadata and design extraction." };
  }
  return { recommendation: "review_required", risk: "medium", notes: "Default curador state for undocumented source." };
}

export function finiteVisualScore(size: number, usefulFor: UsefulFor[]): number {
  const base = usefulFor.includes("assets") ? 3 : usefulFor.includes("ui") ? 2 : 1;
  const sizeBoost = size > 0 ? Math.min(2, Math.log10(size) / 4) : 0;
  return Number(Math.max(0, Math.min(5, base + sizeBoost)).toFixed(2));
}
