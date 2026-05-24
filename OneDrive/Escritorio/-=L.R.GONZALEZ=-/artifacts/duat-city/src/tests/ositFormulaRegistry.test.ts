import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { listOSITFormulaOperators, mapFormulaToOSITModule } from "../osit/formulaRegistry";
import { compileOSITFormulaProfile } from "../osit/ositIntegration";
import { evaluateScienceClaimGate } from "../osit/scienceClaimGate";
import {
  blackScholesRiskProxy,
  boltzmannResidue,
  eulerStep,
  fourierSignalEnergy,
  gaussianEvidenceWeight,
  maxwellFieldProxy,
  navierStokesFlowProxy,
  newtonMotionProxy,
  schrodingerProbabilityBoundary,
  shannonEntropy,
} from "../osit/ositFormulaMath";

describe("OSIT formula registry v1.4", () => {
  it("maps all requested historical operators to gated OSIT modules", () => {
    const formulas = listOSITFormulaOperators();
    expect(formulas.map(item => item.historicalReference)).toEqual([
      "Shannon",
      "Boltzmann",
      "Maxwell",
      "Navier-Stokes",
      "Fourier",
      "Schrodinger",
      "Black-Scholes",
      "Euler",
      "Gauss",
      "Newton",
    ]);
    expect(formulas.every(item => item.publicClaimAllowed === false)).toBe(true);
    expect(mapFormulaToOSITModule("ActionGate").some(item => item.id === "black_scholes_risk_proxy")).toBe(true);
    expect(mapFormulaToOSITModule("PixelLightEngine").length).toBeGreaterThan(2);
  });

  it("computes finite local proxy math without exact-physics claims", () => {
    const values = [
      shannonEntropy([0.5, 0.5]),
      boltzmannResidue(32),
      fourierSignalEnergy([0, 1, 0, -1]),
      gaussianEvidenceWeight(0),
      eulerStep(1, 0.5, 0.1),
      newtonMotionProxy(0, 1, 0.5, 0.2),
      navierStokesFlowProxy(1, 1, 0.2),
      maxwellFieldProxy(0.2, 0.3),
      schrodingerProbabilityBoundary(0.4, 0.5),
      blackScholesRiskProxy(0.3, 1, 1.1),
    ];
    expect(values.every(Number.isFinite)).toBe(true);
    expect(values.every(value => value >= 0)).toBe(true);
  });

  it("compiles profile and blocks exact public science claims", () => {
    const city = createCity();
    const profile = compileOSITFormulaProfile(city);
    expect(profile.schema).toBe("duat/osit-formula-profile/v1.4");
    expect(profile.formulaCount).toBe(10);
    expect(profile.boundary.scienceClaimGate).toBe("ACTIVE");
    expect(profile.boundary.exactPhysicsClaim).toBe(false);
    const blocked = evaluateScienceClaimGate(profile.formulas[5], "exact physical simulation");
    expect(blocked.gate).toBe("BLOCK");
    expect(blocked.downgraded).toBe(true);
  });
});
