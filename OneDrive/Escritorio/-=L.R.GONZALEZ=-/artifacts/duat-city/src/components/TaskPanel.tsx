import type { CityState, Task } from "../core/types";

interface TaskPanelProps { state: CityState; }

const STATUS_COLORS: Record<string, string> = {
  pending: "#6e7681",
  active: "#7bc8f6",
  done: "#00ff9d",
  failed: "#ff4444",
  blocked: "#ffcc00",
};

export function TaskPanel({ state }: TaskPanelProps) {
  const active = state.tasks.filter(t => t.status === "active").slice(0, 10);
  const recent = state.tasks.filter(t => t.status === "done" || t.status === "failed").slice(-5).reverse();

  return (
    <div className="section">
      <button 
        onClick={() => console.log("GM Action: Requesting Quest Update")}
        style={{ fontSize: 10, marginBottom: 5, padding: "2px 5px" }}
      >
        Sync Quests
      </button>
      <div className="section-title">Tasks ({active.length} active)</div>
      {active.map(task => (
        <div key={task.id} style={{ padding: "2px 0", borderBottom: "1px solid #21262d" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ color: "#c9d1d9", fontSize: 11 }}>{task.title}</span>
            <span style={{ color: STATUS_COLORS[task.status], fontSize: 10 }}>{task.status}</span>
          </div>
          <div className="progress-bar" style={{ marginTop: 2 }}>
            <div className="progress-fill bar-phi" style={{ width: `${task.progress * 100}%` }} />
          </div>
        </div>
      ))}
      {active.length === 0 && <span className="stat-key">No active tasks</span>}

      {recent.length > 0 && (
        <>
          <div className="section-title" style={{ marginTop: 6 }}>Recent</div>
          {recent.map(task => (
            <div key={task.id} style={{ display: "flex", justifyContent: "space-between", padding: "1px 0", fontSize: 10 }}>
              <span style={{ color: "#6e7681" }}>{task.title}</span>
              <span style={{ color: STATUS_COLORS[task.status] }}>{task.status}</span>
            </div>
          ))}
        </>
      )}
    </div>
  );
}
