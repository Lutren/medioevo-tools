import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const outJson = resolve(process.argv[2] ?? join(root, "docs", "PERFORMANCE_BENCHMARK_v1_1.json"));
const outMd = resolve(process.argv[3] ?? join(root, "docs", "PERFORMANCE_BENCHMARK_REPORT_v1_1.md"));
const appUrl = process.argv[4] ?? "http://127.0.0.1:18519/duat-city/?benchmark=v1_1&durationMs=1200";
const debugPort = Number(process.argv[5] ?? 18521);
const edge = findEdge();
const profile = join(tmpdir(), `duat-v11-headed-benchmark-${Date.now()}`);

await mkdir(profile, { recursive: true });
await mkdir(dirname(outJson), { recursive: true });

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
  "--disable-gpu",
  "--new-window",
  "--window-size=1280,900",
  appUrl,
], { detached: false, stdio: "ignore" });

try {
  const target = await waitForTarget(debugPort, appUrl, 30_000);
  const result = await waitForBenchmark(target.webSocketDebuggerUrl, 180_000);
  await writeFile(outJson, JSON.stringify(result, null, 2), "utf8");
  await writeFile(outMd, renderReport(result, appUrl), "utf8");
  console.log(JSON.stringify({ ok: true, outJson, outMd, scenarios: result.scenarios.length, visibleBrowser: result.visibleBrowser }, null, 2));
} finally {
  if (!browser.killed) browser.kill();
  await sleep(1200);
  await rm(profile, { recursive: true, force: true }).catch(error => {
    console.warn(JSON.stringify({ cleanup_warning: error.message, profile }));
  });
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

async function waitForTarget(port, url, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const targets = await fetchJsonWithTimeout(`http://127.0.0.1:${port}/json`, 1500);
      const target = targets.find(item => item.type === "page" && String(item.url ?? "").startsWith(url.split("?")[0]));
      if (target?.webSocketDebuggerUrl) return target;
    } catch {
      // Browser is still booting.
    }
    await sleep(300);
  }
  throw new Error("Timed out waiting for Edge CDP page target");
}

async function fetchJsonWithTimeout(url, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await (await fetch(url, { signal: controller.signal })).json();
  } finally {
    clearTimeout(timer);
  }
}

async function waitForBenchmark(webSocketUrl, timeoutMs) {
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
  const send = method => new Promise(resolveMessage => {
    const messageId = ++id;
    pending.set(messageId, resolveMessage);
    ws.send(JSON.stringify({ id: messageId, method }));
  });
  const evalExpr = async expression => {
    const message = await send("Runtime.evaluate", {
      expression,
      returnByValue: true,
      awaitPromise: false,
    });
    return message.result?.result?.value;
  };
  const sendWithParams = (method, params) => new Promise(resolveMessage => {
    const messageId = ++id;
    pending.set(messageId, resolveMessage);
    ws.send(JSON.stringify({ id: messageId, method, params }));
  });
  const evalWithParams = async expression => {
    const message = await sendWithParams("Runtime.evaluate", {
      expression,
      returnByValue: true,
      awaitPromise: false,
    });
    return message.result?.result?.value;
  };
  const start = Date.now();
  let lastStatus = "";
  while (Date.now() - start < timeoutMs) {
    const status = await evalWithParams("window.__DUAT_V11_BENCHMARK_STATUS__ || 'booting'");
    if (status !== lastStatus) {
      console.log(JSON.stringify({ benchmark_status: status }));
      lastStatus = status;
    }
    if (status === "done") {
      const result = await evalWithParams("window.__DUAT_BENCHMARK_RESULT__");
      ws.close();
      return result;
    }
    if (String(status).startsWith("failed:")) throw new Error(status);
    await sleep(800);
  }
  ws.close();
  const href = await evalWithParams("location.href").catch(() => "unknown");
  const body = await evalWithParams("document.body ? document.body.innerText.slice(0, 800) : ''").catch(() => "");
  throw new Error(`Timed out waiting for benchmark result href=${href} body=${body}`);
}

function renderReport(result, appUrl) {
  const rows = result.scenarios.map(s => `| ${s.label} | ${s.qualityPreset} | ${s.avgFPS} | ${s.p95FrameMs} | ${s.minFPS} | ${s.maxFPS} | ${s.droppedFrames} | ${s.activeLightCells} | ${s.activeMaterialCells} | ${s.particles} | ${s.agents} | ${s.pixelFieldResolution} |`).join("\n");
  return `# PERFORMANCE BENCHMARK v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

Visible headed browser benchmark executed locally with Microsoft Edge and CDP automation. No MCP execution, cloud, external API, push, deploy or commit.

- URL: ${appUrl}
- Duration per scenario: ${result.durationMsPerScenario} ms
- Browser visible: ${result.visibleBrowser}
- Browser: ${result.browser}

| Scenario | Quality | avg FPS | p95 frame ms | min FPS | max FPS | dropped | active light cells | active material cells | particles | agents | pixel field |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
${rows}

## Notes

${result.notes.map(note => `- ${note}`).join("\n")}
`;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
