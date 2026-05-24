import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const outDir = resolve(process.argv[2] ?? join(root, "docs", "screenshots", "v1_4"));
const debugPort = Number(process.argv[3] ?? 18584);
const base = process.argv[4] ?? "http://127.0.0.1:18519/duat-city/";
const edge = findEdge();
const profile = join(tmpdir(), `duat-v14-screenshots-${Date.now()}`);

const shots = [
  ["canvas_fallback_operational.png", scenarioUrl(base, { mode: "CITY", view: "OPERATIONAL", vibe: "neon_rain_street", labels: "0" }), "document.querySelector('.city-canvas')?.scrollIntoView({block:'center'})"],
  ["iso3d_renderer_panel.png", scenarioUrl(base, { mode: "CITY", view: "OPERATIONAL", vibe: "neon_rain_street" }), "document.querySelector('[data-qa=\"iso-renderer-panel\"]')?.scrollIntoView({block:'center'})"],
  ["iso3d_billboards_preview.png", scenarioUrl(base, { mode: "CITY", view: "OPERATIONAL", vibe: "neon_rain_street" }), "document.querySelector('[data-qa=\"iso-mini-preview\"]')?.scrollIntoView({block:'center'})"],
  ["q_overlay_debug.png", scenarioUrl(base, { mode: "OSIT", view: "DEBUG", vibe: "archeopunk_city_night", labels: "0" }), "document.querySelector('.city-canvas')?.scrollIntoView({block:'center'})"],
  ["osit_formula_lab_panel.png", scenarioUrl(base, { mode: "OSIT", view: "DEBUG", vibe: "archeopunk_city_night" }), "document.querySelector('[data-qa=\"osit-integration-panel\"]')?.scrollIntoView({block:'center'})"],
  ["audio_gamefeel_panel.png", scenarioUrl(base, { mode: "CITY", view: "OPERATIONAL", sceneDemo: "fire_smoke", vibe: "warm_interior_tavern" }), "document.querySelector('[data-qa=\"audio-gamefeel-panel\"]')?.scrollIntoView({block:'center'})"],
  ["agent_life_panel.png", scenarioUrl(base, { mode: "AGENT", view: "OPERATIONAL", vibe: "neon_rain_street" }), "document.querySelector('[data-qa=\"agent-life-dashboard\"]')?.scrollIntoView({block:'center'})"],
  ["vermeer_light_panel.png", scenarioUrl(base, { mode: "CITY", view: "BEAUTIFUL", vibe: "warm_interior_tavern", cinematic: "1" }), "document.querySelector('[data-qa=\"vermeer-lighting-panel\"]')?.scrollIntoView({block:'center'})"],
];

await mkdir(outDir, { recursive: true });
await mkdir(profile, { recursive: true });
const browser = spawn(edge, [
  `--remote-debugging-port=${debugPort}`,
  `--user-data-dir=${profile}`,
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-background-networking",
  "--disable-background-timer-throttling",
  "--disable-renderer-backgrounding",
  "--disable-backgrounding-occluded-windows",
  "--disable-features=CalculateNativeWinOcclusion",
  "--disable-extensions",
  "--disable-sync",
  "--headless=new",
  "--disable-gpu",
  "--window-size=1366,900",
  "about:blank",
], { stdio: "ignore" });

try {
  const target = await waitForTarget(debugPort, 30_000);
  const cdp = await connect(target.webSocketDebuggerUrl);
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false });
  const results = [];
  for (const [name, url, expression] of shots) {
    await cdp.send("Page.navigate", { url });
    await waitForExpression(cdp, "Boolean(document.querySelector('.duat-root'))", 35_000);
    await sleep(1500);
    await cdp.send("Runtime.evaluate", { expression, returnByValue: true });
    await sleep(500);
    const shot = await cdp.send("Page.captureScreenshot", { format: "png", fromSurface: true });
    const bytes = Buffer.from(shot.result.data, "base64");
    await writeFile(join(outDir, name), bytes);
    results.push({ name, bytes: bytes.length, url });
    console.log(JSON.stringify({ captured: name, bytes: bytes.length }));
  }
  await writeFile(join(outDir, "SCREENSHOT_CAPTURE_REPORT.json"), JSON.stringify({
    schema: "duat.screenshot_capture.v1_4",
    fingerprint: "DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL",
    browserMode: "Edge/CDP/headless",
    generatedAt: new Date().toISOString(),
    shots: results,
  }, null, 2), "utf8");
  cdp.close();
  console.log(JSON.stringify({ ok: true, shots: results.length, outDir }, null, 2));
} finally {
  if (!browser.killed) browser.kill();
  await sleep(800);
  await rm(profile, { recursive: true, force: true }).catch(() => {});
}

function findEdge() {
  const candidates = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  ];
  const found = candidates.find(path => existsSync(path));
  if (!found) throw new Error("Microsoft Edge executable not found");
  return found;
}

function scenarioUrl(baseUrl, params) {
  const url = new URL(baseUrl);
  url.searchParams.set("nativeWin", "1");
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  return url.toString();
}

async function waitForTarget(port, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const target = targets.find(item => item.type === "page" && item.webSocketDebuggerUrl);
      if (target) return target;
    } catch {}
    await sleep(300);
  }
  throw new Error("Timed out waiting for screenshot target");
}

async function connect(webSocketUrl) {
  const ws = new WebSocket(webSocketUrl);
  await new Promise((resolveReady, rejectReady) => {
    ws.addEventListener("open", resolveReady, { once: true });
    ws.addEventListener("error", rejectReady, { once: true });
  });
  let id = 0;
  const pending = new Map();
  ws.addEventListener("message", event => {
    const message = JSON.parse(event.data);
    const resolver = pending.get(message.id);
    if (resolver) {
      pending.delete(message.id);
      resolver(message);
    }
  });
  return {
    send(method, params = {}) {
      const messageId = ++id;
      const promise = new Promise(resolveMessage => pending.set(messageId, resolveMessage));
      ws.send(JSON.stringify({ id: messageId, method, params }));
      return promise;
    },
    close() { ws.close(); },
  };
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForExpression(cdp, expression, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const value = await cdp.send("Runtime.evaluate", { expression, returnByValue: true }).then(message => message.result?.result?.value).catch(() => false);
    if (value) return;
    await sleep(350);
  }
  throw new Error(`Timed out waiting for ${expression}`);
}
