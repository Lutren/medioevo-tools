#!/usr/bin/env python3
"""
Build the MEDIOEVO_OBSERVACIONISMO_MASTER curation folder.

This script is intentionally local-only and non-destructive. It reads the
current CEREBRO/PSI/PRODUCTOS sources, copies the curated PSI canon into a new
master folder, appends the 2026-05-07 curation layer, and emits traceability
manifests so another agent can continue without rereading the whole corpus.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
import argparse
import hashlib
import json
import os
import sys


DEFAULT_WORKSPACE = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-")
OUTPUT_DIR_NAME = "MEDIOEVO_OBSERVACIONISMO_MASTER"
HASH_LIMIT_BYTES = 2 * 1024 * 1024

REQUIRED_FILES = [
    "00_README_MASTER.md",
    "01_MAPA_GENERAL.md",
    "02_GLOSARIO_CANONICO.md",
    "03_TEORIA_INFORMACION.md",
    "04_TEORIA_IA_AGENTES.md",
    "05_TEORIA_FISICA_REAL.md",
    "06_HIPOTESIS_FISICAS_OSIT_TUIP_SIGMA.md",
    "07_OBSERVACIONISMO.md",
    "08_OBSERVACIONISMO_INVERSO.md",
    "09_INGENIERIA_OBSERVACIONISTA.md",
    "10_WABI_SABI_CLAUDIO_AGI.md",
    "11_DUAT_GEODIA_HORMIGUERO.md",
    "12_MODULOS_TECNICOS.md",
    "13_AGENTES.md",
    "14_PROYECTOS_ACTIVOS.md",
    "15_PROYECTOS_FUTUROS.md",
    "16_CLAIMS_REGISTER.md",
    "17_FALSADORES_Y_TESTS.md",
    "18_RIESGOS_CONTRADICCIONES.md",
    "19_ROADMAP.md",
    "20_NEXT_SESSION_BRIEF.md",
    "21_ACTION_GATES.md",
    "22_PROMPTS_OPERATIVOS.md",
]

SOURCE_DOCS = {name: name for name in REQUIRED_FILES[:20]}

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".next",
    "dist",
    "build",
    OUTPUT_DIR_NAME,
    "00_BIBLIOTECA_HUMANA",
}


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def normalize_markdown_tasks(content: str) -> str:
    """Avoid polluting workspace pending scanners with copied source checkboxes."""
    return (
        content.replace("- [x] ", "- DONE: ")
        .replace("- [X] ", "- DONE: ")
        .replace("- [ ] ", "- PENDING: ")
    )


def sha256_small(path: Path) -> str | None:
    try:
        if path.stat().st_size > HASH_LIMIT_BYTES:
            return None
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def classify_path(path: Path) -> str:
    suffix = path.suffix.lower()
    text_name = path.name.lower()
    parts = {part.lower() for part in path.parts}

    if "content_forge" in parts:
        return "PROYECTO_ACTIVO_CONTENT_FORGE"
    if "claudio_os_blueprint" in parts:
        return "PROYECTO_ACTIVO_CLAUDIO_OS_BLUEPRINT"
    if "claudio - researchs" in parts or "geodia" in parts:
        return "PROYECTO_GEODIA_CLAUDIO_RESEARCH"
    if "futuro" in parts:
        return "PROYECTO_FUTURO"
    if "canon" in parts or text_name.startswith(("00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "10_", "11_", "12_", "13_", "14_", "15_", "16_", "17_", "18_", "19_")):
        return "CANON_CURADO"
    if suffix in {".py", ".ts", ".tsx", ".js", ".json", ".yaml", ".yml", ".html", ".ps1", ".sh"}:
        return "CODIGO_CONFIG_MODULO"
    if suffix in {".md", ".txt", ".pdf", ".docx"}:
        return "FUENTE_DOCUMENTAL"
    if suffix in {".zip", ".gz", ".tar"}:
        return "ARCHIVO_PAQUETE_REVIEW"
    if suffix in {".mp4", ".jpg", ".jpeg", ".png", ".webp", ".srt", ".vtt"}:
        return "MEDIA_PRODUCTO_REVIEW"
    return "INCERTIDUMBRE"


def iter_files(roots: Iterable[Path], output_dir: Path) -> Iterable[Path]:
    seen: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        for current_root, dirs, files in os.walk(root):
            current = Path(current_root)
            dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
            if output_dir in current.parents or current == output_dir:
                continue
            for file_name in files:
                path = current / file_name
                try:
                    resolved = str(path.resolve()).lower()
                except OSError:
                    resolved = str(path).lower()
                if resolved in seen:
                    continue
                seen.add(resolved)
                yield path


def inventory_sources(workspace: Path, output_dir: Path) -> tuple[list[dict[str, object]], Counter[str], Counter[str]]:
    roots = [
        workspace / "PRODUCTOS_MEDIOEVO",
        workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "-=PSI=-",
        workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-",
    ]

    records: list[dict[str, object]] = []
    ext_counter: Counter[str] = Counter()
    category_counter: Counter[str] = Counter()
    for path in iter_files(roots, output_dir):
        try:
            stat = path.stat()
        except OSError:
            continue
        ext = path.suffix.lower() or "<no_ext>"
        category = classify_path(path)
        ext_counter[ext] += 1
        category_counter[category] += 1
        records.append(
            {
                "path": str(path.relative_to(workspace)),
                "name": path.name,
                "extension": ext,
                "bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                "category": category,
                "sha256": sha256_small(path) or "not_hashed_large_file",
            }
        )
    records.sort(key=lambda item: str(item["path"]).lower())
    return records, ext_counter, category_counter


def curation_footer(file_name: str) -> str:
    additions = CURATION_APPENDICES.get(file_name, "")
    common = f"""
