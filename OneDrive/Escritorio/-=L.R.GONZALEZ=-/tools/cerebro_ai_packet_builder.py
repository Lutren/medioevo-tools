from __future__ import annotations

import hashlib
import json
import re
import shutil
import textwrap
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WORKSPACE = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-")
DESKTOP = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio")
CEREBRO_ROOT = WORKSPACE / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-"
INDEX_ROOT = WORKSPACE / "runtime" / "cerebro_master_index"
MASTER_ROOT = WORKSPACE / "MEDIOEVO_OBSERVACIONISMO_MASTER"
OUTPUT_ROOT = DESKTOP / "MEDIOEVO_AI_CONTEXT_BATCH_2026-05-07"
FULL_ROOT_NAME = "08_VERSION_COMPLETA_CANONICA"
ZIP_NAME = "MEDIOEVO_AI_CONTEXT_FULL_CANON_20260507.zip"


def main() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    stats = _load_stats()
    generated: list[Path] = []

    generated.extend(_write_setup_docs(stats))
    generated.extend(_write_batteries(stats))
    generated.extend(_write_path_and_status(stats))
    generated.extend(_write_prompt_library(stats))
    generated.extend(_write_full_canonical_version(stats))
    generated.extend(_write_root_docs(stats))
    generated.extend(_write_curator_ficha(stats))

    zip_path = _write_zip()
    generated.append(zip_path)
    generated.extend(_write_security_scan_report(zip_path))
    manifest_path = _write_manifest(stats, generated, zip_path)
    generated.append(manifest_path)

    print(json.dumps({
        "ok": True,
        "output_root": str(OUTPUT_ROOT),
        "zip": str(zip_path),
        "files_written": len(generated),
        "cerebro_files_indexed": stats["file_count"],
        "source_mutations": 0,
    }, indent=2, ensure_ascii=False))
    return 0


def _load_stats() -> dict[str, Any]:
    rows = _read_jsonl(INDEX_ROOT / "LINE_AUDIT_MANIFEST.jsonl")
    signal_lines = _read_jsonl(INDEX_ROOT / "LINE_SIGNAL_INDEX.jsonl")
    variant = _safe_json(INDEX_ROOT / "VARIANT_SEMANTIC_COMPARISON.json")
    duplicate_plan = _safe_json(INDEX_ROOT / "VARIANT_EXACT_DUPLICATE_MIGRATION_PLAN.json")
    merge_review = _safe_json(INDEX_ROOT / "VARIANT_CANON_MERGE_REVIEW_PACK.json")
    top_signals: Counter[str] = Counter()
    suffixes: Counter[str] = Counter()
    classifications: Counter[str] = Counter()
    for row in rows:
        top_signals.update(row.get("signals") or {})
        suffixes[str(row.get("suffix") or "<none>").lower()] += 1
        classifications[str(row.get("classification") or "UNKNOWN")] += 1
    top_files = sorted(rows, key=lambda item: int(item.get("signal_count") or 0), reverse=True)[:24]
    return {
        "generated_at_local": datetime.now().astimezone().replace(microsecond=0).isoformat(),
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "workspace": str(WORKSPACE),
        "cerebro_root": str(CEREBRO_ROOT),
        "index_root": str(INDEX_ROOT),
        "master_root": str(MASTER_ROOT),
        "file_count": len(rows),
        "text_file_count": sum(1 for row in rows if row.get("source_kind") == "filesystem_text"),
        "document_text_count": sum(1 for row in rows if row.get("source_kind") == "document_text"),
        "line_count": sum(int(row.get("line_count") or 0) for row in rows),
        "signal_line_count": len(signal_lines),
        "signal_count": sum(int(row.get("signal_count") or 0) for row in rows),
        "code_candidate_count": sum(int(row.get("code_candidate_count") or 0) for row in rows),
        "top_signals": top_signals.most_common(30),
        "top_files": [
            {
                "path": row.get("path"),
                "line_count": row.get("line_count"),
                "signal_count": row.get("signal_count"),
                "sha256_prefix": str(row.get("sha256") or "")[:12],
            }
            for row in top_files
        ],
        "suffixes": suffixes.most_common(),
        "classifications": classifications.most_common(),
        "variant_summary": variant.get("summary", {}),
        "duplicate_plan_summary": duplicate_plan.get("summary", {}),
        "merge_review_summary": merge_review.get("summary", {}),
        "not_claimed": [
            "No source file was moved, deleted, merged or rewritten.",
            "The package is for local AI context transfer; it is not a public release.",
            "The ZIP contains the complete canonical version only, not the 1/5/10 summary variants.",
        ],
    }


