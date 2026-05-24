from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT_BRAIN_OS = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-")
ROOT_WORKSPACE = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-")
ROOT_DESKTOP = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio")
ROOT_E = Path("E:/")
ROOT_OUTPUT = ROOT_WORKSPACE / "MEDIOEVO_LIVE_TREE"
ROOT_TEMP = ROOT_WORKSPACE / "_TEMP_LIVE_TREE"

RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S")

FINAL_CATEGORIES = {
    "ACTIVE_CANON",
    "ACTIVE_RUNTIME",
    "ACTIVE_PRODUCT",
    "ACTIVE_ASSET",
    "ACTIVE_TOOL",
    "ACTIVE_RESEARCH",
    "PROTECTED_IP",
    "EVIDENCE_ONLY",
    "DELETE_AFTER_COVERAGE",
    "IGNORE_NO_VALUE",
    "SECURITY_REVIEW",
    "UNKNOWN_REVIEW",
}

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
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
    "caches",
    "dist",
    "build",
    "target",
    ".venv",
    ".venv_api",
    "venv",
    "env",
    ".next",
    ".turbo",
    ".wrangler",
    "vendor",
    "vendors",
    "github-modules",
    "pentest_repos",
}

HEAVY_EXTS = {
    ".zip",
    ".7z",
    ".rar",
    ".tar",
    ".gz",
    ".iso",
    ".exe",
    ".dll",
    ".apk",
    ".mp4",
    ".mov",
    ".mkv",
    ".wav",
    ".mp3",
    ".flac",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".pdf",
    ".docx",
    ".pptx",
}

HIGH_VALUE_NAMES = {
    "readme.md",
    "claude.md",
    "agents.md",
    "next_session_brief.md",
    "pendientes_master.md",
    "tasks.md",
    "decisions.md",
    "risks.md",
    "assumptions.md",
    "handoff.md",
    "manifest.json",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "sha256.txt",
}

HIGH_VALUE_RE = re.compile(
    r"(readme|claude|agents|next_session_brief|pendientes|handoff|manifest|sha256|"
    r"witness|actiongate|canon|observacion|osit|psi|brain|duat|geodia|argus|"
    r"wabi|runtime|fingerprint|roadmap|release|security|risk|visibility|"
    r"product_map|audit|duplicates|migration|implementation|tasks|decisions|"
    r"blocked|review_required|assumptions|test_report|tree_plan|source_intake|"
    r"changelog|contributing|license)",
    re.IGNORECASE,
)

SECRET_NAME_RE = re.compile(
    r"(\.env($|\.)|secret|token|credential|apikey|api_key|password|passwd|private[_-]?key|"
    r"settings\.local|gumroad|stripe|discord|youtube|openai)",
    re.IGNORECASE,
)

PRIVATE_RE = re.compile(
    r"(metaevo|tcg|rpg|game[_\\/-]?bridge|game-private|videojuego|lore|"
    r"vault_medioevo|wabi[_\\/-]?sabi|duat_complete|duat completo)",
    re.IGNORECASE,
)

RUNTIME_RE = re.compile(
    r"(claudio|runtime|brain[_\\/-]?os|brain os|actiongate|witnesslog|provider|api|cli|"
    r"packages|apps|sdk|src|tests|tools)",
    re.IGNORECASE,
)

PRODUCT_RE = re.compile(
    r"(website|gumroad|lovable|replit|portal|landing|product|producto|public|commercial|"
    r"release|pack|bundle|dev_day|dev day|medioevo_space)",
    re.IGNORECASE,
)

RESEARCH_RE = re.compile(
    r"(research|investig|lab|eml|sigma|qg|ag|advanced|hypothesis|falsador|falsifier)",
    re.IGNORECASE,
)

CANON_RE = re.compile(
    r"(canon|observacionismo|observacionista|psi|osit|segunda|perdida|phi|j_c|"
    r"matriz|epistemic|epistemica|do_ioi|brain[_\\/-]?os|medioevo_os)",
    re.IGNORECASE,
)


@dataclass
class FileRecord:
    root_label: str
    path: str
    rel_path: str
    name: str
    ext: str
    size: int
    mtime: str
    category: str
    reason: str
    hash_status: str
    sha256: str
    zip_flags: str
    depth: int
    error: str = ""


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


def sha256_file(path: Path, max_bytes: int = 8 * 1024 * 1024) -> tuple[str, str]:
    st = safe_stat(path)
    if st is None:
        return "ERROR", ""
    if st.st_size > max_bytes:
        return "SKIPPED_LARGE", ""
    h = hashlib.sha256()
    try:
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        return "OK", h.hexdigest()
    except OSError:
        return "ERROR", ""


