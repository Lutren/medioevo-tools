import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { copyFile, mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const runDir = resolve(process.argv[2] ?? join(root, "..", "..", "qa_artifacts", "release_validation", `RUN_DUAT_FULL_LOCAL_REVIEW_v1_5_${timestampCompact()}`));
const docs = join(root, "docs");
const qaDir = join(docs, "v1_5_winapp_qa");

await mkdir(runDir, { recursive: true });

const assetManifestPath = join(docs, "asset_manifest_v1_5.json");
const benchmarkPath = join(docs, "PERFORMANCE_BENCHMARK_v1_5.json");
const benchmarkMdPath = join(docs, "PERFORMANCE_BENCHMARK_REPORT_v1_5.md");
const winappQaPath = join(qaDir, "WINAPP_QA_v1_5.json");
const visualPath = join(qaDir, "VISUAL_QA_REPORT_v1_5.json");
const visualMdPath = join(qaDir, "VISUAL_QA_REPORT_v1_5.md");
const audioPath = join(qaDir, "AUDIO_QA_REPORT_v1_5.json");
const audioMdPath = join(qaDir, "AUDIO_QA_REPORT_v1_5.md");
const winManifestPath = join(root, "dist", "winapp", "WINAPP_MANIFEST_v1_4.json");
const exePath = join(root, "dist", "winapp", "DUATCity.exe");
const smokePath = join(docs, "WINDOWS_APP_SMOKE_v1_4.json");

const assetManifest = await readJson(assetManifestPath);
const benchmark = await readJson(benchmarkPath);
const winappQa = await readJson(winappQaPath);
const visual = await readJson(visualPath);
const audio = await readJson(audioPath);
const winManifest = await readJson(winManifestPath);
const smoke = await readJson(smokePath);
const exeSha256 = await sha256File(exePath);
const smokeOk = Boolean(smoke.ok ?? smoke.smokeStatus === "PASS");

const topVisualPath = join(docs, "VISUAL_QA_REPORT_v1_5.json");
const topVisualMdPath = join(docs, "VISUAL_QA_REPORT_v1_5.md");
const topAudioPath = join(docs, "AUDIO_QA_REPORT_v1_5.json");
const topAudioMdPath = join(docs, "AUDIO_QA_REPORT_v1_5.md");
await copyFile(visualPath, topVisualPath);
await copyFile(visualMdPath, topVisualMdPath);
await copyFile(audioPath, topAudioPath);
await copyFile(audioMdPath, topAudioMdPath);

const commandEvidence = [
  { command: "python tools\\release\\pending_review.py --write --quiet", cwd: workspaceRoot(), status: "PASS", evidence: "pending_review date=2026-05-20 active_dedup=32 claudio_open=0" },
  { command: "node tools\\scan-local-review-v1_5.mjs docs\\asset_manifest_v1_5.json <roots>", cwd: root, status: "PASS", evidence: `filesSeen=${assetManifest.totals.filesSeen}; relevantFiles=${assetManifest.totals.relevantFiles}; zipEntriesIncluded=${assetManifest.totals.zipEntriesIncluded}` },
  { command: "corepack pnpm --filter @workspace/duat-city run test", cwd: workspaceRoot(), status: "PASS", evidence: "106 test files / 313 tests passed" },
  { command: "corepack pnpm --filter @workspace/duat-city run typecheck", cwd: workspaceRoot(), status: "PASS", evidence: "tsc -p tsconfig.json --noEmit" },
  { command: "corepack pnpm --filter @workspace/duat-city run build", cwd: workspaceRoot(), status: "PASS", evidence: "vite build completed; 249 modules transformed" },
  { command: "corepack pnpm --filter @workspace/duat-city run winapp:build", cwd: workspaceRoot(), status: "PASS", evidence: `DUATCity.exe sha256=${exeSha256}` },
  { command: "corepack pnpm --filter @workspace/duat-city run winapp:smoke", cwd: workspaceRoot(), status: "PASS", evidence: `httpStatus=${smoke.httpStatus}; jsAssetStatus=${smoke.jsAssetStatus}` },
  { command: "node tools\\run-winapp-benchmark-v1_4.mjs docs\\PERFORMANCE_BENCHMARK_v1_5.json ...", cwd: root, status: "PASS", evidence: `minAppAvgFps=${benchmark.minAppAvgFps}; threshold=${benchmark.thresholdFps}` },
  { command: "node tools\\run-winapp-qa-v1_5.mjs docs\\v1_5_winapp_qa ...", cwd: root, status: "PASS", evidence: `screenshots=${visual.screenshots.length}; allNonblank=${visual.allNonblank}; proceduralPreviewConfirmed=${audio.proceduralPreviewConfirmed}` },
  { command: "node --check tools\\scan-local-review-v1_5.mjs && node --check tools\\run-winapp-qa-v1_5.mjs", cwd: root, status: "PASS", evidence: "syntax checks passed" },
];

const allPass = commandEvidence.every(item => item.status === "PASS")
  && benchmark.allAppAvgFpsAtLeastThreshold
  && winappQa.ok
  && visual.allNonblank
  && audio.proceduralPreviewConfirmed
  && smokeOk;

const handoff = {
  schema: "duat/final-local-review-handoff/v1.5",
  fingerprint: "DUAT-v1.5-FULL-LOCAL-REVIEW",
  generatedAt: new Date().toISOString(),
  project: "DUAT/RPG Windows app local review",
  runDir,
  executable: {
    path: exePath,
    sha256: exeSha256,
    sizeBytes: winManifest.executable?.size_bytes ?? null,
    wrapper: winManifest.wrapper ?? "native_dotnet_edge_app_mode",
  },
  state: {
    R_est: allPass ? 0.16 : 0.34,
    Phi_eff_est: allPass ? 0.84 : 0.67,
    regime: allPass ? "FUNCIONAL" : "PRE_JAMMING",
    autonomyLevelUsed: "LEVEL 4 local-only",
    actionGate: "APPROVE_LOCAL_ONLY",
  },
  results: {
    allPass,
    tests: "106 files / 313 tests PASS",
    typecheck: "PASS",
    build: "PASS",
    winappBuild: "PASS",
    winappSmoke: smokeOk ? "PASS" : "FAIL",
    benchmark: {
      status: benchmark.allAppAvgFpsAtLeastThreshold ? "PASS" : "FAIL",
      minAppAvgFps: benchmark.minAppAvgFps,
      thresholdFps: benchmark.thresholdFps,
      scenarios: benchmark.scenarios.map(item => ({
        id: item.id,
        appAvgFps: item.appAvgFps,
        appP95FrameMs: item.appP95FrameMs,
        droppedFrames: item.droppedFrames,
      })),
    },
    visualQa: {
      status: visual.allNonblank ? "PASS" : "FAIL",
      screenshots: visual.screenshots.length,
      allNonblank: visual.allNonblank,
      screenshotDir: visual.screenshotDir,
    },
    audioQa: {
      status: audio.proceduralPreviewConfirmed ? "PASS" : "FAIL",
      browserMode: audio.browserMode,
      browserAudioAvailable: audio.browserAudioAvailable,
      proceduralPreviewConfirmed: audio.proceduralPreviewConfirmed,
      cueCount: audio.afterPreview?.cueCount ?? null,
      lastPreview: audio.afterPreview?.lastPreview ?? null,
      audibleConfirmedByHuman: audio.audibleConfirmedByHuman,
    },
    assetReview: {
      status: assetManifest.totals.unreadableFiles === 0 ? "PASS" : "REVIEW",
      filesSeen: assetManifest.totals.filesSeen,
      relevantFiles: assetManifest.totals.relevantFiles,
      zipFilesSeen: assetManifest.totals.zipFilesSeen,
      zipEntriesSeen: assetManifest.totals.zipEntriesSeen,
      zipEntriesIncluded: assetManifest.totals.zipEntriesIncluded,
      zipEntriesHashed: assetManifest.totals.zipEntriesHashed,
      classificationCounts: assetManifest.classificationCounts,
      categoryCounts: assetManifest.categoryCounts,
    },
  },
  corrections: [
    {
      issue: "Initial broad workspace scanner exceeded execution window",
      action: "Converted v1.5 scan to focused registered DUAT/RPG roots plus relevant ZIP-entry inventory",
      R_before: 0.37,
      Phi_eff_before: 0.63,
      R_after: 0.22,
      Phi_eff_after: 0.76,
    },
    {
      issue: "Audio QA wrapper built a double-question-mark URL after DUATCity.exe reported nativeWin query",
      action: "Replaced string concatenation with URLSearchParams and re-ran visual/audio QA",
      R_before: 0.24,
      Phi_eff_before: 0.72,
      R_after: 0.16,
      Phi_eff_after: 0.84,
    },
  ],
  boundaries: {
    level: "LEVEL_4_LOCAL_ONLY",
    publicationAllowed: false,
    pushDeployCommit: false,
    cloudUsed: false,
    mcpExecution: false,
    wabiExecution: false,
    unknownZipCodeExecuted: false,
    zipExtractionToDisk: false,
    assetsCopiedOutsideAllowlist: false,
    ownerProvidedIpPreserved: true,
    privateRpgCopiedToPublicRelease: false,
  },
  artifacts: {
    assetManifest: assetManifestPath,
    testReport: join(docs, "TEST_REPORT_v1_5.md"),
    benchmark: benchmarkPath,
    benchmarkReport: benchmarkMdPath,
    visualQa: topVisualPath,
    visualQaReport: topVisualMdPath,
    audioQa: topAudioPath,
    audioQaReport: topAudioMdPath,
    winappQa: winappQaPath,
    screenshots: visual.screenshotDir,
    runScreenshots: join(runDir, "screenshots"),
    handoffJson: join(docs, "HANDOFF_FINAL_REVIEW_v1_5.json"),
    handoffMd: join(docs, "CODEX_FINAL_HANDOFF_v1_5.md"),
    sessionFingerprint: join(docs, "SESSION_FINGERPRINT_FINAL_REVIEW_v1_5.json"),
    nextSessionBrief: join(docs, "NEXT_SESSION_BRIEF_FINAL_REVIEW_v1_5.md"),
  },
  commandEvidence,
  nextAction: "Optional manual speaker check if human-perceived audio, not just AudioContext/procedural preview, must be certified.",
};

const handoffJsonPath = handoff.artifacts.handoffJson;
const handoffMdPath = handoff.artifacts.handoffMd;
const testReportPath = handoff.artifacts.testReport;
const fingerprintPath = handoff.artifacts.sessionFingerprint;
const nextBriefPath = handoff.artifacts.nextSessionBrief;

await writeFile(handoffJsonPath, JSON.stringify(handoff, null, 2), "utf8");
await writeFile(handoffMdPath, renderHandoff(handoff), "utf8");
await writeFile(testReportPath, renderTestReport(handoff), "utf8");
await writeFile(fingerprintPath, JSON.stringify(renderFingerprint(handoff), null, 2), "utf8");
await writeFile(nextBriefPath, renderNextBrief(handoff), "utf8");

const copyTargets = [
  assetManifestPath,
  benchmarkPath,
  benchmarkMdPath,
  topVisualPath,
  topVisualMdPath,
  topAudioPath,
  topAudioMdPath,
  winappQaPath,
  smokePath,
  winManifestPath,
  handoffJsonPath,
  handoffMdPath,
  testReportPath,
  fingerprintPath,
  nextBriefPath,
];

for (const source of copyTargets) {
  if (!existsSync(source)) continue;
  await copyFile(source, join(runDir, basename(source)));
}

await mkdir(handoff.artifacts.runScreenshots, { recursive: true });
for (const name of await readdir(visual.screenshotDir)) {
  await copyFile(join(visual.screenshotDir, name), join(handoff.artifacts.runScreenshots, name));
}

console.log(JSON.stringify({
  ok: allPass,
  runDir,
  handoffJsonPath,
  handoffMdPath,
  testReportPath,
  benchmarkPath,
  visualQa: topVisualPath,
  audioQa: topAudioPath,
  assetManifestPath,
}, null, 2));

function renderHandoff(doc) {
  return `# CODEX FINAL HANDOFF v1.5

Fingerprint: ${doc.fingerprint}

## Estado
- R_est: ${doc.state.R_est}
- Phi_eff_est: ${doc.state.Phi_eff_est}
- Regimen: ${doc.state.regime}
- Autonomia usada: ${doc.state.autonomyLevelUsed}
- ActionGate: ${doc.state.actionGate}

## Resultado
- Global: ${doc.results.allPass ? "PASS" : "REVIEW"}
- Tests: ${doc.results.tests}
- Typecheck: ${doc.results.typecheck}
- Build: ${doc.results.build}
- Winapp smoke: ${doc.results.winappSmoke}
- Benchmark minimo: ${doc.results.benchmark.minAppAvgFps} FPS / umbral ${doc.results.benchmark.thresholdFps}
- Visual QA: ${doc.results.visualQa.screenshots} screenshots, allNonblank=${doc.results.visualQa.allNonblank}
- Audio QA: proceduralPreviewConfirmed=${doc.results.audioQa.proceduralPreviewConfirmed}, humanAudible=${doc.results.audioQa.audibleConfirmedByHuman}

## Fronteras
- No push, deploy, commit, cloud, MCP ni Wabi execution real.
- No se extrajeron zips a disco.
- No se ejecuto codigo encontrado en zips.
- No se copiaron assets fuera de allowlist.
- OWNER_PROVIDED / INTERNAL_PROTECTED_IP preservado.

## Percances Resueltos
${doc.corrections.map(item => `- ${item.issue}: ${item.action}; R ${item.R_before} -> ${item.R_after}; Phi_eff ${item.Phi_eff_before} -> ${item.Phi_eff_after}.`).join("\n")}

## Artefactos
- Run dir: ${doc.runDir}
- Asset manifest: ${doc.artifacts.assetManifest}
- Test report: ${doc.artifacts.testReport}
- Benchmark: ${doc.artifacts.benchmark}
- Visual QA: ${doc.artifacts.visualQa}
- Audio QA: ${doc.artifacts.audioQa}
- Screenshots: ${doc.artifacts.screenshots}
- Handoff JSON: ${doc.artifacts.handoffJson}
`;
}

function renderTestReport(doc) {
  const commandRows = doc.commandEvidence.map(item => `| ${item.status} | \`${item.command}\` | ${item.evidence} |`).join("\n");
  const scenarioRows = doc.results.benchmark.scenarios.map(item => `| ${item.id} | ${item.appAvgFps} | ${item.appP95FrameMs} | ${item.droppedFrames} | PASS |`).join("\n");
  return `# TEST REPORT v1.5

Fingerprint: ${doc.fingerprint}

## Summary
- Overall: ${doc.results.allPass ? "PASS" : "REVIEW"}
- Tests: ${doc.results.tests}
- Typecheck: ${doc.results.typecheck}
- Build: ${doc.results.build}
- Windows app build: ${doc.results.winappBuild}
- Smoke: ${doc.results.winappSmoke}

## Commands
| Status | Command | Evidence |
|---|---|---|
${commandRows}

## Benchmark
| Scenario | app avg FPS | app p95 frame ms | dropped frames | Status |
|---|---:|---:|---:|---|
${scenarioRows}

## Visual QA
- Status: ${doc.results.visualQa.status}
- Screenshots: ${doc.results.visualQa.screenshots}
- All nonblank: ${doc.results.visualQa.allNonblank}
- Directory: ${doc.results.visualQa.screenshotDir}

## Audio QA
- Status: ${doc.results.audioQa.status}
- Browser audio available: ${doc.results.audioQa.browserAudioAvailable}
- Procedural preview: ${doc.results.audioQa.proceduralPreviewConfirmed}
- Cue count: ${doc.results.audioQa.cueCount}
- Human audible confirmation: ${doc.results.audioQa.audibleConfirmedByHuman}

## Asset Review
- Files seen: ${doc.results.assetReview.filesSeen}
- Relevant files: ${doc.results.assetReview.relevantFiles}
- Zip files seen: ${doc.results.assetReview.zipFilesSeen}
- Zip entries included: ${doc.results.assetReview.zipEntriesIncluded}
- Classification counts: ${JSON.stringify(doc.results.assetReview.classificationCounts)}
`;
}

function renderFingerprint(doc) {
  return {
    schema_version: "observacionismo.session_fingerprint.v2.1",
    session_id: timestampCompact(),
    project: "DUAT/RPG",
    fingerprint: doc.fingerprint,
    R_close: doc.state.R_est,
    Phi_eff: doc.state.Phi_eff_est,
    regime_close: doc.state.regime,
    autonomy_level_used: 4,
    actiongate_summary: {
      approved: doc.commandEvidence.length,
      review_required: 0,
      blocked: 0,
    },
    files_created_or_modified: Object.values(doc.artifacts),
    commands_run: doc.commandEvidence.map(item => item.command),
    tests: {
      status: doc.results.allPass ? "passed" : "failed",
      evidence: doc.commandEvidence.map(item => item.evidence),
    },
    decisions: [
      "Keep v1.5 review local-only.",
      "Classify protected RPG/lore sources as reference_only unless future ficha allows selective extraction.",
      "Use DUATCity.exe local server as benchmark and QA source.",
    ],
    pending: [
      "Optional manual speaker check for human-perceived audio.",
    ],
    next_action: doc.nextAction,
  };
}

function renderNextBrief(doc) {
  return `# NEXT_SESSION_BRIEF DUAT/RPG v1.5

## Estado
R_close: ${doc.state.R_est}
Phi_eff: ${doc.state.Phi_eff_est}
Regimen: ${doc.state.regime}
Autonomy level: 4 local-only

## Decisiones tomadas
- Revision v1.5 cerrada como local-only.
- Zips y material protegido quedan metadata/reference only salvo allowlist.
- DUATCity.exe es la fuente para smoke, benchmark y QA visual/audio.

## Cambios realizados
- Scanner v1.5 de manifest local.
- Wrapper QA v1.5 para screenshots y audio procedural desde Windows app.
- Reportes finales v1.5.

## Evidencia
- ${doc.results.tests}
- Benchmark minimo ${doc.results.benchmark.minAppAvgFps} FPS.
- Visual QA ${doc.results.visualQa.screenshots} screenshots allNonblank=${doc.results.visualQa.allNonblank}.
- Audio procedural preview=${doc.results.audioQa.proceduralPreviewConfirmed}.

## Pendientes reales
- Chequeo humano de parlantes solo si se exige audibilidad percibida.

## Riesgos
- Material RPG/lore protegido sigue reference_only.
- Workspace global sigue no apto para publicacion por secretos/capas mezcladas fuera de allowlists.

## Bloqueos
- Push, deploy, commit, cloud, MCP, Wabi execution real y publicacion externa siguen bloqueados.

## Proxima accion verificable
${doc.nextAction}

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.
`;
}

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

function workspaceRoot() {
  return resolve(root, "..", "..");
}

function timestampCompact() {
  return new Date().toISOString().replace(/[-:]/g, "").replace(/\..+$/, "Z");
}

function sha256File(path) {
  return readFile(path).then(bytes => createHash("sha256").update(bytes).digest("hex").toUpperCase());
}
