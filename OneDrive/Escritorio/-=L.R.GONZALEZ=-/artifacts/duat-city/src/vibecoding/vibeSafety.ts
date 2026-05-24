export function sanitizeVibePrompt(prompt: string): { prompt: string; warnings: string[] } {
  const warnings: string[] = [];
  const clean = prompt.replace(/[^\p{L}\p{N}\s,.;:!?_-]/gu, " ").replace(/\s+/g, " ").trim().slice(0, 600);
  if (clean.length < prompt.trim().length) warnings.push("Prompt sanitized for deterministic local parser.");
  const lower = clean.toLowerCase();
  if (/(api|cloud|openai|gemini|claude|http|https|fetch|token|key)/i.test(lower)) {
    warnings.push("External/API terms ignored; VibeCoding is local deterministic parsing only.");
  }
  return { prompt: clean, warnings };
}

export function noCloudSafetyNote(): string {
  return "Local deterministic parser only. No AI call, no cloud, no external API.";
}
