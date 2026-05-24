from __future__ import annotations

from typing import Any


PLAN_ALLOWED_TOOLS = {
    "git_diff",
    "git_log",
    "git_status",
    "inspect_file",
    "list_dir",
    "read_file",
    "rg",
    "search",
}

PLAN_BLOCKED_TOOLS = {
    "create_file",
    "delete_file",
    "edit_file",
    "git_add",
    "git_commit",
    "git_push",
    "github_create_issue",
    "github_create_pr",
    "network",
    "publish",
    "run_command",
    "send_message",
    "subagent_delegate",
    "write_file",
}


def plan_tools() -> dict[str, Any]:
    return {
        "schema_version": "claudio.ghostgate.tools.v0.1",
        "mode": "plan",
        "allowed_tools": sorted(PLAN_ALLOWED_TOOLS),
        "blocked_tools": sorted(PLAN_BLOCKED_TOOLS),
        "contract": "read_list_search_inspect_only",
    }


def evaluate_plan_request(payload: dict[str, Any]) -> dict[str, Any]:
    raw_tools = payload.get("requested_tools") or payload.get("tools") or []
    if not isinstance(raw_tools, list):
        raw_tools = []
    requested = [str(tool).strip() for tool in raw_tools if str(tool).strip()]
    normalized = [tool.lower().replace("-", "_") for tool in requested]
    blocked = sorted({tool for tool in normalized if tool in PLAN_BLOCKED_TOOLS})
    unknown = sorted(
        {tool for tool in normalized if tool not in PLAN_ALLOWED_TOOLS and tool not in PLAN_BLOCKED_TOOLS}
    )
    allowed = sorted({tool for tool in normalized if tool in PLAN_ALLOWED_TOOLS})

    if blocked:
        decision = "BLOCK"
        reason = "plan mode cannot use write, shell, git-write, network, publication or delegation tools"
    elif unknown:
        decision = "REVIEW"
        reason = "plan mode received unknown tools"
    else:
        decision = "APPROVE"
        reason = "plan mode request is read/list/search/inspect only"

    return {
        "schema_version": "claudio.ghostgate.plan_request.v0.1",
        "mode": "plan",
        "decision": decision,
        "reason": reason,
        "allowed": allowed,
        "blocked": blocked,
        "unknown": unknown,
    }