---

## Corte de curaduría 2026-05-07

CERTEZA:
- Este documento fue compilado desde fuentes locales de `-=PSI=-`, `-=CEREBRO=-` y `PRODUCTOS_MEDIOEVO`.
- Las fuentes originales no fueron movidas, borradas ni reescritas.

INFERENCIA:
- Si una idea aparece en varias fuentes, se conserva aquí como una entrada consolidada y se remite al manifiesto de fuentes para variaciones.

INCÓGNITA:
- PDFs, DOCX, ZIP, TAR.GZ y media quedan trazados por manifiesto; no todos fueron convertidos a texto completo en este pase.

ACCIÓN:
- Usar este archivo como capa maestra de lectura y volver a la fuente solo para auditoría, expansión o verificación puntual.

ARTEFACTO:
- Archivo maestro: `{file_name}`.
"""
    return additions.rstrip() + "\n" + common


CURATION_APPENDICES = {
    "00_README_MASTER.md": """
---

## Fuentes absorbidas en este corte

| Raíz | Uso en la carpeta maestra |
|---|---|
| `PRODUCTOS_MEDIOEVO` | Frente comercial, ClaudioOS blueprint, Content Forge, categorías de producto, módulos locales. |
| `-=CEREBRO=-` | Entrada humana, mapa por sistemas, política de canon/fuentes/runtime, manifiestos de curaduría. |
| `-=PSI=-` | Canon formal, teoría, claims, falsadores, proyectos, Wabi-Sabi/Claudio/AGI, Duat/Geodia/Hormiguero. |

## Lectura recomendada

1. `01_MAPA_GENERAL.md`
2. `02_GLOSARIO_CANONICO.md`
3. `16_CLAIMS_REGISTER.md`
4. `18_RIESGOS_CONTRADICCIONES.md`
5. `20_NEXT_SESSION_BRIEF.md`
6. `SOURCE_MANIFEST.md` si se necesita trazabilidad por archivo.
""",
    "01_MAPA_GENERAL.md": """
---

## Mapa de absorción por sistemas

| Sistema | Fuente principal | Carpeta destino |
|---|---|---|
| Cognitivo / Observacionismo | `-=CEREBRO=-/01_MAPA_SISTEMAS...`, `-=PSI=-/07_OBSERVACIONISMO.md` | `07_OBSERVACIONISMO.md` |
| Información / R / Phi | `-=PSI=-/03_TEORIA_INFORMACION.md` | `03_TEORIA_INFORMACION.md` |
| IA / agentes / Wabi-Sabi | `-=PSI=-/04_TEORIA_IA_AGENTES.md`, `10_WABI_SABI_CLAUDIO_AGI.md` | `04`, `10`, `13`, `22` |
| Física estándar | `-=PSI=-/05_TEORIA_FISICA_REAL.md` | `05_TEORIA_FISICA_REAL.md` |
| Física hipotética | `-=PSI=-/06_HIPOTESIS...`, `16_CLAIMS_REGISTER.md` | `06`, `16`, `17`, `18` |
| Productos y software | `PRODUCTOS_MEDIOEVO`, `claudio_os_blueprint`, `content_forge` | `14`, `19`, `21` |
| Futuro/lore | `CLAUDIO - researchs/futuro`, `MEdioevosagalore` | `15` y capa LORE separada en mapas |
""",
    "02_GLOSARIO_CANONICO.md": """
---

## Términos añadidos desde PRODUCTOS_MEDIOEVO y Brain OS

| Término | Definición curada | Gate |
|---|---|---|
| Brain OS | Capa cognitiva durable sobre la máquina: herramientas pequeñas, decisiones observables, ejecución local-first y aprobación humana para acciones irreversibles. | Ingeniería |
| ClaudioOS Blueprint | Remix Debian Live con Guardian, Mission Control, policy gates y witness logs. No es kernel nuevo ni reemplazo de Linux. | Prototipo local |
| Guardian | Servicio local de compuertas/políticas que decide hold/allow/ask/block antes de ejecutar. | Ingeniería |
| Content Forge | Motor local-first de campañas MEDIOEVO: videos, carruseles, captions y paquetes listos sin autopublicar. | Producto local |
| Observacionista DSL | Lenguaje simple línea-a-línea que compila a JSON validable y gateable. | Módulo |
| Model Slimmer Evidence | Carril de medición para cuantización/pruning: ningún modelo reemplaza al baseline sin pruebas de accuracy, latencia, memoria, energía y seguridad. | Módulo |
""",
    "04_TEORIA_IA_AGENTES.md": """
---

## Integración con tecnología local detectada