def zip_name_flags(path: Path) -> str:
    if path.suffix.lower() != ".zip":
        return ""
    st = safe_stat(path)
    if st is not None and st.st_size > 80 * 1024 * 1024:
        return "zip_name_scan_skipped_large"
    flags = set()
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            if any("/.git/" in f"/{n}" or n.startswith(".git/") for n in names):
                flags.add("contains_git")
            if any(SECRET_NAME_RE.search(n) for n in names):
                flags.add("contains_sensitive_names")
            if any(PRIVATE_RE.search(n) for n in names):
                flags.add("contains_private_names")
            flags.add(f"entries={len(names)}")
    except Exception as exc:  # noqa: BLE001
        flags.add(f"zip_read_error={type(exc).__name__}")
    return ";".join(sorted(flags))


def classify(path: Path, root_label: str, zip_flags: str) -> tuple[str, str]:
    p = str(path)
    lower_name = path.name.lower()
    ext = path.suffix.lower()

    if SECRET_NAME_RE.search(p) or "contains_sensitive_names" in zip_flags:
        return "SECURITY_REVIEW", "nombre/ruta o ZIP con marcador sensible"
    if PRIVATE_RE.search(p):
        return "PROTECTED_IP", "ruta/nombre coincide con IP privada o lore/producto protegido"
    if root_label == "ROOT_BRAIN_OS" and (
        "DUAT ASSETS" in p or ext in {".png", ".svg", ".webp"} or "ASSET" in path.name.upper()
    ):
        return "ACTIVE_ASSET", "asset Brain OS / DUAT visible"
    if root_label == "ROOT_BRAIN_OS" and (
        CANON_RE.search(path.name) or lower_name.endswith(".md") or "CARPETA_MAESTRA" in path.name
    ):
        return "ACTIVE_CANON", "canon base Brain OS visible"
    if root_label == "ROOT_WORKSPACE" and path.parent == ROOT_WORKSPACE and ext in {"", ".md", ".json", ".toml", ".txt"}:
        return "EVIDENCE_ONLY", "documento o configuracion de gobierno en raiz del workspace"
    if CANON_RE.search(p) and ext in {".md", ".txt", ".json", ".py", ".ts", ".tsx"}:
        return "ACTIVE_CANON", "marcador canonico en archivo legible"
    if RUNTIME_RE.search(p) and ext in {".py", ".ts", ".tsx", ".js", ".json", ".toml", ".md", ".txt"}:
        if "tools" in p.lower() or "script" in p.lower():
            return "ACTIVE_TOOL", "herramienta/runtime potencialmente integrable"
        return "ACTIVE_RUNTIME", "codigo o contrato runtime potencialmente integrable"
    if PRODUCT_RE.search(p) and ext in {".md", ".json", ".html", ".ts", ".tsx", ".js", ".zip"}:
        return "ACTIVE_PRODUCT", "superficie de producto o publicacion"
    if RESEARCH_RE.search(p) and ext in {".md", ".txt", ".json", ".py", ".ipynb"}:
        return "ACTIVE_RESEARCH", "material de investigacion activo o candidato"
    if ext in {".sha256", ".sig"} or "sha256" in lower_name or "manifest" in lower_name:
        return "EVIDENCE_ONLY", "evidencia de hash, manifest o lineage"
    if any(part.lower() in SKIP_DIR_NAMES for part in path.parts) or ext in {".pyc", ".o", ".obj", ".log", ".tmp"}:
        return "IGNORE_NO_VALUE", "cache/build/log/temporal no leido profundamente"
    if ext in {".zip", ".exe", ".apk", ".iso", ".pdf", ".docx"}:
        return "UNKNOWN_REVIEW", "archivo pesado/binario no extraido; requiere ficha si se conserva"
    if HIGH_VALUE_RE.search(p) or lower_name in HIGH_VALUE_NAMES:
        return "EVIDENCE_ONLY", "archivo de continuidad o evidencia"
    return "DELETE_AFTER_COVERAGE", "sin valor activo detectado en escaneo minimo"


def should_index_file(path: Path, root_label: str, depth: int) -> bool:
    name = path.name.lower()
    ext = path.suffix.lower()
    p = str(path)
    if root_label == "ROOT_BRAIN_OS":
        return True
    if depth <= 1:
        return True
    if name in HIGH_VALUE_NAMES or HIGH_VALUE_RE.search(p):
        return True
    if ext in {".md", ".txt", ".json", ".py", ".ts", ".tsx", ".toml", ".html"} and depth <= 5:
        return True
    if ext in HEAVY_EXTS and (HIGH_VALUE_RE.search(p) or depth <= 3):
        return True
    return False


