from __future__ import annotations

import csv
import json
import os
import re
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


ROOT_BRAIN_OS = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-")
ROOT_WORKSPACE = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-")
ROOT_DESKTOP = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio")
ROOT_E = Path("E:/")
ROOT_OUTPUT = ROOT_WORKSPACE / "MEDIOEVO_LIVE_TREE"

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    ".skills",
    ".claw",
    ".claude",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "cache",
    "dist",
    "build",
    "target",
    ".venv",
    ".venv_api",
    "venv",
    "env",
    ".next",
    ".turbo",
    "vendor",
    "vendors",
    "github-modules",
    "pentest_repos",
}

TEXT_EXTS = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".toml",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".ps1",
    ".bat",
    ".cmd",
    ".env",
}

NAME_PATTERNS = {
    "env_file": re.compile(r"(^|[\\/])\.env($|\.)", re.IGNORECASE),
    "secret_name": re.compile(r"(secret|token|credential|apikey|api_key|password|passwd|private[_-]?key)", re.IGNORECASE),
    "payment_or_provider": re.compile(r"(gumroad|stripe|discord|youtube|openai|anthropic|qwen|nim|nvidia)", re.IGNORECASE),
    "local_settings": re.compile(r"(settings\.local|\.claw|\.claude|\.wrangler)", re.IGNORECASE),
}

CONTENT_PATTERNS = {
    "openai_like_key": re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"),
    "github_like_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer_token": re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{16,}\b", re.IGNORECASE),
    "private_key_header": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "assignment_secret": re.compile(
        r"\b(api[_-]?key|token|secret|password|passwd|client[_-]?secret|access[_-]?key)\b\s*[:=]\s*[\"']?[^\"'\s]{8,}",
        re.IGNORECASE,
    ),
}


@dataclass
class Finding:
    root_label: str
    path: str
    kind: str
    reason: str
    line: int
    redaction: str