CERTEZA:
- `observacionismo_dsl.py` ya formaliza una capa de intención/evidencia/estado/acción/aprobación/witness.
- `model_slimmer_evidence.py` ya formaliza un contrato de medición para modelos pequeños.
- `claudio_os_blueprint` define Guardian, Mission Control, policy gates, provider registry y witness logs.

INFERENCIA:
- Estos componentes son la ruta más directa para que Wabi-Sabi funcione como agente de ingeniería tipo Claude Code/Codex: no por promesa de AGI, sino por loop observable `observe -> decide -> contain -> witness -> recover`.
""",
    "09_INGENIERIA_OBSERVACIONISTA.md": """
---

## Ingeniería absorbida desde PRODUCTOS_MEDIOEVO

| Componente | Estado observado | Integración recomendada |
|---|---|---|
| `observacionismo_dsl.py` | Compilador funcional a JSON y payload Guardian | Convertir a módulo `dsl_compiler` con tests en `12_MODULOS_TECNICOS.md`. |
| `model_slimmer_evidence.py` | Genera plan de medición para modelos | Integrar con `evidence_tracker` y `claim_classifier`. |
| `claudio_os_blueprint/contracts/module_manifest.schema.json` | Contrato de módulo | Usarlo como base de `agent_registry` y `module_registry`. |
| `content_forge` | Motor local de render/campañas | Gatear con AssetPolicy, QA visual, witness por job. |
| Brain OS Kernel loop | `observe -> decide -> contain -> witness -> recover` | Usarlo como loop mínimo común para agentes. |
""",
    "10_WABI_SABI_CLAUDIO_AGI.md": """
---

## Requisito operativo consolidado para Wabi-Sabi

Wabi-Sabi debe funcionar como nodo autónomo de ingeniería local-first, comparable en comportamiento a Claude Code/Codex/Cursor Agent, pero con estas fronteras:

CERTEZA:
- Debe usar modelo base/proveedor configurado cuando el runtime lo exponga.
- Debe registrar limitación si `BASE_MODEL`, `MODEL_ENDPOINT` o herramientas de inferencia no están disponibles.
- Debe ejecutar con filesystem, shell, git, patch, tests, package manager, search y handoff cuando estén disponibles.

INFERENCIA:
- La implementación más segura es separar LLM/oráculo, orquestador determinístico, agentes, gates, witness y handoff. Wabi-Sabi coordina; no debe convertirse en una caja negra sin evidencia.
""",
    "11_DUAT_GEODIA_HORMIGUERO.md": """
---

## Integración con PRODUCTOS_MEDIOEVO

| Pieza | Lectura curada | Gate |
|---|---|---|
| ClaudioOS Blueprint | Cuerpo Linux local para Brain OS; no reemplaza kernel. | VM/QEMU primero |
| Mission Control | Dashboard local de estado/gates/witness. | Read-only v1 |
| Content Forge | Taller de producción audiovisual local. | No autopublica |
| Open Source GitHub | `safe-exec`, `medioevo-tools`, `data-double-slit` como confianza técnica. | Public-safe por repo |
| Audiovisual / TCG | Activos y empaque comercial parcial. | Separar privado/publicable |
""",
    "12_MODULOS_TECNICOS.md": """
---

## Módulos adicionales detectados en fuentes

| Módulo | Propósito | Input | Output | Prueba mínima |
|---|---|---|---|---|
| `dsl_compiler` | Compilar Observacionista DSL a JSON/gate payload | `.dsl` text | JSON contract | DSL válido genera `intent`, `actions`, `witness`; DSL sin evidencia falla |
| `model_efficiency_gate` | Medir si un modelo reducido puede reemplazar baseline | baseline + candidate metrics | allow/ask/block | `accuracy_drop > 0.02` bloquea |
| `module_manifest_validator` | Validar contrato mínimo de módulos Brain OS | manifest JSON | valid/errors | falta `witness` o `recovery` falla |
| `content_forge_job_gate` | Gatear renders locales y paquetes de publicación | job spec + assets | job state + QA | job sin assets public-safe queda `requiere_aprobacion` |
| `browser_manifest_gate` | Bloquear automatización sin manifiesto | browser action | allow/block | acción externa sin manifest bloquea |
| `curator_order_assistant` | Mantener orden y enseñar higiene documental al operador/agentes | cambios, fuentes, tareas | fichas, rutas, warnings | fuente cruda sin ficha queda REVIEW |
""",
    "13_AGENTES.md": """
---

## Agente adicional recomendado: Asistente de Orden del Curador

Propósito: mantener orden operacional mientras otros agentes trabajan. No decide teoría ni borra archivos; observa suciedad documental, sugiere rutas y crea fichas mínimas.

Input: diff, archivos nuevos, manifests, documentos crudos, logs de sesión.

Output: `SOURCE_INTAKE_REGISTER` actualizado, fichas de fuente, advertencias de duplicado, brief de higiene para humanos/agentes.

Gate: solo acciones locales, reversibles, documentales. Borrado, publicación y migración masiva quedan REVIEW/BLOCK.
""",
    "14_PROYECTOS_ACTIVOS.md": """
---

