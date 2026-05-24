import { compileEpistemicStatement } from "./epistemicDialogue";

export function describeToolAction(action: string, evidence: string[] = []) {
  return compileEpistemicStatement(`Tool action requested: ${action}. Local ActionGate review required before execution.`, evidence);
}
