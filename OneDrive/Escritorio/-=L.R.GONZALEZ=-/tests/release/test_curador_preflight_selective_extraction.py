from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "release"))

import curador_preflight  # noqa: E402


def test_preflight_does_not_treat_name_only_match_as_registered(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "POST" / "Untitled.txt"
    source.parent.mkdir(parents=True)
    source.write_text("prototype", encoding="utf-8")
    registry = tmp_path / "SOURCE_INTAKE_REGISTER.md"
    registry.write_text("| `Untitled.txt` | name only |\n", encoding="utf-8")
    monkeypatch.setattr(curador_preflight, "registry_paths", lambda: [registry])

    result = curador_preflight.evaluate(str(source))

    assert result["classification"]["registered"] is False
    assert result["classification"]["partial_match_only"] is True
    assert result["classification"]["decision"] == "NEEDS_FICHA_BEFORE_USE"


def test_preflight_requires_exact_path_to_register_source(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "POST" / "Untitled.txt"
    source.parent.mkdir(parents=True)
    source.write_text("prototype", encoding="utf-8")
    registry = tmp_path / "SOURCE_INTAKE_REGISTER.md"
    registry.write_text(f"| `{source}` | exact path |\n", encoding="utf-8")
    monkeypatch.setattr(curador_preflight, "registry_paths", lambda: [registry])

    result = curador_preflight.evaluate(str(source))

    assert result["classification"]["registered"] is True
    assert result["classification"]["partial_match_only"] is False
    assert result["classification"]["decision"] == "REGISTERED_CONTINUE_WITH_BOUNDARY"


def test_ficha_template_includes_selective_extraction_fields() -> None:
    classification = {
        "required_registers": [
            "SOURCE_INTAKE_REGISTER.md for external/raw sources",
            "PRODUCT_MAP.md and VISIBILITY_MATRIX.md for repos/products",
        ]
    }
    tech = {"signals": ["single_file"]}

    template = curador_preflight.ficha_template(
        r"C:\example\POST\Untitled.txt",
        classification,
        tech,
    )

    assert "useful_deltas" in template
    assert "rejected_material" in template
    assert "target_lane" in template
    assert "claim_boundary" in template
    assert "raw_adoption: `BLOCK`" in template
    assert "action_gate: `REVIEW`" in template