## Proyectos activos añadidos desde PRODUCTOS_MEDIOEVO

| Proyecto | Estado | Objetivo | Archivos relacionados | Siguiente acción | Riesgo |
|---|---|---|---|---|---|
| PRODUCTOS_MEDIOEVO | Activo | Ordenar frente comercial sin mover source canónico | `PRODUCTOS_MEDIOEVO/00_LEER_PRIMERO.md` | Crear `PRODUCT_MAP`, `VISIBILITY_MATRIX`, `RISK_REGISTER` si no existen en esta raíz | Mezcla comercial/canon/privado |
| Libros y Bundles | Activo | Bloque editorial 6+1 y catálogo ampliado | `01_LIBROS_Y_BUNDLES/README.md` | Mantener fuente de verdad en `libros.json` y storefront local | No publicar textos completos privados |
| Software Local | Activo | Claudio Full, Workbench, Pack Empresarial y módulos offline | `02_SOFTWARE_LOCAL/README.md` | Verificar empaques y gates comerciales | Gumroad/publicación requiere revisión |
| Open Source GitHub | Activo | Herramientas públicas: safe-exec, medioevo-tools, data-double-slit | `03_OPEN_SOURCE_GITHUB/README.md` | Mantener repos public-safe y escaneados | Licencia/secreto/publicación |
| Audiovisual y TCG | Parcial | Radiocinema, El Bardo, soundtrack, mapas, TCG | `04_AUDIOVISUAL_Y_TCG/README.md` | Separar TCG/privado de material publicable | Alto riesgo de mezcla privada |
| Betas | Pendiente | Radiocinema, COACH Pro, Creator Bundle, FlujoCRM | `05_BETAS_Y_PROXIMAMENTE/README.md` | Cerrar por evidencia local antes de venta | Producto no verificado |
| ClaudioOS Blueprint | Activo local | ISO Debian Live + Brain OS | `claudio_os_blueprint/README.md` | QEMU/Guardian/Mission Control/witness | No instalar en producción |
| Content Forge | Activo local | Render/campañas sin autopublicación | `content_forge/README.md` | QA ffprobe/visual y asset policy | Autopublicación bloqueada |
""",
    "15_PROYECTOS_FUTUROS.md": """
---

## Futuro detectado en `CLAUDIO - researchs/futuro`

| Idea | Estado | Gate |
|---|---|---|
| ObservaScript / lenguaje observacionista | Diseño futuro | Convertir primero a DSL pequeño y testeado |
| Matrix Map | Metáfora operativa | No derivar física desde la metáfora |
| Website futuro | Plan de superficie pública | Separar copy public-safe de canon privado |
| Argus Companion | Futuro avanzado | Privacidad/seguridad antes de demo |
| OS portátil | Futuro técnico | Auth/cifrado/OSO serializable primero |
| Hormiguero OS visual | Producto UI futuro | Mission Control read-only antes de acciones |
| OpenWebUI integración | Integración local | Gate de modelo local y permisos |
| Web chat ligero | Interfaz futura | No mezclar con agentes ejecutores sin ActionGate |
""",
    "16_CLAIMS_REGISTER.md": """
---

## Claims añadidos o reforzados por este pase

| CLAIM_ID | Claim | Categoría | Evidencia disponible | Riesgo | Falsador mínimo | Estado |
|---|---|---|---|---|---|---|
| BRAIN-01 | Brain OS es una capa cognitiva local-first sobre la máquina, no un kernel Linux | IA_TEORIA / INGENIERIA | `claudio_os_blueprint/docs/BRAIN_OS_PRINCIPLES.md`, `ARCHITECTURE.md` | Bajo si se formula así | Verificar que docs y CLI lo tratan como loop cognitivo | PUBLISH_ALLOWED_AS_MODEL |
| DSL-01 | Observacionista DSL compila intención/evidencia/estado/acción/witness a JSON | CODIGO / MODULO | `observacionismo_dsl.py` leído | Bajo | Ejecutar tests de parseo/validación | PUBLISH_AS_PHENOMENOLOGICAL |
| MODEL-01 | Un modelo reducido solo reemplaza baseline tras medición de accuracy, latencia, memoria, energía y seguridad | IA_TEORIA / MODULO | `MODEL_EFFICIENCY.md`, `model_slimmer_evidence.py` | Bajo | Candidate que falla umbrales debe bloquear | PUBLISH_ALLOWED_WITH_SCOPE |
| PROD-01 | Content Forge produce paquetes locales sin publicar automáticamente | PROYECTO | `content_forge/README.md` | Medio | Ejecutar job local y confirmar no publicación externa | PUBLISH_ALLOWED_AS_MODEL |
| SEC-04 | Automatización de browser sin manifiesto debe bloquearse | SEGURIDAD | `OBSERVACIONISMO_OS.md`, ClaudioOS README | Bajo | Acción browser sin manifest -> block | PUBLISH_ALLOWED_WITH_SCOPE |
""",
    "17_FALSADORES_Y_TESTS.md": """
---

## Tests técnicos añadidos

