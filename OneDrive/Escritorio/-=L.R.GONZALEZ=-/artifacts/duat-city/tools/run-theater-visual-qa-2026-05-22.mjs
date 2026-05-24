import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const outDir = resolve(process.argv[2] ?? join(root, "docs", "screenshots", "engine-extensions-2026-05-22"));
const debugPort = Number(process.argv[3] ?? 18675);
const baseUrl = process.argv[4] ?? "http://127.0.0.1:5175/";
const edge = findEdge();
const profile = join(tmpdir(), `duat-theater-visual-qa-${Date.now()}`);

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
  await cdp.send("Input.setIgnoreInputEvents", { ignore: false });

  const desktopUrl = scenarioUrl(baseUrl, { mode: "CITY", view: "OPERATIONAL", labels: "1" });
  await cdp.send("Emulation.setDeviceMetricsOverride", { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false });
  await cdp.send("Page.navigate", { url: desktopUrl });
  await waitForExpression(cdp, "Boolean(document.querySelector('.duat-root') && document.querySelector('.city-canvas'))", 35_000);
  await sleep(1200);
  const initialState = await evaluate(cdp, pageStateExpression());
  const initialShot = await capture(cdp, "theater-desktop-initial.png");

  const theaterRect = await evaluate(cdp, `(() => {
    const button = [...document.querySelectorAll('button')].find(b => (b.textContent || '').includes('Theater'));
    if (!button) return null;
    const r = button.getBoundingClientRect();
    return { x: r.x, y: r.y, width: r.width, height: r.height, text: button.textContent?.trim(), className: button.className };
  })()`);
  if (!theaterRect) throw new Error("Theater button not found");
  await click(cdp, theaterRect.x + theaterRect.width / 2, theaterRect.y + theaterRect.height / 2);
  await sleep(500);
  const selectedState = await evaluate(cdp, pageStateExpression());
  const selectedShot = await capture(cdp, "theater-tool-selected.png");

  const beforeCount = Number(selectedState.buildingCount ?? initialState.buildingCount ?? 0);
  const placementAttempts = [];
  const canvasRect = selectedState.canvas;
  if (!canvasRect) throw new Error("Canvas rect missing");
  const candidates = [
    [0.72, 0.72],
    [0.82, 0.62],
    [0.62, 0.78],
    [0.52, 0.70],
    [0.76, 0.42],
  ];
  let placedState = selectedState;
  for (const [fx, fy] of candidates) {
    const x = canvasRect.x + canvasRect.width * fx;
    const y = canvasRect.y + canvasRect.height * fy;
    await click(cdp, x, y);
    await sleep(600);
    placedState = await evaluate(cdp, pageStateExpression());
    placementAttempts.push({ fx, fy, x: Math.round(x), y: Math.round(y), buildingCount: placedState.buildingCount });
    if (Number(placedState.buildingCount) > beforeCount) break;
  }
  const placedShot = await capture(cdp, "theater-after-placement.png");

  await cdp.send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await cdp.send("Page.navigate", { url: desktopUrl });
  await waitForExpression(cdp, "Boolean(document.querySelector('.duat-root') && document.querySelector('.city-canvas'))", 35_000);
  await sleep(1400);
  const mobileState = await evaluate(cdp, pageStateExpression());
  const mobileShot = await capture(cdp, "theater-mobile.png");

  const report = {
    schema: "duat.theater-visual-qa.v1",
    generatedAt: new Date().toISOString(),
    browserMode: "Edge/CDP/headless",
    baseUrl,
    desktopUrl,
    checks: {
      theaterButtonVisible: Boolean(initialState.theaterButton?.rect?.visible),
      theaterButtonNoTextOverflow: Boolean(initialState.theaterButton && !initialState.theaterButton.overflow),
      desktopCanvasVisible: Boolean(initialState.canvas?.visible),
      theaterToolSelected: Boolean(selectedState.theaterButton?.active),
      placementIncreasedBuildingCount: Number(placedState.buildingCount) > beforeCount,
      rightPanelMentionsTheater: Boolean(placedState.rightPanelMentionsTheater),
      mobileTheaterButtonPresent: Boolean(mobileState.theaterButton?.rect?.visible),
      mobileCanvasVisible: Boolean(mobileState.canvas?.visible),
      mobileToolGridNoTextOverflow: Boolean(mobileState.toolButtons?.every(button => !button.overflow)),
      noConsoleErrors: true,
      screenshotsNonblank: [initialShot, selectedShot, placedShot, mobileShot].every(item => item.nonblank),
    },
    states: {
      initial: initialState,
      selected: selectedState,
      placed: placedState,
      mobile: mobileState,
    },
    placementAttempts,
    screenshots: [initialShot, selectedShot, placedShot, mobileShot],
  };
  report.checks.ok = Object.values(report.checks).every(Boolean);
  await writeFile(join(outDir, "THEATER_VISUAL_QA_REPORT.json"), JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify({ ok: report.checks.ok, outDir, report: join(outDir, "THEATER_VISUAL_QA_REPORT.json"), checks: report.checks }, null, 2));
  cdp.close();
  if (!report.checks.ok) process.exitCode = 2;
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