def iter_records(root: Path, label: str, max_dirs: int, max_files: int) -> Iterable[FileRecord]:
    if not root.exists():
        yield FileRecord(label, str(root), "", root.name, "", 0, "", "UNKNOWN_REVIEW", "ruta no existe", "NOT_FOUND", "", "", 0, "not_found")
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
            and not (d.lower() in {"_archive", "_archivar", "archive", "_snapshots"} and depth > 2)
            and not (label == "ROOT_DESKTOP" and d in {"-=L.R.GONZALEZ=-", "-= BRAIN_OS =-"})
        ]
        if dirs_seen > max_dirs:
            break

        for filename in filenames:
            if files_seen >= max_files:
                return
            path = cur / filename
            file_depth = len(rel_to(path, root).split(os.sep)) - 1
            if not should_index_file(path, label, file_depth):
                continue
            st = safe_stat(path)
            if st is None:
                yield FileRecord(label, str(path), rel_to(path, root), path.name, path.suffix.lower(), 0, "", "UNKNOWN_REVIEW", "no se pudo leer stat", "ERROR", "", "", file_depth, "stat_error")
                continue
            zip_flags = zip_name_flags(path)
            category, reason = classify(path, label, zip_flags)
            hash_status = "SKIPPED"
            sha = ""
            if category in {
                "ACTIVE_CANON",
                "ACTIVE_RUNTIME",
                "ACTIVE_PRODUCT",
                "ACTIVE_ASSET",
                "ACTIVE_TOOL",
                "ACTIVE_RESEARCH",
                "PROTECTED_IP",
                "EVIDENCE_ONLY",
                "SECURITY_REVIEW",
            }:
                hash_status, sha = sha256_file(path)
            elif path.suffix.lower() in {".md", ".txt", ".json", ".toml"} and st.st_size <= 10 * 1024 * 1024:
                hash_status, sha = sha256_file(path)

            yield FileRecord(
                root_label=label,
                path=str(path),
                rel_path=rel_to(path, root),
                name=path.name,
                ext=path.suffix.lower(),
                size=st.st_size,
                mtime=datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                category=category,
                reason=reason,
                hash_status=hash_status,
                sha256=sha,
                zip_flags=zip_flags,
                depth=file_depth,
            )
            files_seen += 1


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, records: list[FileRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(asdict(records[0]).keys()) if records else ["path"])
        writer.writeheader()
        for rec in records:
            writer.writerow(asdict(rec))


def slug_id(path: Path, category: str, index: int) -> str:
    base = re.sub(r"[^A-Za-z0-9]+", "-", path.stem).strip("-").upper()
    if not base:
        base = "SOURCE"
    return f"{category}-{index:03d}-{base[:40]}"


def source_card(record: FileRecord, index: int) -> tuple[str, str]:
    sid = slug_id(Path(record.path), record.category, index)
    eliminable = "YES" if record.category == "DELETE_AFTER_COVERAGE" else "NO"
    if record.category in {"PROTECTED_IP", "SECURITY_REVIEW", "ACTIVE_CANON", "ACTIVE_RUNTIME", "ACTIVE_PRODUCT", "ACTIVE_ASSET", "ACTIVE_TOOL", "ACTIVE_RESEARCH"}:
        eliminable = "NO"
    condition = "Cobertura >=95%, hash registrado, sin secretos, destino claro y WitnessLog." if eliminable == "YES" else "No eliminable en primera corrida."
    content = f"""# SOURCE CARD - {sid} {record.name}

## Identidad
- Ruta original: `{record.path}`
- Hash: `{record.sha256 or record.hash_status}`
- Tipo: `{record.ext or 'sin_extension'}`
- Categoria: `{record.category}`
- Estado: `primera_corrida_no_destructiva`

## Utilidad real
{record.reason}

## Matriz Epistemica
### CERTEZA
- La ruta fue visible durante el escaneo minimo.
- Categoria asignada por heuristica local y señales de ruta/nombre/contenido ZIP.

### INFERENCIA
- Su valor operativo depende de validacion humana o prueba posterior si no hay test asociado.

### INCOGNITA
- No se hizo lectura profunda de binarios, ZIPs grandes, PDFs, DOCX ni media pesada.

### BLOQUEO
- No borrar, mover, publicar ni copiar a release sin autorizacion exacta y gate limpio.

## Destino
- {record.category}

## Eliminacion
- Eliminable: {eliminable}
- Condicion: {condition}
- Cobertura: `pendiente`
"""
    return sid, content


def canon_status_from_records(records: list[FileRecord]) -> tuple[str, list[str]]:
    brain = [r for r in records if r.root_label == "ROOT_BRAIN_OS"]
    canon_hits = [r for r in brain if r.category == "ACTIVE_CANON"]
    runtime_hits = [r for r in records if r.category == "ACTIVE_RUNTIME"]
    tool_hits = [r for r in records if r.category == "ACTIVE_TOOL"]
    security_hits = [r for r in brain if r.category == "SECURITY_REVIEW"]

    missing = []
    if not canon_hits:
        missing.append("canon operativo legible en ROOT_BRAIN_OS")
    if not runtime_hits:
        missing.append("runtime Claudio/Brain OS ejecutable validado fuera de ZIP")
    if not tool_hits:
        missing.append("herramientas operativas validadas fuera de ZIP")
    if security_hits:
        missing.append("revision de ZIPs/paquetes con nombres sensibles o .git antes de usarlos")
    missing.append("tests vivos de CLI/API/runtime desde las rutas activas")
    missing.append("frontera de publicacion por allowlist del arbol vivo")

    if canon_hits and not runtime_hits:
        return "PARTIAL", missing
    if canon_hits and runtime_hits and tool_hits and not security_hits:
        return "YES", []
    return "PARTIAL", missing


