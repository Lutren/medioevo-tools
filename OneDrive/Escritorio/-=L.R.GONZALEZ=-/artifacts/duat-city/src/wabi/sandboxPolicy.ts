import type { CityState } from "../core/types";
import type { SandboxExecutionDesign } from "./types";

export function createSandboxExecutionDesign(_state: CityState): SandboxExecutionDesign {
  return {
    schema: "wabi/sandbox-policy/v0.5-design",
    sandbox_root: "artifacts/duat-city/.wabi-sandbox",
    allowlist: [
      "pnpm --filter @workspace/duat-city run test",
      "pnpm --filter @workspace/duat-city run typecheck",
      "pnpm --filter @workspace/duat-city run build",
    ],
    denylist: [
      "push",
      "deploy",
      "real_apply",
      "external_api",
      "secrets",
      "global_config",
      "private_rpg",
    ],
    commands: [],
    default_disabled: true,
    requires_future_explicit_opt_in: true,
  };
}
