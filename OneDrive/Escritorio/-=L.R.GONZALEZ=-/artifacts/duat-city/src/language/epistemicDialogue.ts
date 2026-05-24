import type { Gate } from "../core/types";
import type { EpistemicStatement, LanguageMetrics } from "./languageTypes";

const UNSUPPORTED_MARKERS = ["always", "guaranteed", "real physics", "scientifically proven", "omniscient"];

export function compileEpistemicStatement(statement: string, evidence: string[] = []): EpistemicStatement {
  const unsupportedClaims = countUnsupportedClaims(statement, evidence);
  const classification = evidence.length > 0
    ? "CERTEZA"
    : unsupportedClaims > 0
      ? "BLOQUEO"
      : statement.includes("?")
        ? "INCOGNITA"
        : "INFERENCIA";
  return {
    classification,
    text: sanitizeStatement(statement),
    evidence,
    unsupportedClaims,
    gate: gateFor(classification, unsupportedClaims),
  };
}

export function languageGate(statement: EpistemicStatement): EpistemicStatement {
  if (statement.unsupportedClaims > 0 || /real physics|science fact|path tracing/i.test(statement.text)) {
    return {
      ...statement,
      classification: "BLOQUEO",
      gate: "BLOCK",
      text: `${statement.text} [downgraded: unsupported public claim]`,
    };
  }
  return statement;
}

export function computeLanguageMetrics(statements: EpistemicStatement[]): LanguageMetrics {
  const total = Math.max(1, statements.length);
  const unsupported = statements.reduce((sum, item) => sum + item.unsupportedClaims, 0);
  const unknowns = statements.filter(item => item.classification === "INCOGNITA").length;
  const repeats = repetitionCount(statements.map(item => item.text));
  const blocked = statements.filter(item => item.gate === "BLOCK").length;
  const R_language = clamp01((unsupported + unknowns + repeats + blocked) / (total * 4));
  return {
    R_language,
    Phi_language: clamp01(1 - R_language + statements.filter(item => item.evidence.length > 0).length / (total * 6)),
    ambiguity: clamp01(unknowns / total),
    unsupported_claims: unsupported,
    repetition: clamp01(repeats / total),
    narrative_coherence: clamp01(1 - (unsupported + repeats) / (total * 3)),
  };
}

function countUnsupportedClaims(statement: string, evidence: string[]): number {
  const lower = statement.toLowerCase();
  const markerCount = UNSUPPORTED_MARKERS.filter(marker => lower.includes(marker)).length;
  return evidence.length > 0 ? Math.max(0, markerCount - 1) : markerCount;
}

function sanitizeStatement(statement: string): string {
  return statement.replace(/\s+/g, " ").trim().slice(0, 500);
}

function gateFor(classification: EpistemicStatement["classification"], unsupportedClaims: number): Gate {
  if (classification === "BLOQUEO" || unsupportedClaims > 0) return "BLOCK";
  if (classification === "INCOGNITA") return "REVIEW";
  return "APPROVE";
}

function repetitionCount(lines: string[]): number {
  const seen = new Set<string>();
  let repeats = 0;
  for (const line of lines.map(value => value.toLowerCase())) {
    if (seen.has(line)) repeats++;
    seen.add(line);
  }
  return repeats;
}

function clamp01(value: number): number {
  return Number(Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0)).toFixed(3));
}
