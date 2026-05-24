import { describe, expect, it } from "vitest";
import { exportRPGWorld } from "../rpg/worldExport";
import { createCity } from "../sim/city";

describe("RPG OSIT formula integration v1.4", () => {
  it("exports formula profile without public science claim leakage", () => {
    const world = exportRPGWorld(createCity());
    const profile = world.osit_formula_profile as any;
    expect(profile.schema).toBe("duat/osit-formula-profile/v1.4");
    expect(profile.formulaCount).toBe(10);
    expect(profile.boundary.publicPhysicsClaimAllowed).toBe(false);
    expect(profile.boundary.exactPhysicsClaim).toBe(false);
    expect(profile.modules.ActionGate).toContain("black_scholes_risk_proxy");
  });
});
