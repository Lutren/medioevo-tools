import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const outDir = resolve(process.argv[2] ?? join(root, "docs", "screenshots", "v1_2"));
const debugPort = Number(process.argv[3] ?? 18561);
const base = process.argv[4] ?? "http://127.0.0.1:18519/duat-city/";
const edge = findEdge();
const profile = join(tmpdir(), `duat-v12-screenshots-${Date.now()}`);

const shots = [
  ["forbidden_archive_asset_style.png", `${base}?mode=CITY&view=BEAUTIFUL&vibe=warm_interior_tavern`],
  ["central_forge_fire_light.png", `${base}?mode=CITY&view=BEAUTIFUL&sceneDemo=fire_smoke&vibe=warm_interior_tavern`],
  ["biomechanical_garden_water_light.png", `${base}?mode=CITY&view=BEAUTIFUL&sceneDemo=water_reflection&vibe=jungle_waterfall_ruin`],
  ["underground_market_neon_smoke.png", `${base}?mode=CITY&view=BEAUTIFUL&sceneDemo=fire_smoke&vibe=neon_rain_street`],
  ["wet_isometric_city_tiles.png", `${base}?mode=CITY&view=OPERATIONAL&vibe=neon_rain_street`],
  ["duat_ui_asset_atlas.png", `${base}?mode=OSIT&view=OPERATIONAL&vibe=neon_rain_street`],
  ["procedural_vs_asset_comparison.png", `${base}?mode=CITY&view=OPERATIONAL&vibe=archeopunk_city_night`],
  ["vibe_authoring_panel.png", `${base}?mode=CITY&view=OPERATIONAL&vibe=neon_rain_street`],
  ["pixel_physics_material_demo.png", `${base}?mode=CITY&view=OPERATIONAL&sceneDemo=material_placement&vibe=neon_rain_street`],
  ["beautiful_mode_final.png", `${base}?mode=CITY&view=BEAUTIFUL&cinematic=1&vibe=neon_rain_street`],
  ["debug_layers_final.png", `${base}?mode=OSIT&view=DEBUG&sceneDemo=material_placement&vibe=neon_rain_street`],
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
  await cdp.send("Emulation.setDeviceMetricsOverride", { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false });
  const results = [];
  for (const [name, url] of shots) {
    await cdp.send("Page.navigate", { url });
    await sleep(6500);
    const shot = await withTimeout(cdp.send("Page.captureScreenshot", { format: "png", fromSurface: true }), 20_000, `capture timeout ${name}`);
    const outPath = join(outDir, name);
    await writeFile(outPath, Buffer.from(shot.result.data, "base64"));
    results.push({ name, url, bytes: Buffer.byteLength(shot.result.data, "base64") });
    console.log(JSON.stringify({ captured: name, bytes: results.at(-1).bytes }));
  }
  await writeFile(join(outDir, "SCREENSHOT_CAPTURE_REPORT.json"), JSON.stringify({
    schema: "duat.screenshot_capture.v1_2",
    generatedAt: new Date().toISOString(),
    browserMode: "Edge/CDP",
    shots: results,
  }, null, 2), "utf8");
  cdp.close();
  console.log(JSON.stringify({ ok: true, outDir, shots: results.length }, null, 2));
} finally {
  if (!browser.killed) browser.kill();
  await sleep(1200);
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

async function waitForTarget(port, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const target = targets.find(item => item.type === "page" && item.webSocketDebuggerUrl);
      if (target) return target;
    } catch {
      // Browser is still booting.
    }
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

function withTimeout(promise, timeoutMs, label) {
  let timer;
  return Promise.race([
    promise.finally(() => clearTimeout(timer)),
    new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error(label)), timeoutMs);
    }),
  ]);
}
