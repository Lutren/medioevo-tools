from __future__ import annotations

import argparse
import sys

from .brief import render_brief
from .doctor import run_doctor
from .executor import execute_write_file, restore_rollback
from .ghostgate import evaluate_plan_request, plan_tools
from .jsonutil import emit_json, read_json
from .memory_lite import memory_status, search_memory
from .permissions import evaluate_permission
from .rphi_calibration import write_calibration_artifacts
from .rphi_budget import calculate_rphi_budget, write_rphi_artifacts
from .skills_registry import discover_skills, inspect_skill
from .task_board import add_task, list_tasks
from .witness_log import append_witness_event, witness_status


def _print(data: object, as_json: bool) -> None:
    if as_json:
        print(emit_json(data))
    else:
        print(data if isinstance(data, str) else emit_json(data))


def _add_witness_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--witness-root",
        default=None,
        help="append a redacted WitnessLog event under this state root",
    )


def _emit_witness(args: argparse.Namespace, command: str, result: object, actiongate: str = "APPROVE") -> None:
    root = getattr(args, "witness_root", None)
    if root:
        append_witness_event(root, command=command, status="ok", result=result, actiongate=actiongate)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="claudio-agent-runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor")
    doctor.add_argument("--root", default=".")
    doctor.add_argument("--json", action="store_true")
    _add_witness_arg(doctor)

    permissions = sub.add_parser("permissions")
    permissions_sub = permissions.add_subparsers(dest="permissions_command", required=True)
    permissions_check = permissions_sub.add_parser("check")
    permissions_check.add_argument("payload")
    permissions_check.add_argument("--json", action="store_true")
    _add_witness_arg(permissions_check)

    execute = sub.add_parser("execute")
    execute_sub = execute.add_subparsers(dest="execute_command", required=True)
    execute_write = execute_sub.add_parser("write")
    execute_write.add_argument("payload")
    execute_write.add_argument("--root", default=".")
    execute_write.add_argument("--json", action="store_true")
    _add_witness_arg(execute_write)

    rollback = sub.add_parser("rollback")
    rollback_sub = rollback.add_subparsers(dest="rollback_command", required=True)
    rollback_restore = rollback_sub.add_parser("restore")
    rollback_restore.add_argument("rollback_id")
    rollback_restore.add_argument("--root", default=".")
    rollback_restore.add_argument("--json", action="store_true")
    _add_witness_arg(rollback_restore)

    ghostgate = sub.add_parser("ghostgate")
    ghostgate_sub = ghostgate.add_subparsers(dest="ghostgate_command", required=True)
    ghostgate_tools = ghostgate_sub.add_parser("tools")
    ghostgate_tools.add_argument("--json", action="store_true")
    _add_witness_arg(ghostgate_tools)
    ghostgate_check = ghostgate_sub.add_parser("check")
    ghostgate_check.add_argument("payload")
    ghostgate_check.add_argument("--json", action="store_true")
    _add_witness_arg(ghostgate_check)

    skills = sub.add_parser("skills")
    skills_sub = skills.add_subparsers(dest="skills_command", required=True)
    skills_list = skills_sub.add_parser("list")
    skills_list.add_argument("--root", default="skills")
    skills_list.add_argument("--json", action="store_true")
    _add_witness_arg(skills_list)
    skills_inspect = skills_sub.add_parser("inspect")
    skills_inspect.add_argument("path")
    skills_inspect.add_argument("--json", action="store_true")
    _add_witness_arg(skills_inspect)

    memory = sub.add_parser("memory")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)
    memory_status_parser = memory_sub.add_parser("status")
    memory_status_parser.add_argument("--root", default=".")
    memory_status_parser.add_argument("--json", action="store_true")
    _add_witness_arg(memory_status_parser)
    memory_search = memory_sub.add_parser("search")
    memory_search.add_argument("query")
    memory_search.add_argument("--root", default=".")
    memory_search.add_argument("--json", action="store_true")
    _add_witness_arg(memory_search)

    tasks = sub.add_parser("tasks")
    tasks_sub = tasks.add_subparsers(dest="tasks_command", required=True)
    tasks_list = tasks_sub.add_parser("list")
    tasks_list.add_argument("--root", default=".")
    tasks_list.add_argument("--json", action="store_true")
    _add_witness_arg(tasks_list)
    tasks_add = tasks_sub.add_parser("add")
    tasks_add.add_argument("payload")
    tasks_add.add_argument("--root", default=".")
    tasks_add.add_argument("--json", action="store_true")
    _add_witness_arg(tasks_add)

    brief = sub.add_parser("brief")
    brief.add_argument("--root", default=".")
    brief.add_argument("--json", action="store_true")
    _add_witness_arg(brief)

    witness = sub.add_parser("witness")
    witness_sub = witness.add_subparsers(dest="witness_command", required=True)
    witness_status_parser = witness_sub.add_parser("status")
    witness_status_parser.add_argument("--root", default=".")
    witness_status_parser.add_argument("--json", action="store_true")

    budget = sub.add_parser("budget")
    budget_sub = budget.add_subparsers(dest="budget_command", required=True)
    budget_status = budget_sub.add_parser("status")
    budget_status.add_argument("--root", default=".")
    budget_status.add_argument("--json", action="store_true")
    _add_witness_arg(budget_status)
    budget_report = budget_sub.add_parser("report")
    budget_report.add_argument("--root", default=".")
    budget_report.add_argument("--output-root", default=None)
    budget_report.add_argument("--json", action="store_true")
    _add_witness_arg(budget_report)
    budget_calibrate = budget_sub.add_parser("calibrate")
    budget_calibrate.add_argument("--fixtures-root", default=None)
    budget_calibrate.add_argument("--output-root", default=None)
    budget_calibrate.add_argument("--json", action="store_true")
    _add_witness_arg(budget_calibrate)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "doctor":
        result = run_doctor(args.root)
        _emit_witness(args, "doctor", result)
        _print(result, args.json)
        return 0

    if args.command == "permissions" and args.permissions_command == "check":
        result = evaluate_permission(read_json(args.payload))
        _emit_witness(args, "permissions check", result, actiongate=result["decision"])
        _print(result, args.json)
        return 0

    if args.command == "execute" and args.execute_command == "write":
        result = execute_write_file(args.root, read_json(args.payload))
        _emit_witness(args, "execute write", result, actiongate=result["actiongate"])
        _print(result, args.json)
        return 0

    if args.command == "rollback" and args.rollback_command == "restore":
        result = restore_rollback(args.root, args.rollback_id)
        _emit_witness(args, "rollback restore", result)
        _print(result, args.json)
        return 0

    if args.command == "ghostgate" and args.ghostgate_command == "tools":
        result = plan_tools()
        _emit_witness(args, "ghostgate tools", result)
        _print(result, args.json)
        return 0

    if args.command == "ghostgate" and args.ghostgate_command == "check":
        result = evaluate_plan_request(read_json(args.payload))
        _emit_witness(args, "ghostgate check", result, actiongate=result["decision"])
        _print(result, args.json)
        return 0

    if args.command == "skills" and args.skills_command == "list":
        result = {"skills": discover_skills(args.root)}
        _emit_witness(args, "skills list", result)
        _print(result, args.json)
        return 0

    if args.command == "skills" and args.skills_command == "inspect":
        result = inspect_skill(args.path)
        _emit_witness(args, "skills inspect", result)
        _print(result, args.json)
        return 0

    if args.command == "memory" and args.memory_command == "status":
        result = memory_status(args.root)
        _emit_witness(args, "memory status", result)
        _print(result, args.json)
        return 0

    if args.command == "memory" and args.memory_command == "search":
        result = {"results": search_memory(args.root, args.query)}
        _emit_witness(args, "memory search", result)
        _print(result, args.json)
        return 0

    if args.command == "tasks" and args.tasks_command == "list":
        result = list_tasks(args.root)
        _emit_witness(args, "tasks list", result)
        _print(result, args.json)
        return 0

    if args.command == "tasks" and args.tasks_command == "add":
        result = add_task(args.root, read_json(args.payload))
        _emit_witness(args, "tasks add", result)
        _print(result, args.json)
        return 0

    if args.command == "brief":
        text = render_brief(args.root)
        result = {"brief": text}
        _emit_witness(args, "brief", result)
        _print(result, args.json)
        return 0

    if args.command == "witness" and args.witness_command == "status":
        _print(witness_status(args.root), args.json)
        return 0

    if args.command == "budget" and args.budget_command == "status":
        result = calculate_rphi_budget(args.root)
        _emit_witness(args, "budget status", result, actiongate=result["actiongate_suggestion"])
        _print(result, args.json)
        return 0

    if args.command == "budget" and args.budget_command == "report":
        result = write_rphi_artifacts(args.root, output_root=args.output_root)
        _emit_witness(args, "budget report", result["budget"], actiongate=result["budget"]["actiongate_suggestion"])
        _print(result, args.json)
        return 0

    if args.command == "budget" and args.budget_command == "calibrate":
        result = write_calibration_artifacts(fixtures_root=args.fixtures_root, output_root=args.output_root)
        actiongate = "APPROVE" if result["calibration"]["calibration_status"] == "PASS" else "REVIEW"
        _emit_witness(args, "budget calibrate", result["calibration"], actiongate=actiongate)
        _print(result, args.json)
        return 0

    print("unknown command", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