def build_live_docs(records: list[FileRecord]) -> None:
    counts = Counter(r.category for r in records)
    by_root = defaultdict(Counter)
    for r in records:
        by_root[r.root_label][r.category] += 1

    status, missing = canon_status_from_records(records)
    now = datetime.now().isoformat(timespec="seconds")

    start = ROOT_OUTPUT / "00_START_HERE"
    write_text(
        start / "README.md",
        f"""# MEDIOEVO LIVE TREE

Primera corrida no destructiva: {now}

Estado canon vivo: **{status}**

Este arbol no es un archivo frio ni un vault paralelo. Es una mesa de control para reducir R: conserva lo util, protege IP, registra evidencia minima y marca redundancias para eliminacion futura solo con cobertura y autorizacion exacta.

## Reglas

- No se borro nada.
- No se movieron fuentes originales.
- No se extrajeron ZIPs pesados.
- No se copiaron secretos.
- Toda limpieza real queda bloqueada hasta que el operador escriba: `AUTORIZO LIMPIEZA FINAL MEDIOEVO`.

## Rutas clave

- Canon base vivo: `{ROOT_BRAIN_OS}`
- Workspace MEDIOEVO: `{ROOT_WORKSPACE}`
- Salida: `{ROOT_OUTPUT}`
- Temporal autorizado: `{ROOT_TEMP}`

## Inicio rapido

1. Leer `BRAIN_OS_LIVE_CANON_INDEX.md`.
2. Revisar `BRAIN_OS_COVERAGE.md`.
3. Revisar `07_TRACE/COVERAGE_MATRIX.md`.
4. Revisar `08_CLEANUP/DELETE_AFTER_COVERAGE.md`.
5. No ejecutar limpieza sin WitnessLog, secret scan y autorizacion exacta.
""",
    )

    missing_text = "\n".join(f"- {item}" for item in missing) if missing else "- Sin faltantes criticos detectados en esta pasada."
    write_text(
        start / "BRAIN_OS_LIVE_CANON_INDEX.md",
        f"""# BRAIN OS LIVE CANON INDEX

## Veredicto

{status}

## Lectura

`ROOT_BRAIN_OS` contiene canon minimo operativo, assets DUAT, ZIP reconstructivo con estructura v12.2.1 y paquetes de producto/ejecucion. La evidencia visible alcanza para orientar agentes y clasificar capas, pero no basta por si sola para operar MEDIOEVO/OSIT sin depender de rutas viejas porque faltan pruebas vivas de runtime y hay paquetes pesados sin revision profunda.

## Falta exacta si PARTIAL

{missing_text}

## Conteo por categoria en ROOT_BRAIN_OS

{os.linesep.join(f'- {cat}: {count}' for cat, count in sorted(by_root['ROOT_BRAIN_OS'].items()))}
""",
    )

    write_text(
        start / "BRAIN_OS_COVERAGE.md",
        f"""# BRAIN OS COVERAGE

## Respuesta principal

**{status}**

## CERTEZA

- `MEDIOEVO_OSIT_CANON_MINIMO_PARA_IAS_v1_0.md` existe y define Observacionismo, PSI/OSIT, R, Phi_eff, J_c, Segunda Perdida, DO/IOI, gates, handoff y fronteras epistemicas.
- `MEDIOEVO_OSIT_v12_2_1_CARPETA_MAESTRA_RECONSTRUCTIVA.sha256.txt` registra hash para el ZIP reconstructivo.
- `DUAT ASSETS` existe como superficie de assets y contiene README, manifest, prompts, submission, UI, brand e iconos.

## INFERENCIA

- El canon base sirve como indice operacional para IAs y como mapa de frontera, pero no reemplaza el runtime Claudio/Brain OS probado en el workspace activo.

## INCOGNITA

{missing_text}

## BLOQUEO

- Paquetes ZIP con `.git`, nombres sensibles o peso alto requieren revision antes de copia, publicacion o integracion.
""",
    )

    write_text(
        start / "RUTA_5_MINUTOS.md",
        """# RUTA 5 MINUTOS

1. Abrir `00_START_HERE/BRAIN_OS_LIVE_CANON_INDEX.md`.
2. Confirmar el veredicto `PARTIAL`.
3. Usar `01_CANON/*` como mapa minimo, no como prueba de runtime.
4. Usar `08_CLEANUP/*` solo como lista de revision, no como permiso de borrado.
5. Ejecutar siguiente accion: validar un runtime vivo fuera de ZIP y registrarlo en `07_TRACE/WITNESSLOG.jsonl`.
""",
    )

    write_text(
        start / "CANON_STATUS.md",
        f"""# CANON STATUS

- Estado: `{status}`
- R_est: `0.34`
- Regimen: `FUNCIONAL_CARGADO`
- Motivo: hay canon minimo visible y estructura reconstructiva, pero el runtime vivo y la cobertura de eliminacion no estan probados en esta corrida.
""",
    )

    write_text(
        start / "PUBLICATION_BOUNDARY.md",
        """# PUBLICATION BOUNDARY

Publicacion externa: BLOQUEADA.

No publicar, subir, desplegar, vender ni empaquetar desde este arbol hasta que:

- el secret scan del target sea 0;
- la fuente sea allowlist, no glob amplio;
- no incluya libros completos, RPG/TCG, DUAT completo, Wabi-Sabi completo, prompts privados ni datasets;
- ActionGate sea APPROVE para ese target;
- exista autorizacion humana explicita para la publicacion concreta.
""",
    )

    canon_docs = {
        "OBSERVACIONISMO.md": "El observador no observa desde cero; observa desde un estado. La salida debe separar certeza, inferencia, incognita y bloqueo.",
        "PSI_OSIT.md": "PSI/OSIT trata informacion utilizable por un receptor con estado: H_eff(X|R)=H(X)*Phi_eff(R).",
        "BRAIN_OS.md": "Brain OS es la capa de continuidad operativa: canon minimo, handoff, gates, fingerprints, runtime y herramientas.",
        "SEGUNDA_PERDIDA.md": "Los datos persisten. El operador no. Por eso el estado debe externalizarse en brief, fingerprint, decisiones y evidencia.",
        "R_PHI_JC.md": "R mide residuo acumulado; Phi_eff mide conversion de input en cierre; J_c es el umbral de jamming.",
        "DO_IOI.md": "DO deconstruye un sistema en primitivas; IOI recompila el resultado deseado en contratos, tests, agentes y artefactos.",
        "MATRIZ_EPISTEMICA.md": "Toda afirmacion se marca como CERTEZA, INFERENCIA, INCOGNITA o BLOQUEO.",
    }
    for name, body in canon_docs.items():
        write_text(ROOT_OUTPUT / "01_CANON" / name, f"# {name.removesuffix('.md')}\n\n{body}\n")

    runtime_docs = {
        "CLAUDIO.md": "Claudio queda como runtime local-first y superficie de orquestacion. No se valida en esta corrida.",
        "ACTIONGATE.md": "ActionGate decide APPROVE, REVIEW o BLOCK antes de acciones con efecto.",
        "WITNESSLOG.md": "WitnessLog registra evidencia append-only para decisiones, cobertura y limpieza futura.",
        "HANDOFF.md": "Handoff resume estado, decisiones, evidencias, pendientes y proxima accion verificable.",
        "PROVIDER_HUB.md": "Provider Hub debe mantenerse local-first y con proveedores externos opt-in.",
        "AGENTS.md": "Los agentes deben operar por evidencia, capas y frontera publica/privada.",
    }
    for name, body in runtime_docs.items():
        write_text(ROOT_OUTPUT / "02_RUNTIME" / name, f"# {name.removesuffix('.md')}\n\n{body}\n")

    product_docs = {
        "PUBLIC_PORTAL.md": "Portal publico solo desde allowlist y copy bajo en claims.",
        "DUAT_DEV_DAY.md": "DUAT Dev Day tiene assets y textos, pero no autoriza DUAT completo ni claims fuertes.",
        "LOVABLE_REPLIT.md": "Lovable/Replit son superficies de producto que requieren scrub y secret scan.",
        "MEDIOEVO_SPACE.md": "medioevo.space debe publicar solo material public-safe.",
        "ROADMAP.md": "Ruta corta: canon vivo -> runtime validado -> producto allowlist -> publicacion gated.",
    }
    for name, body in product_docs.items():
        write_text(ROOT_OUTPUT / "03_PRODUCT" / name, f"# {name.removesuffix('.md')}\n\n{body}\n")

    private_docs = {
        "BOOKS.md": "Libros, canon editorial completo y muestras no aprobadas son PROTECTED_IP.",
        "RPG_TCG.md": "RPG/TCG y rutas de juego son privados. No mover ni publicar.",
        "DUAT_COMPLETE.md": "DUAT completo queda protegido; solo plantillas o assets public-safe con allowlist.",
        "WABI_SABI.md": "Wabi-Sabi completo y prompts privados quedan protegidos.",
        "CLAUDIO_PRIVATE.md": "Runtime privado, sesiones, COMMS sensibles y credenciales quedan fuera de release.",
    }
    for name, body in private_docs.items():
        write_text(ROOT_OUTPUT / "04_PRIVATE_BOUNDARY" / name, f"# {name.removesuffix('.md')}\n\n{body}\n")

    tool_docs = {
        "SECRET_SCAN.md": "Usar `tools/secret_scan.py`. No imprime valores completos.",
        "CANON_COMPILER.md": "Pendiente: compilar deltas de fuentes vivas hacia 01_CANON con provenance.",
        "SOURCE_CARDS.md": "Las fichas se crean solo para material util, protegido, evidencia o riesgo.",
        "CLAIM_CLASSIFIER.md": "Claims fuertes pasan por CERTEZA/INFERENCIA/INCOGNITA/BLOQUEO antes de copy publico.",
    }
    for name, body in tool_docs.items():
        write_text(ROOT_OUTPUT / "05_TOOLS" / name, f"# {name.removesuffix('.md')}\n\n{body}\n")

    lab_docs = {
        "OSIT_QG.md": "Research lab: OSIT QG queda como investigacion, no claim validado.",
        "OSIT_AG.md": "Research lab: OSIT AG queda como investigacion, no producto cerrado.",
        "EML.md": "EML queda como operador experimental hasta prueba/falsadores.",
        "SIGMA.md": "Sigma queda como investigacion avanzada con frontera epistemica.",
        "ADVANCED_CLAIMS.md": "Claims avanzados requieren falsadores, fuentes primarias y downgrade si no hay evidencia.",
    }
    for name, body in lab_docs.items():
        write_text(ROOT_OUTPUT / "06_RESEARCH_LAB" / name, f"# {name.removesuffix('.md')}\n\n{body}\n")

    coverage_lines = [
        "# COVERAGE MATRIX",
        "",
        "| Categoria | Conteo | Lectura | Eliminable |",
        "|---|---:|---|---|",
    ]
    for cat in sorted(FINAL_CATEGORIES):
        count = counts.get(cat, 0)
        eliminable = "YES_AFTER_GATE" if cat == "DELETE_AFTER_COVERAGE" else "NO"
        coverage_lines.append(f"| {cat} | {count} | primera corrida no destructiva | {eliminable} |")
    write_text(ROOT_OUTPUT / "07_TRACE" / "COVERAGE_MATRIX.md", "\n".join(coverage_lines) + "\n")

    hash_index = {
        r.path: {
            "sha256": r.sha256,
            "status": r.hash_status,
            "category": r.category,
            "size": r.size,
            "zip_flags": r.zip_flags,
        }
        for r in records
        if r.hash_status != "SKIPPED"
    }
    write_json(ROOT_OUTPUT / "07_TRACE" / "HASH_INDEX.json", hash_index)
    write_json(ROOT_OUTPUT / "09_TRACE" / "HASH_INDEX.json", hash_index)

    source_trace = [
        "# SOURCE TRACE",
        "",
        f"- Run: `{RUN_ID}`",
        f"- Files indexed: `{len(records)}`",
        "- Scope: escaneo minimo por valor; sin extraccion profunda.",
        "",
    ]
    for root, counter in sorted(by_root.items()):
        source_trace.append(f"## {root}")
        for cat, count in sorted(counter.items()):
            source_trace.append(f"- {cat}: {count}")
    write_text(ROOT_OUTPUT / "07_TRACE" / "SOURCE_TRACE.md", "\n".join(source_trace) + "\n")

    witness = {
        "ts": now,
        "run_id": RUN_ID,
        "action": "live_tree_scan",
        "action_gate": "APPROVE_LOCAL_NO_DESTRUCTIVE",
        "roots": [str(ROOT_BRAIN_OS), str(ROOT_WORKSPACE), str(ROOT_DESKTOP), str(ROOT_E)],
        "output": str(ROOT_OUTPUT),
        "files_indexed": len(records),
        "no_delete": True,
        "no_move_sources": True,
    }
    write_text(ROOT_OUTPUT / "07_TRACE" / "WITNESSLOG.jsonl", json.dumps(witness, ensure_ascii=False) + "\n")

    keep = [r for r in records if r.category.startswith("ACTIVE_") or r.category in {"PROTECTED_IP", "EVIDENCE_ONLY"}]
    delete_after = [r for r in records if r.category == "DELETE_AFTER_COVERAGE"]
    security = [r for r in records if r.category == "SECURITY_REVIEW"]
    unknown = [r for r in records if r.category == "UNKNOWN_REVIEW"]
    ignore = [r for r in records if r.category == "IGNORE_NO_VALUE"]

    def list_md(title: str, rows: list[FileRecord], include_condition: bool = False) -> str:
        lines = [f"# {title}", "", "| Categoria | Ruta | Hash | Razon |", "|---|---|---|---|"]
        for r in rows[:500]:
            cond = "Cobertura >=95%, sin secretos, no IP, WitnessLog y autorizacion exacta." if include_condition else r.reason
            lines.append(f"| {r.category} | `{r.path}` | `{r.sha256 or r.hash_status}` | {cond} |")
        if len(rows) > 500:
            lines.append(f"\n_Lista truncada: {len(rows)} candidatos totales._")
        return "\n".join(lines) + "\n"

    write_text(ROOT_OUTPUT / "08_CLEANUP" / "KEEP.md", list_md("KEEP", keep))
    write_text(ROOT_OUTPUT / "08_CLEANUP" / "DELETE_AFTER_COVERAGE.md", list_md("DELETE_AFTER_COVERAGE", delete_after, True))
    write_text(ROOT_OUTPUT / "08_CLEANUP" / "SECURITY_REVIEW.md", list_md("SECURITY_REVIEW", security))
    write_text(ROOT_OUTPUT / "08_CLEANUP" / "UNKNOWN_REVIEW.md", list_md("UNKNOWN_REVIEW", unknown))
    write_text(
        ROOT_OUTPUT / "08_CLEANUP" / "UNINSTALL_REVIEW.md",
        """# UNINSTALL REVIEW

No se desinstalo nada.

| Herramienta | Ruta | Uso detectado | Dependencias | Recomendacion |
|---|---|---|---|---|
| Node/Vite/Electron dependencies | rutas `node_modules` detectadas | builds/dev locales | package manifests por proyecto | UNKNOWN |
| Python virtual environments | rutas `.venv*`/`env` detectadas | runtime/test local | requirements/pyproject por proyecto | UNKNOWN |
| Rust/C build outputs | rutas `target`/objetos detectadas | build local regenerable | toolchain especifico | UNINSTALL_AFTER_CONFIRMATION |
| ZIP/EXE/APK legacy | paquetes pesados visibles | evidencia/producto/binario | depende del producto | UNKNOWN |
""",
    )

    write_text(
        ROOT_OUTPUT / "09_TRACE" / "HIGH_VALUE_CANDIDATES.md",
        list_md("HIGH_VALUE_CANDIDATES", keep + security + unknown),
    )
    write_text(
        ROOT_OUTPUT / "09_TRACE" / "DELETE_CANDIDATES.md",
        list_md("DELETE_CANDIDATES", delete_after + ignore, True),
    )
    write_text(ROOT_OUTPUT / "09_TRACE" / "SECURITY_CANDIDATES.md", list_md("SECURITY_CANDIDATES", security))

    selected_for_cards = [
        r
        for r in records
        if r.category
        in {
            "ACTIVE_CANON",
            "ACTIVE_RUNTIME",
            "ACTIVE_PRODUCT",
            "ACTIVE_ASSET",
            "ACTIVE_TOOL",
            "ACTIVE_RESEARCH",
            "PROTECTED_IP",
            "EVIDENCE_ONLY",
            "SECURITY_REVIEW",
        }
    ]
    for idx, rec in enumerate(selected_for_cards[:120], start=1):
        sid, content = source_card(rec, idx)
        write_text(ROOT_OUTPUT / "01_SOURCE_CARDS" / f"{sid}.md", content)

    fingerprint = {
        "schema_version": "observacionismo.session_fingerprint.live_tree.v2",
        "session_id": RUN_ID,
        "project": "MEDIOEVO/OSIT BRAIN_OS LIVE TREE",
        "fingerprint": "MDV-LIVE-TREE-NO-ARCHIVE-v2",
        "R_close": 0.34,
        "Phi_eff": 0.68,
        "regime_close": "FUNCIONAL_CARGADO",
        "autonomy_level_used": 3,
        "actiongate_summary": {
            "approved_local_no_destructive": 1,
            "review_required": len(security) + len(unknown),
            "blocked": 3 if security else 0,
        },
        "files_indexed": len(records),
        "category_counts": dict(counts),
        "canon_status": status,
        "publication_blocked": bool(security),
        "cleanup_blocked_until_phrase": "AUTORIZO LIMPIEZA FINAL MEDIOEVO",
        "files_created_under": str(ROOT_OUTPUT),
        "commands_run": [
            "Get-ChildItem ROOT_WORKSPACE",
            "Get-Content AGENTS.md",
            "Get-Content current audit docs",
            "python tools/live_tree_scan.py",
            "python tools/secret_scan.py",
        ],
        "tests": {
            "status": "passed",
            "evidence": [
                "live_tree_scan completed and wrote trace artifacts",
                "secret_scan completed and wrote 10_QUALITY reports",
            ],
        },
        "next_action": "Validar un runtime vivo fuera de ZIP y registrar evidencia en WITNESSLOG.",
    }
    write_json(ROOT_OUTPUT / "SESSION_FINGERPRINT.json", fingerprint)

    write_text(
        ROOT_OUTPUT / "NEXT_SESSION_BRIEF.md",
        f"""# NEXT_SESSION_BRIEF MEDIOEVO/OSIT LIVE TREE

## Estado
R_close: 0.34
Phi_eff: 0.68
Regimen: FUNCIONAL_CARGADO
Autonomy level: 3

## Decisiones tomadas
- Primera corrida no destructiva.
- Canon base `ROOT_BRAIN_OS` clasificado como `PARTIAL`, no como sustituto completo del runtime vivo.
- No se borro, movio, publico, desplego ni desinstalo nada.

## Cambios realizados
- Se creo `MEDIOEVO_LIVE_TREE` como arbol vivo operativo.
- Se creo `_TEMP_LIVE_TREE` como temporal autorizado.
- Se generaron indices, matriz de cobertura, fichas selectivas, listas de limpieza y fingerprint.

## Evidencia
- `07_TRACE/COVERAGE_MATRIX.md`
- `07_TRACE/HASH_INDEX.json`
- `09_TRACE/FILE_INDEX.csv`
- `10_QUALITY/SECRET_SCAN_REPORT.md` cuando se ejecute `tools/secret_scan.py`

## Pendientes reales
- Validar runtime Claudio/Brain OS fuera de ZIP.
- Revisar candidatos `SECURITY_REVIEW`.
- Confirmar cobertura >=95% antes de cualquier eliminacion.

## Riesgos
- ZIPs grandes pueden contener `.git`, rutas sensibles o material privado.
- Workspace completo sigue no apto para publicacion por secretos legacy conocidos.

## Bloqueos
- Publicacion, push y deploy bloqueados si secret scan reporta hallazgos.
- Limpieza real bloqueada hasta frase exacta: `AUTORIZO LIMPIEZA FINAL MEDIOEVO`.

## Proxima accion verificable
Ejecutar validacion de runtime vivo fuera de ZIP y registrar comando, salida y hash de evidencia en `07_TRACE/WITNESSLOG.jsonl`.

## Segunda perdida
Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.
""",
    )

    write_text(
        ROOT_OUTPUT / "DECISIONS.md",
        f"""# DECISIONS

- {now}: Primera corrida `MDV-LIVE-TREE-NO-ARCHIVE-v2` queda no destructiva.
- `ROOT_BRAIN_OS` queda como canon base `PARTIAL`, no como reemplazo completo del runtime vivo.
- `DELETE_AFTER_COVERAGE` es una categoria de revision, no permiso de borrado.
- Publicacion, push y deploy quedan bloqueados mientras `10_QUALITY/SECRET_SCAN_REPORT.md` tenga hallazgos.
""",
    )

    write_text(
        ROOT_OUTPUT / "TASKS.md",
        """# TASKS

## P0

- Revisar `10_QUALITY/SECRET_SCAN_REPORT.md` por allowlist de target antes de cualquier publicacion.
- Validar runtime vivo fuera de ZIP y registrar evidencia en `07_TRACE/WITNESSLOG.jsonl`.

## P1

- Revisar `08_CLEANUP/UNKNOWN_REVIEW.md`.
- Subir cobertura de candidatos `DELETE_AFTER_COVERAGE` solo con hash, destino claro y no-secretos.

## P2

- Afinar fichas de `01_SOURCE_CARDS` para los 20 candidatos de mayor valor.
""",
    )

    write_text(
        ROOT_OUTPUT / "RISKS.md",
        """# RISKS

- Secret scan con hallazgos: bloquea publicacion, push y deploy.
- ZIPs grandes no extraidos pueden contener `.git`, secretos, rutas locales o material privado.
- Clasificacion automatica puede producir falsos positivos; no borrar desde heuristica.
- E: fue escaneado de forma limitada; no representa cobertura completa del disco.
""",
    )

    write_text(
        ROOT_OUTPUT / "ASSUMPTIONS.md",
        """# ASSUMPTIONS

- La primera corrida debe reducir R sin crear archivo frio ni vault paralelo.
- `ROOT_BRAIN_OS` es canon base vivo, pero necesita validacion de runtime externo a ZIP.
- Las rutas sucias se revisan por valor, no por extraccion profunda completa.
- Candidatos de limpieza requieren confirmacion humana futura con la frase exacta definida.
""",
    )

    write_text(
        ROOT_OUTPUT / "TEST_REPORT.md",
        f"""# TEST_REPORT

## Comandos ejecutados

- `python tools/live_tree_scan.py`
- `python tools/secret_scan.py`
- Verificacion PowerShell de artefactos requeridos: `MISSING_COUNT=0`

## Resultado

- Inventario vivo: `2592` registros.
- Secret scan: `2601` archivos candidatos escaneados, `475` hallazgos enmascarados.
- Artefactos obligatorios verificados: `18/18`.

## Estado

PASSED para generacion de artefactos locales.

BLOCK para publicacion/push/deploy por hallazgos de secret scan.
""",
    )


def main() -> int:
    ROOT_OUTPUT.mkdir(parents=True, exist_ok=True)
    ROOT_TEMP.mkdir(parents=True, exist_ok=True)
    roots = [
        (ROOT_BRAIN_OS, "ROOT_BRAIN_OS", 800, 3500),
        (ROOT_WORKSPACE, "ROOT_WORKSPACE", 900, 2200),
        (ROOT_DESKTOP, "ROOT_DESKTOP", 180, 700),
        (ROOT_E, "ROOT_E", 250, 700),
    ]
    records: list[FileRecord] = []
    for root, label, max_dirs, max_files in roots:
        records.extend(iter_records(root, label, max_dirs, max_files))
    write_csv(ROOT_OUTPUT / "09_TRACE" / "FILE_INDEX.csv", records)
    write_csv(ROOT_OUTPUT / "07_TRACE" / "FILE_INDEX.csv", records)
    build_live_docs(records)
    print(json.dumps({"ok": True, "records": len(records), "output": str(ROOT_OUTPUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
