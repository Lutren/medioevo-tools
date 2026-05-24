from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from obsai_core.tasks import TaskEvidence, TaskManager


class TaskManagerTests(unittest.TestCase):
    def test_task_lifecycle_requires_evidence_to_close(self) -> None:
        manager = TaskManager()
        task = manager.add_task("write focused handoff", priority="P1")

        with self.assertRaises(ValueError):
            manager.close_task(task.task_id)

        closed = manager.close_task(
            task.task_id,
            evidence=TaskEvidence("pytest", "tests/test_task_manager.py", verified=True),
            note="closed with local evidence",
        )

        self.assertEqual(closed.status, "CLOSED")
        self.assertEqual(closed.note, "closed with local evidence")
        self.assertEqual(closed.evidence[0].label, "pytest")
        self.assertEqual(manager.summary()["byStatus"]["CLOSED"], 1)

    def test_task_manager_persists_json_round_trip(self) -> None:
        manager = TaskManager()
        task = manager.add_task(
            "document assumption",
            priority="P2",
            evidence=[TaskEvidence("brief", "NEXT_SESSION_BRIEF.md", verified=True)],
            metadata={"lane": "governance"},
        )
        manager.block_task(task.task_id, note="requires human review")

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            manager.save(path)
            loaded = TaskManager.load(path)

        fetched = loaded.get_task(task.task_id)
        self.assertEqual(fetched.status, "BLOCKED")
        self.assertEqual(fetched.metadata["lane"], "governance")
        self.assertEqual(fetched.evidence[0].source, "NEXT_SESSION_BRIEF.md")


if __name__ == "__main__":
    unittest.main()
