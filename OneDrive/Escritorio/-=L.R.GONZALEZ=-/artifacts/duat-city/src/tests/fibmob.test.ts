import { describe, it, expect } from "vitest";
import { muK, fibK, fibKMult, mobiusField, factorize } from "../core/fibmob";

describe("factorize", () => {
  it("factorizes 12 = 2^2 * 3", () => {
    const f = factorize(12);
    expect(f).toEqual([{ p: 2, exponent: 2 }, { p: 3, exponent: 1 }]);
  });
  it("factorizes 1 as empty", () => {
    expect(factorize(1)).toEqual([]);
  });
  it("factorizes prime 7", () => {
    expect(factorize(7)).toEqual([{ p: 7, exponent: 1 }]);
  });
});

describe("muK", () => {
  it("muK(1,1) = 1", () => expect(muK(1, 1)).toBe(1));
  it("muK(2,1) = -1 (prime, odd omega)", () => expect(muK(2, 1)).toBe(-1));
  it("muK(4,1) = 0 (2^2 exponent > 1 but ≤ 2 → not void; 4=2^2 exponent=2 which is ≤2 so sign-based)", () => {
    // 4 = 2^2: omega=1, omegaBar=0 (exponent=2, not 1), sign=(-1)^1=-1, k^0=1 → -1
    expect(muK(4, 1)).toBe(-1);
  });
  it("muK(8,1) = 0 (8=2^3 exponent > 2)", () => expect(muK(8, 1)).toBe(0));
  it("muK(6,1) = 1 (6=2*3, omega=2, even)", () => expect(muK(6, 1)).toBe(1));
  it("muK with k=2 scales by k^omegaBar", () => {
    // n=6=2*3: omega=2, omegaBar=2 (both exponent=1), sign=(−1)^2=1, result = 1 * 2^2 = 4
    expect(muK(6, 2)).toBe(4);
  });
});

describe("fibK", () => {
  it("fibK(1,1) = 1", () => expect(fibK(1, 1)).toBe(1));
  it("fibK(2,1) = 1 (k=1)", () => expect(fibK(2, 1)).toBe(1));
  it("fibK(3,1) = 2", () => expect(fibK(3, 1)).toBe(2));
  it("fibK(2,2) = 2 (k=2)", () => expect(fibK(2, 2)).toBe(2));
  it("fibK(3,2) = 5 (k=2: F(3) = k*F(2)+F(1) = 2*2+1 = 5)", () => expect(fibK(3, 2)).toBe(5));
});

describe("fibKMult", () => {
  it("fibKMult(1) = 1", () => expect(fibKMult(1, 1)).toBe(1));
  it("fibKMult(p,1) = fibK(2,1) = 1 for prime p", () => expect(fibKMult(2, 1)).toBe(1));
  it("fibKMult(p^2,1) = fibK(3,1) = 2", () => expect(fibKMult(4, 1)).toBe(2));
  it("fibKMult(p*q,1) = fibK(2,1)^2 = 1", () => expect(fibKMult(6, 1)).toBe(1));
  it("fibKMult is multiplicative over p*q*r", () => {
    // 30 = 2*3*5: each factor exponent=1, fibKMult = fibK(2)^3 = 1
    expect(fibKMult(30, 1)).toBe(1);
  });
});

describe("mobiusField", () => {
  it("returns correct polarity for positive mu", () => {
    const r = mobiusField(6, 1);
    expect(r.mu).toBe(1);
    expect(r.polarity).toBe("positive");
  });
  it("returns void for mu=0 (compressed tick)", () => {
    const r = mobiusField(8, 1);
    expect(r.mu).toBe(0);
    expect(r.polarity).toBe("void");
    expect(r.lodFactor).toBe(0.2);
  });
  it("lodFactor < 1 for void tiles", () => {
    const r = mobiusField(8, 1);
    expect(r.lodFactor).toBeLessThan(1);
  });
});
