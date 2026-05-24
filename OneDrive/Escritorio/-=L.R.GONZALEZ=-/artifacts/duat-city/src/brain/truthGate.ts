export function runTruthGate(evidence: string[]) {
  const complete = evidence.includes("tests") && evidence.includes("typecheck");
  return {
    gate: complete ? "APPROVE" as const : "REVIEW" as const,
    R: complete ? 0.08 : 0.28,
    Phi_eff: complete ? 0.86 : 0.62,
    evidence,
  };
}
