import { mkdir, rm, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const exe = resolve(root, "dist", "winapp", "DUATCity.exe");
const outJson = resolve(process.argv[2] ?? join(root, "docs", "PERFORMANCE_BENCHMARK_WINAPP_v1_4.json"));
const outMd = resolve(process.argv[3] ?? join(root, "docs", "PERFORMANCE_BENCHMARK_WINAPP_REPORT_v1_4.md"));
const port = Number(process.argv[4] ?? 18642);
const debugPort = Number(process.argv[5] ?? 18643);
const edge = findEdge();
const profile = join(tmpdir(), `duat-winapp-benchmark-${Date.now()}`);

if (!existsSync(exe)) throw new Error(`Windows app executable missing: ${exe}`);
await mkdir(dirname(outJson), { recursive: true });
await mkdir(profile, { recursive: true });

const server = spawn(exe, ["--serve-only", "--port", String(port), "--duration-ms", "120000"], { stdio: ["ignore", "pipe", "pipe"] });

try {
  const base = await waitForUrl(server, 8000);
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
    "--autoplay-policy=user-gesture-required",
    "--window-size=1366,900",
    "--new-window",
    "about:blank",
  ], { stdio: "ignore" });

  let cdp;
  try {
    await sleep(1200);
    const focusAttempt = await focusEdgeWindow(browser.pid);
    const target = await waitForTarget(debugPort, 30_000);
    cdp = await connect(target.webSocketDebuggerUrl);
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");
    const scenarios = [
      { id: "winapp_high_iso3d_operational", url: scenarioUrl(base, { mode: "CITY", view: "OPERATIONAL", vibe: "neon_rain_street" }) },
      { id: "winapp_beautiful_vermeer_city", url: scenarioUrl(base, { mode: "CITY", view: "BEAUTIFUL", vibe: "warm_interior_tavern" }) },
      { id: "winapp_debug_osit_formula_lab", url: scenarioUrl(base, { mode: "OSIT", view: "DEBUG", vibe: "archeopunk_city_night" }) },
    ];
    const results = [];
    for (const scenario of scenarios) {
      console.log(JSON.stringify({ scenario: scenario.id, status: "start" }));
      await cdp.send("Page.navigate", { url: scenario.url });
      await waitForExpression(cdp, "Boolean(document.querySelector('.duat-root'))", 35_000);
      await waitForExpression(cdp, "Boolean(window.__DUAT_PERF_SNAPSHOT__)", 35_000);
      await sleep(6000);
      await evalValue(cdp, "typeof window.__DUAT_RESET_FPS__ === 'function' ? (window.__DUAT_RESET_FPS__(), true) : false").catch(() => false);
      await sleep(500);
      const sampleRaw = await evalValue(cdp, `(() => new Promise(resolve => {
        const durationMs = 5000;
        const deltas = [];
        let last = performance.now();
        const start = last;
        function step(now) {
          deltas.push(now - last);
          last = now;
          if (now - start < durationMs) requestAnimationFrame(step);
          else {
            const sorted = deltas.slice(1).sort((a,b) => a-b);
            const avg = sorted.reduce((s,v)=>s+v,0) / Math.max(1, sorted.length);
            const p95 = sorted[Math.floor(sorted.length * 0.95)] || avg;
            const min = Math.max(...sorted);
            const max = Math.min(...sorted);
            resolve(JSON.stringify({
              avgFps: Number((1000 / avg).toFixed(2)),
              minFps: Number((1000 / min).toFixed(2)),
              maxFps: Number((1000 / max).toFixed(2)),
              p95FrameMs: Number(p95.toFixed(2)),
              droppedFrames: sorted.filter(v => v > 33.34).length,
              frames: sorted.length,
              focusStatus: document.hasFocus() ? 'focused' : (document.visibilityState === 'visible' ? 'unconfirmed' : 'not_available')
            }));
          }
        }
        requestAnimationFrame(step);
      }))()`);
      const sample = typeof sampleRaw === "string" ? JSON.parse(sampleRaw) : sampleRaw;
      const appSnapshot = await evalValue(cdp, "window.__DUAT_PERF_SNAPSHOT__ || null").catch(() => null);
      results.push({
        ...scenario,
        ...sample,
        appAvgFps: Number(Number(appSnapshot?.snapshot?.avgFps ?? 0).toFixed(2)),
        appP95FrameMs: Number(Number(appSnapshot?.snapshot?.p95FrameMs ?? 0).toFixed(2)),
        runtimeMode: appSnapshot?.benchmarkStatic ? "static-render-benchmark" : "live-simulation",
        renderCounters: appSnapshot?.renderCounters,
      });
      console.log(JSON.stringify({ scenario: scenario.id, status: "done", avgFps: results[results.length - 1].avgFps }));
    }
    const doc = {
      schema: "duat/windows-app-performance-benchmark/v1.4",
      fingerprint: "DUAT-v1.4-WINAPP-CONVERSION",
      generatedAt: new Date().toISOString(),
      browserMode: "Edge/CDP/headed-winapp",
      wrapper: "native_dotnet_edge_app_mode",
      focusAttempt,
      headedFpsVerified: results.some(item => item.focusStatus === "focused" || item.focusStatus === "unconfirmed"),
      scenarios: results,
      notes: [
        "Windows app benchmark uses the native DUATCity.exe loopback server and visible Edge App runtime.",
        "Scenarios use benchmarkStatic=1 to isolate renderer cost from simulation ticks.",
        "Audio audibility is validated separately because autoplay remains blocked until user gesture.",
      ],
    };
    await writeFile(outJson, JSON.stringify(doc, null, 2), "utf8");
    await writeFile(outMd, renderReport(doc), "utf8");
    console.log(JSON.stringify({ ok: true, scenarios: results.length, outJson, outMd }, null, 2));
  } finally {
    if (cdp) cdp.close();
    if (!browser.killed) browser.kill();
  }
} finally {
  if (!server.killed) server.kill();
  await sleep(1000);
  await rm(profile, { recursive: true, force: true }).catch(() => {});
}

