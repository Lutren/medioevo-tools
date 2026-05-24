"""Output weighting policy for clean and user-adapted DUAT outputs."""

from __future__ import annotations


def output_weights(task_type: str = "technical") -> dict[str, float]:
    label = task_type.lower().strip()
    if label in {"creative", "explanatory", "narrative", "design"}:
        return {"alpha": 0.45, "beta": 0.45, "gamma": 0.10}
    if label in {"technical", "critical", "code", "data", "legal", "security", "prediction"}:
        return {"alpha": 0.75, "beta": 0.20, "gamma": 0.05}
    return {"alpha": 0.65, "beta": 0.25, "gamma": 0.10}


def validate_weights(alpha: float, beta: float, gamma: float, task_type: str = "technical") -> bool:
    if abs((alpha + beta + gamma) - 1.0) > 0.0001:
        return False
    label = task_type.lower().strip()
    if label in {"technical", "critical", "code", "data", "legal", "security", "prediction"}:
        return alpha >= 0.70 and beta <= 0.25 and gamma <= 0.10
    if label in {"creative", "explanatory", "narrative", "design"}:
        return alpha >= 0.40 and beta <= 0.50 and gamma <= 0.15
    return alpha >= beta
