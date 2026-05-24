import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const outDir = resolve(process.argv[2] ?? join(root, "docs", "screenshots", "v1_3_1"));
const debugPort = Number(process.argv[3] ?? 18571);
const base = process.argv[4] ?? "http://127.0.0.1:18519/duat-city/";
const edge = findEdge();
const profile = join(tmpdir(), `duat-v131-screenshots-${Date.now()}`);

const shots = [
  ["audio_gamefeel_panel_off.png", `${base}?mode=CITY&view=OPERATIONAL&sceneDemo=fire_smoke&vibe=neon_rain_street`, "document.querySelector('.panel-left')?.scrollTo(0, 1420)"],
  ["audio_gamefeel_neon_rain_cues.png", `${base}?mode=CITY&view=OPERATIONAL&sceneDemo=material_placement&vibe=neon_rain_street`, "document.querySelector('.panel-left')?.scrollTo(0, 1420)"],
  ["agent_life_relationship_graph.png", `${base}?mode=AGENT&view=OPERATIONAL&vibe=neon_rain_street`, ""],
  ["fire_smoke_gamefeel.png", `${base}?mode=CITY&view=OPERATIONAL&sceneDemo=fire_smoke&vibe=warm_interior_tavern`, "document.querySelector('.panel-left')?.scrollTo(0, 1420)"],
  ["brain_runtime_audio_system.png", `${base}?mode=CITY&view=OPERATIONAL&vibe=archeopunk_city_night`, ""],
  ["rpg_mode_audio_export_ready.png", `${base}?mode=RPG&view=OPERATIONAL&sceneDemo=material_placement&vibe=neon_rain_street`, ""],
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
    await sleep(2200);
    if (expression) {
      await cdp.send("Runtime.evaluate", { expression, returnByValue: true });
      await sleep(700);
    }
    const shot = await withTimeout(cdp.send("Page.captureScreenshot", { format: "png", fromSurface: true }), 20_000, `capture timeout ${name}`);
    const outPath = join(outDir, name);
    await writeFile(outPath, Buffer.from(shot.result.data, "base64"));
    results.push({ name, url, bytes: Buffer.byteLength(shot.result.data, "base64") });
    console.log(JSON.stringify({ captured: name, bytes: results.at(-1).bytes }));
  }
  await writeFile(join(outDir, "SCREENSHOT_CAPTURE_REPORT.json"), JSON.stringify({
    schema: "duat.screenshot_capture.v1_3_1",
    generatedAt: new Date().toISOString(),
    browserMode: "Edge/CDP/headless",
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

async function waitForExpression(cdp, expression, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const value = await cdp.send("Runtime.evaluate", { expression, returnByValue: true }).then(message => message.result?.result?.value).catch(() => false);
    if (value) return;
    await sleep(350);
  }
  const debug = await cdp.send("Runtime.evaluate", {
    expression: "document.body ? document.body.innerText.slice(0, 500) : ''",
    returnByValue: true,
  }).then(message => message.result?.result?.value).catch(() => "");
  throw new Error(`Timed out waiting for ${expression}; body=${debug}`);
}