function renderReport(doc) {
  const rows = doc.scenarios.map(s => `| ${s.id} | ${s.avgFps} | ${s.p95FrameMs} | ${s.appAvgFps} | ${s.appP95FrameMs} | ${s.droppedFrames} | ${s.focusStatus} | ${s.runtimeMode} |`).join("\n");
  return `# DUAT Windows App Performance Benchmark v1.4

Fingerprint: ${doc.fingerprint}

Mode: ${doc.browserMode}
Wrapper: ${doc.wrapper}
Focus attempt: ${doc.focusAttempt}

| Scenario | external avg FPS | external p95 ms | app avg FPS | app p95 ms | dropped | focus | runtime |
|---|---:|---:|---:|---:|---:|---|---|
${rows}

Notes:
${doc.notes.map(n => `- ${n}`).join("\n")}
`;
}

function scenarioUrl(baseUrl, params) {
  const url = new URL(baseUrl);
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  url.searchParams.set("benchmarkStatic", "1");
  url.searchParams.set("labels", "0");
  url.searchParams.set("nativeWin", "1");
  if (params.view !== "DEBUG") url.searchParams.set("cinematic", "1");
  return url.toString();
}

function findEdge() {
  const candidates = ["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"];
  const found = candidates.find(path => existsSync(path));
  if (!found) throw new Error("Microsoft Edge executable not found");
  return found;
}

async function waitForUrl(child, timeoutMs) {
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

async function focusEdgeWindow(pid) {
  const script = `
$shell = New-Object -ComObject WScript.Shell
Start-Sleep -Milliseconds 500
if ($shell.AppActivate(${Number(pid)})) { 'focused_by_pid' } else { 'focus_unconfirmed' }
`;
  const ps = spawn("powershell", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script], { stdio: ["ignore", "pipe", "pipe"] });
  return await new Promise(resolve => {
    let stdout = "";
    let stderr = "";
    ps.stdout.on("data", chunk => { stdout += String(chunk); });
    ps.stderr.on("data", chunk => { stderr += String(chunk); });
    ps.on("close", code => resolve(stdout.trim() || stderr.trim() || `focus_exit_${code}`));
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