def _write_setup_docs(stats: dict[str, Any]) -> list[Path]:
    out = OUTPUT_ROOT / "01_SETUP_IA"
    out.mkdir(parents=True, exist_ok=True)
    full = _doc(
        "SETUP IA COMPLETO",
        f"""
        CERTEZA:
        - Este setup esta diseñado para modelos que permiten instrucciones largas en `Custom Instructions`,
          `Preferred responses`, `User preferences`, `System prompt` o perfil persistente.
        - El corpus fuente es CEREBRO: `{stats['cerebro_root']}`.
        - Indice operativo usado: `{stats['index_root']}`.

        CONFIGURACION RECOMENDADA:
        1. Idioma preferido: español neutro. Si el usuario escribe en otro idioma, responde en ese idioma.
        2. Estilo: directo, pragmatico, sin relleno. No elogies. No sobreprometas.
        3. Formato por defecto: `CERTEZA / INFERENCIA / INCOGNITA / ACCION / ARTEFACTO`.
        4. Antes de actuar: separa evidencia directa, inferencia razonable e incognita.
        5. Observacionismo: no asumas desde cero; observa desde estado, reduce ruido, mide residuo `R`,
           estima eficiencia `Phi_eff`, detecta jamming `J_c` y actua solo cuando el siguiente paso sea verificable.
        6. Observacionismo inverso: extrae estructura desde sistemas ruidosos, carpetas, textos, codigo,
           historiales y contradicciones; no conviertas ruido en canon.
        7. Seguridad: no pidas ni expongas secretos; no ejecutes acciones destructivas; no publiques, despliegues
           ni hagas push sin gate dedicado.
        8. Claims: separa fisica estandar, analogia, hipotesis, lore y producto. Claims fuertes requieren falsador.
        9. Codigo: lee archivos reales primero, aplica cambios pequeños, ejecuta tests, registra evidencia.
        10. Agentes: cada agente debe producir artefacto, no solo respuesta. Usa handoff, manifest y fingerprint.

        PREFERRED RESPONSE BASE:
        ```
        Actua como agente observacionista local-first. Responde con evidencia. Separa CERTEZA, INFERENCIA e
        INCOGNITA. No inventes implementaciones ni resultados. Si trabajas en codigo, lee el repo, modifica solo
        lo necesario, ejecuta pruebas y entrega handoff. Usa ActionGate: APPROVE para trabajo local reversible,
        REVIEW para red/publicacion/legal/secretos, BLOCK para destructivo/exfiltracion/privado. Mantén
        Observacionismo como metodo: reducir R, aumentar Phi_eff, evitar jamming J_c, y cerrar tareas verificables.
        ```

        MODELO DE LENGUAJE:
        - Respuestas cortas cuando el usuario pide decision.
        - Respuestas estructuradas cuando hay curaduria, investigacion o codigo.
        - Si una afirmacion es solo hipotesis, etiquetala como HIPOTESIS.
        - Si una fuente falta, marca `INCÓGNITA`, no rellenes con narrativa.

        INSIGHTS OPERATIVOS:
        - La continuidad no se obtiene metiendo todo en contexto; se obtiene externalizando estado.
        - Mas contexto despues de `J_c` puede empeorar el resultado.
        - El ultimo registro util debe ser de agente si la curaduria ya fue procesada.
        - Una carpeta limpia es una interfaz cognitiva: nombres claros, manifiesto, canon, archivo, evidencia.
        - Un agente que no deja test, manifest o handoff aumenta `R`.
        """,
    )
    short = _doc(
        "SETUP IA RESUMIDO",
        """
        Copiar en modelos con poco espacio de instrucciones:

        ```
        Usa Observacionismo: separa CERTEZA, INFERENCIA e INCOGNITA; no inventes; no amplifiques; reduce ruido y
        cierra acciones verificables. Responde en español neutro. Si haces codigo: lee archivos reales, aplica
        cambios pequeños, ejecuta tests y entrega handoff. Usa ActionGate: APPROVE para local reversible, REVIEW
        para red/publicacion/legal/secretos, BLOCK para destructivo/exfiltracion/privado. Distingue fisica real,
        hipotesis, analogia, lore y producto. No afirmes implementacion sin evidencia.
        ```
        """,
    )
    tiny = _doc(
        "SETUP IA ULTRACORTO",
        """
        ```
        Responde como agente observacionista: evidencia primero, CERTEZA/INFERENCIA/INCOGNITA, cero invencion,
        ActionGate, tests/handoff si hay codigo, claims fuertes solo con falsador.
        ```
        """,
    )
    paths = [
        _write(out / "SETUP_IA_PREFERRED_RESPONSES_COMPLETO.md", full),
        _write(out / "SETUP_IA_PREFERRED_RESPONSES_RESUMIDO.md", short),
        _write(out / "SETUP_IA_PREFERRED_RESPONSES_ULTRACORTO.md", tiny),
    ]
    return paths


def _write_batteries(stats: dict[str, Any]) -> list[Path]:
    written: list[Path] = []
    one = OUTPUT_ROOT / "02_BATERIA_1_DOCUMENTO"
    one.mkdir(parents=True, exist_ok=True)
    written.append(_write(one / "BATERIA_IA_1_DOCUMENTO_CONTEXT_CORE.md", _battery_one(stats)))

    five = OUTPUT_ROOT / "03_BATERIA_5_DOCUMENTOS"
    five.mkdir(parents=True, exist_ok=True)
    docs5 = [
        ("01_OBSERVACIONISMO_E_INFORMACION.md", "Observacionismo e informacion", _section_observacionismo()),
        ("02_IA_AGENTES_WABI_CLAUDIO.md", "IA, agentes, Wabi/Sabi y Claudio", _section_agents()),
        ("03_INGENIERIA_MODULOS_CONTRATOS.md", "Ingenieria, modulos y contratos", _section_engineering()),
        ("04_DUAT_GEODIA_PROYECTOS.md", "DUAT, GEODIA, Hormiguero y proyectos", _section_duat()),
        ("05_CLAIMS_SEGURIDAD_FALSADORES.md", "Claims, seguridad y falsadores", _section_claims()),
    ]
    for name, title, body in docs5:
        written.append(_write(five / name, _doc(title, body)))

    ten = OUTPUT_ROOT / "04_BATERIA_10_DOCUMENTOS"
    ten.mkdir(parents=True, exist_ok=True)
    docs10 = [
        ("01_COMO_LEER_ESTE_CORPUS.md", "Como leer este corpus", _section_reading(stats)),
        ("02_GLOSARIO_MINIMO.md", "Glosario minimo", _section_glossary()),
        ("03_OBSERVACIONISMO_CORE.md", "Observacionismo core", _section_observacionismo()),
        ("04_OBSERVACIONISMO_INVERSO_CURADURIA.md", "Observacionismo inverso y curaduria", _section_inverse()),
        ("05_TEORIA_INFORMACION_IA.md", "Teoria de informacion e IA", _section_info_ai()),
        ("06_AGENTES_Y_ORQUESTACION.md", "Agentes y orquestacion", _section_agents()),
        ("07_WABI_SABI_CLAUDIO_OS.md", "Wabi/Sabi, Claudio y OS local", _section_wabi_claudio()),
        ("08_DUAT_GEODIA_HORMIGUERO.md", "DUAT, GEODIA y Hormiguero", _section_duat()),
        ("09_CLAIMS_RIESGO_SEGURIDAD.md", "Claims, riesgo y seguridad", _section_claims()),
        ("10_ROADMAP_IMPLEMENTACION.md", "Roadmap de implementacion", _section_roadmap()),
    ]
    for name, title, body in docs10:
        written.append(_write(ten / name, _doc(title, body)))
    return written


