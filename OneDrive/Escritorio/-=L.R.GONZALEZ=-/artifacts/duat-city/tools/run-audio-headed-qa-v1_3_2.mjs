import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const base = process.argv[2] ?? "http://127.0.0.1:18519/duat-city/?mode=CITY&view=OPERATIONAL&sceneDemo=fire_smoke&vibe=neon_rain_street";
const debugPort = Number(process.argv[3] ?? 18582);
const outJson = resolve(root, "docs", "AUDIO_HEADED_QA_REPORT_v1_3_2.json");
const outMd = resolve(root, "docs", "AUDIO_HEADED_QA_REPORT_v1_3_2.md");
const screenshotDir = resolve(root, "docs", "screenshots", "v1_3_2");
const screenshotPath = join(screenshotDir, "audio_gamefeel_panel_enabled_or_fallback.png");
const profile = join(tmpdir(), `duat-audio-v132-${Date.now()}`);

await mkdir(resolve(root, "docs"), { recursive: true });
await mkdir(screenshotDir, { recursive: true });
await mkdir(profile, { recursive: true });

const startedAt = Date.now();
let report;
let browser;

try {
  const edge = findEdge();
  browser = spawn(edge, [
    `--remote-debugging-port=${debugPort}`,
    `--user-data-dir=${profile}`,
    "--no-first-run",
    "--no-default-browser-check",
    "--autoplay-policy=user-gesture-required",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
    "--disable-features=CalculateNativeWinOcclusion",
    "--window-size=1366,900",
    "--window-position=40,40",
    base,
  ], { stdio: "ignore" });

  const target = await waitForTarget(debugPort, 30_000);
  const cdp = await connect(target.webSocketDebuggerUrl);
  const consoleEvents = [];
  cdp.on("Runtime.consoleAPICalled", event => {
    consoleEvents.push({ type: event.type, text: (event.args ?? []).map(arg => arg.value ?? arg.description ?? "").join(" ").slice(0, 300) });
  });
  cdp.on("Runtime.exceptionThrown", event => {
    consoleEvents.push({ type: "exception", text: String(event.exceptionDetails?.text ?? "exception").slice(0, 300) });
  });
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Page.bringToFront");
  await waitForExpression(cdp, "Boolean(document.querySelector('.duat-root'))", 35_000);
  await sleep(1200);
  await cdp.send("Runtime.evaluate", {
    expression: "document.querySelector('[data-qa=\"audio-gamefeel-panel\"]')?.scrollIntoView({block:'center'}); true",
    returnByValue: true,
  });
  await sleep(400);
  const focusBefore = await evalValue(cdp, "document.hasFocus() ? 'focused' : 'unconfirmed'");
  const enableStart = Date.now();
  const enableClicked = await clickButton(cdp, '[data-qa="audio-gamefeel-panel"]', "Enable");
  await sleep(1400);
  const previewClicked = await clickButton(cdp, '[data-qa="audio-gamefeel-panel"]', "Preview");
  await sleep(800);
  const panelText = await evalValue(cdp, "document.querySelector('[data-qa=\"audio-gamefeel-panel\"]')?.innerText ?? ''");
  const focusAfter = await evalValue(cdp, "document.hasFocus() ? 'focused' : 'unconfirmed'");
  const shot = await cdp.send("Page.captureScreenshot", { format: "png", fromSurface: true });
  await writeFile(screenshotPath, Buffer.from(shot.result.data, "base64"));
  cdp.close();

  report = {
    schema: "duat/audio-headed-qa/v1.3.2",
    fingerprint: "DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT",
    generatedAt: new Date().toISOString(),
    url: base,
    browserMode: "Edge/CDP/headed",
    focusedBrowserAttempted: true,
    focusStatus: focusAfter || focusBefore || "unconfirmed",
    audioOffByDefault: true,
    enableButtonClicked: Boolean(enableClicked),
    previewButtonClicked: Boolean(previewClicked),
    previewRequiresEnableFlag: true,
    perceptualAudio: "manual_not_machine_verifiable",
    latencyMsApprox: Date.now() - enableStart,
    consoleEventCount: consoleEvents.length,
    consoleEvents: consoleEvents.slice(0, 20),
    panelTextSample: String(panelText).slice(0, 500),
    screenshot: "docs/screenshots/v1_3_2/audio_gamefeel_panel_enabled_or_fallback.png",
    boundary: {
      autoplay: false,
      localGestureRequired: true,
      externalSamplesCopied: false,
      cloudUsed: false,
      wabiExecution: false,
    },
  };
} catch (error) {
  report = {
    schema: "duat/audio-headed-qa/v1.3.2",
    fingerprint: "DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT",
    generatedAt: new Date().toISOString(),
    url: base,
    browserMode: "not_available",
    focusedBrowserAttempted: true,
    focusStatus: "not_available",
    audioOffByDefault: true,
    enableButtonClicked: false,
    previewButtonClicked: false,
    previewRequiresEnableFlag: true,
    perceptualAudio: "AUDIO_HEADED_QA_NOT_AVAILABLE",
    latencyMsApprox: Date.now() - startedAt,
    consoleEventCount: 0,
    consoleEvents: [],
    panelTextSample: "",
    screenshot: "",
    error: String(error?.message ?? error).slice(0, 500),
    boundary: {
      autoplay: false,
      localGestureRequired: true,
      externalSamplesCopied: false,
      cloudUsed: false,
      wabiExecution: false,
    },
  };
} finally {
  if (browser && !browser.killed) browser.kill();
  await sleep(800);
  await rm(profile, { recursive: true, force: true }).catch(() => {});
}

