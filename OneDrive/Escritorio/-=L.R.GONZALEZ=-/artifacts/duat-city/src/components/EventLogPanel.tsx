import type { CityState } from "../core/types";

interface EventLogPanelProps { state: CityState; }

const TYPE_CLASS: Record<string, string> = {
  need: "event-task", task: "event-task", building: "event-system",
  resource: "event-resource", risk: "event-risk", rpg: "event-rpg", system: "event-system",
};

export function EventLogPanel({ state }: EventLogPanelProps) {
  const events = [...state.events].reverse().slice(0, 20);
  return (
    <div className="bottom-bar">
      <div className="event-log">
        {events.length === 0 && <span className="stat-key">No events yet</span>}
        {events.map(evt => (
          <div key={evt.id} className="event-entry">
            <span className="event-tick">T{evt.tick}</span>
            <span className={`event-type ${TYPE_CLASS[evt.type] ?? "event-system"}`}>{evt.type.toUpperCase()}</span>
            <span className="event-title">{evt.title} — {evt.detail}</span>
            {evt.R_delta !== 0 && (
              <span style={{ color: evt.R_delta > 0 ? "#ff4444" : "#00ff9d", fontSize: 10, marginLeft: "auto" }}>
                R{evt.R_delta > 0 ? "+" : ""}{evt.R_delta.toFixed(2)}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