def rel_to(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def safe_stat(path: Path):
    try:
        return path.stat()
    except OSError:
        return None


def file_is_candidate(path: Path, depth: int) -> bool:
    name = path.name.lower()
    ext = path.suffix.lower()
    p = str(path)
    if any(rx.search(p) for rx in NAME_PATTERNS.values()):
        return True
    if ext in TEXT_EXTS and depth <= 6:
        return True
    if name in {"package.json", "pyproject.toml", "requirements.txt", "readme.md", "agents.md", "claude.md"}:
        return True
    if ext == ".zip" and depth <= 3:
        return True
    return False


def iter_paths(root: Path, label: str, max_dirs: int, max_files: int):
    if not root.exists():
        return
    dirs_seen = 0
    files_seen = 0
    for current, dirnames, filenames in os.walk(root):
        cur = Path(current)
        dirs_seen += 1
        depth = len(rel_to(cur, root).split(os.sep)) if cur != root else 0
        dirnames[:] = [
            d
            for d in dirnames
            if d.lower() not in SKIP_DIR_NAMES
            and not (label == "ROOT_DESKTOP" and d in {"-=L.R.GONZALEZ=-", "-= BRAIN_OS =-"})
        ]
        if dirs_seen > max_dirs:
            return
        for filename in filenames:
            if files_seen >= max_files:
                return
            path = cur / filename
            file_depth = len(rel_to(path, root).split(os.sep)) - 1
            if not file_is_candidate(path, file_depth):
                continue
            files_seen += 1
            yield label, path


def scan_zip_names(label: str, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if path.suffix.lower() != ".zip":
        return findings
    try:
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                for kind, rx in NAME_PATTERNS.items():
                    if rx.search(name):
                        findings.append(
                            Finding(label, str(path), "zip_name", f"{kind} inside ZIP name", 0, "REDACTED_ZIP_ENTRY_NAME")
                        )
                        return findings
    except Exception as exc:  # noqa: BLE001
        findings.append(Finding(label, str(path), "zip_read_error", type(exc).__name__, 0, "NO_CONTENT_READ"))
    return findings


def scan_file(label: str, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    p = str(path)
    for kind, rx in NAME_PATTERNS.items():
        if rx.search(p):
            findings.append(Finding(label, p, "path_name", kind, 0, "REDACTED_PATH_VALUE"))

    if path.suffix.lower() == ".zip":
        findings.extend(scan_zip_names(label, path))
        return findings

    st = safe_stat(path)
    if st is None:
        findings.append(Finding(label, p, "read_error", "stat_error", 0, "NO_CONTENT_READ"))
        return findings
    if st.st_size > 2 * 1024 * 1024:
        if findings:
            findings.append(Finding(label, p, "content_skipped", "file_too_large_for_content_scan", 0, "NO_CONTENT_READ"))
        return findings
    if path.suffix.lower() not in TEXT_EXTS and not findings:
        return findings

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for number, line in enumerate(fh, start=1):
                for kind, rx in CONTENT_PATTERNS.items():
                    if rx.search(line):
                        findings.append(Finding(label, p, "content", kind, number, "REDACTED_MATCH"))
                        break
    except OSError as exc:
        findings.append(Finding(label, p, "read_error", type(exc).__name__, 0, "NO_CONTENT_READ"))
    return findings


def write_csv(path: Path, rows: list[Finding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(asdict(rows[0]).keys()) if rows else ["root_label", "path", "kind", "reason", "line", "redaction"])
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    roots = [
        (ROOT_BRAIN_OS, "ROOT_BRAIN_OS", 800, 3500),
        (ROOT_WORKSPACE, "ROOT_WORKSPACE", 900, 2200),
        (ROOT_DESKTOP, "ROOT_DESKTOP", 180, 700),
        (ROOT_E, "ROOT_E", 250, 700),
    ]
    findings: list[Finding] = []
    scanned = 0
    for root, label, max_dirs, max_files in roots:
        for file_label, path in iter_paths(root, label, max_dirs, max_files):
            scanned += 1
            findings.extend(scan_file(file_label, path))

    report_path = ROOT_OUTPUT / "10_QUALITY" / "SECRET_SCAN_REPORT.md"
    checklist_path = ROOT_OUTPUT / "10_QUALITY" / "SECRET_ROTATION_CHECKLIST.md"
    csv_path = ROOT_OUTPUT / "10_QUALITY" / "SECRET_SCAN_FINDINGS.csv"
    write_csv(csv_path, findings)

    by_kind = Counter(f.kind for f in findings)
    by_reason = Counter(f.reason for f in findings)
    publication_blocked = bool(findings)
    now = datetime.now().isoformat(timespec="seconds")
    top_rows = "\n".join(
        f"| `{f.root_label}` | `{f.path}` | `{f.kind}` | `{f.reason}` | `{f.line}` | `{f.redaction}` |"
        for f in findings[:200]
    )
    if not top_rows:
        top_rows = "| - | - | - | - | - | - |"

    write_text(
        report_path,
        f"""# SECRET_SCAN_REPORT

Fecha: {now}

Metodo: escaneo no destructivo por nombres sensibles y patrones de contenido. Este reporte no imprime valores completos; las coincidencias se reemplazan por `REDACTED_*`.

## Resultado ejecutivo

- Archivos candidatos escaneados: `{scanned}`
- Hallazgos reportados: `{len(findings)}`
- BLOQUEO_PUBLICACION: `{str(publication_blocked).upper()}`
- BLOQUEO_PUSH: `{str(publication_blocked).upper()}`
- BLOQUEO_DEPLOY: `{str(publication_blocked).upper()}`

## Conteo por tipo

{chr(10).join(f'- {k}: {v}' for k, v in sorted(by_kind.items())) or '- Sin hallazgos'}

## Conteo por razon

{chr(10).join(f'- {k}: {v}' for k, v in sorted(by_reason.items())) or '- Sin hallazgos'}

## Hallazgos enmascarados

| Root | Ruta | Tipo | Razon | Linea | Redaccion |
|---|---|---|---:|---:|---|
{top_rows}

## Bloqueo

Si `Hallazgos reportados > 0`, no publicar, no hacer push y no desplegar desde las rutas escaneadas. Revisar por allowlist de target, no por glob amplio.
""",
    )

    write_text(
        checklist_path,
        """# SECRET_ROTATION_CHECKLIST

Usar solo si se confirma que un hallazgo corresponde a secreto real.

1. Identificar proveedor sin imprimir el valor.
2. Revocar o rotar credencial desde el panel del proveedor.
3. Confirmar que el archivo queda fuera de Git, ZIPs y paquetes.
4. Reemplazar por ejemplo seguro si el proyecto necesita plantilla.
5. Reejecutar `tools/secret_scan.py`.
6. Registrar evidencia en `07_TRACE/WITNESSLOG.jsonl`.

No borrar archivos fuente en esta corrida.
""",
    )

    print(json.dumps({"ok": True, "scanned": scanned, "findings": len(findings), "report": str(report_path)}, ensure_ascii=False))
    return 0 if True else 1


if __name__ == "__main__":
    raise SystemExit(main())
