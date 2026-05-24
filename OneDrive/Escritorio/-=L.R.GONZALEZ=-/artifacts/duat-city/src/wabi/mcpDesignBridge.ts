import type { WabiMcpStatus } from "./types";

export function getWabiMcpStatus(): WabiMcpStatus {
  return {
    version: "v0.5-design",
    mode: "LOCALHOST_ONLY_READ_PREPARE_SANDBOX_OPT_IN_DESIGN",
    gated_write_enabled: false,
    execution_allowed: false,
    sandbox_execution_allowed: false,
    real_apply_allowed: false,
    external_clients_allowed: false,
  };
}
