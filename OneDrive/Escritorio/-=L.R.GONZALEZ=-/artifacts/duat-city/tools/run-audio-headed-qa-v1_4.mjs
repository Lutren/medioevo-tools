import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const outJson = resolve(process.argv[2] ?? join(root, "docs", "AUDIO_HEADED_QA_v1_4.json"));
const outMd = resolve(process.argv[3] ?? join(root, "docs", "AUDIO_GAMEFEEL_QA_v1_4.md"));
const debugPort = Number(process.argv[4] ?? 18593);
const appUrl = process.argv[5] ?? "http://127.0.0.1:18519/duat-city/?mode=CITY&view=OPERATIONAL&sceneDemo=fire_smoke&vibe=warm_interior_tavern";
const requestedMode = process.argv[6] === "headless" ? "headless" : "headed";
const edge = findEdge();
const profile = join(tmpdir(), `duat-v14-audio-headed-${Date.now()}`);

await mkdir(dirname(outJson), { recursive: true });
await mkdir(profile, { recursive: true });

const browser = spawn(edge, [
  `--remote-debugging-port=${debugPort}`,
  `--user-data-dir=${profile}`,
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-background-networking",
  "--disable-renderer-backgrounding",
  "--disable-backgrounding-occluded-windows",
  "--disable-features=CalculateNativeWinOcclusion",
  "--disable-extensions",
  "--disable-sync",
  "--autoplay-policy=user-gesture-required",
  "--window-size=1366,920",
  ...(requestedMode === "headless" ? ["--headless=new", "--disable-gpu"] : ["--new-window"]),
  appUrl,
], { stdio: "ignore" });

try {
  await sleep(1400);
  const focusAttempt = await focusEdgeWindow(browser.pid);
  const target = await waitForTarget(debugPort, appUrl, 30_000);
  const cdp = await connect(target.webSocketDebuggerUrl);
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Input.setIgnoreInputEvents", { ignore: false }).catch(() => {});
  await waitForExpression(cdp, "Boolean(window.__DUAT_AUDIO_QA__)", 45_000);

  const before = await evalValue(cdp, "window.__DUAT_AUDIO_QA__");
  const enableStartedAt = performance.now();
  const enableClicked = await clickButtonByText(cdp, "Enable");
  await sleep(900);
  const afterEnable = await evalValue(cdp, "window.__DUAT_AUDIO_QA__");
  const previewStartedAt = performance.now();
  const previewClicked = await clickButtonByText(cdp, "Preview");
  await sleep(900);
  const afterPreview = await evalValue(cdp, "window.__DUAT_AUDIO_QA__");

  const result = {
    schema: "duat/audio-headed-qa/v1.4",
    fingerprint: "DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL",
    generatedAt: new Date().toISOString(),
    appUrl,
    browserMode: requestedMode === "headless" ? "Edge/CDP/headless-fallback" : "Edge/CDP/headed",
    focusAttempt,
    focusStatus: await evalValue(cdp, "document.hasFocus() ? 'focused' : (document.visibilityState === 'visible' ? 'unconfirmed' : 'not_available')").catch(() => "not_available"),
    audioOffByDefault: before?.enabled === false,
    browserAudioAvailable: Boolean(before?.browserAudioAvailable),
    enableClicked,
    previewClicked,
    afterEnable,
    afterPreview,
    enableLatencyMs: Number((performance.now() - enableStartedAt).toFixed(1)),
    previewLatencyMs: Number((performance.now() - previewStartedAt).toFixed(1)),
    proceduralPreviewConfirmed: String(afterPreview?.lastPreview ?? "").includes("previewed"),
    audibleConfirmedByHuman: false,
    notes: [
      `CDP dispatched ${requestedMode} mouse clicks to Enable and Preview.`,
      "Audio remains off by default before the local gesture.",
      "This verifies browser AudioContext/procedural preview state, not human-perceived audibility.",
      "No samples, cloud, Wabi execution, push, deploy or MCP execution were used.",
    ],
  };
  await writeFile(outJson, JSON.stringify(result, null, 2), "utf8");
  await writeFile(outMd, renderReport(result), "utf8");
  cdp.close();
  console.log(JSON.stringify({ ok: true, outJson, outMd, proceduralPreviewConfirmed: result.proceduralPreviewConfirmed, focusStatus: result.focusStatus }, null, 2));
} finally {
  if (!browser.killed) browser.kill();
  await sleep(1200);
  await rm(profile, { recursive: true, force: true }).catch(() => {});
}

