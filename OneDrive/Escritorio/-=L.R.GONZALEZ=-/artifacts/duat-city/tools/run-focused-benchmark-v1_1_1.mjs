import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const outJson = resolve(process.argv[2] ?? join(root, "docs", "PERFORMANCE_BENCHMARK_v1_1_1.json"));
const outMd = resolve(process.argv[3] ?? join(root, "docs", "PERFORMANCE_BENCHMARK_REPORT_v1_1_1.md"));
const appUrl = process.argv[4] ?? "http://127.0.0.1:18519/duat-city/?benchmark=v1_1_1&durationMs=10000&browserMode=CDP";
const debugPort = Number(process.argv[5] ?? 18531);
const edge = findEdge();
const profile = join(tmpdir(), `duat-v111-focused-benchmark-${Date.now()}`);

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
  "--new-window",
  "--window-size=1366,920",
  appUrl,
], { detached: false, stdio: "ignore" });

try {
  await sleep(1400);
  const focusAttempt = await focusEdgeWindow(browser.pid);
  const target = await waitForTarget(debugPort, appUrl, 30_000);
  const result = await waitForBenchmark(target.webSocketDebuggerUrl, 900_000);
  result.notes = [
    ...(result.notes ?? []),
    `Local focus attempt: ${focusAttempt}`,
    result.focusStatus === "focused" ? "Focused browser verified by document.hasFocus()." : "FOCUSED_BROWSER_NOT_AVAILABLE: automation could not guarantee active user focus.",
  ];
  await writeFile(outJson, JSON.stringify(result, null, 2), "utf8");
  await writeFile(outMd, renderReport(result, appUrl), "utf8");
  console.log(JSON.stringify({
    ok: true,
    outJson,
    outMd,
    scenarios: result.scenarios.length,
    browserMode: result.browserMode,
    focusStatus: result.focusStatus,
    focusedBrowserAvailable: result.focusedBrowserAvailable,
  }, null, 2));
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

async function focusEdgeWindow(pid) {
  const script = `
$shell = New-Object -ComObject WScript.Shell
Start-Sleep -Milliseconds 400
if ($shell.AppActivate(${Number(pid)})) { 'focused_by_pid' } else { 'focus_unconfirmed' }
`;
  try {
    const ps = spawn("powershell", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], { stdio: ["ignore", "pipe", "pipe"] });
    const output = await new Promise(resolve => {
      let stdout = "";
      let stderr = "";
      ps.stdout.on("data", chunk => { stdout += String(chunk); });
      ps.stderr.on("data", chunk => { stderr += String(chunk); });
      ps.on("close", code => resolve({ code, stdout: stdout.trim(), stderr: stderr.trim() }));
    });
    return output.stdout || output.stderr || `focus_exit_${output.code}`;
  } catch (error) {
    return `focus_error:${error instanceof Error ? error.message : String(error)}`;
  }
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
  const evalWithParams = async expression => {
    const messageId = ++id;
    const response = await new Promise(resolveMessage => {
      pending.set(messageId, resolveMessage);
      ws.send(JSON.stringify({
        id: messageId,
        method: "Runtime.evaluate",
        params: { expression, returnByValue: true, awaitPromise: false },
      }));
    });
    return response.result?.result?.value;
  };
  const start = Date.now();
  let lastStatus = "";
  while (Date.now() - start < timeoutMs) {
    const status = await evalWithParams("window.__DUAT_V111_BENCHMARK_STATUS__ || 'booting'");
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
  const body = await evalWithParams("document.body ? document.body.innerText.slice(0, 1000) : ''").catch(() => "");
  throw new Error(`Timed out waiting for v1.1.1 benchmark result href=${href} body=${body}`);
}

function renderReport(result, appUrl) {
  const rows = result.scenarios.map(s => `| ${s.label} | ${s.qualityPreset} | ${s.viewMode} | ${s.avgFps} | ${s.p95FrameMs} | ${s.p99FrameMs} | ${s.minFps} | ${s.maxFps} | ${s.droppedFrames} | ${s.activeLightCells} | ${s.activeMaterialCells} | ${s.particles} | ${s.agents} | ${s.browserMode} | ${s.focusStatus} |`).join("\n");
  return `# PERFORMANCE BENCHMARK v1.1.1

Fingerprint: DUAT-v1.1.1-FOCUSED-FPS-CLOSURE

Local focused/headed benchmark attempted with Microsoft Edge and CDP. No MCP execution, cloud, external API, push, deploy or commit.

- URL: ${appUrl}
- Duration per scenario: ${result.durationMsPerScenario} ms
- Browser mode: ${result.browserMode}
- Focus status: ${result.focusStatus}
- Focused browser available: ${result.focusedBrowserAvailable}
- Browser: ${result.browser}

| Scenario | Quality | View | avg FPS | p95 ms | p99 ms | min FPS | max FPS | dropped | active light cells | active material cells | particles | agents | browser mode | focus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
${rows}

## Notes

${result.notes.map(note => `- ${note}`).join("\n")}
`;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
