import type { CodeCandidateRecord, ZipEntryRecord } from "./forensicTypes";

export function toCodeCandidate(record: ZipEntryRecord): CodeCandidateRecord | null {
  const ext = record.extension.toLowerCase();
  const language: CodeCandidateRecord["language"] =
    ext === "ts" || ext === "tsx" ? "typescript" :
      ext === "js" || ext === "jsx" || ext === "mjs" || ext === "cjs" ? "javascript" :
        ext === "json" ? "json" :
          ext === "md" ? "markdown" :
            ext === "css" ? "css" :
              ext === "html" ? "html" : "unknown";
  if (language === "unknown") return null;
  return {
    ...record,
    language,
    exports_hint: inferExports(record.path_original),
    safe_to_execute: false,
  };
}

export function scanCodeCandidates(records: ZipEntryRecord[]): CodeCandidateRecord[] {
  return records.map(toCodeCandidate).filter((value): value is CodeCandidateRecord => Boolean(value));
}

function inferExports(path: string): string[] {
  const p = path.toLowerCase();
  const hints = [
    ["audio", "audio adapter"],
    ["worklet", "audio worklet"],
    ["light", "light engine"],
    ["physics", "physics field"],
    ["brain", "brain runtime"],
    ["cortex", "language or social cortex"],
    ["gate", "gate policy"],
    ["handoff", "handoff persistence"],
  ] as const;
  return hints.filter(([needle]) => p.includes(needle)).map(([, label]) => label);
}
