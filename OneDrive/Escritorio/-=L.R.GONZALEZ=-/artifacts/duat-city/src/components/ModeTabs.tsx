import type { Mode } from "../core/types";

interface ModeTabsProps {
  mode: Mode;
  onMode: (m: Mode) => void;
}

const MODES: { key: Mode; label: string; icon: string }[] = [
  { key: "CITY",  label: "City Builder",   icon: "🏙️" },
  { key: "AGENT", label: "Agent Life",     icon: "🤖" },
  { key: "RPG",   label: "RPG Builder",    icon: "⚔️" },
  { key: "OSIT",  label: "OSIT / DUAT",   icon: "📊" },
];

export function ModeTabs({ mode, onMode }: ModeTabsProps) {
  return (
    <div className="mode-tabs">
      {MODES.map(m => (
        <button
          key={m.key}
          className={`mode-tab ${mode === m.key ? "active" : ""}`}
          onClick={() => onMode(m.key)}
        >
          {m.icon} {m.label}
        </button>
      ))}
    </div>
  );
}
