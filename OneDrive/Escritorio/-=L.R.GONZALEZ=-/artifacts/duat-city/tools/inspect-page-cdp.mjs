import { existsSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";

const url = process.argv[2] ?? "http://127.0.0.1:18519/duat-city/";
const debugPort = Number(process.argv[3] ?? 18579);
const edge = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
].find(path => existsSync(path));
if (!edge) throw new Error("Microsoft Edge executable not found");
const profile = join(tmpdir(), `duat-page-inspect-${Date.now()}`);
const browser = spawn(edge, [
  `--remote-debugging-port=${debugPort}`,
  `--user-data-dir=${profile}`,
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-background-networking",
  "--disable-extensions",
  "--headless=new",
  "--window-size=1366,900",
  url,
], { stdio: "ignore" });

try {
  const target = await waitForTarget(debugPort, 30_000);
  const cdp = await connect(target.webSocketDebuggerUrl);
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Page.navigate", { url });
  await sleep(7000);
  const result = await cdp.send("Runtime.evaluate", {
    expression: `({
      href: location.href,
      title: document.title,
      body: document.body ? document.body.innerText.slice(0, 1000) : '',
      rootHtml: document.querySelector('#root')?.innerHTML.slice(0, 1000) ?? '',
      bg: getComputedStyle(document.body).backgroundColor,
      errors: window.__DUAT_CAPTURE_ERRORS__ || []
    })`,
    returnByValue: true,
  });
  console.log(JSON.stringify(result.result.result.value, null, 2));
  cdp.close();
} finally {
  browser.kill();
}

async function waitForTarget(port, timeoutMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const target = targets.find(item => item.type === "page" && item.webSocketDebuggerUrl);
      if (target?.webSocketDebuggerUrl) return target;
    } catch {
      // waiting
    }
    await sleep(250);
  }
  throw new Error("Timed out waiting for page target");
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