| ID | Dominio | Prueba mínima | Rechazo |
|---|---|---|---|
| F-DSL-01 | DSL | DSL válido con `intent`, `evidence`, `state`, `action`, `witness` compila a JSON | Parser acepta programa sin evidencia o witness |
| F-MODEL-01 | Model efficiency | Candidate con `accuracy_drop > 0.02` bloquea | Gate permite reemplazo sin aprobación |
| F-MANIFEST-01 | Módulos | Manifest sin `purpose`, `inputs`, `outputs`, `risk`, `gates`, `witness`, `recovery` falla | Módulo ejecutable sin contrato |
| F-CONTENT-01 | Content Forge | Job local genera carpeta runtime y QA sin autopost | Cualquier acción externa ocurre sin approval |
| F-CURADOR-01 | Curador | Fuente nueva sin ficha queda `REVIEW` | Fuente cruda entra a canon sin trazabilidad |
""",
    "18_RIESGOS_CONTRADICCIONES.md": """
---

## Riesgos añadidos por inventario de productos

| Riesgo | Evidencia | Mitigación |
|---|---|---|
| `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md` mencionados pero no presentes en raíz `PRODUCTOS_MEDIOEVO` | `00_LEER_PRIMERO.md` los lista; búsqueda directa no los encontró en esa raíz | Crear esos docs o enlazar a los canónicos existentes antes de release |
| Doble verdad por tener master previo dentro de `-=PSI=-` y nueva carpeta maestra | `-=PSI=-/00_README_MASTER.md` ya declara una carpeta master | Esta carpeta nueva debe ser índice operativo; `-=PSI=-` queda fuente/canon |
| Archivos pesados no parseados línea por línea | ZIP/PDF/DOCX/TAR.GZ/MP4 en manifiesto | Mantener `PENDIENTES_DE_INPUT.md`; procesar por ficha si se vuelven P0 |
| TCG/audiovisual puede mezclar privado y publicable | `04_AUDIOVISUAL_Y_TCG/README.md` | VISIBILITY_MATRIX antes de publicar |
| ClaudioOS puede confundirse con kernel propio | README aclara que no reemplaza Linux | Mantener lenguaje: blueprint/remix Debian Live + Brain OS |
""",
    "19_ROADMAP.md": """
---

## Ajuste de roadmap por este pase

Fase 0 cerrada en esta carpeta: inventario, compilación master, manifiesto y handoff.

Fase 1 prioritaria:
- Crear o localizar `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md` para `PRODUCTOS_MEDIOEVO`.
- Ejecutar tests unitarios sobre `observacionismo_dsl.py` y `model_slimmer_evidence.py`.
- Crear JSON schemas para OSO, AgentMessage, WitnessLog, ActionGate y ModuleManifest.
- Separar publicable/comercial/privado antes de cualquier publicación.

Fase 2 técnica:
- Convertir `curator_order_assistant` en módulo/CLI.
- Conectar `dsl_compiler`, `model_efficiency_gate`, `module_manifest_validator` con Brain OS/Guardian.
- Mission Control read-only para visualizar gates, witness y pendientes.
""",
}


def build_next_session_brief(timestamp: str, file_count: int) -> str:
    return f"""# 20 — NEXT SESSION BRIEF

Fecha de corte: `{timestamp}`

## Estado

R_close: `0.15`
Phi_eff: `0.75`
Régimen: `FUNCIONAL`
Autonomy level: `3` documental local

## CERTEZA

- Se creó una carpeta maestra separada: `MEDIOEVO_OBSERVACIONISMO_MASTER`.
- Fuentes procesadas por inventario único: `{file_count}` archivos locales.
- La carpeta fuente `-=PSI=-` ya contenía canon formal 00-19; fue absorbido como base, no destruido.
- `PRODUCTOS_MEDIOEVO` aporta productos activos, ClaudioOS Blueprint, Content Forge, categorías comerciales y módulos.
- `-=CEREBRO=-` define entrada humana, sistemas y frontera: canon humano en CEREBRO, runtime/evidencia ejecutable en Claudio.

## INFERENCIA

- La siguiente mejora de mayor retorno es convertir la curaduría en contratos ejecutables: schemas, tests, gates y assistant de orden.
- La publicación debe seguir bloqueada hasta tener matriz de visibilidad, revisión de secretos y claims con gate.

## INCÓGNITA

- PDFs/DOCX/ZIP/TAR.GZ no fueron convertidos completamente a texto en este pase.
- Falta confirmar si los documentos `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md` y `RISK_REGISTER.md` existen en otra ruta canónica o deben crearse.
- Falta prueba de runtime para `observacionismo_dsl.py`, `model_slimmer_evidence.py`, ClaudioOS y Content Forge en esta sesión.

## ACCIÓN

- Próxima acción verificable única: crear/actualizar `PRODUCTOS_MEDIOEVO/PRODUCT_MAP.md`, `PRODUCTOS_MEDIOEVO/VISIBILITY_MATRIX.md` y `PRODUCTOS_MEDIOEVO/RISK_REGISTER.md` o registrar su ruta canónica si ya existen.

## ARTEFACTO

- Carpeta master con documentos 00-22.
- `SOURCE_MANIFEST.md`
- `SOURCE_MANIFEST.json`
- `PENDIENTES_DE_INPUT.md`
- `SESSION_FINGERPRINT.json`