def _write_path_and_status(stats: dict[str, Any]) -> list[Path]:
    out = OUTPUT_ROOT / "05_CAMINO_Y_ESTADO"
    out.mkdir(parents=True, exist_ok=True)
    camino = _doc(
        "CAMINO COMPLETO BUSCADO",
        f"""
        CERTEZA:
        - CEREBRO fue indexado localmente: `{stats['file_count']}` registros, `{stats['line_count']}` lineas.
        - Existen carriles funcionales para Wabi/Sabi, CEREBRO index, ActionGate, browser gate y estado funcional.

        OBJETIVO:
        Construir un ecosistema local-first donde Claudio/Wabi-Sabi puedan:
        - comprender teoria y contexto sin cargar ruido completo;
        - programar con patch plans, rollback, tests y evidencia;
        - usar navegador de forma gateada;
        - curar carpetas y datos antes de actuar;
        - convertir Observacionismo en modulos, contratos, claims y falsadores;
        - separar open source, comercial, editorial, privado y archivo.

        RUTA:
        1. Canon documental: consolidar CEREBRO en documentos IA legibles.
        2. Runtime operativo: ActionGate, ObservationEnvelope, WitnessLog, TaskSpec, PatchPlan, SafeExecutor.
        3. Agentes: curador, programador, debugger, investigador, fisico esceptico, documentador, release guard.
        4. Navegador: local/read-only permitido; login, publicaciones, pagos y acciones persistentes a REVIEW.
        5. DUAT/GEODIA: mantener como research/synthetic hasta falsadores numericos y datos licenciados.
        6. Producto: abrir herramientas public-safe; vender UI, plantillas, soporte, instaladores y bundles.
        7. Publicacion: solo por allowlist, secret scan, claims scan, license gate y ActionGate.

        CRITERIO:
        No declarar avance por volumen. Declarar avance solo si hay artefacto, prueba, manifest o handoff.
        """,
    )
    estado = _doc(
        "PROYECTOS Y TRABAJOS HASTA AHORA",
        f"""
        CERTEZA:
        - CEREBRO: indexado con `{stats['file_count']}` registros y `{stats['variant_summary'].get('variant_group_count', 'unknown')}` grupos de variantes.
        - Duplicados exactos: `{stats['duplicate_plan_summary'].get('exact_duplicate_groups', 'unknown')}` grupos, `{stats['duplicate_plan_summary'].get('proposed_archive_moves', 'unknown')}` movimientos dry-run.
        - Merge canonico: `{stats['merge_review_summary'].get('review_candidate_groups', 'unknown')}` candidatos, `auto_merge_actions=0`.
        - Wabi/Sabi local: CLI/agentes, comparadores, planificadores y status funcional.
        - Claudio/DUAT/GEODIA: carril local con evidencia separada; claims fuertes siguen gateados.
        - Publicacion: el workspace completo no es publicable por secretos/privado/vendors; los paquetes se publican por allowlist.

        ESTADO POR CARRIL:
        - CEREBRO/Canon: util como fuente teorica y mapa de conceptos; no como repo a publicar crudo.
        - Observacionismo/PSI-IA: listo para prompts, agentes, gates, documentos y modulos pequenos.
        - Wabi/Sabi: carril local de ejecucion y curaduria.
        - Claudio: runtime/orquestador, requiere gates para autonomia amplia.
        - DUAT/GEODIA/Hormiguero: investigacion, simulacion, OS local y ciudad de agentes; no claim cientifico fuerte.
        - Productos: open-dev, comerciales, editorial y privado separados por matrices.
        - Seguridad: no ZIP por glob amplio; denylist de secretos, vendors, TCG/game, runtime y caches.
        """,
    )
    return [
        _write(out / "CAMINO_COMPLETO_BUSCADO.md", camino),
        _write(out / "PROYECTOS_Y_TRABAJOS_ESTADO_ACTUAL.md", estado),
    ]


def _write_prompt_library(stats: dict[str, Any]) -> list[Path]:
    out = OUTPUT_ROOT / "06_PROMPTS_ESPECIFICOS"
    out.mkdir(parents=True, exist_ok=True)
    prompts = _prompt_specs()
    written = []
    index_lines = ["# PROMPTS ESPECIFICOS", "", "Uso: copiar el prompt completo y sustituir los bloques entre corchetes.", ""]
    for number, (slug, title, prompt) in enumerate(prompts, start=1):
        filename = f"{number:02d}_{slug}.md"
        index_lines.append(f"{number}. `{filename}` - {title}")
        written.append(_write(out / filename, _prompt_doc(title, prompt)))
    written.append(_write(out / "00_PROMPTS_INDEX.md", "\n".join(index_lines) + "\n"))
    return written