function renderReport(result) {
  return `# Audio Game-Feel QA v1.4

Fingerprint: ${result.fingerprint}

Status:
- browser mode: ${result.browserMode}
- focus status: ${result.focusStatus}
- audio off by default: ${result.audioOffByDefault}
- browser audio available: ${result.browserAudioAvailable}
- enable clicked: ${result.enableClicked}
- preview clicked: ${result.previewClicked}
- procedural preview confirmed: ${result.proceduralPreviewConfirmed}
- audible confirmed by human: ${result.audibleConfirmedByHuman}
- enable latency estimate: ${result.enableLatencyMs} ms
- preview latency estimate: ${result.previewLatencyMs} ms

Boundary:
- no autoplay.
- no external samples.
- no cloud.
- no Wabi execution.
- CDP click QA does not prove human-perceived audio; manual owner confirmation remains required.

Last preview:
- ${result.afterPreview?.lastPreview ?? "unknown"}
`;
}

async function clickButtonByText(cdp, text) {
  const rect = await evalValue(cdp, `(() => {
    const buttons = Array.from(document.querySelectorAll('button'));
    const button = buttons.find(item => item.textContent && item.textContent.trim().includes(${JSON.stringify(text)}));
    if (!button) return null;
    button.scrollIntoView({ block: 'center', inline: 'center' });
    const r = button.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  })()`);
  if (!rect || !Number.isFinite(rect.x) || !Number.isFinite(rect.y)) return false;
  await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: rect.x, y: rect.y, button: "none" });
  await cdp.send("Input.dispatchMouseEvent", { type: "mousePressed", x: rect.x, y: rect.y, button: "left", clickCount: 1 });
  await cdp.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: rect.x, y: rect.y, button: "left", clickCount: 1 });
  return true;
}

function findEdge() {
  const candidates = ["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"];
  const found = candidates.find(path => existsSync(path));
  if (!found) throw new Error("Microsoft Edge executable not found");
  return found;
}

async function focusEdgeWindow(pid) {
  const script = `
$shell = New-Object -ComObject WScript.Shell
Start-Sleep -Milliseconds 500
if ($shell.AppActivate(${Number(pid)})) { 'focused_by_pid' } else { 'focus_unconfirmed' }
`;
  try {
    const ps = spawn("powershell", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], { stdio: ["ignore", "pipe", "pipe"] });
    return await new Promise(resolve => {
      let stdout = "";
      let stderr = "";
      ps.stdout.on("data", chunk => { stdout += String(chunk); });
      ps.stderr.on("data", chunk => { stderr += String(chunk); });
      ps.on("close", code => resolve(stdout.trim() || stderr.trim() || `focus_exit_${code}`));
    });
  } catch (error) {
    return `focus_error:${error instanceof Error ? error.message : String(error)}`;
  }
}

async function waitForTarget(port, url, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const target = targets.find(item => item.type === "page" && String(item.url ?? "").startsWith(url.split("?")[0]));
      if (target?.webSocketDebuggerUrl) return target;
    } catch {}
    await sleep(300);
  }
  throw new Error("Timed out waiting for browser target");
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

async function evalValue(cdp, expression) {
  const result = await cdp.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  return result.result?.result?.value;
}

async function waitForExpression(cdp, expression, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const value = await evalValue(cdp, expression).catch(() => false);
    if (value) return;
    await sleep(300);
  }
  throw new Error(`Timed out waiting for ${expression}`);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