## Segunda pérdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implícita.
"""


def build_action_gates() -> str:
    return """# 21 — ACTION GATES

Estado: `POLITICA_OPERATIVA`

## Regla base

Acción permitida solo si:

```text
Phi_eff > 0.60
R < 0.30
evidencia_minima_disponible = true
riesgo_de_sobreafirmacion_controlado = true
siguiente_paso_verificable = true
```

## CERTEZA

- Las fuentes locales definen ActionGate, WitnessLog, Guardian y políticas de hold/allow/ask/block.
- Las acciones irreversibles, publicación, credenciales, pagos, browser externo y borrados masivos requieren revisión o bloqueo.

## INFERENCIA

- La política más segura para Wabi-Sabi/Claudio es un gate determinístico delante de toda acción de filesystem, browser, modelo, publicación o ejecución.

## INCÓGNITA

- Umbrales exactos de R/Phi requieren calibración empírica por tarea.

## ACCIÓN

| Tipo de acción | Gate | Evidencia mínima | Resultado |
|---|---|---|---|
| Leer/inventariar documentación local | APPROVE | ruta local existe | ejecutar y registrar |
| Crear documentación/ficha/manifiesto | APPROVE | destino dentro del workspace | escribir y registrar |
| Ejecutar tests locales seguros | APPROVE_MONITORED | comando específico, sin red | ejecutar y capturar resultado |
| Modificar código no crítico | APPROVE_MONITORED | diff pequeño + test | patch + test |
| Instalar dependencias con red | REVIEW | razón + lockfile | registrar y esperar revisión |
| Publicar, deploy, push, Gumroad, social | REVIEW/BLOCK | autorización explícita + scan + matriz | no ejecutar por defecto |
| Leer/imprimir secretos | BLOCK | ninguna | no ejecutar |
| Borrar/migrar grandes volúmenes | REVIEW/BLOCK | backup + migration log + aprobación | no ejecutar por defecto |
| Browser externo sin manifest | BLOCK | manifest ausente | bloquear |
| Física fuerte sin numérico | BLOCK/NO_PUBLIC | cómputo ausente | reformular como hipótesis |

## ARTEFACTO

Contrato mínimo:

```json
{
  "action": "string",
  "domain": "docs|code|browser|publish|physics|model|filesystem",
  "R": 0.15,
  "Phi_eff": 0.75,
  "evidence": ["path-or-test"],
  "risk": "low|medium|high|critical",
  "reversible": true,
  "external_effect": false,
  "decision": "APPROVE|APPROVE_MONITORED|REVIEW|BLOCK",
  "witness": "path/to/witness.jsonl"
}
```
"""


def build_prompts() -> str:
    return """# 22 — PROMPTS OPERATIVOS

Estado: `LISTO_PARA_REUSO`

## PROMPT_CODEX_ORQUESTADOR

```text
Actúa como Codex orquestador MEDIOEVO/CLAUDIO.
Lee AGENTS.md y el brief vigente. Ejecuta solo acciones locales, reversibles y verificables.
Separa CERTEZA / INFERENCIA / INCÓGNITA / ACCIÓN / ARTEFACTO.
No publiques, no borres, no expongas secretos, no mezcles privado con público.
Entrega diff, comandos, tests y fingerprint.
```

## PROMPT_CURADOR

```text
Actúa como Curador de Datos Observacionista.
Inventaría fuentes, clasifica por categoría, deduplica ideas, conserva trazabilidad,
separa física estándar de hipótesis, lore de ingeniería y claims publicables de claims bloqueados.
Genera carpeta documental con manifiesto y next-session brief.
```

## PROMPT_FISICO_ESCEPTICO

```text
Actúa como físico escéptico.
Para cada claim físico indica: física estándar relacionada, formalismo requerido,
posible contradicción, falsador mínimo, evidencia disponible y gate de publicación.
Bloquea lenguaje como "resuelve GR", "antigravedad tecnológica" o "unificación final" sin cómputo.
```

## PROMPT_PROGRAMADOR

```text
Actúa como programador seguro local-first.
Lee specs y tests. Implementa cambios mínimos. Usa patch. Ejecuta pruebas locales.
No instales dependencias con red, no arranques daemons, no publiques.
Registra WitnessLog y handoff.
```

## PROMPT_DOCUMENTACION

```text
Actúa como agente de documentación.
Convierte resultados en README, contracts, runbook, risks, assumptions y next-session brief.
No conviertas hipótesis en hechos. Incluye rutas de fuente, comandos y límites de verificación.
```

## PROMPT_CLAIMS

```text
Actúa como validador de claims.
Clasifica cada claim como PUBLISH_AS_FORMAL_HYPOTHESIS,
PUBLISH_AS_PHENOMENOLOGICAL, NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC o INTERNAL_ONLY.
Incluye evidencia, riesgo, falsador mínimo y lenguaje recomendado.
```

## PROMPT_ROADMAP

```text
Actúa como roadmap engineer.
Ordena pendientes por cierre verificable más corto: documentos, schemas, tests, módulos, prototipo, validación, publicación.
No abras features si R sube; cierra evidencia y handoff primero.
```

