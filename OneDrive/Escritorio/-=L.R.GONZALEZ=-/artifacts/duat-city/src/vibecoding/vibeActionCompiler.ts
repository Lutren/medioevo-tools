import type { VibeCommandParseResult } from "./vibeCommandParser";
import { parseVibeCommand } from "./vibeCommandParser";

export interface CompiledVibeAction extends VibeCommandParseResult {
  apply: true;
  undo: true;
}

export function compileVibeAction(command: string): CompiledVibeAction {
  return { ...parseVibeCommand(command), apply: true, undo: true };
}
