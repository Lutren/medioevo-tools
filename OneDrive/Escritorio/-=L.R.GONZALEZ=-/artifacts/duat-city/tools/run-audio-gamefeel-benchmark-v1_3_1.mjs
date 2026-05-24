import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { mkdirSync, writeFileSync } from "node:fs";
import { createServer } from "vite";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const iterations = Number(process.argv[2] ?? 160);
const outputPath = resolve(root, process.argv[3] ?? "docs/PERFORMANCE_BENCHMARK_v1_3_1.json");

process.env.VITEST = process.env.VITEST ?? "1";

const server = await createServer({
  root,
  configFile: resolve(root, "vite.config.ts"),
  logLevel: "silent",
  server: { middlewareMode: true },
});

try {
  const mod = await server.ssrLoadModule("/src/audio/audioBenchmark.ts");
  const doc = mod.runAudioGameFeelBenchmark(iterations);
  mkdirSync(dirname(outputPath), { recursive: true });
  writeFileSync(outputPath, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  console.log(JSON.stringify({
    status: "ok",
    outputPath,
    scenarios: doc.scenarios.length,
    iterationsPerScenario: doc.iterationsPerScenario,
    browserAudioUsed: doc.browserAudioUsed,
  }));
} finally {
  await server.close();
}