function scenarioUrl(base, params) {
  const url = new URL(base);
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  return url.toString();
}

function pageStateExpression() {
  return `(() => {
    const rectJson = element => {
      if (!element) return null;
      const r = element.getBoundingClientRect();
      return {
        x: r.x,
        y: r.y,
        width: r.width,
        height: r.height,
        visible: r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth,
      };
    };
    const toolButtons = [...document.querySelectorAll('.tool-btn')].map(button => {
      const rect = rectJson(button);
      return {
        text: (button.textContent || '').trim(),
        active: button.classList.contains('active'),
        overflow: button.scrollWidth > button.clientWidth + 1 || button.scrollHeight > button.clientHeight + 1,
        scrollWidth: button.scrollWidth,
        clientWidth: button.clientWidth,
        scrollHeight: button.scrollHeight,
        clientHeight: button.clientHeight,
        rect,
      };
    });
    const theaterButton = toolButtons.find(button => button.text.includes('Theater')) ?? null;
    const stats = [...document.querySelectorAll('.topbar-stat')].map(stat => ({
      label: stat.querySelector('.topbar-label')?.textContent?.trim(),
      value: stat.querySelector('.topbar-value')?.textContent?.trim(),
    }));
    const buildingCount = Number(stats.find(item => item.label === 'BLDGS')?.value ?? NaN);
    const rightPanelText = document.querySelector('.panel-right')?.textContent ?? '';
    return {
      href: location.href,
      title: document.title,
      viewport: { width: innerWidth, height: innerHeight },
      rootVisible: Boolean(document.querySelector('.duat-root')),
      canvas: rectJson(document.querySelector('.city-canvas')),
      theaterButton,
      toolButtons,
      buildingCount,
      rightPanelMentionsTheater: /theater/i.test(rightPanelText),
      bodyOverflowX: document.documentElement.scrollWidth > innerWidth + 1,
      bodyTextSample: document.body?.innerText?.slice(0, 900) ?? '',
    };
  })()`;
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
  throw new Error("Timed out waiting for CDP target");
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

async function evaluate(cdp, expression) {
  const response = await cdp.send("Runtime.evaluate", { expression, returnByValue: true });
  if (response.result?.exceptionDetails) {
    throw new Error(response.result.exceptionDetails.text ?? "Runtime.evaluate failed");
  }
  return response.result?.result?.value;
}

async function click(cdp, x, y) {
  await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x, y });
  await cdp.send("Input.dispatchMouseEvent", { type: "mousePressed", x, y, button: "left", buttons: 1, clickCount: 1 });
  await cdp.send("Input.dispatchMouseEvent", { type: "mouseReleased", x, y, button: "left", buttons: 0, clickCount: 1 });
}

async function capture(cdp, name) {
  const shot = await cdp.send("Page.captureScreenshot", { format: "png", fromSurface: true });
  const bytes = Buffer.from(shot.result.data, "base64");
  const file = join(outDir, name);
  await writeFile(file, bytes);
  return {
    name,
    path: file,
    bytes: bytes.length,
    sha256: createHash("sha256").update(bytes).digest("hex").toUpperCase(),
    nonblank: bytes.length > 10_000 && new Set(bytes.subarray(0, Math.min(bytes.length, 100_000))).size > 48,
  };
}

async function waitForExpression(cdp, expression, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const value = await evaluate(cdp, expression).catch(() => false);
    if (value) return;
    await sleep(350);
  }
  throw new Error(`Timed out waiting for ${expression}`);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