def _write_full_canonical_version(stats: dict[str, Any]) -> list[Path]:
    full = OUTPUT_ROOT / FULL_ROOT_NAME
    full.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    written.append(_write(full / "00_LEER_PRIMERO_IA.md", _full_readme(stats)))
    canon = full / "01_CANON_MASTER_CURADO"
    canon.mkdir(parents=True, exist_ok=True)
    for src in sorted(MASTER_ROOT.glob("*.md")):
        target = canon / src.name
        target.write_text(src.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        written.append(target)
    setup = full / "02_SETUP_IA"
    setup.mkdir(parents=True, exist_ok=True)
    for src in (OUTPUT_ROOT / "01_SETUP_IA").glob("*.md"):
        target = setup / src.name
        target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(target)
    prompts = full / "03_PROMPTS_OPERATIVOS"
    prompts.mkdir(parents=True, exist_ok=True)
    for src in (OUTPUT_ROOT / "06_PROMPTS_ESPECIFICOS").glob("*.md"):
        target = prompts / src.name
        target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(target)
    evidence = full / "04_EVIDENCIA_Y_LIMITES"
    evidence.mkdir(parents=True, exist_ok=True)
    written.append(_write(evidence / "EVIDENCIA_EXTRACCION_CEREBRO.md", _evidence_doc(stats)))
    written.append(_write(evidence / "LIMITES_Y_NO_CLAIMS.md", _limits_doc()))
    machine = {
        "schema": "medioevo.ai_context_packet.v1",
        "generated_at_utc": stats["generated_at_utc"],
        "cerebro_root": stats["cerebro_root"],
        "stats": {
            "files": stats["file_count"],
            "lines": stats["line_count"],
            "signal_lines": stats["signal_line_count"],
            "variant_groups": stats["variant_summary"].get("variant_group_count"),
        },
        "operating_format": "CERTEZA/INFERENCIA/INCOGNITA/ACCION/ARTEFACTO",
        "action_gate": ["APPROVE_LOCAL_REVERSIBLE", "REVIEW_EXTERNAL_OR_SECRET_OR_LEGAL", "BLOCK_DESTRUCTIVE_OR_PRIVATE_EXFILTRATION"],
    }
    written.append(_write(full / "machine_context.json", json.dumps(machine, indent=2, ensure_ascii=False)))
    return written


def _write_root_docs(stats: dict[str, Any]) -> list[Path]:
    readme = _doc(
        "MEDIOEVO AI CONTEXT BATCH",
        f"""
        CERTEZA:
        - Carpeta generada para que una IA comprenda contexto, teoria, agentes, seguridad y ruta de implementacion.
        - Fuente principal: `{stats['cerebro_root']}`.
        - No se copiaron fuentes crudas de CEREBRO al ZIP.
        - No se movieron, borraron ni fusionaron archivos fuente.

        ESTRUCTURA:
        - `01_SETUP_IA`: instrucciones completas/resumidas para settings de modelos.
        - `02_BATERIA_1_DOCUMENTO`: contexto compacto en un solo documento.
        - `03_BATERIA_5_DOCUMENTOS`: bateria media por temas.
        - `04_BATERIA_10_DOCUMENTOS`: bateria granular para ingestion por partes.
        - `05_CAMINO_Y_ESTADO`: camino completo y estado de proyectos/trabajos.
        - `06_PROMPTS_ESPECIFICOS`: prompts listos para IA/agentes.
        - `{FULL_ROOT_NAME}`: version mas completa y canonica.
        - `{ZIP_NAME}`: ZIP de la version completa, sin baterias alternativas 1/5/10.

        USO RECOMENDADO:
        1. Para un modelo pequeño: cargar `SETUP_IA_PREFERRED_RESPONSES_RESUMIDO.md` y `BATERIA_IA_1_DOCUMENTO_CONTEXT_CORE.md`.
        2. Para un modelo medio: cargar la bateria de 5 documentos.
        3. Para un modelo grande/agente: cargar `{FULL_ROOT_NAME}/00_LEER_PRIMERO_IA.md` y luego el canon completo.
        4. Para tareas concretas: usar un prompt de `06_PROMPTS_ESPECIFICOS`.

        NO CLAIM:
        Este paquete no es publicacion, paper, release legal ni prueba cientifica. Es un paquete local de transferencia
        de contexto para IA.
        """,
    )
    return [_write(OUTPUT_ROOT / "00_README_USO_DEL_PAQUETE_IA.md", readme)]


def _write_curator_ficha(stats: dict[str, Any]) -> list[Path]:
    ficha = _doc(
        "CURADOR FICHA PAQUETE IA",
        f"""
        CERTEZA:
        - Paquete generado localmente para transferencia de contexto a IA.
        - Fuente principal: `{stats['cerebro_root']}`.
        - Indice usado: `{stats['index_root']}`.
        - Archivos fuente indexados: `{stats['file_count']}`.
        - Lineas fuente indexadas: `{stats['line_count']}`.
        - Mutaciones sobre fuente: `0`.

        CLASIFICACION:
        - Tipo: `AI_CONTEXT_PACKET`.
        - Visibilidad: `LOCAL_INTERNAL`.
        - Capa: `CEREBRO / OBSERVACIONISMO / CLAUDIO / WABI_SABI`.
        - Estado: `GENERATED_CURATED_BATCH`.

        INFERENCIA:
        - El paquete es util para agentes que necesitan entender contexto, teoria, prompts,
          separacion de claims, ActionGate y ruta de implementacion sin leer todo CEREBRO crudo.

        INCOGNITA:
        - No sustituye revision humana de claims publicables.
        - No certifica licencias de todo el corpus historico.
        - No autoriza publicacion, deploy, push, venta ni exposicion externa.

        ACCION:
        - Usar primero `00_README_USO_DEL_PAQUETE_IA.md`.
        - Para modelos pequenos: usar `01_SETUP_IA` + `02_BATERIA_1_DOCUMENTO`.
        - Para agentes grandes: usar `{FULL_ROOT_NAME}` o el ZIP `{ZIP_NAME}`.

        ARTEFACTO:
        - Carpeta: `{OUTPUT_ROOT}`.
        - ZIP canonico completo: `{OUTPUT_ROOT / ZIP_NAME}`.
        """,
    )
    return [_write(OUTPUT_ROOT / "CURADOR_FICHA_PAQUETE_IA.md", ficha)]


def _battery_one(stats: dict[str, Any]) -> str:
    return _doc(
        "BATERIA IA EN 1 DOCUMENTO",
        f"""
        CERTEZA:
        - CEREBRO contiene teoria, prompts, codigo, proyectos, claims, arquitectura y residuos.
        - Indice actual: `{stats['file_count']}` archivos, `{stats['line_count']}` lineas, `{stats['signal_line_count']}` lineas con señal.
        - Señales dominantes: {', '.join(name for name, _ in stats['top_signals'][:12])}.

        NUCLEO:
        Observacionismo es un metodo operativo para observar sistemas desde un estado, reducir ruido, separar señal,
        medir residuo `R`, estimar eficiencia de actualizacion `Phi_eff`, detectar jamming `J_c` y actuar solo con
        evidencia suficiente. No busca producir volumen; busca cerrar ciclos verificables.

        OBSERVACIONISMO INVERSO:
        Extrae estructura desde ruido: carpetas desordenadas, codigo, historia, cultura, textos, logs, modelos y
        contradicciones. No fusiona por parecido superficial: conserva variaciones cuando cambian variables, claims,
        condiciones de borde o estado epistémico.

        IA Y AGENTES:
        Claudio/Wabi-Sabi son nodos cognitivo-operativos: reciben input humano, lo convierten en tareas, llaman agentes,
        validan resultados, ejecutan herramientas locales, registran evidencia y entregan handoff. El agente correcto
        no es un chatbot; es un operador con ActionGate, memoria externa, pruebas y rollback.

        INGENIERIA:
        Modulos clave: ActionGate, ObservationEnvelope, WitnessLog, EvidenceStore, TaskManager, DecisionLog,
        RMonitor, PhiEffMeter, EML, Router, Curator, Validator, PatchPlanner, SafeExecutor, RollbackStore,
        ContextCompactor, ClaimClassifier y SimulationCore.

        DUAT / GEODIA / HORMIGUERO:
        Se entienden como ciudad/sistema operativo/agentes: una arquitectura local-first donde los procesos son
        observables, gateados y trazables. GEODIA se mantiene como research/synthetic hasta evidencia numerica y
        licencia de datos. Hormiguero es la metafora de ciudad viva y coordinacion de agentes.

        CLAIMS:
        Fisica estandar se separa de hipotesis propias. OSIT/TUIP/Sigma/POVM/Gauss-Bonnet/QNM/dark information son
        carriles de hipotesis o analogia salvo prueba formal o numerica. Publicacion fuerte requiere falsador minimo.

        SEGURIDAD:
        No pedir secretos, no imprimir tokens, no publicar workspace completo, no tocar game/TCG privado, no hacer ZIP
        por glob amplio. ActionGate: local reversible APPROVE; legal/red/publicacion/secretos REVIEW; destructivo o
        exfiltracion BLOCK.

        CAMINO:
        1. Ordenar canon.
        2. Convertir teoria en modulos.
        3. Ejecutar agentes locales con gates.
        4. Integrar navegador seguro.
        5. Validar claims.
        6. Separar open/comercial/editorial/privado.
        7. Publicar solo por allowlist.

        ACCION:
        Si una IA usa este documento, debe responder siempre con evidencia, no asumir, y producir artefacto verificable.
        """,
    )


def _section_reading(stats: dict[str, Any]) -> str:
    return f"""
    CERTEZA:
    - Este corpus fue reducido desde CEREBRO y sus subcarpetas.
    - Indice: {stats['file_count']} registros, {stats['line_count']} lineas, {stats['variant_summary'].get('variant_group_count', 'unknown')} grupos de variantes.

    LECTURA:
    - Si eres IA pequeña: lee primero setup resumido + bateria de 1 documento.
    - Si eres IA media: lee bateria de 5 documentos.
    - Si eres agente grande: lee version completa canonica y prompts.
    - No confundas resumen con fuente unica: los documentos resumen son entradas operativas.
    """


def _section_glossary() -> str:
    return """
    - R: residuo acumulado, friccion o deuda de contexto.
    - Phi_eff: eficiencia de actualizacion; cuanto avance real genera una accion.
    - J_c: umbral de jamming; punto donde mas contexto/tareas empeora.
    - Sigma: perfil/estado del observador o sistema.
    - EML / exp-minus-log: heuristica de estabilidad que premia evidencia y penaliza residuo.
    - ActionGate: compuerta APPROVE/REVIEW/BLOCK.
    - WitnessLog: registro append-only de acciones/evidencia.
    - ObservationEnvelope: envoltorio de observacion, evidencia y resultado.
    - Observacionismo inverso: reconstruir estructura desde residuos.
    - Claudio: orquestador/nodo cognitivo-operativo.
    - Wabi/Sabi: agente local-first de ingenieria/curaduria.
    - DUAT/GEODIA/Hormiguero: sistema/city OS/agentes/investigacion.
    - OSIT/TUIP: hipotesis/formalismos internos; no tratarlos como fisica establecida sin prueba.
    """


def _section_observacionismo() -> str:
    return """
    Observacionismo es un metodo de operacion:
    - observar desde estado, no desde cero;
    - separar señal, ruido, residuo e incognita;
    - no colapsar prematuramente una idea por parecido superficial;
    - mantener trazabilidad de fuente, certeza y falsador;
    - decidir por Phi_eff y riesgo, no por volumen.

    Reglas:
    - Si `R` sube, cerrar y documentar antes de abrir features.
    - Si `Phi_eff` baja, compactar contexto o cambiar estrategia.
    - Si hay contradiccion, crear registro de conflicto.
    - Si falta evidencia, marcar INCÓGNITA.
    """


def _section_inverse() -> str:
    return """
    Observacionismo inverso convierte caos en mapa:
    - inventario de carpetas, archivos, nombres y hashes;
    - separacion de canon, codigo, lore, research, producto, privado y archivo;
    - extraccion de modulos desde textos y codigo mezclados;
    - comparacion de variantes antes de fusionar;
    - ficha antes de borrar, mover, publicar o importar.

    El objetivo no es ordenar por estetica, sino reducir residuo para humanos, agentes y sistemas.
    """


def _section_info_ai() -> str:
    return """
    Teoria de informacion aplicada:
    - contexto es recurso limitado;
    - compresion util preserva estructura accionable;
    - redundancia puede proteger memoria o aumentar ruido;
    - anti-informacion/dark information se tratan como hipotesis operativas hasta formalizacion;
    - continuidad real = estado externo + manifest + brief + fingerprint.

    Para IA:
    - preferir vectores de informacion utiles: definicion, fuente, estado, modulo, test, riesgo.
    - no pedir "mas texto"; pedir estructura, falsador, contrato y decision.
    """


def _section_agents() -> str:
    return """
    Agentes requeridos:
    - Curador: ordena, clasifica, deduplica y crea fichas.
    - Programador: implementa con PatchPlan, tests y rollback.
    - Debugger: reproduce, diagnostica, corrige y reejecuta.
    - Investigador: busca fuentes, separa evidencia de hipotesis.
    - Fisico esceptico: bloquea claims fuertes sin formalismo/falsador.
    - Documentador: convierte avance en handoff.
    - ReleaseGuard: secret scan, license, private boundary y checklist.

    Cada agente debe producir artefacto verificable: doc, patch, test, manifest, cola o fingerprint.
    """


def _section_engineering() -> str:
    return """
    Contratos implementables:
    - ObservationEnvelope(input, evidence, inference, unknown, action, artifact).
    - ActionGate(action, target, risk) -> APPROVE/REVIEW/BLOCK.
    - TaskSpec(goal, files, constraints, tests, rollback).
    - PatchPlan(files, hunks, validation, risk).
    - ClaimContract(claim, evidence, falsifier, publish_state).
    - EvidenceStore(source, hash, timestamp, result).
    - ContextCompactor(raw, canon, residue, next_action).

    Metricas:
    - R baja si se cierran tareas con evidencia.
    - Phi_eff sube si una accion produce avance reusable.
    - EML penaliza acciones ruidosas y premia pruebas/manifest/handoff.
    """


def _section_wabi_claudio() -> str:
    return """
    Wabi/Sabi:
    - agente local-first de ingenieria;
    - lee repo, edita, prueba, documenta;
    - usa modelo base si esta expuesto, sin simular acceso;
    - conserva logs, memoria local y handoff.

    Claudio:
    - orquestador/nodo operativo;
    - coordina agentes, COMMS, Mission Control, browser gates y runtime;
    - destino: autonomia amplia con rollback, tests y ActionGate.
    """


def _section_duat() -> str:
    return """
    DUAT/GEODIA/Hormiguero:
    - DUAT: capa de sistema/estructura simbolica y operacional.
    - GEODIA: research/simulacion/ciudad o dinamica observable; mantener SYNTHETIC_ONLY o RESEARCH_ONLY sin validacion numerica.
    - Hormiguero: ciudad de agentes, coordinacion viva, paneles y rutas.

    Regla:
    - No vender ni publicar claims de prediccion/fisica sin datos, falsadores y licencia.
    - Usar fixtures sinteticos para demos.
    """


def _section_claims() -> str:
    return """
    Claims:
    - Fisica estandar: solo lo compatible con relatividad, termodinamica, QFT, cosmologia observacional o teoria de informacion establecida.
    - Hipotesis OSIT/TUIP/Sigma: publicables solo como hipotesis formal o fenomenologica.
    - Lore/metafora: separado de ciencia e ingenieria.

    Falsador minimo:
    - definir variable observable;
    - definir prediccion;
    - definir baseline;
    - ejecutar simulacion/test;
    - registrar resultado y downgrade si falla.

    Seguridad:
    - No secretos.
    - No workspace completo.
    - No rutas privadas.
    - No publicacion sin ActionGate.
    """


def _section_roadmap() -> str:
    return """
    Roadmap:
    0. Congelar ruido: inventario, variantes, duplicados, riesgos.
    1. Canon IA: paquetes de contexto como este.
    2. Modulos: ActionGate, EvidenceStore, ClaimContract, TaskSpec, SafeExecutor.
    3. Agentes: curador, programador, debugger, investigador, release guard.
    4. Browser: smoke local/read-only, login/publicacion a REVIEW.
    5. DUAT/GEODIA: simulaciones sinteticas y falsadores.
    6. Producto: open-dev, comercial, editorial y privado separados.
    7. Release: allowlist, secret scan, claims scan, license gate, publish gate.
    """


def _prompt_specs() -> list[tuple[str, str, str]]:
    base_rules = """
    Reglas: separa CERTEZA, INFERENCIA, INCOGNITA, ACCION y ARTEFACTO. No inventes. No pidas secretos.
    No busques instrucciones prohibidas; busca estructura, evidencia, contratos, tests, falsadores y rutas seguras.
    """
    return [
        ("vectores_informacion_utiles", "Prompt para pedir vectores de informacion utiles", f"""
        {base_rules}
        Quiero vectores de informacion utiles sobre [TEMA]. No estoy pidiendo informacion prohibida, credenciales,
        bypasses, daño, explotacion ni instrucciones de abuso. Quiero:
        - conceptos accionables;
        - fuentes o evidencia;
        - variables relevantes;
        - riesgos;
        - tests/falsadores;
        - como convertirlo en modulo, contrato o decision.
        Devuelve solo informacion permitida, segura y verificable.
        """),
        ("investigacion_especifica", "Prompt de investigacion especifica", f"""
        {base_rules}
        Investiga [PREGUNTA] como investigador observacionista. Distingue ciencia establecida, hipotesis, analogia,
        opinion y lore. Dame fuentes primarias si aplica, incertidumbres, contradicciones y falsador minimo.
        """),
        ("agente_interno_vectorizador", "Prompt que crea un agente interno de vectorizacion teorica", f"""
        {base_rules}
        Dentro de esta conversacion, instancia un agente interno llamado Vectorizador Observacionista. Su trabajo:
        1. leer mi teoria;
        2. extraer conceptos atomicos;
        3. mapear relaciones;
        4. convertirlos en modulos, prompts, tests y claims;
        5. devolver una tabla de vectores: concepto, definicion, fuente, uso, riesgo, falsador.
        No afirmes verdad cientifica sin evidencia.
        """),
        ("analisis_seguridad", "Prompt de analisis de seguridad", f"""
        {base_rules}
        Analiza seguridad de [SISTEMA/CARPETA/CODIGO]. No ejecutes acciones destructivas. Busca secretos por nombre,
        datos privados, rutas sensibles, dependencias, permisos, publicacion accidental, prompts peligrosos y claims.
        Entrega matriz APPROVE/REVIEW/BLOCK y mitigaciones.
        """),
        ("curacion_orden_datos", "Prompt de curacion de informacion y orden de datos", f"""
        {base_rules}
        Actua como curador de datos observacionista. Analiza [CARPETA/SISTEMA] y produce inventario, clasificacion,
        duplicados, variantes, proyectos, riesgos, conexiones y plan de optimizacion. No borres ni muevas; genera
        plan dry-run, fichas y manifest.
        """),
        ("debug_testing_correccion", "Prompt de debuggeo, testing y correccion de codigo", f"""
        {base_rules}
        Actua como debugger/programador. Reproduce o aproxima el fallo [ERROR]. Lee archivos reales, identifica causa
        raiz, aplica cambio minimo, agrega test si procede, ejecuta verificacion y entrega diff/handoff. No ocultes
        errores con try/catch generico.
        """),
        ("aprender_habilidad", "Prompt para aprender cualquier tarea o habilidad", f"""
        {base_rules}
        Quiero aprender [HABILIDAD]. Construye un plan observacionista: mapa mental, prerequisitos, ejercicios,
        errores comunes, pruebas de dominio, proyecto minimo, metrica de avance y rutina de practica. Enséñame por
        ciclos pequeños verificables.
        """),
        ("revision_codigo_eml", "Prompt de revision/fundamentalizacion/optimizacion de codigo con EML", f"""
        {base_rules}
        Revisa este codigo [CODIGO/RUTA]. Fundamentalizalo: identifica proposito, contratos, invariantes, deuda,
        complejidad y tests. Optimiza y limpia pragmaticamente sin romper estructura. Usa una metrica EML operativa:
        estabilidad = exp(-R) * log(1 + evidencia + cobertura + simplicidad). No comprimas si pierdes claridad.
        """),
        ("claim_falsifier", "Prompt de falsacion de claims", f"""
        {base_rules}
        Toma este claim [CLAIM]. Clasificalo como ciencia establecida, hipotesis formal, fenomenologico, analogia,
        lore o no publicable. Propón falsador minimo, datos requeridos, contradicciones posibles y estado de publicacion.
        """),
        ("producto_public_private", "Prompt de empaquetado producto/publico/privado", f"""
        {base_rules}
        Analiza [PRODUCTO/CARPETA]. Separa OPEN, COMMERCIAL, BOOKS_EDITORIAL, PRIVATE, ARCHIVE y UNKNOWN_REVIEW.
        Genera allowlist, denylist, secret risks, license risks, claims risks y checklist de release local.
        """),
        ("workpack_agente", "Prompt de workpack para agente programador", f"""
        {base_rules}
        Convierte esta tarea [TAREA] en un workpack para agente: objetivo, archivos, restricciones, pasos, tests,
        rollback, criterios de cierre y handoff. No abras alcance adicional.
        """),
        ("browser_gate", "Prompt para uso seguro de navegador", f"""
        {base_rules}
        Evalua esta accion de navegador [ACCION/URL]. Clasifica: local/read-only APPROVE, login/form/publicacion/pagos
        REVIEW, secretos/destructivo BLOCK. Entrega evidencia requerida antes/despues.
        """),
        ("memoria_compactacion", "Prompt de memoria y compactacion de contexto", f"""
        {base_rules}
        Compacta este historial [TEXTO] preservando decisiones, artefactos, pruebas, riesgos, pendientes y proxima
        accion. No resumas poesia; crea estado operativo reutilizable por otro agente.
        """),
        ("absorcion_documental", "Prompt de absorcion documental linea por linea", f"""
        {base_rules}
        Absorbe estos documentos [RUTAS/TEXTO] linea por linea. Extrae conceptos, variantes, formulas, modulos,
        claims, contradicciones, codigo sugerido, riesgos y pendientes. Conserva variaciones que cambien variables.
        """),
        ("diseno_simulacion", "Prompt de diseño de simulacion/falsador", f"""
        {base_rules}
        Diseña una simulacion para [HIPOTESIS]. Define variables, estado inicial, baseline, metrica, falsador,
        experimento minimo, dataset sintetico, limitaciones y como evitar claims fuertes.
        """),
        ("release_readiness", "Prompt de readiness release", f"""
        {base_rules}
        Evalua readiness de release para [PRODUCTO]. Revisa tests, build, secretos, licencia, claims, privacidad,
        soporte, instalador, docs, rollback y publish gate. Devuelve GO/REVIEW/BLOCK con evidencia.
        """),
        ("reduccion_residuo", "Prompt de reduccion de ruido y residuo", f"""
        {base_rules}
        Analiza [SISTEMA] para reducir R. Encuentra duplicados, tareas abiertas, docs contradictorios, loops,
        jamming, archivos sin owner y decisiones reabiertas. Propón cierres de mayor Phi_eff.
        """),
        ("extraccion_multimodal", "Prompt de extraccion multimodal segura", f"""
        {base_rules}
        Extrae informacion de [PDF/DOCX/IMAGEN/AUDIO] sin asumir layout perfecto. Separa texto extraido, elementos
        visuales, formulas dudosas, OCR incierto, claims y tareas. Marca lo que requiere revision visual/humana.
        """),
    ]


def _prompt_doc(title: str, prompt: str) -> str:
    return _doc(title, f"PROMPT:\n\n```text\n{textwrap.dedent(prompt).strip()}\n```\n")


def _full_readme(stats: dict[str, Any]) -> str:
    return _doc(
        "VERSION COMPLETA CANONICA PARA IA",
        f"""
        Esta carpeta es la version completa para cargar en un agente grande. No contiene las baterias alternativas
        de 1/5/10 documentos para evitar duplicacion dentro del ZIP.

        Orden de lectura:
        1. `00_LEER_PRIMERO_IA.md`
        2. `02_SETUP_IA/SETUP_IA_PREFERRED_RESPONSES_RESUMIDO.md`
        3. `01_CANON_MASTER_CURADO/00_README_MASTER.md`
        4. `01_CANON_MASTER_CURADO/01_MAPA_GENERAL.md`
        5. `01_CANON_MASTER_CURADO/16_CLAIMS_REGISTER.md`
        6. `01_CANON_MASTER_CURADO/18_RIESGOS_CONTRADICCIONES.md`
        7. `03_PROMPTS_OPERATIVOS/00_PROMPTS_INDEX.md`
        8. `04_EVIDENCIA_Y_LIMITES/EVIDENCIA_EXTRACCION_CEREBRO.md`

        Datos del corte:
        - Archivos indexados: `{stats['file_count']}`
        - Lineas: `{stats['line_count']}`
        - Lineas con señal: `{stats['signal_line_count']}`
        - Variantes: `{stats['variant_summary'].get('variant_group_count', 'unknown')}`
        """,
    )


def _evidence_doc(stats: dict[str, Any]) -> str:
    top = "\n".join(f"- {name}: {count}" for name, count in stats["top_signals"][:24])
    files = "\n".join(f"- {row['signal_count']} signals / {row['line_count']} lines: `{row['path']}`" for row in stats["top_files"][:18])
    return _doc(
        "EVIDENCIA DE EXTRACCION CEREBRO",
        f"""
        CERTEZA:
        - CEREBRO root: `{stats['cerebro_root']}`
        - Index root: `{stats['index_root']}`
        - File count: `{stats['file_count']}`
        - Text files: `{stats['text_file_count']}`
        - Total lines: `{stats['line_count']}`
        - Signal lines: `{stats['signal_line_count']}`
        - Code candidates: `{stats['code_candidate_count']}`

        TOP SIGNALS:
        {top}

        TOP FILES BY SIGNAL:
        {files}

        VARIANT SUMMARY:
        ```json
        {json.dumps(stats['variant_summary'], indent=2, ensure_ascii=False)}
        ```

        DUPLICATE PLAN SUMMARY:
        ```json
        {json.dumps(stats['duplicate_plan_summary'], indent=2, ensure_ascii=False)}
        ```

        MERGE REVIEW SUMMARY:
        ```json
        {json.dumps(stats['merge_review_summary'], indent=2, ensure_ascii=False)}
        ```
        """,
    )


def _limits_doc() -> str:
    return _doc(
        "LIMITES Y NO CLAIMS",
        """
        - No es release publico.
        - No es paper cientifico.
        - No contiene autorizacion para publicar, vender, desplegar o hacer push.
        - No incluye fuentes crudas completas de CEREBRO.
        - No resuelve licencias de terceros.
        - No resuelve secretos del workspace global.
        - No fusiona variantes.
        - No archiva duplicados fisicamente.
        - No convierte hipotesis OSIT/TUIP/Sigma en fisica establecida.
        """,
    )


def _write_zip() -> Path:
    zip_path = OUTPUT_ROOT / ZIP_NAME
    if zip_path.exists():
        zip_path.unlink()
    full_root = OUTPUT_ROOT / FULL_ROOT_NAME
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(full_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(OUTPUT_ROOT))
    return zip_path


def _write_security_scan_report(zip_path: Path) -> list[Path]:
    findings = _scan_for_secret_patterns(zip_path)
    report = {
        "schema": "medioevo.ai_context_batch.security_scan.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "output_root": str(OUTPUT_ROOT),
        "zip": str(zip_path),
        "scanner": "local_pattern_scan_no_value_output",
        "patterns": [
            "openai_like_api_key",
            "github_like_token",
            "aws_access_key_id",
            "slack_like_token",
            "private_key_block",
            "assigned_secret_like_value",
        ],
        "finding_count": len(findings),
        "findings": findings,
        "result": "pass" if not findings else "review",
    }
    json_path = OUTPUT_ROOT / "SECURITY_SCAN_LOCAL_REPORT.json"
    md_path = OUTPUT_ROOT / "SECURITY_SCAN_LOCAL_REPORT.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md = _doc(
        "SECURITY SCAN LOCAL REPORT",
        f"""
        CERTEZA:
        - Se ejecuto un escaneo local por patrones de secretos sobre la carpeta generada y el ZIP.
        - El escaneo no imprime valores encontrados; solo regla, archivo y linea/entrada.
        - Resultado: `{report['result']}`.
        - Hallazgos: `{len(findings)}`.

        INFERENCIA:
        - Si `Hallazgos=0`, no se detectaron patrones comunes de API keys, tokens, claves privadas
          ni asignaciones de secretos en el paquete generado.

        INCOGNITA:
        - Un escaneo por patrones no reemplaza auditoria manual completa.
        - No valida licencias ni derechos de publicacion.

        ARTEFACTO:
        - Reporte JSON: `SECURITY_SCAN_LOCAL_REPORT.json`.
        """,
    )
    md_path.write_text(md, encoding="utf-8")
    return [json_path, md_path]