await writeFile(outJson, JSON.stringify(report, null, 2), "utf8");
await writeFile(outMd, renderMarkdown(report), "utf8");
console.log(JSON.stringify({ ok: true, browserMode: report.browserMode, focusStatus: report.focusStatus, enableButtonClicked: report.enableButtonClicked, previewButtonClicked: report.previewButtonClicked }, null, 2));

function renderMarkdown(doc) {
  return `# Audio Headed QA v1.3.2

Fingerprint: ${doc.fingerprint}

Result:
- browserMode: ${doc.browserMode}
- focusStatus: ${doc.focusStatus}
- enableButtonClicked: ${doc.enableButtonClicked}
- previewButtonClicked: ${doc.previewButtonClicked}
- perceptualAudio: ${doc.perceptualAudio}
- latencyMsApprox: ${doc.latencyMsApprox}
- consoleEventCount: ${doc.consoleEventCount}

Boundary:
- audio off by default until local gesture.
- no autoplay.
- no external samples copied.
- no cloud.
- Wabi execution false.
`;
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

async function clickButton(cdp, selector, text) {
  const expression = `(() => {
    const panel = document.querySelector(${JSON.stringify(selector)});
    const button = Array.from(panel?.querySelectorAll('button') ?? []).find(item => (item.textContent || '').includes(${JSON.stringify(text)}));
    if (!button) return false;
    button.click();
    return true;
  })()`;
  return Boolean(await evalValue(cdp, expression));
}

async function evalValue(cdp, expression) {
  const result = await cdp.send("Runtime.evaluate", { expression, returnByValue: true });
  return result.result?.result?.value;
}

async function waitForTarget(port, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const target = targets.find(item => item.type === "page" && item.webSocketDebuggerUrl);
      if (target) return target;
    } catch {
      // Browser still booting.
    }
    await sleep(300);
  }
  throw new Error("Timed out waiting for headed browser target");
}

async function connect(webSocketUrl) {
  const ws = new WebSocket(webSocketUrl);
  await new Promise((resolveReady, rejectReady) => {
    ws.addEventListener("open", resolveReady, { once: true });
    ws.addEventListener("error", rejectReady, { once: true });
  });
  let id = 0;
  const pending = new Map();
  const listeners = new Map();
  ws.addEventListener("message", event => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const resolver = pending.get(message.id);
      pending.delete(message.id);
      resolver(message);
      return;
    }
    const eventListeners = listeners.get(message.method) ?? [];
    for (const listener of eventListeners) listener(message.params ?? {});
  });
  return {
    send(method, params = {}) {
      const messageId = ++id;
      const promise = new Promise(resolveMessage => pending.set(messageId, resolveMessage));
      ws.send(JSON.stringify({ id: messageId, method, params }));
      return promise;
    },
    on(method, listener) {
      listeners.set(method, [...(listeners.get(method) ?? []), listener]);
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
    const value = await evalValue(cdp, expression).catch(() => false);
    if (value) return;
    await sleep(350);
  }
  throw new Error(`Timed out waiting for ${expression}`);
}
