"""Prerequisite-gated knowledge graph helpers."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Tuple


class NodeState(str, Enum):
    LOCKED = "LOCKED"
    ACCESSIBLE = "ACCESSIBLE"
    INTEGRATED = "INTEGRATED"


@dataclass
class KnowledgeNode:
    node_id: str
    title: str
    content: str
    prerequisites: List[str] = field(default_factory=list)
    unlock_phi_threshold: float = 0.60
    max_r_threshold: float = 0.45
    state: NodeState = NodeState.LOCKED
    evidence: List[str] = field(default_factory=list)

    def can_unlock(self, *, phi_eff: float, r: float, integrated_nodes: Set[str]) -> Tuple[bool, str]:
        if self.state == NodeState.INTEGRATED:
            return True, "already_integrated"
        missing = [node_id for node_id in self.prerequisites if node_id not in integrated_nodes]
        if missing:
            return False, "missing_prerequisites:" + ",".join(missing)
        if phi_eff < self.unlock_phi_threshold:
            return False, "phi_eff_below_unlock_threshold"
        if r > self.max_r_threshold:
            return False, "r_above_unlock_threshold"
        return True, "unlock_allowed"


class KnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: Dict[str, KnowledgeNode] = {}

    def add_node(self, node: KnowledgeNode) -> None:
        if node.node_id in self.nodes:
            raise ValueError(f"duplicate_node:{node.node_id}")
        self.nodes[node.node_id] = node

    def integrated_ids(self) -> Set[str]:
        return {node_id for node_id, node in self.nodes.items() if node.state == NodeState.INTEGRATED}

    def attempt_access(self, node_id: str, *, phi_eff: float, r: float) -> dict:
        node = self.nodes[node_id]
        allowed, reason = node.can_unlock(phi_eff=phi_eff, r=r, integrated_nodes=self.integrated_ids())
        if not allowed:
            return {"node_id": node_id, "status": NodeState.LOCKED.value, "reason": reason, "content": None}
        if node.state == NodeState.LOCKED:
            node.state = NodeState.ACCESSIBLE
        return {"node_id": node_id, "status": node.state.value, "reason": reason, "content": node.content}

    def integrate(self, node_id: str, evidence: List[str]) -> dict:
        node = self.nodes[node_id]
        if node.state != NodeState.ACCESSIBLE:
            raise ValueError(f"node_not_accessible:{node_id}")
        if not evidence:
            raise ValueError("integration_evidence_required")
        node.evidence = list(evidence)
        node.state = NodeState.INTEGRATED
        return {"node_id": node_id, "status": node.state.value, "evidence_count": len(evidence)}

    def progress(self) -> dict:
        counts = {state.value: 0 for state in NodeState}
        for node in self.nodes.values():
            counts[node.state.value] += 1
        total = len(self.nodes)
        return {
            "total": total,
            "locked": counts[NodeState.LOCKED.value],
            "accessible": counts[NodeState.ACCESSIBLE.value],
            "integrated": counts[NodeState.INTEGRATED.value],
            "progress_pct": round(100 * counts[NodeState.INTEGRATED.value] / total, 1) if total else 0.0,
        }

