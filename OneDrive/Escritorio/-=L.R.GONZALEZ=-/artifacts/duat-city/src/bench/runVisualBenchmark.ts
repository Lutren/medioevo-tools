import { writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { runVisualBenchmark } from "./visualBenchmark";

export function generateVisualBenchmarkArtifact(outPath: string, framesPerScenario = 260): void {
  const output = runVisualBenchmark(framesPerScenario);
  writeFileSync(resolve(outPath), JSON.stringify(output, null, 2), "utf8");
}

const outArg = process.argv.find(arg => arg.startsWith("--out="));
if (outArg) {
  const framesArg = process.argv.find(arg => arg.startsWith("--frames="));
  generateVisualBenchmarkArtifact(outArg.slice("--out=".length), Number(framesArg?.slice("--frames=".length) ?? 260));
}
