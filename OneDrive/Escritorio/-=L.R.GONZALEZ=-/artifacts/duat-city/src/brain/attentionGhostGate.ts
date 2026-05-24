export function filterAttentionGhostEvent(event: { id: string; R: number; signal: number }) {
  const noisy = event.R > 0.6 && event.signal < 0.35;
  return {
    id: event.id,
    accepted: !noisy,
    reason: noisy ? "GhostGate filtered noisy high-residue event." : "Event accepted by attention gate.",
  };
}
