from __future__ import annotations

import json
from pathlib import Path

from brain_os_post_learning_program import compile_learning_program


ROOT = Path(__file__).resolve().parents[2]
MATRIX_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json"
WORKPACK_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_PROGRAMMING_LEARNING_MODULES_2026-05-18.json"
OUT_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_COMPILED_LEARNING_PROGRAM_2026-05-18.json"
OUT_MD = ROOT / "docs" / "intake" / "BRAIN_OS_POST_COMPILED_LEARNING_PROGRAM_2026-05-18.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_md(payload: dict) -> str:
    lines = [
        "# BRAIN_OS POST Compiled Learning Program 2026-05-18",
        "",
        "Status: `LOCAL_PROGRAMMING_CONTRACTS_COMPILED`",
        "",
        "RuntimeImport=BLOCK",
        "PublicationGate=BLOCK",
        "RawAdoption=BLOCK",
        "ModelTraining=BLOCK",
        "CloudTraining=BLOCK",
        "ZipExtraction=BLOCK",
        "",
        "This program turns the curated POST workpack into deterministic local programming contracts, fixtures and benchmark requirements. It does not train a model, publish content, import raw source, extract ZIP members or approve runtime adoption.",
        "",
        "## Coverage",
        "",
        f"- Modules: `{payload['coverage']['module_count']}`",
        f"- Covered deltas: `{len(payload['coverage']['covered_delta_ids'])}`",
        f"- Uncovered deltas: `{len(payload['coverage']['uncovered_delta_ids'])}`",
        f"- Modules with missing deltas: `{len(payload['coverage']['modules_with_missing_delta_ids'])}`",
        "",
        "## Compiled Modules",
        "",
        "| module | family | gate | evidence | target |",
        "|---|---|---|---|---|",
    ]
    for module in payload["compiled_modules"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{module['module_id']}`",
                    f"`{module['family']}`",
                    f"`{module['gate']}`",
                    f"`{module['evidence_state']}`",
                    module["target_lane"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## ZIP Evidence",
            "",
            "| zip | entries | testzip | extraction | runtime import |",
            "|---|---:|---|---|---|",
        ]
    )
    for item in payload["zip_evidence"]:
        name = Path(item["path"]).name
        lines.append(
            f"| `{name}` | `{item['entry_count']}` | `{item['testzip']}` | `{item['extraction_gate']}` | `{item['runtime_import_gate']}` |"
        )

    lines.extend(
        [
            "",
            "## Benchmarks",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in payload["benchmarks"])
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    payload = compile_learning_program(load_json(MATRIX_JSON), load_json(WORKPACK_JSON))
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "schema_version": payload["schema_version"],
                "compiled_modules": len(payload["compiled_modules"]),
                "uncovered_delta_ids": payload["coverage"]["uncovered_delta_ids"],
                "output": str(OUT_JSON),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

