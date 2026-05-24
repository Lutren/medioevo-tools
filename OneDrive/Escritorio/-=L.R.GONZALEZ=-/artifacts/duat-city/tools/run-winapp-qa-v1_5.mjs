import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const exe = resolve(root, "dist", "winapp", "DUATCity.exe");
const outDir = resolve(process.argv[2] ?? join(root, "docs", "v1_5_winapp_qa"));
const port = Number(process.argv[3] ?? 18652);
const debugBase = Number(process.argv[4] ?? 18660);

if (!existsSync(exe)) throw new Error(`Windows app executable missing: ${exe}`);
await mkdir(outDir, { recursive: true });

const server = spawn(exe, ["--serve-only", "--port", String(port), "--duration-ms", "240000"], { stdio: ["ignore", "pipe", "pipe"] });
const steps = [];

try {
  const base = await waitForUrl(server, 12_000);
  const screenshotDir = join(outDir, "screenshots");
  const audioJson = join(outDir, "AUDIO_QA_REPORT_v1_5.json");
  const audioMd = join(outDir, "AUDIO_QA_REPORT_v1_5.md");
  const visualJson = join(outDir, "VISUAL_QA_REPORT_v1_5.json");
  const visualMd = join(outDir, "VISUAL_QA_REPORT_v1_5.md");

  steps.push(await runNode("screenshots", [
    join(root, "tools", "capture-screenshots-v1_4.mjs"),
    screenshotDir,
    String(debugBase),
    base,
  ]));
  steps.push(await runNode("audio_headless", [
    join(root, "tools", "run-audio-headed-qa-v1_4.mjs"),
    audioJson,
    audioMd,
    String(debugBase + 1),
    withParams(base, { mode: "CITY", view: "OPERATIONAL", sceneDemo: "fire_smoke", vibe: "warm_interior_tavern" }),
    "headless",
  ]));

  const visual = await analyzeScreenshots(screenshotDir);
  await writeFile(visualJson, JSON.stringify(visual, null, 2), "utf8");
  await writeFile(visualMd, renderVisualReport(visual), "utf8");
  const audio = JSON.parse(await readFile(audioJson, "utf8"));
  const result = {
    schema: "duat/winapp-qa/v1.5",
    fingerprint: "DUAT-v1.5-FULL-LOCAL-REVIEW",
    generatedAt: new Date().toISOString(),
    baseUrl: base,
    outDir,
    steps,
    visual: {
      json: visualJson,
      markdown: visualMd,
      screenshotDir,
      screenshotCount: visual.screenshots.length,
      allNonblank: visual.allNonblank,
    },
    audio: {
      json: audioJson,
      markdown: audioMd,
      proceduralPreviewConfirmed: Boolean(audio.proceduralPreviewConfirmed),
      browserAudioAvailable: Boolean(audio.browserAudioAvailable),
      audibleConfirmedByHuman: Boolean(audio.audibleConfirmedByHuman),
      focusStatus: audio.focusStatus,
    },
    ok: steps.every(step => step.code === 0) && visual.allNonblank && Boolean(audio.proceduralPreviewConfirmed),
    boundary: {
      cloudUsed: false,
      mcpExecution: false,
      wabiExecution: false,
      pushDeployCommit: false,
      screenshotsOnly: true,
    },
  };
  const resultPath = join(outDir, "WINAPP_QA_v1_5.json");
  await writeFile(resultPath, JSON.stringify(result, null, 2), "utf8");
  console.log(JSON.stringify({ ok: result.ok, resultPath, screenshotDir, audioJson, visualJson }, null, 2));
  if (!result.ok) process.exitCode = 2;
} finally {
  if (!server.killed) server.kill();
}

function withParams(baseUrl, params) {
  const url = new URL(baseUrl);
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  return url.toString();
}

