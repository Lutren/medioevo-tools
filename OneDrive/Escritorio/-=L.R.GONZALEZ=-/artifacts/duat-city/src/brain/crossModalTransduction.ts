export function compileCrossModalTransduction(input: { visual: string; audio?: string; language?: string; physics?: string }) {
  return {
    schema: "duat/cross-modal-transduction/v1.3",
    channels: input,
    cloudUsed: false,
    summary: [input.visual, input.audio, input.language, input.physics].filter(Boolean).join(" -> "),
  };
}
