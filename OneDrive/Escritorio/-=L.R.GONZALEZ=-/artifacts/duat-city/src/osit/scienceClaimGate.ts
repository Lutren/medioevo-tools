import type { OSITFormulaOperator, ScienceClaimGateResult } from "./ositTypes";

const BLOCKED_PUBLIC_CLAIM_PATTERNS = [
  /physics\s+is\s+proven/i,
  /exact\s+physical\s+simulation/i,
  /real\s+quantum\s+consciousness/i,
  /path\s+tracing\s+real/i,
  /cosmology\s+is\s+science\s+fact/i,
];

export function evaluateScienceClaimGate(formula: OSITFormulaOperator, claim = ""): ScienceClaimGateResult {
  const blockedClaim = BLOCKED_PUBLIC_CLAIM_PATTERNS.some(pattern => pattern.test(claim));
  const boundaryRisk = formula.boundary === "IN_WORLD_LORE" || formula.boundary === "FORMAL_LAB_ONLY" ? 0.18 : 0.04;
  const R = clamp(formula.risk + boundaryRisk + (blockedClaim ? 0.45 : 0));
  const Phi_eff = clamp(formula.Phi_eff - (blockedClaim ? 0.35 : 0));
  const gate = blockedClaim || R >= 0.55 ? "BLOCK" : R >= 0.32 || Phi_eff < 0.6 ? "REVIEW" : "APPROVE";
  return {
    gate,
    R,
    Phi_eff,
    downgraded: blockedClaim || formula.publicClaimAllowed === false,
    reason: blockedClaim
      ? "ScienceClaimGate blocked exact/public physics claim."
      : "Formula allowed only as OSIT formal-lab or operational approximation.",
  };
}

function clamp(value: number): number {
  return Number(Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0)).toFixed(3));
}
