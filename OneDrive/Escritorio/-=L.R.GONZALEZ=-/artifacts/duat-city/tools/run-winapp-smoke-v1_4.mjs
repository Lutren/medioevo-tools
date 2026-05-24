import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const exe = resolve(root, "dist", "winapp", "DUATCity.exe");
const outJson = resolve(process.argv[2] ?? join(root, "docs", "WINDOWS_APP_SMOKE_v1_4.json"));
const outMd = resolve(process.argv[3] ?? join(root, "docs", "WINDOWS_APP_QA_v1_4.md"));
const port = Number(process.argv[4] ?? 18641);

if (!existsSync(exe)) {
  throw new Error(`Windows app executable missing: ${exe}`);
}

await mkdir(dirname(outJson), { recursive: true });

const smoke = await runExe(["--smoke"]);
const server = spawn(exe, ["--serve-only", "--port", String(port), "--duration-ms", "20000"], { stdio: ["ignore", "pipe", "pipe"] });

try {
  const url = await waitForUrl(server, 8000);
  const smokeUrl = `${url}&mode=CITY&view=OPERATIONAL&vibe=neon_rain_street`;
  const response = await fetch(smokeUrl);
  const html = await response.text();
  const assetMatch = html.match(/src="([^"]+\.js)"/);
  let assetStatus = 0;
  if (assetMatch) {
    const assetUrl = new URL(assetMatch[1], url).toString();
    assetStatus = (await fetch(assetUrl)).status;
  }
  const result = {
    schema: "duat/windows-app-smoke/v1.4",
    fingerprint: "DUAT-v1.4-WINAPP-CONVERSION",
    generatedAt: new Date().toISOString(),
    executable: "dist/winapp/DUATCity.exe",
    wrapper: "native_dotnet_edge_app_mode",
    preferredWrappers: ["electron", "tauri"],
    smokeStatus: smoke.status,
    serverUrl: url,
    httpStatus: response.status,
    indexContainsRoot: html.includes('id="root"'),
    jsAssetStatus: assetStatus,
    publication_allowed: false,
    wabi_execution_allowed: false,
    cloud_used: false,
    mcp_execution: false,
    unknown_zip_code_executed: false,
    notes: [
      "Serve-only smoke uses the native launcher static server without launching external cloud services.",
      "Electron/Tauri were not installed locally; this is the no-new-dependency Windows wrapper path.",
    ],
  };
  await writeFile(outJson, JSON.stringify(result, null, 2), "utf8");
  await writeFile(outMd, renderReport(result), "utf8");
  console.log(JSON.stringify({ ok: true, outJson, outMd, httpStatus: response.status, jsAssetStatus: assetStatus }, null, 2));
} finally {
  if (!server.killed) server.kill();
}

function renderReport(result) {
  return `# DUAT Windows App QA v1.4

Fingerprint: ${result.fingerprint}

Status:
- executable: ${result.executable}
- wrapper: ${result.wrapper}
- preferred wrappers: ${result.preferredWrappers.join(", ")}
- smoke status: ${result.smokeStatus}
- server URL: ${result.serverUrl}
- HTTP status: ${result.httpStatus}
- JS asset status: ${result.jsAssetStatus}
- root present: ${result.indexContainsRoot}

Boundary:
- publication_allowed=false
- wabi_execution_allowed=false
- cloud_used=false
- mcp_execution=false
- unknown_zip_code_executed=false

Notes:
${result.notes.map(note => `- ${note}`).join("\n")}
`;
}

async function runExe(args) {
  const child = spawn(exe, args, { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", chunk => { stdout += String(chunk); });
  child.stderr.on("data", chunk => { stderr += String(chunk); });
  const code = await new Promise(resolve => child.on("close", resolve));
  return { code, stdout, stderr, status: code === 0 ? "PASS" : "FAIL" };
}

function waitForUrl(child, timeoutMs) {
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
    child.stderr.on("data", chunk => {
      output += String(chunk);
    });
    child.on("exit", code => {
      if (!output.includes("DUAT_WINAPP_URL=")) {
        clearTimeout(timer);
        rejectReady(new Error(`launcher exited before URL, code=${code}, output=${output}`));
      }
    });
  });
}