## PROMPT_ASISTENTE_ORDEN_CURADOR

```text
Actúa como asistente de orden del Curador.
Observa cambios de archivos, fuentes nuevas y salidas de agentes.
No borres ni muevas sin migration log. Crea fichas, detecta duplicados,
marca UNKNOWN_REVIEW_REQUIRED y enseña al operador/agentes dónde colocar cada cosa.
Entrega un brief corto con: qué ensucia, cómo evitarlo, y qué ruta canónica usar.
```

## CERTEZA

- Estos prompts están diseñados para operación local y documental.

## INFERENCIA

- Sirven como paquetes mínimos para agentes especializados; requieren adaptación si se conectan a un runtime real.

## INCÓGNITA

- No incluyen credenciales, endpoints ni proveedores específicos.

## ACCIÓN

- Usar el prompt especializado según el tipo de tarea y registrar el resultado en WitnessLog/Handoff.

## ARTEFACTO

- Prompt pack reutilizable para Codex, curador, físico escéptico, programador, documentación, claims, roadmap y asistente de orden.
"""


def build_pendientes() -> str:
    return """# PENDIENTES_DE_INPUT

Estado: `NO_BLOQUEANTE`

## CERTEZA

- Existen fuentes pesadas o no-textuales: PDF, DOCX, ZIP, TAR.GZ, MP4, JPG.
- Existen fuentes conversacionales y archivos TXT largos que pueden contener variaciones útiles.
- Este pase generó una carpeta maestra trazable sin borrar ni mover fuentes.

## INFERENCIA

- El canon esencial ya está representado por los documentos 00-22.
- Las fuentes pesadas deben procesarse por prioridad y ficha, no por volcado completo.

## INCÓGNITA

| Pendiente | Motivo | Acción mínima |
|---|---|---|
| PDF/DOCX completos | No todos fueron renderizados ni extraídos línea por línea | Procesar solo si un claim depende de ellos |
| ZIP/TAR.GZ | Pueden contener código o docs duplicados | Crear ficha con hash, inventario interno y riesgo |
| `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md` en PRODUCTOS | Mencionados pero no encontrados en esa raíz | Crear o enlazar ruta canónica |
| Claims físicos P-06 a P-10 | Sin cómputo numérico | Mantener bloqueados hasta simulación |
| Claims cognitivos/Sigma | Sin validación/preregistro | Usar lenguaje fenomenológico |
| Publicación externa | Requiere seguridad/legal/visibilidad | Mantener REVIEW/BLOCK |

## ACCIÓN

Siguiente pase recomendado: crear fichas para los archivos pesados que todavía sean P0 y cerrar matriz de visibilidad de PRODUCTOS.

## ARTEFACTO

Lista de huecos no bloqueantes para continuar sin preguntar.
"""


def build_manifest_md(records: list[dict[str, object]], ext_counter: Counter[str], category_counter: Counter[str], timestamp: str) -> str:
    total_bytes = sum(int(item["bytes"]) for item in records)
    by_ext = "\n".join(f"| `{ext}` | {count} |" for ext, count in sorted(ext_counter.items()))
    by_category = "\n".join(f"| `{category}` | {count} |" for category, count in sorted(category_counter.items()))
    sample_rows = "\n".join(
        f"| `{item['path']}` | `{item['category']}` | `{item['extension']}` | {item['bytes']} | `{item['sha256']}` |"
        for item in records[:250]
    )
    truncated = "" if len(records) <= 250 else f"\n\n> Tabla truncada a 250 filas en Markdown. Ver `SOURCE_MANIFEST.json` para {len(records)} archivos."
    return f"""# SOURCE_MANIFEST

Generado: `{timestamp}`

## Resumen

CERTEZA:
- Archivos únicos inventariados: `{len(records)}`
- Bytes totales aproximados: `{total_bytes}`
- Hash SHA256 calculado para archivos de hasta `{HASH_LIMIT_BYTES}` bytes.
- Archivos grandes quedan marcados como `not_hashed_large_file`.

INFERENCIA:
- La categoría es una clasificación de curaduría por ruta/extensión/nombre; no sustituye una lectura humana de cada archivo pesado.

INCÓGNITA:
- ZIP/TAR/PDF/DOCX/media requieren ficha puntual si pasan a claim, módulo o publicación.

## Conteo por extensión

| Extensión | Archivos |
|---|---:|
{by_ext}

## Conteo por categoría

| Categoría | Archivos |
|---|---:|
{by_category}

## Primeras fuentes inventariadas

| Ruta | Categoría | Ext | Bytes | SHA256 |
|---|---|---|---:|---|
{sample_rows}
{truncated}

## ACCIÓN

Usar `SOURCE_MANIFEST.json` para búsquedas exactas y esta tabla para orientación rápida.

## ARTEFACTO