async function runNode(label, args) {
  const child = spawn(process.execPath, args, { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", chunk => { stdout += String(chunk); });
  child.stderr.on("data", chunk => { stderr += String(chunk); });
  const code = await new Promise(resolve => child.on("close", resolve));
  if (stdout.trim()) process.stdout.write(stdout);
  if (stderr.trim()) process.stderr.write(stderr);
  return { label, code, stdoutTail: tail(stdout), stderrTail: tail(stderr) };
}

function tail(value) {
  return String(value).split(/\r?\n/).filter(Boolean).slice(-12).join("\n");
}

function waitForUrl(child, timeoutMs) {
  return new Promise((resolveReady, rejectReady) => {
    let output = "";
    const timer = setTimeout(() => rejectReady(new Error("Timed out waiting for DUAT_WINAPP_URL")), timeoutMs);
    child.stdout.on("data", chunk => {
      output += String(chunk);
      const match = output.match(/DUAT_WINAPP_URL=(.+)/);
      if (match) {
        clearTimeout(timer);
        resolveReady(match[1].trim());
      }
    });
    child.stderr.on("data", chunk => { output += String(chunk); });
    child.on("exit", code => {
      if (!output.includes("DUAT_WINAPP_URL=")) {
        clearTimeout(timer);
        rejectReady(new Error(`launcher exited before URL, code=${code}, output=${output}`));
      }
    });
  });
}

async function analyzeScreenshots(screenshotDir) {
  const names = [
    "canvas_fallback_operational.png",
    "iso3d_renderer_panel.png",
    "iso3d_billboards_preview.png",
    "q_overlay_debug.png",
    "osit_formula_lab_panel.png",
    "audio_gamefeel_panel.png",
    "agent_life_panel.png",
    "vermeer_light_panel.png",
  ];
  const screenshots = [];
  for (const name of names) {
    const file = join(screenshotDir, name);
    const bytes = await readFile(file);
    const png = parsePng(bytes);
    const uniqueSampleBytes = new Set(bytes.subarray(0, Math.min(bytes.length, 100_000))).size;
    screenshots.push({
      name,
      path: file,
      bytes: bytes.length,
      sha256: await sha256Buffer(bytes),
      width: png.width,
      height: png.height,
      validPng: png.valid,
      uniqueSampleBytes,
      nonblank: png.valid && bytes.length > 10_000 && uniqueSampleBytes > 48,
    });
  }
  return {
    schema: "duat/visual-qa/v1.5",
    fingerprint: "DUAT-v1.5-FULL-LOCAL-REVIEW",
    generatedAt: new Date().toISOString(),
    screenshotDir,
    screenshots,
    allNonblank: screenshots.every(item => item.nonblank),
    notes: [
      "Visual QA checks PNG integrity, dimensions, byte entropy and required panel coverage.",
      "Screenshots were captured from DUATCity.exe local server through Edge/CDP.",
    ],
  };
}

function parsePng(bytes) {
  const valid = bytes.length > 24
    && bytes[0] === 0x89
    && bytes[1] === 0x50
    && bytes[2] === 0x4e
    && bytes[3] === 0x47;
  return {
    valid,
    width: valid ? bytes.readUInt32BE(16) : 0,
    height: valid ? bytes.readUInt32BE(20) : 0,
  };
}

async function sha256Buffer(bytes) {
  const { createHash } = await import("node:crypto");
  return createHash("sha256").update(bytes).digest("hex").toUpperCase();
}

function renderVisualReport(visual) {
  const rows = visual.screenshots.map(item => `| ${item.name} | ${item.width}x${item.height} | ${item.bytes} | ${item.nonblank ? "PASS" : "REVIEW"} | ${item.sha256} |`).join("\n");
  return `# Visual QA Report v1.5

Fingerprint: ${visual.fingerprint}

All screenshots nonblank: ${visual.allNonblank}

| Screenshot | Dimensions | Bytes | Status | SHA256 |
|---|---:|---:|---|---|
${rows}

Notes:
${visual.notes.map(note => `- ${note}`).join("\n")}
`;
}
