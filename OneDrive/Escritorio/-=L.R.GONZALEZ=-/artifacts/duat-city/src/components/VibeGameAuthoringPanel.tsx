import { useMemo, useState } from "react";
import { compileVibeAction } from "../vibecoding/vibeActionCompiler";

interface VibeGameAuthoringPanelProps {
  onApplyCommand?: (command: string) => void;
}

export function VibeGameAuthoringPanel({ onApplyCommand }: VibeGameAuthoringPanelProps) {
  const [command, setCommand] = useState("haz un mercado subterraneo con luces rosas y humo");
  const [lastCommand, setLastCommand] = useState<string | null>(null);
  const compiled = useMemo(() => compileVibeAction(command), [command]);
  return (
    <div className="section vibe-panel">
      <div className="section-title">Vibe Game Authoring</div>
      <textarea className="vibe-textarea" value={command} onChange={event => setCommand(event.target.value)} />
      <div className="ctrl-row compact">
        <button className="ctrl-btn primary" onClick={() => { setLastCommand(command); onApplyCommand?.(command); }}>Apply Command</button>
        <button className="ctrl-btn" disabled={!lastCommand} onClick={() => lastCommand && setCommand(lastCommand)}>Undo Preview</button>
      </div>
      <div className="scene-preview">
        <div><b>Preview:</b> {compiled.preview}</div>
        <div><b>Intent:</b> {compiled.parsedIntent.slice(0, 8).join(", ")}</div>
        <div><b>Cloud/API:</b> false / false</div>
      </div>
      {compiled.warnings.length > 0 && <div className="panel-note warn">{compiled.warnings.join(" ")}</div>}
    </div>
  );
}