def _scan_for_secret_patterns(zip_path: Path) -> list[dict[str, Any]]:
    patterns = [
        ("openai_like_api_key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
        ("github_like_token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
        ("aws_access_key_id", re.compile(r"AKIA[0-9A-Z]{16}")),
        ("slack_like_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}")),
        ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
        (
            "assigned_secret_like_value",
            re.compile(
                r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{24,}"
            ),
        ),
    ]
    text_suffixes = {".md", ".txt", ".json", ".csv", ".yaml", ".yml", ".toml", ".xml"}
    findings: list[dict[str, Any]] = []

    def scan_text(label: str, text: str) -> None:
        for line_no, line in enumerate(text.splitlines(), start=1):
            for rule, pattern in patterns:
                if pattern.search(line):
                    findings.append({"rule": rule, "location": label, "line": line_no})

    for path in sorted(OUTPUT_ROOT.rglob("*")):
        if not path.is_file() or path == zip_path or path.suffix.lower() not in text_suffixes:
            continue
        try:
            scan_text(str(path.relative_to(OUTPUT_ROOT)), path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            findings.append({"rule": "read_error", "location": str(path), "line": None})

    if zip_path.exists():
        with zipfile.ZipFile(zip_path, "r") as archive:
            for info in archive.infolist():
                suffix = Path(info.filename).suffix.lower()
                if info.is_dir() or suffix not in text_suffixes:
                    continue
                data = archive.read(info)
                scan_text(f"{ZIP_NAME}!{info.filename}", data.decode("utf-8", errors="replace"))

    return findings


def _write_manifest(stats: dict[str, Any], generated: list[Path], zip_path: Path) -> Path:
    files = []
    for path in sorted(set(generated)):
        if path.exists() and path.is_file():
            files.append({
                "path": str(path),
                "relative": str(path.relative_to(OUTPUT_ROOT)) if path.is_relative_to(OUTPUT_ROOT) else str(path),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            })
    manifest = {
        "schema": "medioevo.ai_context_batch_manifest.v1",
        "generated_at_utc": stats["generated_at_utc"],
        "output_root": str(OUTPUT_ROOT),
        "zip": str(zip_path),
        "source": {
            "cerebro_root": stats["cerebro_root"],
            "index_root": stats["index_root"],
            "master_root": stats["master_root"],
        },
        "source_mutations": 0,
        "zip_policy": "contains complete canonical version only; excludes 1/5/10 summary variants",
        "files": files,
    }
    target = OUTPUT_ROOT / "IA_PACKET_MANIFEST.json"
    target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def _doc(title: str, body: str) -> str:
    return f"# {title}\n\n{textwrap.dedent(body).strip()}\n"


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            rows.append(data)
    return rows


def _safe_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