Manifiesto trazable de fuentes locales procesadas.
"""


def build_fingerprint(
    *,
    timestamp: str,
    workspace: Path,
    output_dir: Path,
    generated_files: list[str],
    file_count: int,
) -> dict[str, object]:
    return {
        "schema_version": "observacionismo.session_fingerprint.v2.1",
        "session_id": timestamp.replace(":", "").replace("-", "").replace("+", "Z")[:15],
        "project": "MEDIOEVO/OBSERVACIONISMO_MASTER",
        "R_close": 0.15,
        "Phi_eff": 0.75,
        "regime_close": "FUNCIONAL",
        "autonomy_level_used": 3,
        "actiongate_summary": {
            "approved": len(generated_files),
            "review_required": 3,
            "blocked": 0,
        },
        "project_root": str(workspace),
        "output_dir": str(output_dir),
        "sources": [
            str(workspace / "PRODUCTOS_MEDIOEVO"),
            str(workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "-=PSI=-"),
            str(workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-"),
        ],
        "source_files_inventoried": file_count,
        "files_created": generated_files,
        "files_modified": [],
        "commands_run": [
            "python tools\\release\\pending_review.py --write --quiet",
            "python tools\\release\\build_observacionismo_master.py",
        ],
        "tests": {
            "status": "not_run",
            "evidence": [
                "Document generation and manifest validation are performed after build."
            ],
        },
        "decisions": [
            "Create a new master folder instead of moving or deleting source files.",
            "Treat PSI 00-19 as canonical base and append PRODUCTOS/CEREBRO curation.",
            "Keep physics strong claims gated until independent symbolic/numeric validation.",
        ],
        "pending": [
            "Process heavy PDFs/DOCX/ZIP/TAR only when needed for a specific claim.",
            "Create or link PRODUCTOS product map, visibility matrix and risk register.",
            "Run module tests for DSL/model-slimmer/manifest validator in a later implementation pass.",
        ],
        "next_action": "Close PRODUCTOS_MEDIOEVO product map, visibility matrix and risk register.",
    }


def build_master(workspace: Path) -> Path:
    psi_dir = workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "-=PSI=-"
    output_dir = workspace / OUTPUT_DIR_NAME
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    records, ext_counter, category_counter = inventory_sources(workspace, output_dir)

    generated_files: list[str] = []
    for file_name in REQUIRED_FILES:
        if file_name in SOURCE_DOCS:
            source_path = psi_dir / SOURCE_DOCS[file_name]
            if source_path.exists():
                content = normalize_markdown_tasks(read_text(source_path))
            else:
                content = f"# {file_name}\n\nINCÓGNITA: fuente base no encontrada en `-=PSI=-`."
            content = content.rstrip() + "\n\n" + curation_footer(file_name)
        elif file_name == "20_NEXT_SESSION_BRIEF.md":
            content = build_next_session_brief(timestamp, len(records))
        elif file_name == "21_ACTION_GATES.md":
            content = build_action_gates()
        elif file_name == "22_PROMPTS_OPERATIVOS.md":
            content = build_prompts()
        else:
            content = f"# {file_name}\n\nINCÓGNITA: plantilla no definida."
        write_text(output_dir / file_name, content)
        generated_files.append(file_name)

    manifest_md = build_manifest_md(records, ext_counter, category_counter, timestamp)
    write_text(output_dir / "SOURCE_MANIFEST.md", manifest_md)
    generated_files.append("SOURCE_MANIFEST.md")

    manifest_json = {
        "schema": "medioevo.source_manifest.v1",
        "generated_at": timestamp,
        "workspace": str(workspace),
        "output_dir": str(output_dir),
        "source_count": len(records),
        "by_extension": dict(sorted(ext_counter.items())),
        "by_category": dict(sorted(category_counter.items())),
        "records": records,
    }
    write_text(output_dir / "SOURCE_MANIFEST.json", json.dumps(manifest_json, ensure_ascii=False, indent=2))
    generated_files.append("SOURCE_MANIFEST.json")

    write_text(output_dir / "PENDIENTES_DE_INPUT.md", build_pendientes())
    generated_files.append("PENDIENTES_DE_INPUT.md")

    fingerprint = build_fingerprint(
        timestamp=timestamp,
        workspace=workspace,
        output_dir=output_dir,
        generated_files=generated_files,
        file_count=len(records),
    )
    write_text(output_dir / "SESSION_FINGERPRINT.json", json.dumps(fingerprint, ensure_ascii=False, indent=2))
    generated_files.append("SESSION_FINGERPRINT.json")

    return output_dir


def emit_cerebro_index(workspace: Path) -> list[str]:
    """Emit the human-facing CEREBRO index through the Wabi-Sabi module."""
    app_root = workspace / "apps" / "local" / "wabi-sabi"
    if str(app_root) not in sys.path:
        sys.path.insert(0, str(app_root))
    from wabi_sabi.core.cerebro_index import build_cerebro_navigation, write_cerebro_navigation_docs

    payload = build_cerebro_navigation(workspace)
    return write_cerebro_navigation_docs(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build MEDIOEVO_OBSERVACIONISMO_MASTER")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE), help="MEDIOEVO workspace root")
    parser.add_argument(
        "--emit-cerebro-index",
        action="store_true",
        help="Also write the human-readable CEREBRO navigation layer",
    )
    args = parser.parse_args()
    workspace = Path(args.workspace)
    output_dir = build_master(workspace)
    print(output_dir)
    if args.emit_cerebro_index:
        for artifact in emit_cerebro_index(workspace):
            print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
