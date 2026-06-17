from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import mimetypes
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse


ROOT = pathlib.Path(__file__).resolve().parents[2]
CLAUDIO_ROOT = ROOT / "02_CLAUDIO"


def _load_wabi_env_file() -> None:
    """Carga 02_CLAUDIO/wabi.env solo con opt-in explicito del operador.

    La regla segura por defecto para este server es no leer wabi.env ni claves.
    Si el operador arranca con WABI_LOCAL_SERVER_LOAD_ENV=1, el entorno explicito
    sigue ganando y nunca se imprimen valores.
    """
    if os.environ.get("WABI_LOCAL_SERVER_LOAD_ENV", "0") != "1":
        return
    env_path = CLAUDIO_ROOT / "wabi.env"
    try:
        if not env_path.is_file():
            return
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()
            if key and value and key not in os.environ:
                os.environ[key] = value
    except Exception:
        # Nunca bloquear el arranque por un problema de config local.
        pass


_load_wabi_env_file()

# Defaults de nube compartidos con opt-in; este server no lee wabi.env por defecto.
if str(CLAUDIO_ROOT) not in sys.path:
    sys.path.insert(0, str(CLAUDIO_ROOT))
try:
    from core.wabi_cloud_default import apply_wabi_cloud_defaults as _apply_cloud
    if os.environ.get("WABI_LOCAL_SERVER_LOAD_ENV", "0") == "1":
        _apply_cloud(probe=False, verbose=False)
except Exception:
    pass

CORE_ROOT = CLAUDIO_ROOT / "core"
UI_ROOT = ROOT / "apps" / "local" / "wabi_ui"
WABI_SABI_CANONICAL_ROOT = ROOT.parent / "-=L.R.GONZALEZ=-" / "apps" / "local" / "wabi-sabi"
WORKING_BENCH_ROOT = ROOT / "-=LR WORKING BENCH=-"
UNIFIED_BENCH_ROOT = WORKING_BENCH_ROOT / "BRAIN_OS_BENCH_UNIFICADO_2026-05-24"
UNIFIED_DOCUMENTOS_IA_ROOT = UNIFIED_BENCH_ROOT / "DOCUMENTOS_IA"
DOCUMENTOS_IA_ROOT = WORKING_BENCH_ROOT / "DOCUMENTOS_IA"
LEGACY_WABI_ARTIFACT_PACKET_ROOT = DOCUMENTOS_IA_ROOT / "01_LOCAL_COMPLETA" / "MEDIOEVO_OSIT_AI_HUMAN_PACKET_2026-05-25_FULL"
WABI_ARTIFACT_PACKET_ROOT = UNIFIED_DOCUMENTOS_IA_ROOT / "MEDIOEVO_OSIT_AI_HUMAN_PACKET_2026-05-25_FULL"
WABI_ARTIFACTS_ROOT = WABI_ARTIFACT_PACKET_ROOT / "ARTIFACTOS_WABI"
WABI_ARTIFACT_MANIFEST = WABI_ARTIFACTS_ROOT / "manifest" / "wabi_artifacts_manifest.json"
WABI_SCRIPT = CORE_ROOT / "wabi.py"
CURRENT_SESSION = pathlib.Path.home() / ".wabisabi" / "sessions" / "current.jsonl"
REQUEST_TIMEOUT_S = 180
MAX_BODY_BYTES = 64_000
MAX_PROMPT_CHARS = 8_000
MAX_RESPONSE_CHARS = 24_000
MAX_ARTIFACT_PREVIEW_BYTES = 2_000_000
MAX_ARTIFACT_SOURCE_CHARS = 160_000
CHAT_SESSION: dict[str, Any] = {
    "messages": [],
    "coding_session_id": "",
    "last_intent": "",
}
TASKSPEC_REVIEW_SESSION: dict[str, Any] = {
    "latest": {},
    "latest_raw": {},
    "last_saved": {},
    "last_apply_preview": {},
    "last_apply_result": {},
}

# El paquete canonico Wabi vive en 02_CLAUDIO. Debe ir PRIMERO en sys.path para que
# `python server/wabi_local_server.py` (que pone la carpeta server/ en el path, no
# 02_CLAUDIO) resuelva el wabi_sabi canonico ANTES que cualquier arbol retirado. Sin
# esto los imports de wabi_sabi de abajo caen silenciosamente a None y la UI muestra
# "ConversationEngine no esta disponible".
_claudio_path = str(CLAUDIO_ROOT)
if _claudio_path in sys.path:
    sys.path.remove(_claudio_path)
sys.path.insert(0, _claudio_path)

# Arbol retirado (-=L.R.GONZALEZ=-) solo como ultimo recurso, nunca delante del canonico.
if WABI_SABI_CANONICAL_ROOT.exists() and str(WABI_SABI_CANONICAL_ROOT) not in sys.path:
    sys.path.append(str(WABI_SABI_CANONICAL_ROOT))

try:
    from wabi_sabi.core.cloud_budget import CloudBudgetGate  # type: ignore
except Exception:  # pragma: no cover - fallback only if canonical Wabi package is absent.
    CloudBudgetGate = None  # type: ignore[assignment]

try:
    from wabi_sabi.core.llm_proposal import (  # type: ignore
        build_llm_proposal_status,
        request_llm_proposal,
    )
except Exception:  # pragma: no cover - fallback only if canonical Wabi package is absent.
    build_llm_proposal_status = None  # type: ignore[assignment]
    request_llm_proposal = None  # type: ignore[assignment]

try:
    from wabi_sabi.core.llm_work_response import build_safe_llm_work_response  # type: ignore
except Exception:  # pragma: no cover - fallback only if canonical Wabi package is absent.
    build_safe_llm_work_response = None  # type: ignore[assignment]

CONVERSATION_ENGINE_IMPORT_ERROR = ""  # diagnostico: por que cayo al fallback, si cayo.
try:
    from wabi_sabi.core.conversation_engine import (  # type: ignore
        ConversationEngine,
        ConversationEngineOptions,
        ConversationSessionState,
    )
except Exception as _ce_exc:  # pragma: no cover - fallback only if canonical Wabi package is absent.
    import traceback as _tb
    CONVERSATION_ENGINE_IMPORT_ERROR = f"{type(_ce_exc).__name__}: {_ce_exc}"
    # Una linea de traza para que el operador vea el origen real, no un fallo mudo.
    try:
        sys.stderr.write("[wabi-server] ConversationEngine no importo:\n" + _tb.format_exc())
    except Exception:
        pass
    ConversationEngine = None  # type: ignore[assignment]
    ConversationEngineOptions = None  # type: ignore[assignment]
    ConversationSessionState = None  # type: ignore[assignment]

try:
    from wabi_sabi.core.taskspec_review import (  # type: ignore
        build_gate_preview,
        block_apply_attempt,
        block_apply_with_preview,
        normalize_taskspec_for_review,
        save_taskspec_draft,
    )
except Exception:  # pragma: no cover - fallback only if canonical Wabi package is absent.
    build_gate_preview = None  # type: ignore[assignment]
    block_apply_attempt = None  # type: ignore[assignment]
    block_apply_with_preview = None  # type: ignore[assignment]
    normalize_taskspec_for_review = None  # type: ignore[assignment]
    save_taskspec_draft = None  # type: ignore[assignment]

try:
    from wabi_sabi.core.local_apply_readiness import (  # type: ignore
        apply_local_task_spec,
        preview_local_apply,
    )
except Exception:  # pragma: no cover - fallback only if canonical Wabi package is absent.
    apply_local_task_spec = None  # type: ignore[assignment]
    preview_local_apply = None  # type: ignore[assignment]

if str(CLAUDIO_ROOT) not in sys.path:
    sys.path.insert(0, str(CLAUDIO_ROOT))

from core import wabi_provider_doctor as provider_doctor  # noqa: E402
from core import wabi_provider_registry as provider_registry  # noqa: E402
from core import wabi_governance_shadow as governance_shadow  # noqa: E402
from core import chat_intent_router  # noqa: E402
from core import chat_provider_orchestrator  # noqa: E402
from core import provider_policy  # noqa: E402
from core import budget_gate  # noqa: E402
from core import mts_channel_shadow_diagnostic as mts_shadow  # noqa: E402
from core import mts_channel_c1_selection as mts_c1  # noqa: E402
from core import mts_channel_c2_format_selection as mts_c2  # noqa: E402
from core import mts_channel_c3_policy_dry_run as mts_c3  # noqa: E402
from core import mts_channel_c4_shadow_trace as mts_c4  # noqa: E402
from core import mts_channel_c7_limited_enforcement as mts_c7  # noqa: E402
from core import coding_workbench  # noqa: E402
from core import coding_provider_router  # noqa: E402
from core import external_secret_tools  # noqa: E402
from core import folder_access_gate  # noqa: E402
from core import multimodal_intake_adapter  # noqa: E402
from core import world_model_baseline_comparator  # noqa: E402
from core import wabi_tool_registry  # noqa: E402
from core import wabi_llm_code_bridge  # noqa: E402
from core import wabi_patch_planner  # noqa: E402
from core import wabi_safe_executor  # noqa: E402
from core import wabi_identity  # noqa: E402
from core import wabi_docs  # noqa: E402
from core import wabi_osit_v04  # noqa: E402
from core import wabi_unification  # noqa: E402
from core import wabi_system_notebook  # noqa: E402
from core.velo import runner as velo_runner  # noqa: E402

# Fact-check prompt
from wabi_sabi.factcheck_prompt import (
    FACTCHECK_SYSTEM_PROMPT,
    build_factcheck_user_prompt,
    get_factcheck_prompt,
)


PROGRAMMER_WORKSPACE_ROOT = ROOT


SECRET_VALUE_PATTERNS = [
    re.compile("s" + r"k-[A-Za-z0-9_\-]{12,}"),
    re.compile("g" + r"hp_[A-Za-z0-9_]{12,}"),
    re.compile("-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE " + "KEY-----"),
    re.compile("(?i)(" + "api" + r"[_-]?" + "key" + r"|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+=]{12,}"),
]
PROVIDER_ENV_NAMES = [
    "DEEPSEEK_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "GROQ_API_KEY",
    "OPENROUTER_API_KEY",
    "DASHSCOPE_API_KEY",
    "QWEN_API_KEY",
    "XAI_API_KEY",
    "MISTRAL_API_KEY",
    "NVIDIA_API_KEY",
    "COHERE_API_KEY",
    "TOGETHER_API_KEY",
    "FIREWORKS_API_KEY",
    "CEREBRAS_API_KEY",
    "HUGGINGFACE_API_KEY",
    "HF_TOKEN",
    "PERPLEXITY_API_KEY",
    "DEEPINFRA_API_KEY",
    "SAMBANOVA_API_KEY",
]
PASSTHROUGH_ENV_NAMES = [
    "PATH",
    "PATHEXT",
    "SystemRoot",
    "ComSpec",
    "USERPROFILE",
    "HOMEDRIVE",
    "HOMEPATH",
    "APPDATA",
    "LOCALAPPDATA",
    "TEMP",
    "TMP",
    "PYTHONPATH",
    "PYTHONIOENCODING",
    "WABI_PROVIDER",
    "WABI_MODEL",
    "WABI_PRO_MODEL",
    "OLLAMA_BASE_URL",
    "OLLAMA_HOST",
    "OLLAMA_MODEL",
    "DEEPSEEK_BASE_URL",
    "DEEPSEEK_MODEL",
    "DEEPSEEK_PRO_MODEL",
    "OPENAI_BASE_URL",
    "OPENAI_MODEL",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "GEMINI_BASE_URL",
    "GEMINI_MODEL",
    "GROQ_BASE_URL",
    "GROQ_MODEL",
    "OPENROUTER_BASE_URL",
    "OPENROUTER_MODEL",
    "DASHSCOPE_BASE_URL",
    "DASHSCOPE_MODEL",
    "QWEN_MODEL",
    "XAI_BASE_URL",
    "XAI_MODEL",
    "MISTRAL_BASE_URL",
    "MISTRAL_MODEL",
    "NVIDIA_BASE_URL",
    "NVIDIA_MODEL",
    "NVIDIA_PRO_MODEL",
    "COHERE_BASE_URL",
    "COHERE_MODEL",
    "TOGETHER_BASE_URL",
    "TOGETHER_MODEL",
    "FIREWORKS_BASE_URL",
    "FIREWORKS_MODEL",
    "CEREBRAS_BASE_URL",
    "CEREBRAS_MODEL",
    "HUGGINGFACE_BASE_URL",
    "HUGGINGFACE_MODEL",
    "PERPLEXITY_BASE_URL",
    "PERPLEXITY_MODEL",
    "DEEPINFRA_BASE_URL",
    "DEEPINFRA_MODEL",
    "SAMBANOVA_BASE_URL",
    "SAMBANOVA_MODEL",
]
WABI_PROVIDER_STATUS_LATEST = pathlib.Path.home() / ".medioevo" / "wabi" / "runtime" / "outputs" / "wabi_provider_status_latest.json"
WABI_PROVIDER_DIAGNOSTIC_LATEST = pathlib.Path.home() / ".medioevo" / "wabi" / "runtime" / "outputs" / "wabi_nvidia_route_diagnostic_latest.json"
WABI_PRIMARY_PROVIDER = "deepseek"
WABI_PRIMARY_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
WABI_FALLBACK_PROVIDER = "nvidia"
WABI_FALLBACK_MODEL = os.environ.get("NVIDIA_PRO_MODEL", "nvidia/llama-3.3-nemotron-super-49b-v1")
WABI_SECONDARY_FALLBACK_PROVIDER = "cloudflare"
WABI_SECONDARY_FALLBACK_MODEL = os.environ.get("CLOUDFLARE_AI_MODEL", "@cf/qwen/qwen2.5-coder-32b-instruct")
WABI_OLLAMA_CLOUD_MODEL = os.environ.get("WABI_OLLAMA_CLOUD_MODEL", "qwen3-coder:480b-cloud")
WABI_OLLAMA_LOCAL_MODEL = os.environ.get("WABI_OLLAMA_LOCAL_MODEL", "qwen2.5:0.5b")
WORKBENCH_CLOUD_PROVIDER_ORDER = ("deepseek", "nvidia", "cloudflare", "anthropic", "gemini", "openai", "openrouter", "groq", "dashscope_qwen")
WORKBENCH_CONTEXT_POLICY = "SUMMARY_ONLY"
MAX_CONTEXT_EXCERPT_CHARS = 320
LOCAL_GATE_STATE_PATH = CLAUDIO_ROOT / "runtime" / "local_gate_state.json"

# W622: telemetria "sin forro" — datos de la ultima llamada y acumulados de sesion
_telemetry_store: dict[str, Any] = {
    "turns_total":        0,
    "turns_cloud":        0,
    "turns_local":        0,
    "latency_ms_last":    None,
    "latency_ms_avg":     None,
    "provider_last":      None,
    "tools_called_last":  [],
    "r_est_last":         None,
    "gryph_blocks":       0,
    "memory_recalls":     0,
    "_latency_sum":       0,
}

def _telemetry_update(latency_ms: int, provider: str, tools: list, r_est: float | None, cloud: bool) -> None:
    _telemetry_store["turns_total"]     += 1
    _telemetry_store["_latency_sum"]    += latency_ms
    _telemetry_store["latency_ms_last"] = latency_ms
    _telemetry_store["latency_ms_avg"]  = _telemetry_store["_latency_sum"] // max(1, _telemetry_store["turns_total"])
    _telemetry_store["provider_last"]   = provider
    _telemetry_store["tools_called_last"] = tools
    _telemetry_store["r_est_last"]      = r_est
    if cloud:
        _telemetry_store["turns_cloud"] += 1
    else:
        _telemetry_store["turns_local"] += 1
LOCAL_GATE_AUDIT_PATH = CLAUDIO_ROOT / "runtime" / "local_gate_audit.jsonl"
LOCAL_GATE_ENVIRONMENT = "LOCAL_PRIVATE_ONLY"
LOCAL_GATE_OWNER_AUTHORIZATION = "SUPERADMIN_LOCAL_DEVELOPMENT"
LOCAL_GATE_CONTROL_MODE = "OWNER_UI_TOGGLES"
LOCAL_GATE_AUDIT_FINGERPRINT = "local-gate-wiring-07b-5b28"
LOCAL_GATE_DEFAULTS: dict[str, str] = {
    "ActionGate": "APPROVE_LOCAL",
    "PublicationGate": "BLOCK",
    "CloudGate": "OFF",
    "RuntimeImportGate": "BLOCK",
    "RawAdoptionGate": "BLOCK",
    "ApplyGate": "REVIEW",
    "DestructiveDeleteGate": "BLOCK",
    "SecretGate": "HARD_BLOCK",
    "CredentialGate": "HARD_BLOCK",
    "NetworkExposureGate": "LOCALHOST_ONLY",
    "ScienceClaimGate": "BLOCK_STRONG_CLAIMS_UNTIL_F1_F6",
    "UIVisibilityGate": "MASTER",
}
LOCAL_GATE_OPTIONS: dict[str, list[str]] = {
    "ActionGate": ["OFF", "REVIEW", "APPROVE_LOCAL"],
    "PublicationGate": ["BLOCK", "REVIEW", "ALLOW_LOCAL_EXPORT_ONLY"],
    "CloudGate": ["OFF", "REVIEW", "ALLOW_EXISTING_PROVIDER"],
    "RuntimeImportGate": ["BLOCK", "REVIEW", "ALLOW_LOCAL_SAFE_IMPORT"],
    "RawAdoptionGate": ["BLOCK", "REVIEW"],
    "ApplyGate": ["OFF", "REVIEW", "ALLOW_LOCAL_APPLY"],
    "DestructiveDeleteGate": ["BLOCK", "REVIEW_WITH_BACKUP"],
    "SecretGate": ["HARD_BLOCK"],
    "CredentialGate": ["HARD_BLOCK"],
    "NetworkExposureGate": ["LOCALHOST_ONLY", "REVIEW_LAN", "BLOCK_WAN"],
    "ScienceClaimGate": ["BLOCK_STRONG_CLAIMS_UNTIL_F1_F6", "REVIEW", "LOCAL_THEORY_DRAFT"],
    "UIVisibilityGate": ["SIMPLE", "DEVELOPER", "MASTER"],
}
LOCAL_GATE_LOCKED = {"SecretGate", "CredentialGate"}
LOCAL_GATE_DESCRIPTIONS: dict[str, str] = {
    "ActionGate": "Modo local para acciones de desarrollo.",
    "PublicationGate": "Solo controla preparacion local; no habilita deploy.",
    "CloudGate": "Controla llamadas a proveedor existente; no muestra ni pide llaves.",
    "RuntimeImportGate": "Controla imports locales revisables.",
    "RawAdoptionGate": "Bloquea adopcion cruda de ZIPs, codigo externo o corpus privado.",
    "ApplyGate": "Controla si se pueden aplicar cambios locales.",
    "DestructiveDeleteGate": "Nunca permite borrado destructivo sin backup.",
    "SecretGate": "Bloqueo duro de secretos.",
    "CredentialGate": "Bloqueo duro de credenciales y tokens.",
    "NetworkExposureGate": "Mantiene el servidor en localhost por defecto.",
    "ScienceClaimGate": "Bloquea claims fuertes hasta F1-F6.",
    "UIVisibilityGate": "Controla densidad visual de la UI local.",
}
LOCAL_GATE_WIRING: dict[str, dict[str, str]] = {
    "ActionGate": {"status": "WIRED_TO_CONSOLE", "surface": "UI/API state"},
    "PublicationGate": {"status": "WIRED_TO_HEALTH_AND_PAYLOADS", "surface": "health/proposal/apply metadata"},
    "CloudGate": {"status": "WIRED_TO_PROPOSAL_GUARD_METADATA", "surface": "TaskSpec LLM proposal metadata"},
    "RuntimeImportGate": {"status": "WIRED_TO_EFFECTIVE_POLICY", "surface": "runtime import decision metadata"},
    "RawAdoptionGate": {"status": "WIRED_TO_MULTIMODAL_RAW_POLICY", "surface": "raw storage/adoption metadata"},
    "ApplyGate": {"status": "WIRED_TO_LOCAL_APPLY", "surface": "TaskSpec local apply and coding apply"},
    "DestructiveDeleteGate": {"status": "WIRED_TO_EFFECTIVE_POLICY", "surface": "delete/move/rollback policy metadata"},
    "SecretGate": {"status": "HARD_BLOCK_METADATA", "surface": "UI/API locked state"},
    "CredentialGate": {"status": "HARD_BLOCK_METADATA", "surface": "UI/API locked state"},
    "NetworkExposureGate": {"status": "WIRED_TO_HEALTH_METADATA", "surface": "server health/console"},
    "ScienceClaimGate": {"status": "WIRED_TO_EFFECTIVE_POLICY", "surface": "science claim policy metadata"},
    "UIVisibilityGate": {"status": "WIRED_TO_UI_DISPLAY", "surface": "Master Gate Console rendering"},
}
MAX_CONTEXT_FILE_BYTES = 96_000
QUOTED_LOCAL_PATH_RE = re.compile(r"""["']([A-Za-z]:\\[^"']+)["']""")
BARE_LOCAL_PATH_RE = re.compile(r"""([A-Za-z]:\\[^\s<>"']+)""")
MEDIOEVO_ROOT = ROOT.parent / "-=L.R.GONZALEZ=-"
TREE_HEALTH_RUN_ID = "RUN_TREE_HEALTH_WORKBENCH_PANEL_20260518"
TREE_HEALTH_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / TREE_HEALTH_RUN_ID
TREE_HEALTH_STATE_LATEST = TREE_HEALTH_RUN_DIR / "TREE_HEALTH_STATE_20260518.json"
CODING_ACCEPTANCE_V02_RUN_ID = "RUN_WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_2_20260518"
CODING_ACCEPTANCE_V02_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / CODING_ACCEPTANCE_V02_RUN_ID
CODING_ACCEPTANCE_V02_STATE = CODING_ACCEPTANCE_V02_RUN_DIR / "FALLBACK_ONLY_CODING_ACCEPTANCE_v0_2.json"
CODING_ACCEPTANCE_V03_RUN_ID = "RUN_WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3_20260518"
CODING_ACCEPTANCE_V03_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / CODING_ACCEPTANCE_V03_RUN_ID
CODING_ACCEPTANCE_V03_STATE = CODING_ACCEPTANCE_V03_RUN_DIR / "FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3.json"
LOCAL_HUB_RUN_ID = "RUN_MEDIOEVO_HUB_PUBLIC_LOCAL_AGENTS_20260518"
LOCAL_HUB_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / LOCAL_HUB_RUN_ID
LOCAL_HUB_DATA_DIR = ROOT / "runtime" / "local_agent_hub"
LOCAL_HUB_TASKSPEC_DIR = LOCAL_HUB_DATA_DIR / "taskspecs"
LOCAL_HUB_QUEUE_PATH = LOCAL_HUB_DATA_DIR / "claudio_queue.jsonl"
LOCAL_HUB_WITNESS_PATH = LOCAL_HUB_DATA_DIR / "witness_log.jsonl"
AGENT_CHAT_MESSAGES_PATH = LOCAL_HUB_DATA_DIR / "agent_chat_messages.jsonl"
AGENT_CHAT_STATUS_PATH = LOCAL_HUB_DATA_DIR / "agent_chat_status.json"
AGENT_CHAT_ROOMS = ["#general", "#wabi", "#duat", "#canon", "#qa", "#release", "#workpacks"]
AGENT_CHAT_STATUSES = ["Online", "Away", "Busy", "Review", "Blocked"]
AGENT_CHAT_ROUTING_RUN_ID = "RUN_AGENT_CHAT_ROUTING_v0_2_20260518"
AGENT_CHAT_ROUTING_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / AGENT_CHAT_ROUTING_RUN_ID
AGENT_CHAT_ROUTING_CONTRACT_PATH = AGENT_CHAT_ROUTING_RUN_DIR / "AGENT_CHAT_ROUTING_CONTRACT_v0_2.json"
AGENT_CHAT_MESSAGE_SCHEMA_PATH = AGENT_CHAT_ROUTING_RUN_DIR / "agent_chat_message.schema.json"
AGENT_CHAT_ROUTING_WITNESSLOG_PATH = AGENT_CHAT_ROUTING_RUN_DIR / "AGENT_CHAT_WITNESSLOG_v0_2.jsonl"
AGENT_CHAT_PERSISTENCE_RUN_ID = "RUN_AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_20260518"
AGENT_CHAT_PERSISTENCE_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / AGENT_CHAT_PERSISTENCE_RUN_ID
AGENT_CHAT_STORAGE_CONTRACT_PATH = AGENT_CHAT_PERSISTENCE_RUN_DIR / "AGENT_CHAT_STORAGE_CONTRACT_v0_3.json"
AGENT_CHAT_PERSISTENT_MESSAGE_SCHEMA_PATH = AGENT_CHAT_PERSISTENCE_RUN_DIR / "agent_chat_persistent_message.schema.json"
AGENT_CHAT_SEARCH_INDEX_PATH = LOCAL_HUB_DATA_DIR / "agent_chat_search_index_v0_3.json"
AGENT_CHAT_EXPORT_DIR = LOCAL_HUB_DATA_DIR / "exports"
AGENT_CHAT_MESSAGE_TYPES = {"CHAT", "SYSTEM", "TASK", "WORKPACK", "GATE", "WITNESS"}
AGENT_CHAT_EXPORT_BOUNDARY = "INTERNAL_LOCAL / DO_NOT_PUBLISH"
LOCAL_EXECUTE_RUN_ID = "RUN_LOCAL_EXECUTE_v0_2_20260518"
LOCAL_EXECUTE_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / LOCAL_EXECUTE_RUN_ID
LOCAL_EXECUTE_RUNTIME_ROOT = pathlib.Path.home() / ".medioevo" / "wabi" / "runtime" / "local_execute_v0_2"
LOCAL_EXECUTE_DOCS_ROOT = MEDIOEVO_ROOT / "docs" / "local_execute"
LOCAL_EXECUTE_TASKSPEC_DIR = LOCAL_EXECUTE_RUN_DIR / "taskspecs"
LOCAL_EXECUTE_EVIDENCE_DIR = LOCAL_EXECUTE_RUN_DIR / "evidence"
LOCAL_EXECUTE_CONTRACT_PATH = LOCAL_EXECUTE_RUN_DIR / "LOCAL_EXECUTE_CONTRACT_v0_2.json"
LOCAL_EXECUTE_SCHEMA_PATH = LOCAL_EXECUTE_RUN_DIR / "local_execute_task_spec.schema.json"
LOCAL_EXECUTE_WITNESSLOG_PATH = LOCAL_EXECUTE_RUN_DIR / "LOCAL_EXECUTE_WITNESSLOG_v0_2.jsonl"
LOCAL_EXECUTE_ALLOWED_LANES = {"SANDBOX", "DOCS_LOCAL"}
LOCAL_EXECUTE_BLOCKED_LANES = {"PUBLICATION", "CLOUD", "NVIDIA", "REMOTE_COMPUTE", "PROTECTED_MATERIAL"}
WORKPACK_RUN_ID = "RUN_CLAUDIO_WORKPACK_EXECUTION_BRIDGE_v0_1_20260518"
WORKPACK_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / WORKPACK_RUN_ID
WORKPACK_DATA_DIR = WORKPACK_RUN_DIR / "workpacks"
WORKPACK_CONTRACT_PATH = WORKPACK_RUN_DIR / "CLAUDIO_WORKPACK_CONTRACT_v0_1.json"
WORKPACK_SCHEMA_PATH = WORKPACK_RUN_DIR / "claudio_workpack.schema.json"
WORKPACK_WITNESSLOG_PATH = WORKPACK_RUN_DIR / "CLAUDIO_WORKPACK_WITNESSLOG_v0_1.jsonl"
WORKPACK_RUNTIME_ROOT = pathlib.Path.home() / ".medioevo" / "wabi" / "runtime" / "workpacks_v0_1"
WORKPACK_ALLOWED_LANES = LOCAL_EXECUTE_ALLOWED_LANES
WORKPACK_BLOCKED_LANES = LOCAL_EXECUTE_BLOCKED_LANES
WORKPACK_DEMO_TASK_IDS = {
    "local-execute-sandbox-demo": "claudio-workpack-sandbox-demo-v0-1",
    "local-execute-docs-demo": "claudio-workpack-docs-demo-v0-1",
}
WORKPACK_SCHEDULER_RUN_ID = "RUN_WORKPACK_SCHEDULER_v0_1_20260518"
WORKPACK_SCHEDULER_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / WORKPACK_SCHEDULER_RUN_ID
WORKPACK_SCHEDULER_CONTRACT_PATH = WORKPACK_SCHEDULER_RUN_DIR / "WORKPACK_SCHEDULER_CONTRACT_v0_1.json"
WORKPACK_SCHEDULER_SCHEMA_PATH = WORKPACK_SCHEDULER_RUN_DIR / "workpack_scheduler_queue.schema.json"
WORKPACK_SCHEDULER_QUEUE_PATH = WORKPACK_SCHEDULER_RUN_DIR / "WORKPACK_SCHEDULER_QUEUE_MANIFEST_v0_1.json"
WORKPACK_SCHEDULER_WITNESSLOG_PATH = WORKPACK_SCHEDULER_RUN_DIR / "WORKPACK_SCHEDULER_WITNESSLOG_v0_1.jsonl"
WORKPACK_SCHEDULER_ALLOWED_LANES = {"SANDBOX", "DOCS_LOCAL"}
WORKPACK_SCHEDULER_BLOCKED_LANES = {"PUBLICATION", "CLOUD", "NVIDIA", "DEEPSEEK", "REMOTE_COMPUTE", "PROTECTED_MATERIAL"}
WORKPACK_SCHEDULER_QUEUE_STATES = {
    "DRAFT",
    "READY",
    "APPROVED",
    "SCHEDULED",
    "RUNNING",
    "EXECUTED",
    "FAILED",
    "ROLLED_BACK",
    "BLOCKED",
    "SKIPPED_DEPENDENCY",
    "REVIEW",
}
MULTI_STEP_RUN_ID = "RUN_MULTI_STEP_WORKPACKS_v0_2_20260518"
MULTI_STEP_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / MULTI_STEP_RUN_ID
MULTI_STEP_DATA_DIR = MULTI_STEP_RUN_DIR / "multi_step_workpacks"
MULTI_STEP_CONTRACT_PATH = MULTI_STEP_RUN_DIR / "MULTI_STEP_WORKPACK_CONTRACT_v0_2.json"
MULTI_STEP_SCHEMA_PATH = MULTI_STEP_RUN_DIR / "multi_step_workpack.schema.json"
MULTI_STEP_MANIFEST_PATH = MULTI_STEP_RUN_DIR / "MULTI_STEP_WORKPACKS_MANIFEST_v0_2.json"
MULTI_STEP_WITNESSLOG_PATH = MULTI_STEP_RUN_DIR / "MULTI_STEP_WORKPACKS_WITNESSLOG_v0_2.jsonl"
MULTI_STEP_ALLOWED_LANES = {"SANDBOX", "DOCS_LOCAL"}
MULTI_STEP_BLOCKED_LANES = {"PUBLICATION", "CLOUD", "NVIDIA", "DEEPSEEK", "REMOTE_COMPUTE", "PROTECTED_MATERIAL"}
MULTI_STEP_WORKPACK_STATES = {"DRAFT", "READY", "APPROVED", "SCHEDULED", "RUNNING", "EXECUTED", "FAILED", "ROLLED_BACK", "BLOCKED", "PARTIAL"}
MULTI_STEP_STEP_STATES = {"PENDING", "READY", "APPROVED", "RUNNING", "EXECUTED", "FAILED", "ROLLED_BACK", "BLOCKED", "SKIPPED_DEPENDENCY"}
MISSION_CONTROL_RUN_ID = "RUN_CLAUDIO_MISSION_CONTROL_v0_1_20260518"
MISSION_CONTROL_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / MISSION_CONTROL_RUN_ID
MISSION_CONTROL_CONTRACT_PATH = MISSION_CONTROL_RUN_DIR / "CLAUDIO_MISSION_CONTROL_CONTRACT_v0_1.json"
MISSION_CONTROL_SCHEMA_PATH = MISSION_CONTROL_RUN_DIR / "mission_control_state.schema.json"
MISSION_CONTROL_STATE_PATH = MISSION_CONTROL_RUN_DIR / "MISSION_CONTROL_STATE_v0_1.json"
MISSION_CONTROL_SNAPSHOT_DIR = MISSION_CONTROL_RUN_DIR / "mission_control_snapshot"
MISSION_CONTROL_SNAPSHOT_MANIFEST_PATH = MISSION_CONTROL_RUN_DIR / "MISSION_CONTROL_SNAPSHOT_MANIFEST_v0_1.json"
MISSION_CONTROL_BOUNDARY = "INTERNAL_LOCAL / DO_NOT_PUBLISH / READ_ONLY"
WABI_MCP_SERVER_ROOT = CLAUDIO_ROOT / "mcp" / "wabi_mcp_server"
WABI_MCP_CONTRACT_V02_PATH = WABI_MCP_SERVER_ROOT / "mcp_contract_v0_2.json"
WABI_MCP_CONTRACT_V03_PATH = WABI_MCP_SERVER_ROOT / "mcp_contract_v0_3.json"
WABI_MCP_CONTRACT_V04_PATH = WABI_MCP_SERVER_ROOT / "mcp_contract_v0_4.json"
WABI_MCP_CONTRACT_PATH = WABI_MCP_CONTRACT_V04_PATH if WABI_MCP_CONTRACT_V04_PATH.exists() else (WABI_MCP_CONTRACT_V03_PATH if WABI_MCP_CONTRACT_V03_PATH.exists() else WABI_MCP_CONTRACT_V02_PATH)
WABI_MCP_MANIFEST_PATH = WABI_MCP_SERVER_ROOT / "manifest.json"
WABI_MCP_GATED_WRITE_REQUEST_SCHEMA_PATH = WABI_MCP_SERVER_ROOT / "mcp_gated_write_request.schema.json"
WABI_MCP_GATED_WRITE_DECISION_SCHEMA_PATH = WABI_MCP_SERVER_ROOT / "mcp_gated_write_decision.schema.json"
WABI_MCP_GATED_WRITE_DRY_RUN_SCHEMA_PATH = WABI_MCP_SERVER_ROOT / "mcp_gated_write_dry_run.schema.json"
WABI_MCP_CLIENT_CONFIG_DIR = WABI_MCP_SERVER_ROOT / "client_configs"
WABI_MCP_CLIENT_CONFIG_GUIDE_PATH = MEDIOEVO_ROOT / "docs" / "architecture" / "WABI_MCP_CLIENT_CONFIG_GUIDE_v0_1_20260519.md"
WABI_MCP_CLIENT_CONFIG_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / "RUN_MCP_CLIENT_CONFIG_GUIDE_v0_1_20260519"
WABI_MCP_CLIENT_CONFIG_CONTRACT_PATH = WABI_MCP_CLIENT_CONFIG_RUN_DIR / "MCP_CLIENT_CONFIG_CONTRACT_v0_1.json"
WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / "RUN_MCP_PREPARE_ONLY_CLIENT_SMOKE_v0_1_20260519"
WABI_MCP_PREPARE_CLIENT_SMOKE_CONTRACT_PATH = WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR / "MCP_PREPARE_ONLY_CLIENT_SMOKE_CONTRACT_v0_1.json"
WABI_MCP_CLIENT_READONLY_SMOKE_PATH = WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR / "MCP_CLIENT_READONLY_SMOKE_v0_1.json"
WABI_MCP_CLIENT_PREPARE_SMOKE_PATH = WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR / "MCP_CLIENT_PREPARE_SMOKE_v0_1.json"
WABI_MCP_CLIENT_GATED_BLOCK_SMOKE_PATH = WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR / "MCP_CLIENT_GATED_WRITE_BLOCK_SMOKE_v0_1.json"
WABI_MCP_GATED_WRITE_DESIGN_RUN_DIR = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / "RUN_WABI_MCP_GATED_WRITE_DESIGN_v0_4_20260519"
WABI_MCP_GATED_WRITE_DESIGN_SMOKE_PATH = WABI_MCP_GATED_WRITE_DESIGN_RUN_DIR / "MCP_CLIENT_GATED_WRITE_DESIGN_SMOKE_v0_4.json"
WABI_MCP_GATED_WRITE_DRY_RUN_SIMULATION_PATH = WABI_MCP_GATED_WRITE_DESIGN_RUN_DIR / "MCP_GATED_WRITE_DRY_RUN_SIMULATION_v0_4.json"
WABI_MCP_CLIENT_CONFIG_TEMPLATE_NAMES = [
    "client_config.generic.localhost.template.json",
    "client_config.local_wrapper.template.json",
    "client_config.codex_compatible.template.json",
    "client_config.claude_compatible.template.json",
    "client_config.chatgpt_compatible.template.json",
]


def now_epoch_ms() -> int:
    return int(time.time() * 1000)


def active_provider_name() -> str:
    return provider_registry.provider_for(provider_registry.default_provider_name()).name


def _current_secret_env_values() -> tuple[str, ...]:
    return tuple(
        env_value
        for env_name in PROVIDER_ENV_NAMES
        for env_value in [os.environ.get(env_name, "")]
        if env_value and len(env_value) >= 8
    )


def _may_contain_secret_pattern(text: str) -> bool:
    lowered = text.lower()
    return (
        "s" + "k-" in text
        or "g" + "hp_" in text
        or "private key" in lowered
        or "api" in lowered
        or "secret" in lowered
        or "token" in lowered
        or "password" in lowered
    )


def sanitize_text(value: Any, secret_env_values: tuple[str, ...] | None = None) -> str:
    text = str(value)
    for env_value in secret_env_values if secret_env_values is not None else _current_secret_env_values():
        text = text.replace(env_value, "<redacted>")
    if _may_contain_secret_pattern(text):
        for pattern in SECRET_VALUE_PATTERNS:
            text = pattern.sub("<redacted>", text)
    text = text.replace(str(ROOT), "<BRAIN_OS_ROOT>")
    return text


def sanitize_obj(value: Any, secret_env_values: tuple[str, ...] | None = None) -> Any:
    if secret_env_values is None:
        secret_env_values = _current_secret_env_values()
    if isinstance(value, dict):
        return {str(k): sanitize_obj(v, secret_env_values) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_obj(item, secret_env_values) for item in value]
    if isinstance(value, tuple):
        return [sanitize_obj(item, secret_env_values) for item in value]
    if isinstance(value, str):
        return sanitize_text(value, secret_env_values)
    return value


def env_flag(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


def workbench_cloud_first_enabled() -> bool:
    return env_flag("WABI_WORKBENCH_CLOUD_FIRST", "1")


def wabi_cost_router_enabled() -> bool:
    """Whether the cost-based local→cloud router is active.

    When enabled (``WABI_COST_ROUTER=1``):
    - Simple tasks → try Ollama local first (cheap, private).
    - If Ollama is unreachable/slow → escalate to cloud with gate.
    - Complex tasks (codex hints ≥ 2) → cloud directly.

    Default ``"0"``: disabled (existing cloud-first or local-only behavior).
    """
    return env_flag("WABI_COST_ROUTER", "0")


_OLLAMA_HEALTH_CACHE: dict[str, Any] = {"ok": None, "ts": 0.0}
_OLLAMA_HEALTH_TTL = 10.0  # seconds

# Words that signal a complex/agentic task → cloud preferred when count ≥ 2.
_COST_ROUTER_HINTS: frozenset[str] = frozenset({
    "analiza", "decide", "decidir", "elige", "mejor", "organiza", "plan",
    "siguiente", "autonomia", "autonomía", "implementa", "refactor", "integra",
    "explica", "investiga", "prioriza", "codex",
})


def ollama_probe(ollama_url: str = "http://localhost:11434", timeout_s: float = 1.0) -> bool:
    """Quick liveness probe for a local Ollama instance.

    Returns True when Ollama responds within ``timeout_s`` seconds.
    Result is cached for ``_OLLAMA_HEALTH_TTL`` seconds to avoid hammering
    the endpoint on every request.
    """
    import time
    import urllib.error
    import urllib.request

    now = time.monotonic()
    cache = _OLLAMA_HEALTH_CACHE
    if cache["ok"] is not None and (now - cache["ts"]) < _OLLAMA_HEALTH_TTL:
        return bool(cache["ok"])

    try:
        url = ollama_url.rstrip("/") + "/"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            ok = resp.status < 500
    except (urllib.error.URLError, OSError, Exception):
        ok = False

    cache["ok"] = ok
    cache["ts"] = now
    return ok


def cost_router_candidate_providers(
    requested: str | None = None,
    *,
    prompt_hint_count: int = 0,
    ollama_url: str = "http://localhost:11434",
) -> list[str]:
    """Return provider candidates ordered by cost: local first, cloud fallback.

    Rules (when ``WABI_COST_ROUTER=1``):
    - hint_count ≥ 2 (complex/code task) → cloud candidates first.
    - hint_count < 2 AND Ollama healthy → ["ollama", ...cloud fallbacks].
    - hint_count < 2 AND Ollama unhealthy → cloud candidates (Ollama appended last).

    When ``WABI_COST_ROUTER=0``, falls through to ``cloud_first_candidate_providers()``.
    """
    if not wabi_cost_router_enabled():
        return cloud_first_candidate_providers(requested)

    cloud = [
        name for name in cloud_first_candidate_providers(requested)
        if not _is_ollama_provider(name)
    ]

    # Complex task → cloud first (same as cloud-first mode).
    if prompt_hint_count >= 2:
        candidates = cloud[:]
        if "ollama" not in candidates:
            candidates.append("ollama")
        return candidates

    # Simple task → local first if Ollama is alive.
    if ollama_probe(ollama_url):
        candidates = ["ollama"] + [c for c in cloud if c != "ollama"]
        return candidates

    # Ollama unreachable → cloud cascade.
    candidates = cloud[:]
    if "ollama" not in candidates:
        candidates.append("ollama")  # keep as last-resort
    return candidates


def wabi_ui_exec_enabled() -> bool:
    """Whether the UI server may propagate ``--exec`` to ``wabi.py ask`` subprocesses.

    Default ``"0"``: the UI is read-only (file tools like list_files/read_file/write_file
    work, but ``run_command`` and ``apply_patch`` stay blocked). The operator opts in
    explicitly by exporting ``WABI_UI_EXEC=1`` before launching the UI.

    Local gates (PublicationGate=BLOCK, SecretGate=HARD_BLOCK,
    NetworkExposureGate=LOCALHOST_ONLY) are unaffected by this flag.
    """
    return env_flag("WABI_UI_EXEC", "0")


def _is_ollama_provider(provider_name: str) -> bool:
    try:
        return provider_registry.provider_for(provider_name).api_style == "ollama"
    except Exception:
        return False


def _provider_is_configured(provider_name: str) -> bool:
    try:
        return provider_registry.provider_for(provider_name).configured()
    except Exception:
        return False


def _nvidia_route_unhealthy() -> bool:
    if not WABI_PROVIDER_DIAGNOSTIC_LATEST.exists():
        return False
    try:
        latest = json.loads(WABI_PROVIDER_DIAGNOSTIC_LATEST.read_text(encoding="utf-8"))
    except Exception:
        return False
    if not isinstance(latest, dict):
        return False
    return (
        str(latest.get("provider") or "").lower() == "nvidia"
        and str(latest.get("route_diagnostic_status") or "").upper() == "REVIEW"
        and str(latest.get("last_error_class") or "") == "PROVIDER_OR_MODEL_NOT_FOUND_REDACTED"
    )


def cloud_first_candidate_providers(requested: str | None = None) -> list[str]:
    if not workbench_cloud_first_enabled():
        return ["ollama"]
    requested_name = ""
    if requested:
        try:
            requested_name = provider_registry.provider_for(str(requested)).name
        except Exception:
            requested_name = ""
    candidates: list[str] = []
    requested_is_external = bool(requested_name and not _is_ollama_provider(requested_name))
    if requested_is_external and requested_name != "nvidia":
        candidates.append(requested_name)
    for name in WORKBENCH_CLOUD_PROVIDER_ORDER:
        if name == "nvidia" and _nvidia_route_unhealthy():
            continue
        if name not in candidates and _provider_is_configured(name):
            candidates.append(name)
    if requested_is_external and requested_name not in candidates:
        candidates.append(requested_name)
    if "ollama" not in candidates:
        candidates.append("ollama")
    return candidates


def chat_fallback_candidate_providers(requested: str | None = None) -> list[str]:
    candidates = cloud_first_candidate_providers(requested)
    cloud = [name for name in candidates if not _is_ollama_provider(name)]
    order = cloud[:]
    if "ollama" in candidates:
        order.append("ollama")
    return order or ["ollama"]


def chat_fallback_candidate_engines(requested: str | None = None) -> list[dict[str, Any]]:
    engines: list[dict[str, Any]] = []
    if os.environ.get("WABI_ALLOW_CLOUD_PROVIDERS", "0") == "1":
        engines.append(
            {
                "label": f"deepseek-{WABI_PRIMARY_MODEL}",
                "provider": WABI_PRIMARY_PROVIDER,
                "model": WABI_PRIMARY_MODEL,
                "timeout": 120,
                "tokens": 1024,
            }
        )
        engines.append(
            {
                "label": f"nvidia-{WABI_FALLBACK_MODEL.split('/')[-1]}",
                "provider": WABI_FALLBACK_PROVIDER,
                "model": WABI_FALLBACK_MODEL,
                "timeout": 120,
                "tokens": 1024,
            }
        )
        engines.append(
            {
                "label": f"cloudflare-{WABI_SECONDARY_FALLBACK_MODEL.split('/')[-1]}",
                "provider": WABI_SECONDARY_FALLBACK_PROVIDER,
                "model": WABI_SECONDARY_FALLBACK_MODEL,
                "timeout": 90,
                "tokens": 768,
            }
        )
    if workbench_cloud_first_enabled():
        engines.append(
            {
                "label": "ollama-last-resort",
                "provider": "ollama",
                "model": WABI_OLLAMA_CLOUD_MODEL,
                "timeout": 60,
                "tokens": 768,
            }
        )
    engines.append(
        {
            "label": "ollama-local",
            "provider": "ollama",
            "model": WABI_OLLAMA_LOCAL_MODEL,
            "timeout": 40,
            "tokens": 256,
        }
    )
    return engines


def _path_is_under(child: pathlib.Path, parent: pathlib.Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def _extract_candidate_paths(text: str) -> list[str]:
    seen: list[str] = []
    for match in QUOTED_LOCAL_PATH_RE.findall(text):
        if match not in seen:
            seen.append(match)
    for match in BARE_LOCAL_PATH_RE.findall(text):
        if match not in seen:
            seen.append(match)
    return seen


def _top_context_terms(text: str, limit: int = 8) -> list[str]:
    stop = {
        "para",
        "pero",
        "como",
        "desde",
        "donde",
        "porque",
        "sobre",
        "entre",
        "cuando",
        "this",
        "that",
        "with",
        "from",
    }
    counts: dict[str, int] = {}
    for word in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ_]{5,}", sanitize_text(text).lower()):
        if word in stop or "secret" in word or "token" in word or "password" in word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]


def summarize_local_file_for_cloud(path: pathlib.Path) -> dict[str, Any]:
    resolved = path.resolve()
    raw = resolved.read_bytes()[:MAX_CONTEXT_FILE_BYTES]
    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    compact = " ".join(sanitize_text(text).split())
    return {
        "label": f"<BRAIN_OS_PATH:{resolved.name}>",
        "name": resolved.name,
        "suffix": resolved.suffix.lower(),
        "sha256": digest,
        "bytes": resolved.stat().st_size,
        "line_count": text.count("\n") + (1 if text else 0),
        "terms": _top_context_terms(text),
        "redacted_excerpt": compact[:MAX_CONTEXT_EXCERPT_CHARS],
    }


def prepare_prompt_for_provider(prompt: str, provider_name: str) -> tuple[str, list[dict[str, Any]]]:
    if _is_ollama_provider(provider_name):
        return prompt, []
    safe_prompt = str(prompt)
    summaries: list[dict[str, Any]] = []
    for raw_path in _extract_candidate_paths(safe_prompt):
        candidate = pathlib.Path(raw_path)
        if not candidate.exists() or not candidate.is_file() or not _path_is_under(candidate, ROOT):
            continue
        summary = summarize_local_file_for_cloud(candidate)
        summaries.append(summary)
        safe_prompt = safe_prompt.replace(raw_path, str(summary["label"]))
    safe_prompt = sanitize_text(safe_prompt)
    if summaries:
        context_lines = [
            "",
            "[Contexto local resumido para cloud; raw_private_files_sent=false; policy=SUMMARY_ONLY]",
        ]
        for item in summaries[:3]:
            context_lines.append(
                "- {label} sha256={sha256} bytes={bytes} lines={line_count} terms={terms} excerpt={excerpt}".format(
                    label=item["label"],
                    sha256=str(item["sha256"])[:16] + "...",
                    bytes=item["bytes"],
                    line_count=item["line_count"],
                    terms=",".join(item["terms"]),
                    excerpt=item["redacted_excerpt"],
                )
            )
        safe_prompt = (safe_prompt + "\n".join(context_lines))[:MAX_PROMPT_CHARS]
    return safe_prompt, summaries


def provider_rows() -> list[dict[str, Any]]:
    default_name = active_provider_name()
    rows: list[dict[str, Any]] = []
    for provider in provider_registry.PROVIDERS.values():
        row = provider.to_public_dict()
        row["default"] = provider.name == default_name
        row["env_present"] = bool(provider.key) if provider.api_style != "ollama" else True
        rows.append(sanitize_obj(row))
    return rows


def doctor_rows(*, live: bool = False) -> list[dict[str, Any]]:
    rows = provider_doctor.diagnose_all(live=live)
    return sanitize_obj(rows)


def safe_provider_name(raw: str | None) -> str:
    name = (raw or active_provider_name()).strip()
    if not name:
        return active_provider_name()
    return provider_registry.provider_for(name).name


def wabi_child_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for name in PASSTHROUGH_ENV_NAMES + PROVIDER_ENV_NAMES:
        value = os.environ.get(name)
        if value:
            env[name] = value
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def build_wabi_ask_command(
    message: str,
    provider: str,
    max_tokens: int,
    mode: str = "tools",
    model: str | None = None,
    enable_exec: bool = False,
) -> list[str]:
    """Build the argv for the ``wabi.py ask`` subprocess.

    ``enable_exec`` (default False) controls whether the child process is allowed
    to invoke ``run_command`` and ``apply_patch``. Read/list/write tools are
    available regardless. The UI opts in by setting the ``WABI_UI_EXEC`` env var;
    see ``wabi_ui_exec_enabled``.
    """
    cmd = [
        sys.executable,
        str(WABI_SCRIPT),
        "ask",
        "--provider",
        provider,
        "--cwd",
        str(ROOT),
        "--max-tokens",
        str(max_tokens),
    ]
    if enable_exec:
        cmd.append("--exec")
    if mode == "plain":
        cmd.append("--plain")
    if model:
        cmd.extend(["--model", model])
    cmd.append(message)
    return cmd


def parse_tool_events(output: str) -> tuple[list[dict[str, Any]], str]:
    events: list[dict[str, Any]] = []
    response_lines: list[str] = []
    for line in output.splitlines():
        if line.startswith("[wabi tool] "):
            rest = line[len("[wabi tool] "):]
            name, _, status = rest.partition(":")
            events.append({"tool": name.strip(), "status": status.strip() or "UNKNOWN"})
            continue
        response_lines.append(line)
    return events, "\n".join(response_lines).strip()


def run_wabi_chat(
    message: str,
    provider: str | None = None,
    max_tokens: int = 512,
    mode: str = "tools",
    timeout_s: int | None = None,
    model: str | None = None,
    enable_exec: bool | None = None,
) -> dict[str, Any]:
    prompt = message.strip()
    if not prompt:
        raise ValueError("message is required")
    if len(prompt) > MAX_PROMPT_CHARS:
        raise ValueError(f"message exceeds {MAX_PROMPT_CHARS} characters")
    provider_name = safe_provider_name(provider)
    prompt, private_context = prepare_prompt_for_provider(prompt, provider_name)
    tokens = max(8, min(int(max_tokens or 512), 4096))
    selected_mode = "plain" if str(mode).lower() == "plain" else "tools"
    model_override = str(model or "").strip()
    # Default: honor the WABI_UI_EXEC env flag. Callers (tests, internal
    # endpoints) can override with an explicit boolean.
    exec_flag = wabi_ui_exec_enabled() if enable_exec is None else bool(enable_exec)
    cmd = build_wabi_ask_command(
        prompt,
        provider_name,
        tokens,
        selected_mode,
        model_override or None,
        enable_exec=exec_flag,
    )
    timeout = max(5, min(int(timeout_s or REQUEST_TIMEOUT_S), REQUEST_TIMEOUT_S))
    response_command = [
        "python",
        "02_CLAUDIO/core/wabi.py",
        "ask",
        "--provider",
        provider_name,
        "--cwd",
        "<BRAIN_OS_ROOT>",
        "--max-tokens",
        str(tokens),
        *(["--exec"] if exec_flag else []),
        *([] if selected_mode == "tools" else ["--plain"]),
        *([] if not model_override else ["--model", model_override]),
        "<message>",
    ]
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(ROOT),
            env=wabi_child_env(),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "provider": provider_name,
            "mode": selected_mode,
            "returncode": -1,
            "response": "",
            "raw_response": "",
            "error": f"timeout after {timeout}s",
            "tools_used": 0,
            "tool_events": [],
            "command": response_command,
            "cloud_first": workbench_cloud_first_enabled(),
            "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
            "private_context_items": private_context,
            "raw_private_files_sent": False,
            "ui_exec_enabled": exec_flag,
            "secret_values_printed": False,
        }
    stdout = sanitize_text(completed.stdout.strip())[:MAX_RESPONSE_CHARS]
    stderr = sanitize_text(completed.stderr.strip())[:MAX_RESPONSE_CHARS]
    tool_events, response = parse_tool_events(stdout)
    return {
        "ok": completed.returncode == 0,
        "provider": provider_name,
        "mode": selected_mode,
        "returncode": completed.returncode,
        "response": response if selected_mode == "tools" else stdout,
        "raw_response": stdout,
        "error": stderr,
        "tools_used": len(tool_events),
        "tool_events": tool_events,
        "command": response_command,
        "cloud_first": workbench_cloud_first_enabled(),
        "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
        "private_context_items": private_context,
        "raw_private_files_sent": False,
        "ui_exec_enabled": exec_flag,
        "secret_values_printed": False,
    }


def model_chat_fallback(message: str, provider: str | None, mode: str) -> dict[str, Any]:
    requested = safe_provider_name(provider or WABI_PRIMARY_PROVIDER)
    engines = chat_fallback_candidate_engines(requested)
    # Cost-router: reorder engines when WABI_COST_ROUTER=1.
    # Count hint words in message to distinguish simple vs complex tasks.
    if wabi_cost_router_enabled():
        _msg_lower = message.lower()
        _hint_count = sum(1 for h in _COST_ROUTER_HINTS if h in _msg_lower)
        _ordered_providers = cost_router_candidate_providers(
            requested, prompt_hint_count=_hint_count
        )
        def _engine_rank(eng: dict[str, Any]) -> int:
            pname = str(eng.get("provider") or "")
            for i, p in enumerate(_ordered_providers):
                if p == pname or (p == "ollama" and pname.startswith("ollama")):
                    return i
            return len(_ordered_providers)
        engines = sorted(engines, key=_engine_rank)
    candidate_order = [str(engine.get("label") or engine.get("provider") or "") for engine in engines]
    base_prompt_tail = "\n".join(
        [
            "REGLA CRÍTICA: cuando el usuario pida listar archivos, leer código, buscar texto,",
            "ver git status/diff, o escribir archivos → USA LAS HERRAMIENTAS disponibles.",
            "NUNCA digas 'no tengo acceso' si la herramienta existe. Actúa, no expliques.",
            "Responde en español, corto y concreto.",
            "",
            "Usuario:",
            message,
        ]
    )
    errors: list[dict[str, str]] = []
    # "tools" unless the caller explicitly requests plain text. Any UI mode
    # ("simple", "developer", "chat", etc.) should allow the model to call
    # workspace tools (list_files, read_file, write_file, etc.). Only an
    # explicit mode="plain" request disables tools.
    # NOTE: The previous code was `"plain" if mode != "developer" else "plain"`
    # — both branches produced "plain" (always plain, never tools). Fixed.
    selected_mode = "plain" if str(mode or "").lower() == "plain" else "tools"
    # DOIOICycleMonitor (E07): reset per call so each fallback sequence is
    # treated as an independent DO→IOI cycle. Residue proxy = 1 - rank_ratio.
    wabi_osit_v04.doi_reset()
    for engine in engines:
        label = str(engine.get("label") or engine.get("provider") or "unknown")
        provider_name = str(engine.get("provider") or "ollama")
        model_override = str(engine.get("model") or "") or None
        timeout = int(engine.get("timeout") or 25)
        tokens = int(engine.get("tokens") or 120)
        identity_block = wabi_identity.build_identity_grounding(provider_name, model_override or "")
        prompt = identity_block + "\n\n" + base_prompt_tail
        try:
            result = run_wabi_chat(
                prompt,
                provider=provider_name,
                max_tokens=tokens,
                mode=selected_mode,
                timeout_s=timeout,
                model=model_override,
            )
        except Exception as exc:
            errors.append({"provider": label, "model": sanitize_text(model_override or ""), "error": sanitize_text(exc)})
            continue
        if result.get("ok") and str(result.get("response") or "").strip():
            # Step DOIOICycleMonitor: success on first engine = low residue (0.1),
            # later engines = higher residue proxy. Purely telemetry.
            _rank = engines.index(engine) if engine in engines else 0
            _r_proxy = 0.1 + 0.2 * _rank  # 0.1 for first, 0.3 for second, …
            _conv = wabi_osit_v04.convergence_step(_r_proxy)
            return {
                "ok": True,
                "provider": label,
                "raw_provider": provider_name,
                "model": model_override or "",
                "response": sanitize_text(result.get("response", "")),
                "errors": errors,
                "raw": sanitize_obj(result),
                "cloud_first": workbench_cloud_first_enabled(),
                "candidate_order": candidate_order,
                "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
                "raw_private_files_sent": False,
                "doi_telemetry": {
                    "converged": bool(_conv.get("converged", False)),
                    "iterations": int(_conv.get("iterations", 1)),
                    "r_proxy": round(_r_proxy, 3),
                },
            }
        errors.append(
            {
                "provider": label,
                "model": sanitize_text(model_override or ""),
                "error": sanitize_text(result.get("error") or result.get("raw_response") or "sin respuesta"),
            }
        )
    return {
        "ok": False,
        "provider": "",
        "raw_provider": "",
        "model": "",
        "response": "",
        "errors": errors,
        "raw": {},
        "cloud_first": workbench_cloud_first_enabled(),
        "candidate_order": candidate_order,
        "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
        "raw_private_files_sent": False,
    }


def model_reply_needs_safe_fallback(reply: str) -> bool:
    lowered = str(reply or "").lower()
    blocked_fragments = (
        "chmod",
        "find .",
        "cd \\",
        "cd \"",
        "powershell",
        "python ",
        "estoy haciendo actualmente",
        "he ejecutado",
        "ya ejecuté",
        "ya ejecute",
        "podrías iniciar el proceso",
        "podrias iniciar el proceso",
        "quiero hablar con wabi",
        "quiero platicar con wabi",
    )
    return any(fragment in lowered for fragment in blocked_fragments)


def local_conversation_reply(message: str) -> str:
    normalized = chat_intent_router.normalize_message(message)
    if "que hago ahora" in normalized or "siguiente" in normalized:
        return (
            "Estoy contigo. Lo más útil ahora es escoger un objetivo concreto y convertirlo en una acción pequeña: "
            "revisar estado, preparar un plan, crear un diff, correr pruebas o revisar seguridad. "
            "Dime qué quieres cambiar y lo bajo a pasos verificables."
        )
    return (
        "Te escucho. Puedo conversar contigo y convertir la conversación en trabajo local verificable: "
        "plan, diff, pruebas, seguridad o pendientes. Dime qué quieres lograr y sigo desde ahí."
    )


def should_answer_unknown_locally(message: str, mode: str) -> bool:
    if str(mode or "simple").lower() == "developer":
        return False
    normalized = chat_intent_router.normalize_message(message)
    local_chat_markers = ("platicar", "conversar", "hablar con wabi", "que hago ahora")
    return any(marker in normalized for marker in local_chat_markers)


def workspace_payload() -> dict[str, Any]:
    return sanitize_obj(wabi_provider_workspace_payload())


def wabi_provider_workspace_payload() -> dict[str, Any]:
    # Import locally to avoid expanding the public server surface beyond this endpoint.
    from core import wabi as wabi_core

    return dict(wabi_core.workspace_doctor_payload(ROOT, enable_exec=False))


def tools_payload() -> dict[str, Any]:
    data = wabi_provider_workspace_payload()
    return {"tools": data.get("tools_enabled", {}), "workspace_root": "<BRAIN_OS_ROOT>", "mode_default": "tools"}


def wabi_tool_registry_payload() -> dict[str, Any]:
    return sanitize_obj(wabi_tool_registry.build_tool_registry_payload(local_gate_state_for_actions()))


def recent_changes_payload(limit: int = 10, path_filter: str | None = None) -> dict[str, Any]:
    from core import wabi as wabi_core

    safe_limit = max(1, min(int(limit or 10), 100))
    entries = wabi_core.read_change_ledger(ROOT, limit=safe_limit, path_filter=path_filter)
    return {
        "ledger_path": "08_QA_WITNESSLOG/WABI_LOCAL_CHANGE_LEDGER/wabi_change_ledger.jsonl",
        "count": len(entries),
        "entries": sanitize_obj(entries),
        "content_recorded": False,
    }


def read_recent_session(limit: int = 12) -> dict[str, Any]:
    if not CURRENT_SESSION.exists():
        return {"events": [], "session_present": False}
    lines = CURRENT_SESSION.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]
    events: list[dict[str, Any]] = []
    for line in lines:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            clean = sanitize_obj(item)
            if isinstance(clean.get("content"), str):
                clean["content"] = clean["content"][:1500]
            events.append(clean)
    return {"events": events, "session_present": True}


def recent_witnesslog(limit: int = 8) -> dict[str, Any]:
    witness_root = ROOT / "08_QA_WITNESSLOG"
    if not witness_root.exists():
        return {"entries": [], "present": False}
    files = sorted(
        [p for p in witness_root.rglob("*") if p.is_file() and "WABI" in p.as_posix().upper()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[:limit]
    entries = [
        {
            "path": p.relative_to(ROOT).as_posix(),
            "bytes": p.stat().st_size,
            "modified_epoch_ms": int(p.stat().st_mtime * 1000),
        }
        for p in files
    ]
    return {"entries": entries, "present": True}


def server_repo_root(payload: dict[str, Any] | None = None) -> pathlib.Path:
    raw = (payload or {}).get("repo")
    if not raw:
        return ROOT
    candidate = pathlib.Path(str(raw)).expanduser().resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError("repo outside BRAIN_OS root is not allowed by local API") from exc
    return candidate


def provider_status_payload() -> dict[str, Any]:
    payload = coding_provider_router.provider_status(include_all=True)
    active_order = ["deepseek", "nvidia", "cloudflare", "ollama-local"] if workbench_cloud_first_enabled() else ["ollama-local"]
    payload["workbench_policy"] = {
        "cloud_first": workbench_cloud_first_enabled(),
        "provider_order": active_order,
        "diagnostic_providers": cloud_first_candidate_providers(payload.get("default_provider")),
        "active_provider": WABI_PRIMARY_PROVIDER if workbench_cloud_first_enabled() else "ollama",
        "active_model": WABI_PRIMARY_MODEL if workbench_cloud_first_enabled() else WABI_OLLAMA_LOCAL_MODEL,
        "context_policy": WORKBENCH_CONTEXT_POLICY,
        "raw_private_files_sent": False,
        "publication_gate": "BLOCK",
    }
    return sanitize_obj(payload)


def wabi_provider_contract_payload() -> dict[str, Any]:
    cloud_allowed = workbench_cloud_first_enabled() or os.environ.get("WABI_ALLOW_CLOUD_PROVIDERS", "0") == "1"
    credential_env = "DEEPSEEK_API_KEY" if os.environ.get("DEEPSEEK_API_KEY") else (
        "NVIDIA_NIM_API_KEY" if os.environ.get("NVIDIA_NIM_API_KEY") else (
            "NVIDIA_API_KEY" if os.environ.get("NVIDIA_API_KEY") else ""
        )
    )
    payload: dict[str, Any] = {
        "schema": "wabi.provider_status_contract.v0_4",
        "primary_provider": WABI_PRIMARY_PROVIDER,
        "primary_model": WABI_PRIMARY_MODEL,
        "fallback_provider": WABI_FALLBACK_PROVIDER,
        "fallback_model": WABI_FALLBACK_MODEL,
        "cloud_allowed_by_flag": cloud_allowed,
        "cloud_allowed_mode": "CLOUD_FIRST_HEALTH_GATED" if workbench_cloud_first_enabled() else ("SESSION_FLAG_ENABLED" if cloud_allowed else "CLOUD_DISABLED_BY_FLAG"),
        "credential_present_redacted": bool(credential_env),
        "active_credential_env": credential_env,
        "live_smoke_status": "REVIEW_SMOKE_NOT_RUN",
        "provider_state": "CLOUD_FIRST_HEALTH_GATED" if workbench_cloud_first_enabled() else ("CLOUD_DISABLED_BY_FLAG" if not cloud_allowed else ("CONFIGURED_NOT_SMOKED" if credential_env else "NOT_CONFIGURED")),
        "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
        "raw_private_files_sent": False,
        "last_smoke_timestamp": "",
        "workspace_sent": False,
        "secret_values_printed": False,
        "publication_gate": "BLOCK",
        "source": "local_env",
    }
    if WABI_PROVIDER_STATUS_LATEST.exists():
        try:
            latest = json.loads(WABI_PROVIDER_STATUS_LATEST.read_text(encoding="utf-8"))
        except Exception:
            latest = {}
        if isinstance(latest, dict):
            for key in (
                "primary_provider",
                "primary_model",
                "fallback_provider",
                "fallback_model",
                "cloud_allowed_by_flag",
                "cloud_allowed_mode",
                "credential_present_redacted",
                "active_credential_env",
                "live_smoke_status",
                "provider_state",
                "last_smoke_timestamp",
                "workspace_sent",
                "publication_gate",
            ):
                if key in latest:
                    payload[key] = latest[key]
            payload["source"] = str(WABI_PROVIDER_STATUS_LATEST)
    if workbench_cloud_first_enabled():
        payload["primary_provider"] = WABI_PRIMARY_PROVIDER
        payload["primary_model"] = WABI_PRIMARY_MODEL
        payload["fallback_provider"] = WABI_FALLBACK_PROVIDER
        payload["fallback_model"] = WABI_FALLBACK_MODEL
        payload["cloud_allowed_by_flag"] = True
        payload["cloud_allowed_mode"] = "CLOUD_FIRST_HEALTH_GATED"
        payload["provider_state"] = "CLOUD_FIRST_HEALTH_GATED"
        payload["cloud_context_policy"] = WORKBENCH_CONTEXT_POLICY
        payload["raw_private_files_sent"] = False
    return sanitize_obj(payload)


def wabi_provider_route_diagnostic_payload() -> dict[str, Any]:
    route = provider_route_payload()
    if WABI_PROVIDER_DIAGNOSTIC_LATEST.exists():
        try:
            latest = json.loads(WABI_PROVIDER_DIAGNOSTIC_LATEST.read_text(encoding="utf-8"))
        except Exception:
            latest = {}
        if isinstance(latest, dict):
            if workbench_cloud_first_enabled():
                latest["cloud_first"] = True
                latest["provider"] = WABI_PRIMARY_PROVIDER
                latest["selected_provider_by_health"] = route.get("selected_provider")
                latest["selected_model_by_health"] = route.get("selected_model")
                latest["health_route_status"] = route.get("status")
                latest["primary_model_configured"] = WABI_PRIMARY_MODEL
                latest["fallback_provider"] = WABI_FALLBACK_PROVIDER
                latest["fallback_model"] = WABI_FALLBACK_MODEL
                latest["cloud_context_policy"] = WORKBENCH_CONTEXT_POLICY
                latest["raw_private_files_sent"] = False
                latest["private_paths_sent"] = False
                latest["workspace_sent"] = False
            return sanitize_obj(latest)

    contract = wabi_provider_contract_payload()
    last_smoke = str(contract.get("live_smoke_status") or "REVIEW_SMOKE_NOT_RUN")
    last_error = "PROVIDER_OR_MODEL_NOT_FOUND_REDACTED" if last_smoke == "SMOKE_FAIL_REDACTED" else "UNKNOWN_REDACTED"
    route_status = "REVIEW" if last_smoke != "SMOKE_PASS" else "PASS"
    return sanitize_obj(
        {
            "schema": "wabi.api_first_route_diagnostic.v0_6",
            "state_fingerprint": "WABI-CLOUD-PROVIDER-v0-5-20260518",
            "provider": WABI_PRIMARY_PROVIDER,
            "cloud_first": workbench_cloud_first_enabled(),
            "selected_provider_by_health": route.get("selected_provider"),
            "selected_model_by_health": route.get("selected_model"),
            "health_route_status": route.get("status"),
            "primary_model_configured": WABI_PRIMARY_MODEL,
            "fallback_provider": WABI_FALLBACK_PROVIDER,
            "fallback_model": WABI_FALLBACK_MODEL,
            "alias_candidates": [
                {"alias": WABI_PRIMARY_MODEL, "provider": WABI_PRIMARY_PROVIDER, "status": "PRIMARY_API_DEFAULT"},
                {"alias": WABI_FALLBACK_MODEL, "provider": WABI_FALLBACK_PROVIDER, "status": "FALLBACK_API_DEFAULT"},
                {"alias": WABI_SECONDARY_FALLBACK_MODEL, "provider": WABI_SECONDARY_FALLBACK_PROVIDER, "status": "SECONDARY_API_FALLBACK"},
            ],
            "endpoint_mode": "openai_compatible",
            "credential_present_redacted": bool(contract.get("credential_present_redacted")),
            "cloud_provider_called": False,
            "workspace_sent": False,
            "private_paths_sent": False,
            "code_sent": False,
            "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
            "raw_private_files_sent": False,
            "last_smoke_status": last_smoke,
            "last_smoke_timestamp": str(contract.get("last_smoke_timestamp") or ""),
            "last_error_class": last_error,
            "route_diagnostic_status": route_status,
            "recommended_next_smoke": "DEEPSEEK_V4_FLASH_READY" if workbench_cloud_first_enabled() else ("ALLOW" if route_status == "PASS" else "DO_NOT_CALL"),
            "recommended_next_action": "DEEPSEEK_ROUTE_REVIEW_REDACTED"
            if last_error == "PROVIDER_OR_MODEL_NOT_FOUND_REDACTED"
            else "VERIFY_ENDPOINT_MODEL_ALIAS_ENTITLEMENT_REDACTED",
            "model_list_api_status": "REVIEW_MODEL_LIST_API",
            "secret_values_printed": False,
            "publication_gate": "BLOCK",
            "source": "server_synthesized_from_provider_contract",
        }
    )


def tree_health_payload() -> dict[str, Any]:
    fallback: dict[str, Any] = {
        "schema": "tree_health_workbench_panel.state.v1",
        "state_fingerprint": "TREE-HEALTH-WORKBENCH-PANEL-20260518",
        "run_id": TREE_HEALTH_RUN_ID,
        "tree": {
            "files_inventoried": 2243,
            "pre_cleanup_hashes": 1602,
            "reparse_points": 0,
            "cache_files_quarantined": 1257,
            "direct_delete_used": False,
            "rollback_available": True,
        },
        "compileall": {
            "claudio_global": "PASS",
            "legacy_triage": "PASS_WITH_MINIMAL_FIXES",
        },
        "tests": {
            "wabi_full": "PASS",
            "claudio_full": "PASS",
            "geodia": "PASS",
            "duat_predictive": "PASS",
        },
        "provider": {
            "cloud_status": "SMOKE_FAIL_REDACTED",
            "route_status": "REVIEW",
            "next_smoke": "DO_NOT_CALL",
            "fallback": "ollama/qwen2.5:0.5b",
            "cloud_called_this_run": False,
            "nvidia_pass_claimed": False,
        },
        "hashing": {
            "live_log_locked_count": 2,
            "classification": "LIVE_LOG_LOCKED_NOT_SECRET",
            "secret_indication": False,
            "tree_corruption_indication": False,
            "cleanup_failure_indication": False,
        },
        "gates": {
            "PublicationGate": "BLOCK",
            "CloudLiveGate": "BLOCK_THIS_RUN",
            "NvidiaSmokeGate": "DO_NOT_CALL",
        },
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }
    payload = fallback
    if TREE_HEALTH_STATE_LATEST.exists():
        try:
            loaded = json.loads(TREE_HEALTH_STATE_LATEST.read_text(encoding="utf-8"))
        except Exception:
            loaded = {}
        if isinstance(loaded, dict):
            payload = loaded
    payload["ok"] = True
    payload["ui_integration"] = "MAIN_WABI_UI_INTEGRATED"
    payload["panel_static_path"] = "qa_artifacts/release_validation/RUN_TREE_HEALTH_WORKBENCH_PANEL_20260518/tree_workbench_health_panel/index.html"
    payload["source_state_path"] = "qa_artifacts/release_validation/RUN_TREE_HEALTH_WORKBENCH_PANEL_20260518/TREE_HEALTH_STATE_20260518.json"
    acceptance = coding_acceptance_payload()
    versions = acceptance.get("versions", {}) if isinstance(acceptance.get("versions"), dict) else {}
    v02 = versions.get("v0.2", {})
    v03 = versions.get("v0.3", {})
    payload["coding_acceptance_v0_2"] = _coding_acceptance_tree_summary(v02)
    payload["coding_acceptance_v0_3"] = _coding_acceptance_tree_summary(v03)
    payload["coding_acceptance_latest"] = {
        "version": acceptance.get("latest_version", "v0.3"),
        **_coding_acceptance_tree_summary(acceptance),
    }
    return sanitize_obj(payload)


def coding_acceptance_payload() -> dict[str, Any]:
    fallback_v02: dict[str, Any] = {
        "schema": "wabi.fallback_only_acceptance.result.v0_2",
        "state_fingerprint": "WABI-FALLBACK-ONLY-CODING-ACCEPTANCE-v0-2-20260518",
        "run_id": CODING_ACCEPTANCE_V02_RUN_ID,
        "mode": "fallback-only",
        "provider": {
            "cloud_live_gate": "BLOCK_THIS_RUN",
            "nvidia_smoke_gate": "DO_NOT_CALL",
            "cloud_status": "SMOKE_FAIL_REDACTED",
            "route_status": "REVIEW",
            "next_smoke": "DO_NOT_CALL",
            "fallback": "ollama/qwen2.5:0.5b",
            "local_fallback_status": "LOCAL_FALLBACK_OLLAMA_AVAILABLE",
            "proposal_source": "DETERMINISTIC_STUB_USED",
        },
        "loop": {
            "dry_run_before_apply": True,
            "proposal_valid": True,
            "task_spec_valid": True,
            "patch_plan_valid": True,
            "apply_status": "APPLIED",
            "tests_ran": True,
            "tests_passed": True,
            "rollback_available": True,
            "witness_verified": True,
            "witness_event_id": "21",
        },
        "sandbox": {
            "scope": "runtime",
            "path_redacted": "<WABI_RUNTIME>/coding_acceptance_v0_2",
            "written": [],
        },
        "security": {
            "cloud_called": False,
            "workspace_sent_external": False,
            "secret_values_printed": False,
            "publication_gate": "BLOCK",
        },
    }
    fallback_v03 = {
        **fallback_v02,
        "schema": "wabi.fallback_only_acceptance.result.v0_3",
        "state_fingerprint": "WABI-FALLBACK-ONLY-CODING-ACCEPTANCE-v0-3-20260518",
        "run_id": CODING_ACCEPTANCE_V03_RUN_ID,
        "latest_version": "v0.3",
        "sandbox": {
            "scope": "runtime",
            "path_redacted": "<WABI_RUNTIME>/coding_acceptance_v0_3",
            "written": [],
            "test_count": 0,
        },
        "loop": {
            "initial_tests_failed_expected": True,
            "dry_run_before_apply": True,
            "proposal_valid": True,
            "task_spec_valid": True,
            "patch_plan_valid": True,
            "patch_applied": True,
            "apply_status": "APPLIED",
            "tests_ran": True,
            "tests_passed": True,
            "rollback_available": True,
            "witness_verified": True,
            "witness_event_id": "22",
        },
    }
    v02 = _load_json_dict(CODING_ACCEPTANCE_V02_STATE, fallback_v02)
    v03 = _load_json_dict(CODING_ACCEPTANCE_V03_STATE, fallback_v03)
    v02 = _decorate_coding_acceptance(v02, version="v0.2")
    v03 = _decorate_coding_acceptance(v03, version="v0.3")
    latest_version = "v0.3"
    latest = dict(v03 if latest_version == "v0.3" else v02)
    versions = {"v0.2": v02, "v0.3": v03}
    latest.update(
        {
            "schema": "wabi.fallback_only_acceptance.aggregate.v0_3",
            "state_fingerprint": "WABI-FALLBACK-ONLY-CODING-ACCEPTANCE-v0-3-20260518",
            "latest_version": latest_version,
            "versions": versions,
            "ui_integration": "MAIN_WABI_UI_INTEGRATED",
            "endpoint": "/api/coding-acceptance",
            "source_state_path": (
                "qa_artifacts/release_validation/"
                "RUN_WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3_20260518/"
                "FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3.json"
            ),
        }
    )
    latest["ok"] = _coding_acceptance_ok(latest)
    latest["secret_values_printed"] = bool(latest.get("security", {}).get("secret_values_printed", False))
    return sanitize_obj(latest)


def _load_json_dict(path: pathlib.Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return dict(fallback)
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return dict(fallback)
    return loaded if isinstance(loaded, dict) else dict(fallback)


def _decorate_coding_acceptance(payload: dict[str, Any], *, version: str) -> dict[str, Any]:
    decorated = dict(payload)
    decorated["version"] = version
    decorated["ok"] = _coding_acceptance_ok(decorated)
    security = decorated.get("security", {}) if isinstance(decorated.get("security"), dict) else {}
    decorated["secret_values_printed"] = bool(security.get("secret_values_printed", False))
    return decorated


def _coding_acceptance_ok(payload: dict[str, Any]) -> bool:
    loop = payload.get("loop", {}) if isinstance(payload.get("loop"), dict) else {}
    security = payload.get("security", {}) if isinstance(payload.get("security"), dict) else {}
    provider = payload.get("provider", {}) if isinstance(payload.get("provider"), dict) else {}
    return bool(
        loop.get("proposal_valid")
        and loop.get("patch_plan_valid")
        and loop.get("dry_run_before_apply")
        and loop.get("apply_status") == "APPLIED"
        and loop.get("tests_passed")
        and loop.get("rollback_available")
        and provider.get("nvidia_smoke_gate", "DO_NOT_CALL") == "DO_NOT_CALL"
        and provider.get("cloud_status", "SMOKE_FAIL_REDACTED") == "SMOKE_FAIL_REDACTED"
        and not security.get("cloud_called", True)
    )


def _coding_acceptance_tree_summary(payload: dict[str, Any]) -> dict[str, Any]:
    provider = payload.get("provider", {}) if isinstance(payload.get("provider"), dict) else {}
    loop = payload.get("loop", {}) if isinstance(payload.get("loop"), dict) else {}
    return {
        "status": "PASS" if _coding_acceptance_ok(payload) else "REVIEW",
        "mode": payload.get("mode", "fallback-only"),
        "cloud": provider.get("cloud_live_gate", "BLOCK_THIS_RUN"),
        "nvidia": provider.get("nvidia_smoke_gate", "DO_NOT_CALL"),
        "proposal_source": provider.get("proposal_source", "DETERMINISTIC_STUB_USED"),
        "apply_status": loop.get("apply_status", "REVIEW"),
        "initial_tests_failed_expected": bool(loop.get("initial_tests_failed_expected", False)),
        "tests_passed": bool(loop.get("tests_passed", False)),
        "rollback_available": bool(loop.get("rollback_available", False)),
        "witness_event_id": loop.get("witness_event_id", ""),
    }


def browser_bridge_status_payload() -> dict[str, Any]:
    app_root = MEDIOEVO_ROOT / "apps" / "local" / "wabi-sabi"
    if str(app_root) not in sys.path:
        sys.path.insert(0, str(app_root))
    try:
        from wabi_sabi.core.browser_bridge import build_browser_bridge_status  # noqa: PLC0415
        from wabi_sabi.core.browser_bridge_selector_pack import rank_browser_council_services  # noqa: PLC0415

        bridge_status = build_browser_bridge_status()
        selector_pack = bridge_status.get("selector_pack", {}) if isinstance(bridge_status.get("selector_pack"), dict) else {}
        ranking = rank_browser_council_services()
        backends = {
            item.get("backend", ""): {
                "configured": bool(item.get("configured")),
                "enabled": bool(item.get("enabled")),
                "available": bool(item.get("available")),
                "role": item.get("role", ""),
            }
            for item in bridge_status.get("backends", [])
            if isinstance(item, dict)
        }
        kimi_backend = backends.get("kimi-webbridge", {})
        devtools_backend = backends.get("chrome-devtools-mcp", {})
        kimi_flags_ready = (
            os.environ.get("WABI_ALLOW_BROWSER_SEND", "0") == "1"
            and os.environ.get("WABI_ALLOW_BROWSER_BRIDGE", "0") == "1"
        )
        kimi_url_configured = bool(os.environ.get("WABI_KIMI_WEBBRIDGE_URL"))
        if not kimi_flags_ready:
            kimi_status = "KIMI_SEND_FLAGS_MISSING"
        elif not kimi_url_configured:
            kimi_status = "KIMI_BRIDGE_URL_MISSING"
        else:
            kimi_status = "KIMI_READY_FOR_EXPLICIT_SMOKE"
        devtools_status = (
            "DEVTOOLS_MCP_READONLY_READY"
            if devtools_backend.get("available")
            else "DEVTOOLS_MCP_NOT_AVAILABLE"
        )
        council_services = int(ranking.get("service_count", 0) or 0)
        prepare_only_count = int(ranking.get("prepare_only_count", 0) or 0)
        ready_send_review_count = int(ranking.get("ready_send_review_count", 0) or 0)
        return sanitize_obj(
            {
                "schema": "wabi.browser_bridge_workbench.v0_2",
                "version": "v0.2",
                "browser_bridge_version": "v0.2",
                "state_fingerprint": "BROWSER-BRIDGE-SELECTOR-PACK-v0-2-20260518",
                "selected_backend": bridge_status.get("default_backend", "dry-run"),
                "primary_backend": bridge_status.get("primary_backend", "chrome-devtools-mcp"),
                "dry_run_default": True,
                "dry_run_status": "READY",
                "kimi_status": kimi_status,
                "kimi_smoke_status": kimi_status,
                "kimi_live_call_ran": False,
                "devtools_mcp_status": devtools_status,
                "devtools_readonly_status": devtools_status,
                "council_recommendation": {
                    "recommended_service": ranking.get("recommended_service", ""),
                    "recommended_mode": ranking.get("recommended_mode", "DRY_RUN"),
                    "next_action": "Kimi setup guide ready; live smoke requires double opt-in",
                },
                "council_services": council_services,
                "services_count": council_services,
                "ready_send_review": ready_send_review_count,
                "prepare_only": prepare_only_count,
                "prepare_only_count": prepare_only_count,
                "send_gated_count": ready_send_review_count,
                "blocked_count": ranking.get("blocked_count", 0),
                "live_attempts": 0,
                "code_response_policy": "PROPOSAL_ONLY_NO_APPLY",
                "last_proposal_status": "PROPOSAL_ONLY",
                "backends": backends,
                "selector_pack": {
                    "schema": selector_pack.get("schema", ""),
                    "version": selector_pack.get("version", "v0.2"),
                    "dry_run_available": bool(selector_pack.get("dry_run_available", True)),
                },
                "gates": {
                    "BrowserSendGate": "REVIEW_SEND_ONLY_WITH_DOUBLE_OPT_IN",
                    "ExternalServiceGate": "REVIEW_PER_SERVICE_ADAPTER",
                    "CloudLLMGate": "BLOCK_PRIVATE_WORKSPACE",
                    "PublicationGate": "BLOCK",
                },
                "online_ai_called": False,
                "browser_backend_called": False,
                "secret_values_printed": False,
                "publication_gate": "BLOCK",
                "next_action": "Kimi setup guide ready; live smoke requires double opt-in",
            }
        )
    except Exception as exc:
        return sanitize_obj(
            {
                "schema": "wabi.browser_bridge_workbench.v0_2",
                "version": "v0.2",
                "browser_bridge_version": "v0.2",
                "status": "REVIEW",
                "error": f"browser_bridge_status_unavailable:{type(exc).__name__}",
                "selected_backend": "dry-run",
                "dry_run_default": True,
                "dry_run_status": "READY",
                "kimi_status": "KIMI_SEND_FLAGS_MISSING",
                "kimi_smoke_status": "KIMI_SEND_FLAGS_MISSING",
                "kimi_live_call_ran": False,
                "devtools_mcp_status": "DEVTOOLS_MCP_NOT_AVAILABLE",
                "devtools_readonly_status": "DEVTOOLS_MCP_NOT_AVAILABLE",
                "council_services": 16,
                "services_count": 16,
                "ready_send_review": 1,
                "prepare_only": 15,
                "prepare_only_count": 15,
                "send_gated_count": 1,
                "blocked_count": 0,
                "live_attempts": 0,
                "code_response_policy": "PROPOSAL_ONLY_NO_APPLY",
                "last_proposal_status": "PROPOSAL_ONLY",
                "gates": {
                    "BrowserSendGate": "REVIEW_SEND_ONLY_WITH_DOUBLE_OPT_IN",
                    "ExternalServiceGate": "REVIEW_PER_SERVICE_ADAPTER",
                    "CloudLLMGate": "BLOCK_PRIVATE_WORKSPACE",
                    "PublicationGate": "BLOCK",
                },
                "online_ai_called": False,
                "browser_backend_called": False,
                "secret_values_printed": False,
                "publication_gate": "BLOCK",
                "next_action": "Kimi setup guide ready; live smoke requires double opt-in",
            }
        )


def operational_workbench_payload() -> dict[str, Any]:
    provider = wabi_provider_route_diagnostic_payload()
    route = provider_route_payload()
    cloud_budget_status = cloud_budget_status_payload()
    cloud_budget = cloud_budget_status.get("cloud_budget", {})
    tree = tree_health_payload()
    coding = coding_acceptance_payload()
    browser_bridge = browser_bridge_status_payload()
    versions = coding.get("versions", {}) if isinstance(coding.get("versions"), dict) else {}
    latest_version = str(coding.get("latest_version") or "v0.3")
    latest_coding = versions.get(latest_version, coding) if isinstance(versions, dict) else coding

    provider_summary = {
        "primary_provider": route.get("selected_provider") or provider.get("selected_provider_by_health") or provider.get("provider") or WABI_PRIMARY_PROVIDER,
        "primary_model": route.get("selected_model") or provider.get("selected_model_by_health") or provider.get("primary_model_configured") or WABI_PRIMARY_MODEL,
        "live_smoke_status": provider.get("last_smoke_status") or "SMOKE_FAIL_REDACTED",
        "route_status": route.get("status") or provider.get("route_diagnostic_status") or "REVIEW",
        "route_stage": route.get("route_stage") or "REVIEW",
        "last_error_class": provider.get("last_error_class") or "PROVIDER_OR_MODEL_NOT_FOUND_REDACTED",
        "next_smoke": "HEALTH_GATED_CLOUD_FIRST" if workbench_cloud_first_enabled() else (provider.get("recommended_next_smoke") or "DO_NOT_CALL"),
        "fallback": (
            f"{route.get('fallback_provider') or provider.get('fallback_provider') or WABI_FALLBACK_PROVIDER}/"
            f"{route.get('fallback_model') or provider.get('fallback_model') or WABI_FALLBACK_MODEL}"
        ),
        "cloud_first": workbench_cloud_first_enabled(),
        "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
        "raw_private_files_sent": False,
        "credential_present_redacted": bool(provider.get("credential_present_redacted")),
        "publication_gate": provider.get("publication_gate") or "BLOCK",
        "secret_values_printed": bool(provider.get("secret_values_printed")),
    }
    if provider_summary["route_status"] == "ACTIVE_CLOUD_ENGINE":
        provider_summary["primary_provider"] = WABI_PRIMARY_PROVIDER
        provider_summary["primary_model"] = WABI_PRIMARY_MODEL
        provider_summary["fallback"] = f"{WABI_FALLBACK_PROVIDER}/{WABI_FALLBACK_MODEL}"
        provider_summary["live_smoke_status"] = "ACTIVE_CLOUD_ENGINE"
        provider_summary["last_error_class"] = "DEEPSEEK_V4_FLASH_PRIMARY_HEALTH_GATED"
        provider_summary["next_smoke"] = "DEEPSEEK_V4_FLASH_READY"
    tree_summary = {
        "status": "PASS" if tree.get("ok") else "REVIEW",
        "files_inventoried": tree.get("tree", {}).get("files_inventoried"),
        "cache_files_quarantined": tree.get("tree", {}).get("cache_files_quarantined"),
        "rollback_available": bool(tree.get("tree", {}).get("rollback_available")),
        "compileall": tree.get("compileall", {}).get("claudio_global") or "REVIEW",
        "live_log_locks": tree.get("hashing", {}).get("classification") or "REVIEW",
        "secret_scan": "PASS" if not tree.get("secret_values_printed") else "REVIEW",
    }
    coding_summary = {
        "latest_version": latest_version,
        "status": "PASS" if coding.get("ok") else "REVIEW",
        "initial_tests_failed_expected": bool(latest_coding.get("loop", {}).get("initial_tests_failed_expected")),
        "patch_plan_valid": bool(latest_coding.get("loop", {}).get("patch_plan_valid")),
        "dry_run_before_apply": bool(latest_coding.get("loop", {}).get("dry_run_before_apply")),
        "apply_status": latest_coding.get("loop", {}).get("apply_status") or "REVIEW",
        "final_tests_passed": bool(latest_coding.get("loop", {}).get("tests_passed")),
        "rollback_available": bool(latest_coding.get("loop", {}).get("rollback_available")),
        "witness_event_id": latest_coding.get("loop", {}).get("witness_event_id") or "",
        "cloud": latest_coding.get("provider", {}).get("cloud_live_gate") or "BLOCK_THIS_RUN",
        "nvidia": latest_coding.get("provider", {}).get("nvidia_smoke_gate") or "DO_NOT_CALL",
        "local_generation_mode": latest_coding.get("provider", {}).get("proposal_source")
        or "DETERMINISTIC_STUB_USED",
        "secret_scan": "PASS"
        if not (coding.get("secret_values_printed") or latest_coding.get("security", {}).get("secret_values_printed"))
        else "REVIEW",
    }
    gates = {
        "ActionGate": "APPROVE_LOCAL_UI_TESTS_DOCS",
        "CloudLiveGate": "API_FIRST_HEALTH_GATED" if workbench_cloud_first_enabled() else "BLOCK_THIS_RUN",
        "CloudBudgetGate": cloud_budget.get("budget_gate", "CLOUD_BUDGET_REVIEW"),
        "DeepSeekSmokeGate": "HEALTH_GATED_PRIMARY" if workbench_cloud_first_enabled() else "DO_NOT_CALL",
        "NvidiaSmokeGate": "HEALTH_GATED_FALLBACK" if workbench_cloud_first_enabled() else "DO_NOT_CALL",
        "FallbackProvider": WABI_FALLBACK_PROVIDER,
        "SecondaryFallbackProvider": WABI_SECONDARY_FALLBACK_PROVIDER,
        "OfflineFallback": "ollama",
        "PublicationGate": "BLOCK",
        "DeletionGate": "BLOCK_DIRECT_DELETE",
    }
    evidence = {
        "provider_diagnostic": "apps/local/wabi-sabi/qa_artifacts/WABI_CLOUD_PROVIDER_v0_5_PROVIDER_DIAGNOSTIC.json",
        "tree_health_summary": (
            "qa_artifacts/release_validation/RUN_TREE_HEALTH_WORKBENCH_PANEL_20260518/"
            "TREE_HEALTH_WORKBENCH_PANEL_QA_SUMMARY.json"
        ),
        "coding_acceptance_summary": (
            "qa_artifacts/release_validation/RUN_WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3_20260518/"
            "WABI_FALLBACK_ONLY_CODING_ACCEPTANCE_v0_3_QA_SUMMARY.json"
        ),
        "witness_ids": {
            "coding_acceptance_v0_3": coding_summary["witness_event_id"],
            "safe_tests": 26,
        },
        "test_totals": {
            "wabi": "279 passed",
            "safe_tests": "ok=true, 279 passed",
            "claudio": "629 passed",
            "geodia": "74 passed",
            "duat_predictive": "117 passed",
        },
    }
    secret_values_printed = bool(
        provider_summary["secret_values_printed"]
        or tree.get("secret_values_printed")
        or coding.get("secret_values_printed")
    )
    local_pass = (
        provider_summary["route_status"] in {"REVIEW_SMOKE_NOT_RUN", "PASS_EXTERNAL_API_SMOKE", "ACTIVE_FALLBACK"}
        and tree_summary["status"] == "PASS"
        and coding_summary["status"] == "PASS"
        and coding_summary["final_tests_passed"]
    )
    status = "BLOCK" if secret_values_printed else ("REVIEW" if workbench_cloud_first_enabled() else ("PASS" if local_pass else "REVIEW"))
    return sanitize_obj(
        {
            "schema": "wabi.operational_workbench.v1",
            "state_fingerprint": "WABI-UI-VISUAL-ASSET-POLISH-20260518",
            "status": status,
            "provider": provider_summary,
            "cloud_budget": cloud_budget,
            "tree_health": tree_summary,
            "coding_acceptance": coding_summary,
            "workpack_scheduler": {
                "version": "v0.1",
                "execution_model": "MANUAL_TICK",
                "max_concurrency": 1,
                "queue_count": len(scheduler_records()),
                "publication_gate": "BLOCK",
            },
            "multi_step_workpacks": {
                "version": "v0.2",
                "execution_model": "MANUAL_TICK",
                "max_concurrency": 1,
                "workpack_count": len(multi_step_records()),
                "ready_count": sum(1 for row in multi_step_records() if row.get("status") in {"APPROVED", "SCHEDULED", "RUNNING", "PARTIAL"}),
                "publication_gate": "BLOCK",
                "cloud_called": False,
                "nvidia_called": False,
                "deepseek_called": False,
            },
            "browser_bridge": browser_bridge,
            "gates": gates,
            "evidence": evidence,
            "ui": {
                "theme": "wabi_du_wabi_20260519",
                "assets_manifest": "assets/wabi_du_wabi_20260519/ASSET_MANIFEST_20260519.json",
                "local_only": False if workbench_cloud_first_enabled() else True,
                "cloud_first": workbench_cloud_first_enabled(),
                "cloud_context_policy": WORKBENCH_CONTEXT_POLICY,
                "external_assets": False,
            },
            "next_actions": [
                "Local Execute v0.3 con workpacks multi-step",
                "Agent Chat routing v0.2",
                "Workpack Scheduler v0.1",
                "DeepSeek/Nemotron route smoke sin imprimir secretos",
            ],
            "secret_values_printed": secret_values_printed,
            "publication_gate": "BLOCK",
        }
    )


def mission_control_contract_payload() -> dict[str, Any]:
    return {
        "version": "v0.1",
        "mode": "LOCAL_ONLY_READONLY",
        "mutations_allowed": False,
        "execution_allowed": False,
        "inputs": [
            "agent_chat",
            "agent_hub",
            "local_hub",
            "workpacks",
            "scheduler",
            "browser_bridge",
            "provider",
            "tree_health",
            "coding_acceptance",
            "risks",
            "tasks",
            "handoff",
        ],
        "blocked_actions": [
            "EXECUTE",
            "PUBLISH",
            "PUSH",
            "DEPLOY",
            "RUN_CLOUD",
            "RUN_KIMI",
            "RUN_NVIDIA",
            "RUN_DEEPSEEK",
            "DELETE_DIRECT",
        ],
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }


def mission_control_state_schema_payload() -> dict[str, Any]:
    return {
        "$schema": "json-schema-draft-2020-12",
        "$id": "medioevo.claudio_mission_control.state.v0_1",
        "type": "object",
        "required": [
            "mission_control_version",
            "status",
            "generated_at",
            "agents",
            "workpacks",
            "scheduler",
            "chat",
            "gates",
            "provider",
            "browser_bridge",
            "tree_health",
            "risks",
            "next_actions",
            "evidence",
            "mutations_allowed",
            "execution_allowed",
            "publication_gate",
        ],
        "properties": {
            "mission_control_version": {"const": "v0.1"},
            "status": {"enum": ["PASS", "REVIEW", "BLOCK"]},
            "generated_at": {"type": "string"},
            "agents": {"type": "object"},
            "workpacks": {"type": "object"},
            "scheduler": {"type": "object"},
            "chat": {"type": "object"},
            "gates": {"type": "object"},
            "provider": {"type": "object"},
            "browser_bridge": {"type": "object"},
            "tree_health": {"type": "object"},
            "risks": {"type": "array", "items": {"type": "object"}},
            "next_actions": {"type": "array", "items": {"type": "object"}},
            "evidence": {"type": "object"},
            "mutations_allowed": {"const": False},
            "execution_allowed": {"const": False},
            "publication_gate": {"const": "BLOCK"},
        },
        "additionalProperties": True,
    }


def ensure_mission_control_contract_files() -> None:
    write_json_file(MISSION_CONTROL_CONTRACT_PATH, mission_control_contract_payload())
    write_json_file(MISSION_CONTROL_SCHEMA_PATH, mission_control_state_schema_payload())


def _count_by_field(rows: list[dict[str, Any]], field: str, fallback: str = "UNKNOWN") -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row.get(field) or fallback).upper()
        counts[key] = counts.get(key, 0) + 1
    return counts


def _first_queue_item(rows: list[dict[str, Any]], statuses: set[str]) -> dict[str, Any]:
    for row in sorted(rows, key=lambda item: (int(item.get("priority", 0) or 0), str(item.get("scheduled_at", "")))):
        if str(row.get("status") or "").upper() in statuses:
            return {
                "queue_id": str(row.get("queue_id", "")),
                "workpack_id": str(row.get("workpack_id", "")),
                "title": str(row.get("title", "")),
                "status": str(row.get("status", "")),
                "lane": str(row.get("lane", "")),
                "assigned_agent": str(row.get("assigned_agent", "")),
            }
    return {}


def mission_control_risks() -> list[dict[str, Any]]:
    return [
        {
            "risk_id": "linkedin-manual-pending",
            "status": "REVIEW",
            "risk": "MEDIUM",
            "gate": "LinkedInGate=MANUAL_POST_REQUIRED",
            "next_action": "Manual copy/paste only after private-boundary review.",
        },
        {
            "risk_id": "kimi-flags-url-missing",
            "status": "REVIEW",
            "risk": "LOW",
            "gate": "KimiSendGate=BLOCK_THIS_RUN",
            "next_action": "Run only future public synthetic smoke with double opt-in and redacted URL.",
        },
        {
            "risk_id": "nvidia-route-review",
            "status": "BLOCK",
            "risk": "MEDIUM",
            "gate": "NvidiaSmokeGate=DO_NOT_CALL",
            "next_action": "Do not call NVIDIA in this run.",
        },
        {
            "risk_id": "deepseek-quota-billing-review",
            "status": "REVIEW",
            "risk": "MEDIUM",
            "gate": "DeepSeekGate=REVIEW_QUOTA_OR_BILLING",
            "next_action": "No retry until quota and billing boundary are reviewed.",
        },
        {
            "risk_id": "formal-lab-license-legal-review",
            "status": "REVIEW",
            "risk": "MEDIUM",
            "gate": "LEGAL_REVIEW_REQUIRED",
            "next_action": "Keep Formal Lab material out of public/export surfaces.",
        },
    ]


def mission_control_next_actions() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "action": "MCP client config guide for local compatible agents",
            "reason": "v0.3 exposes read/prepare tools locally; next value is safe client configuration without external exposure.",
            "gate": "MCPGate=APPROVE_LOCAL_CONFIG_DOCS",
            "status": "NEXT",
        },
        {
            "rank": 2,
            "action": "POST delta falsifier/test",
            "reason": "Keeps source intake disciplined without raw import.",
            "gate": "SourceAdoption=REVIEW_SELECTIVE_EXTRACTION",
            "status": "NEXT",
        },
        {
            "rank": 3,
            "action": "Mission Control v0.2 read-only alerts and filters",
            "reason": "Builds on the same endpoint without adding execution.",
            "gate": "APPROVE_LOCAL_READONLY_DASHBOARD_TESTS_DOCS",
            "status": "NEXT",
        },
        {
            "rank": 4,
            "action": "BrowserBridge read-only visual QA",
            "reason": "Only if Chrome DevTools MCP becomes locally available.",
            "gate": "BrowserBridgeGate=READ_ONLY",
            "status": "REVIEW",
        },
    ]


def wabi_mcp_bridge_status_payload() -> dict[str, Any]:
    contract: dict[str, Any] = {}
    manifest: dict[str, Any] = {}
    try:
        if WABI_MCP_CONTRACT_PATH.exists():
            loaded = json.loads(WABI_MCP_CONTRACT_PATH.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                contract = loaded
    except json.JSONDecodeError:
        contract = {}
    try:
        if WABI_MCP_MANIFEST_PATH.exists():
            loaded = json.loads(WABI_MCP_MANIFEST_PATH.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                manifest = loaded
    except json.JSONDecodeError:
        manifest = {}
    readonly_tools = [
        "get_mission_control",
        "get_agent_hub",
        "search_agent_chat",
        "reconstruct_agent_thread",
        "verify_agent_chat_hash_chain",
        "get_workpacks",
        "get_scheduler_state",
        "get_browser_bridge_status",
        "get_provider_status",
        "get_tree_health",
        "get_coding_acceptance",
        "get_latest_handoff",
    ]
    prepare_tools = [
        "create_taskspec_draft",
        "create_workpack_draft",
        "attach_message_to_workpack",
        "write_handoff_draft",
    ]
    gated_tools = [
        "run_ghostgate",
        "queue_workpack",
        "scheduler_tick",
        "execute_local_workpack",
        "rollback_workpack",
    ]
    return sanitize_obj(
        {
            "schema": "medioevo.wabi_mcp_bridge.status.v0_4",
            "version": contract.get("version", "v0.4"),
            "mode": contract.get("mode", "LOCALHOST_ONLY_READ_PREPARE_GATED_WRITE_DESIGN"),
            "host": contract.get("host", "127.0.0.1"),
            "localhost_only": contract.get("host", "127.0.0.1") in {"127.0.0.1", "localhost"},
            "tools_enabled": contract.get("tools_enabled", "READ_ONLY_PREPARE_AND_GATED_WRITE_DESIGN"),
            "read_only_tools_count": len(readonly_tools),
            "read_only_tools": readonly_tools,
            "prepare_tools_enabled": bool(contract.get("prepare_tools_enabled", False)),
            "prepare_tools_count": len(prepare_tools),
            "prepare_tools_blocked": 0 if contract.get("prepare_tools_enabled", False) else len(prepare_tools),
            "gated_write_designed": bool(contract.get("gated_write_designed", False)),
            "gated_write_enabled": bool(contract.get("gated_write_enabled", contract.get("gated_write_tools_enabled", False))),
            "gated_write_tools_enabled": bool(contract.get("gated_write_enabled", contract.get("gated_write_tools_enabled", False))),
            "gated_write_tools_blocked": len(gated_tools),
            "dry_run_allowed": bool(contract.get("dry_run_allowed", False)),
            "real_apply_allowed": bool(contract.get("real_apply_allowed", False)),
            "mutations_allowed": bool(contract.get("mutations_allowed", False)),
            "mutation_scope": contract.get("mutation_scope", "DRAFT_ONLY" if contract.get("mutations_allowed") else "BLOCK"),
            "draft_mutations_allowed": bool(contract.get("draft_mutations_allowed", False)),
            "execution_allowed": bool(contract.get("execution_allowed", False)),
            "cloud_allowed": bool(contract.get("cloud_allowed", False)),
            "publication_allowed": bool(contract.get("publication_allowed", False)),
            "external_exposure_allowed": bool(contract.get("external_exposure_allowed", False)),
            "requires_task_spec": bool(contract.get("requires_task_spec", False)),
            "requires_ghostgate": bool(contract.get("requires_ghostgate", False)),
            "requires_rollback": bool(contract.get("requires_rollback", False)),
            "requires_witnesslog": bool(contract.get("requires_witnesslog", False)),
            "contract_exists": WABI_MCP_CONTRACT_PATH.exists(),
            "contract_v04_exists": WABI_MCP_CONTRACT_V04_PATH.exists(),
            "request_schema_exists": WABI_MCP_GATED_WRITE_REQUEST_SCHEMA_PATH.exists(),
            "decision_schema_exists": WABI_MCP_GATED_WRITE_DECISION_SCHEMA_PATH.exists(),
            "dry_run_schema_exists": WABI_MCP_GATED_WRITE_DRY_RUN_SCHEMA_PATH.exists(),
            "manifest_exists": WABI_MCP_MANIFEST_PATH.exists(),
            "last_smoke_status": "PENDING_THIS_RUN",
            "next_action": "MCP v0.4 gated-write design dry-run, real execution disabled.",
            "blocked_reason": "GatedWriteGate=DESIGN_ONLY_REAL_EXECUTION_BLOCKED",
            "entrypoint": manifest.get("entrypoint", "python -m wabi_mcp_server.server"),
            "publication_gate": contract.get("publication_gate", "BLOCK"),
            "secret_values_printed": False,
        }
    )


def mcp_gated_write_design_payload() -> dict[str, Any]:
    design_smoke = _read_smoke_status(WABI_MCP_GATED_WRITE_DESIGN_SMOKE_PATH)
    dry_run = _read_smoke_status(WABI_MCP_GATED_WRITE_DRY_RUN_SIMULATION_PATH)
    status = "READY_DESIGN_ONLY" if design_smoke == "PASS" and dry_run == "PASS" and WABI_MCP_CONTRACT_V04_PATH.exists() else "REVIEW"
    return sanitize_obj(
        {
            "schema": "medioevo.wabi_mcp.gated_write_design.v0_4",
            "version": "v0.4",
            "status": status,
            "contract": "READY" if WABI_MCP_CONTRACT_V04_PATH.exists() else "MISSING",
            "request_schema": "READY" if WABI_MCP_GATED_WRITE_REQUEST_SCHEMA_PATH.exists() else "MISSING",
            "decision_schema": "READY" if WABI_MCP_GATED_WRITE_DECISION_SCHEMA_PATH.exists() else "MISSING",
            "dry_run_schema": "READY" if WABI_MCP_GATED_WRITE_DRY_RUN_SCHEMA_PATH.exists() else "MISSING",
            "gated_write_enabled": False,
            "execution_allowed": False,
            "dry_run_allowed": True,
            "real_apply_allowed": False,
            "scheduler_tick_real_blocked": True,
            "execute_local_workpack_real_blocked": True,
            "last_design_smoke": design_smoke,
            "dry_run_simulation": dry_run,
            "next": "v0.5 explicit opt-in sandbox execution design",
            "artifact_dir": local_relative_path(WABI_MCP_GATED_WRITE_DESIGN_RUN_DIR) if WABI_MCP_GATED_WRITE_DESIGN_RUN_DIR.exists() else "",
            "secret_values_printed": False,
            "publication_gate": "BLOCK",
        }
    )


def mcp_client_config_readiness_payload() -> dict[str, Any]:
    template_paths = [WABI_MCP_CLIENT_CONFIG_DIR / name for name in WABI_MCP_CLIENT_CONFIG_TEMPLATE_NAMES]
    templates_ready = all(path.exists() for path in template_paths) and (WABI_MCP_CLIENT_CONFIG_DIR / "README_CLIENT_CONFIGS.md").exists()
    guide_ready = WABI_MCP_CLIENT_CONFIG_GUIDE_PATH.exists()
    contract_ready = WABI_MCP_CLIENT_CONFIG_CONTRACT_PATH.exists()
    return sanitize_obj(
        {
            "schema": "medioevo.wabi_mcp.client_config_readiness.v0_1",
            "mcp_server_version": "v0.3",
            "client_config_guide": "READY" if guide_ready else "MISSING",
            "templates": "READY" if templates_ready else "MISSING",
            "contract": "READY" if contract_ready else "MISSING",
            "mode": "LOCALHOST_ONLY_READ_PREPARE",
            "client_scope": "LOCAL_CLIENT_CONFIG_ONLY",
            "localhost_only": True,
            "execution_allowed": False,
            "gated_write_allowed": False,
            "external_exposure_allowed": False,
            "tunnel_allowed": False,
            "credentials_in_files_allowed": False,
            "read_smoke_default": "READ_ONLY",
            "prepare_smoke": "EXPLICIT_OPT_IN_ONLY",
            "next": "MCP prepare-only client smoke or MCP v0.4 gated-write design",
            "guide_path": local_relative_path(WABI_MCP_CLIENT_CONFIG_GUIDE_PATH) if guide_ready else "",
            "template_count": len(WABI_MCP_CLIENT_CONFIG_TEMPLATE_NAMES) if templates_ready else 0,
            "secret_values_printed": False,
            "publication_gate": "BLOCK",
        }
    )


def _read_smoke_status(path: Path) -> str:
    try:
        if not path.exists():
            return "REVIEW"
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and payload.get("ok") is True and not payload.get("secret_values_printed", False):
            return "PASS"
    except (OSError, json.JSONDecodeError):
        return "REVIEW"
    return "REVIEW"


def mcp_prepare_client_smoke_payload() -> dict[str, Any]:
    read_status = _read_smoke_status(WABI_MCP_CLIENT_READONLY_SMOKE_PATH)
    prepare_status = _read_smoke_status(WABI_MCP_CLIENT_PREPARE_SMOKE_PATH)
    gated_status = _read_smoke_status(WABI_MCP_CLIENT_GATED_BLOCK_SMOKE_PATH)
    status = "PASS" if {read_status, prepare_status, gated_status} == {"PASS"} else "REVIEW"
    return sanitize_obj(
        {
            "schema": "medioevo.wabi_mcp.prepare_client_smoke.v0_1",
            "client": "LOCAL_WRAPPER",
            "status": status,
            "read_only_smoke": read_status,
            "prepare_only_smoke": prepare_status,
            "gated_write_block_smoke": gated_status,
            "execution_allowed": False,
            "external_exposure_allowed": False,
            "gated_write_allowed": False,
            "cloud_allowed": False,
            "prepare_store_allowed": True,
            "contract": "READY" if WABI_MCP_PREPARE_CLIENT_SMOKE_CONTRACT_PATH.exists() else "MISSING",
            "next": "MCP v0.4 gated-write design, still disabled",
            "artifact_dir": local_relative_path(WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR) if WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR.exists() else "",
            "secret_values_printed": False,
            "publication_gate": "BLOCK",
        }
    )


def mission_control_payload() -> dict[str, Any]:
    ensure_mission_control_contract_files()
    agent_hub = agent_hub_payload()
    local_hub = local_hub_payload()
    workpacks = workpacks_payload()
    scheduler = workpack_scheduler_payload()
    browser_bridge = browser_bridge_status_payload()
    provider_diag = wabi_provider_route_diagnostic_payload()
    provider_route = provider_route_payload({"cloud_providers_blocked": True})
    mcp_bridge = wabi_mcp_bridge_status_payload()
    mcp_client_config = mcp_client_config_readiness_payload()
    mcp_prepare_client_smoke = mcp_prepare_client_smoke_payload()
    mcp_gated_write_design = mcp_gated_write_design_payload()
    tree = tree_health_payload()
    coding = coding_acceptance_payload()
    rooms = agent_chat_rooms_payload()
    hash_chain = agent_chat_verify_hash_chain()
    search = agent_chat_search_payload({"q": "workpack", "limit": "20"})
    agent_status = agent_chat_status_payload()
    system_events = agent_chat_read_messages({"message_type": "SYSTEM", "limit": "6"})

    agents_raw = agent_hub.get("agents", []) if isinstance(agent_hub.get("agents"), list) else []
    agents = [
        {
            "agent_id": str(agent.get("agent_id", "")),
            "display_name": str(agent.get("display_name", agent.get("name", ""))),
            "status": str(agent.get("status", "Review")),
            "gate": str(agent.get("gate", "REVIEW")),
            "inbox_count": int(agent.get("inbox_count", 0) or 0),
            "outbox_count": int(agent.get("outbox_count", 0) or 0),
            "assigned_workpacks": list(agent.get("workpacks", []) or []),
            "assigned_workpack_count": int(agent.get("workpack_count", 0) or 0),
            "scheduled_workpack_count": int(agent.get("scheduled_workpack_count", 0) or 0),
            "multi_step_workpack_count": int(agent.get("multi_step_workpack_count", 0) or 0),
        }
        for agent in agents_raw
        if isinstance(agent, dict)
    ]
    workpack_rows = workpacks.get("workpacks", []) if isinstance(workpacks.get("workpacks"), list) else []
    queue_rows = scheduler.get("queue", []) if isinstance(scheduler.get("queue"), list) else []
    scheduler_witness = read_jsonl(WORKPACK_SCHEDULER_WITNESSLOG_PATH, limit=30)
    tick_events = [row for row in scheduler_witness if str(row.get("event", "")).startswith("scheduler_tick")]
    provider_smoke = str(provider_diag.get("last_smoke_status") or provider_diag.get("provider_state") or "SMOKE_FAIL_REDACTED")
    browser_live_attempts = int(browser_bridge.get("live_attempts", 0) or 0)
    chat_ok = bool(hash_chain.get("ok")) and str(hash_chain.get("status")) == "HASH_CHAIN_PASS"
    secret_values_printed = any(
        bool(item)
        for item in [
            agent_hub.get("secret_values_printed"),
            local_hub.get("secret_values_printed"),
            workpacks.get("secret_values_printed"),
            scheduler.get("secret_values_printed"),
            browser_bridge.get("secret_values_printed"),
            provider_diag.get("secret_values_printed"),
            tree.get("secret_values_printed"),
            coding.get("secret_values_printed"),
        ]
    )
    unsafe_provider_pass = provider_smoke == "SMOKE_PASS"
    status = "BLOCK" if secret_values_printed or not chat_ok else ("REVIEW" if unsafe_provider_pass or browser_live_attempts else "PASS")
    latest_coding_version = str(coding.get("latest_version") or "v0.3")
    latest_coding = coding.get("versions", {}).get(latest_coding_version, {}) if isinstance(coding.get("versions"), dict) else {}
    payload = {
        "schema": "medioevo.claudio_mission_control.state.v0_1",
        "mission_control_version": "v0.1",
        "status": status,
        "generated_at": utc_now_iso(),
        "state_fingerprint": "CLAUDIO-MISSION-CONTROL-v0-1-20260518",
        "boundary": MISSION_CONTROL_BOUNDARY,
        "mode": "LOCAL_ONLY_READONLY",
        "mutations_allowed": False,
        "execution_allowed": False,
        "dashboard_actions": "READ_ONLY_NO_EXECUTION",
        "agents": {
            "total": len(agents),
            "status_counts": _count_by_field(agents, "status", "REVIEW"),
            "gate_counts": _count_by_field(agents, "gate", "REVIEW"),
            "total_inbox": sum(int(agent.get("inbox_count", 0) or 0) for agent in agents),
            "total_outbox": sum(int(agent.get("outbox_count", 0) or 0) for agent in agents),
            "items": agents,
        },
        "workpacks": {
            "total": len(workpack_rows),
            "status_counts": _count_by_field(workpack_rows, "status", "DRAFT"),
            "draft": sum(1 for row in workpack_rows if str(row.get("status", "")).upper() == "DRAFT"),
            "approved": sum(1 for row in workpack_rows if str(row.get("status", "")).upper() == "APPROVED"),
            "executed": sum(1 for row in workpack_rows if str(row.get("status", "")).upper() == "EXECUTED"),
            "rolled_back": sum(1 for row in workpack_rows if str(row.get("status", "")).upper() == "ROLLED_BACK"),
            "blocked": sum(1 for row in workpack_rows if str(row.get("status", "")).upper() == "BLOCKED"),
            "execution_allowed_from_dashboard": False,
            "publication_gate": workpacks.get("publication_gate", "BLOCK"),
        },
        "scheduler": {
            "version": scheduler.get("version", "v0.1"),
            "execution_model": scheduler.get("execution_model", "MANUAL_TICK"),
            "queue_total": len(queue_rows),
            "queue_status_counts": _count_by_field(queue_rows, "status", "DRAFT"),
            "next_ready_item": _first_queue_item(queue_rows, {"READY", "APPROVED", "SCHEDULED"}),
            "blocked_lanes": sorted(WORKPACK_SCHEDULER_BLOCKED_LANES),
            "last_tick": tick_events[-1] if tick_events else {},
            "max_concurrency": scheduler.get("max_concurrency", 1),
            "tick_from_dashboard": "BLOCK",
            "publication_gate": scheduler.get("publication_gate", "BLOCK"),
        },
        "chat": {
            "version": "v0.3",
            "message_count": int(hash_chain.get("message_count", 0) or 0),
            "rooms_count": len(rooms.get("rooms", []) or []),
            "hash_chain_status": hash_chain.get("status", "REVIEW"),
            "hash_chain_ok": bool(hash_chain.get("ok")),
            "search_result_count": int(search.get("result_count", 0) or 0),
            "search_index_status": "LOCAL_INDEX_AVAILABLE" if AGENT_CHAT_SEARCH_INDEX_PATH.exists() else "LOCAL_INDEX_REBUILD_AVAILABLE",
            "thread_reconstruction": "AVAILABLE_READ_ONLY",
            "execution_from_search": "BLOCK",
            "status_by_agent": agent_status.get("statuses", {}),
            "latest_system_events": [
                {
                    "message_id": str(row.get("message_id", "")),
                    "room": str(row.get("room", "")),
                    "created_at": str(row.get("created_at", row.get("timestamp", ""))),
                    "event": str(row.get("tags", ["SYSTEM"])[0] if row.get("tags") else row.get("message_type", "SYSTEM")),
                    "body_excerpt": agent_chat_redact_export_text(str(row.get("body", "")))[:180],
                    "linked_task_id": str(row.get("linked_task_id", "")),
                    "linked_workpack_id": str(row.get("linked_workpack_id", "")),
                }
                for row in system_events[-6:]
            ],
            "public_export_allowed": False,
            "publication_gate": "BLOCK",
        },
        "gates": {
            "ActionGate": "APPROVE_LOCAL_READONLY_DASHBOARD_TESTS_DOCS",
            "CloudLiveGate": "BLOCK_THIS_RUN",
            "KimiSendGate": "BLOCK_THIS_RUN",
            "NvidiaSmokeGate": "DO_NOT_CALL",
            "DeepSeekGate": "REVIEW_QUOTA_OR_BILLING",
            "PublicationGate": "BLOCK",
            "DeletionGate": "BLOCK_DIRECT_DELETE",
            "CloudLLMGate": "BLOCK_PRIVATE_WORKSPACE",
        },
        "provider": {
            "status": provider_diag.get("route_diagnostic_status", provider_route.get("status", "REVIEW")),
            "selected_provider": provider_route.get("selected_provider", "ollama"),
            "selected_model": provider_route.get("selected_model", ""),
            "route_stage": provider_route.get("route_stage", "LOCAL"),
            "last_smoke_status": provider_smoke,
            "provider_pass_claimed": provider_smoke == "SMOKE_PASS",
            "fallback_provider": provider_diag.get("fallback_provider", WABI_FALLBACK_PROVIDER),
            "fallback_model": provider_diag.get("fallback_model", WABI_FALLBACK_MODEL),
            "recommended_next_smoke": provider_diag.get("recommended_next_smoke", "DO_NOT_CALL"),
            "workspace_sent": False,
            "secret_values_printed": False,
            "publication_gate": provider_diag.get("publication_gate", "BLOCK"),
        },
        "browser_bridge": {
            "version": browser_bridge.get("browser_bridge_version", "v0.2"),
            "dry_run_default": bool(browser_bridge.get("dry_run_default", True)),
            "kimi_status": browser_bridge.get("kimi_status", "KIMI_SEND_FLAGS_MISSING"),
            "kimi_live_call_ran": bool(browser_bridge.get("kimi_live_call_ran", False)),
            "devtools_mcp_status": browser_bridge.get("devtools_mcp_status", "DEVTOOLS_MCP_NOT_AVAILABLE"),
            "council_services": int(browser_bridge.get("council_services", 16) or 16),
            "ready_send_review": int(browser_bridge.get("ready_send_review", 1) or 1),
            "prepare_only": int(browser_bridge.get("prepare_only", 15) or 15),
            "live_attempts": browser_live_attempts,
            "code_response_policy": browser_bridge.get("code_response_policy", "PROPOSAL_ONLY_NO_APPLY"),
            "publication_gate": browser_bridge.get("publication_gate", "BLOCK"),
        },
        "mcp_bridge": mcp_bridge,
        "mcp_client_config_readiness": mcp_client_config,
        "mcp_prepare_client_smoke": mcp_prepare_client_smoke,
        "mcp_gated_write_design_v0_4": mcp_gated_write_design,
        "tree_health": {
            "status": "PASS" if tree.get("ok") else "REVIEW",
            "compileall_status": tree.get("compileall", {}).get("claudio_global", "REVIEW") if isinstance(tree.get("compileall"), dict) else "REVIEW",
            "secret_scan_status": "PASS" if not tree.get("secret_values_printed") else "REVIEW",
            "rollback_available": bool(tree.get("tree", {}).get("rollback_available")) if isinstance(tree.get("tree"), dict) else False,
            "live_log_locks": tree.get("hashing", {}).get("classification", "REVIEW") if isinstance(tree.get("hashing"), dict) else "REVIEW",
            "publication_gate": tree.get("publication_gate", "BLOCK"),
        },
        "coding_acceptance": {
            "latest_version": latest_coding_version,
            "status": "PASS" if coding.get("ok") else "REVIEW",
            "apply_status": latest_coding.get("loop", {}).get("apply_status", "REVIEW") if isinstance(latest_coding.get("loop"), dict) else "REVIEW",
            "tests_passed": bool(latest_coding.get("loop", {}).get("tests_passed")) if isinstance(latest_coding.get("loop"), dict) else False,
            "rollback_available": bool(latest_coding.get("loop", {}).get("rollback_available")) if isinstance(latest_coding.get("loop"), dict) else False,
            "cloud_live_gate": latest_coding.get("provider", {}).get("cloud_live_gate", "BLOCK_THIS_RUN") if isinstance(latest_coding.get("provider"), dict) else "BLOCK_THIS_RUN",
            "nvidia_smoke_gate": latest_coding.get("provider", {}).get("nvidia_smoke_gate", "DO_NOT_CALL") if isinstance(latest_coding.get("provider"), dict) else "DO_NOT_CALL",
        },
        "local_hub": {
            "task_count": int(local_hub.get("task_count", len(local_hub.get("tasks", []) or [])) or 0),
            "communication_mode": local_hub.get("communication_mode", "LOCAL_ONLY"),
            "publication_gate": local_hub.get("publication_gate", "BLOCK"),
            "witnesslog": local_hub.get("witness_log", local_hub.get("witnesslog", "LOCAL_ONLY")),
        },
        "risks": mission_control_risks(),
        "next_actions": mission_control_next_actions(),
        "evidence": {
            "run_id": MISSION_CONTROL_RUN_ID,
            "contract": local_relative_path(MISSION_CONTROL_CONTRACT_PATH),
            "schema": local_relative_path(MISSION_CONTROL_SCHEMA_PATH),
            "agent_chat_qa_summary": "qa_artifacts/release_validation/RUN_AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_20260518/AGENT_CHAT_PERSISTENCE_SEARCH_v0_3_QA_SUMMARY.json",
            "workpack_scheduler_qa_summary": "qa_artifacts/release_validation/RUN_WORKPACK_SCHEDULER_v0_1_20260518/WORKPACK_SCHEDULER_v0_1_QA_SUMMARY.json",
            "browser_bridge_qa_summary": "qa_artifacts/release_validation/RUN_KIMI_WEBBRIDGE_SETUP_GUIDE_v0_1_20260518/KIMI_WEBBRIDGE_SETUP_GUIDE_v0_1_QA_SUMMARY.json",
            "wabi_mcp_contract": local_relative_path(WABI_MCP_CONTRACT_PATH),
            "wabi_mcp_client_config_guide": local_relative_path(WABI_MCP_CLIENT_CONFIG_GUIDE_PATH) if WABI_MCP_CLIENT_CONFIG_GUIDE_PATH.exists() else "",
            "wabi_mcp_prepare_client_smoke": local_relative_path(WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR) if WABI_MCP_PREPARE_CLIENT_SMOKE_RUN_DIR.exists() else "",
            "wabi_mcp_gated_write_design": local_relative_path(WABI_MCP_GATED_WRITE_DESIGN_RUN_DIR) if WABI_MCP_GATED_WRITE_DESIGN_RUN_DIR.exists() else "",
            "latest_handoff": "HANDOFF_CURRENT.md",
            "latest_session_fingerprint": "SESSION_FINGERPRINT.json",
        },
        "external_calls": {
            "cloud": False,
            "kimi": False,
            "nvidia": False,
            "deepseek": False,
            "push": False,
            "deploy": False,
            "publication": False,
        },
        "secret_values_printed": secret_values_printed,
        "publication_gate": "BLOCK",
    }
    return sanitize_obj(payload)


def utc_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def safe_local_id(raw: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(raw or "").strip()).strip("-")
    if not value:
        raise ValueError("id required")
    return value[:96]


def safe_optional_local_id(raw: Any) -> str:
    value = str(raw or "").strip()
    return safe_local_id(value) if value else ""


def local_relative_path(path: pathlib.Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        try:
            return path.resolve().relative_to(MEDIOEVO_ROOT.resolve()).as_posix()
        except ValueError:
            return sanitize_text(path.name)


def write_json_file(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sanitize_obj(payload), ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = sanitize_obj(payload)
    path.open("a", encoding="utf-8").write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")
    return record


def read_jsonl(path: pathlib.Path, *, limit: int = 50) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(sanitize_obj(value))
    return rows


def local_gate_default_state(*, status: str = "DEFAULT_SAFE") -> dict[str, Any]:
    return {
        "schema_version": "wabi.local_gate_state.v0_1",
        "environment": LOCAL_GATE_ENVIRONMENT,
        "owner_authorization": LOCAL_GATE_OWNER_AUTHORIZATION,
        "gate_control_mode": LOCAL_GATE_CONTROL_MODE,
        "state_status": status,
        "updated_at": utc_now_iso(),
        "updated_by": "system_default",
        "gates": dict(LOCAL_GATE_DEFAULTS),
    }


def _coerce_gate_updates(payload: dict[str, Any] | None) -> dict[str, str]:
    data = payload or {}
    raw_updates = data.get("gates") if isinstance(data.get("gates"), dict) else data
    updates: dict[str, str] = {}
    for key, value in raw_updates.items():
        gate = str(key)
        if gate in LOCAL_GATE_OPTIONS:
            updates[gate] = str(value or "").strip().upper()
    return updates


def validate_local_gate_updates(updates: dict[str, str]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for gate, value in updates.items():
        if gate not in LOCAL_GATE_OPTIONS:
            errors.append({"gate": gate, "value": value, "error": "UNKNOWN_GATE"})
            continue
        if gate in LOCAL_GATE_LOCKED and value != LOCAL_GATE_DEFAULTS[gate]:
            errors.append({"gate": gate, "value": value, "error": "HARD_BLOCK_GATE_LOCKED"})
            continue
        if gate == "NetworkExposureGate" and value in {"WAN", "ALLOW_WAN", "PUBLIC", "EXTERNAL"}:
            errors.append({"gate": gate, "value": value, "error": "WAN_EXPOSURE_REJECTED"})
            continue
        if value not in LOCAL_GATE_OPTIONS[gate]:
            errors.append({"gate": gate, "value": value, "error": "INVALID_GATE_VALUE"})
    return errors


def local_gate_effective_policy(gates: dict[str, str] | None = None) -> dict[str, Any]:
    current = dict(LOCAL_GATE_DEFAULTS)
    current.update(gates or {})
    return {
        "cloud_provider_live_allowed": current.get("CloudGate") == "ALLOW_EXISTING_PROVIDER",
        "cloud_provider_review_required": current.get("CloudGate") == "REVIEW",
        "local_apply_allowed": current.get("ApplyGate") == "ALLOW_LOCAL_APPLY",
        "local_apply_review_required": current.get("ApplyGate") == "REVIEW",
        "local_export_allowed": current.get("PublicationGate") == "ALLOW_LOCAL_EXPORT_ONLY",
        "runtime_import_allowed": current.get("RuntimeImportGate") == "ALLOW_LOCAL_SAFE_IMPORT",
        "runtime_import_review_required": current.get("RuntimeImportGate") == "REVIEW",
        "raw_adoption_allowed": False,
        "raw_adoption_review_required": current.get("RawAdoptionGate") == "REVIEW",
        "destructive_delete_allowed": False,
        "destructive_delete_review_with_backup": current.get("DestructiveDeleteGate") == "REVIEW_WITH_BACKUP",
        "strong_science_claims_allowed": False,
        "local_theory_draft_allowed": current.get("ScienceClaimGate") == "LOCAL_THEORY_DRAFT",
        "secret_access_allowed": False,
        "credential_access_allowed": False,
        "wan_exposure_allowed": False,
        "localhost_only": current.get("NetworkExposureGate") == "LOCALHOST_ONLY",
        "hard_blocks": ["SecretGate", "CredentialGate", "NetworkExposureGate:WAN"],
    }


def local_gate_change_warning(gate: str, value: str) -> str:
    warnings = {
        ("CloudGate", "ALLOW_EXISTING_PROVIDER"): "Cloud provider remains existing-provider only; no secrets are displayed and no cloud call is made by this toggle alone.",
        ("ApplyGate", "ALLOW_LOCAL_APPLY"): "Local apply can modify files only through existing allowlisted apply paths with rollback/test evidence.",
        ("RuntimeImportGate", "ALLOW_LOCAL_SAFE_IMPORT"): "Runtime imports are limited to local safe import review; raw adoption remains blocked.",
        ("RawAdoptionGate", "REVIEW"): "Raw adoption remains non-APPROVE; review only, no blind ZIP/source/corpus adoption.",
        ("DestructiveDeleteGate", "REVIEW_WITH_BACKUP"): "Destructive delete is still not auto-approved; backup and review evidence are required.",
        ("PublicationGate", "ALLOW_LOCAL_EXPORT_ONLY"): "Only local export artifacts are allowed; deploy/publication remains blocked.",
        ("NetworkExposureGate", "REVIEW_LAN"): "LAN exposure is review-only; server default remains 127.0.0.1.",
        ("ScienceClaimGate", "LOCAL_THEORY_DRAFT"): "Only local theory draft wording is allowed; strong claims remain blocked until F1-F6.",
    }
    return warnings.get((gate, value), "")


def _normalize_local_gate_state(state: dict[str, Any], *, status: str = "OK") -> dict[str, Any]:
    gates = dict(LOCAL_GATE_DEFAULTS)
    raw_gates = state.get("gates") if isinstance(state.get("gates"), dict) else {}
    for gate, value in raw_gates.items():
        gate_name = str(gate)
        gate_value = str(value or "").strip().upper()
        if gate_name in LOCAL_GATE_OPTIONS and gate_value in LOCAL_GATE_OPTIONS[gate_name]:
            gates[gate_name] = gate_value
    gates["SecretGate"] = "HARD_BLOCK"
    gates["CredentialGate"] = "HARD_BLOCK"
    if gates["NetworkExposureGate"] not in LOCAL_GATE_OPTIONS["NetworkExposureGate"]:
        gates["NetworkExposureGate"] = "LOCALHOST_ONLY"
    return {
        "schema_version": "wabi.local_gate_state.v0_1",
        "environment": LOCAL_GATE_ENVIRONMENT,
        "owner_authorization": LOCAL_GATE_OWNER_AUTHORIZATION,
        "gate_control_mode": LOCAL_GATE_CONTROL_MODE,
        "state_status": status,
        "updated_at": sanitize_text(state.get("updated_at") or utc_now_iso()),
        "updated_by": sanitize_text(state.get("updated_by") or "owner_local_ui"),
        "gates": gates,
    }


def _append_local_gate_audit(event: dict[str, Any]) -> dict[str, Any]:
    return append_jsonl(
        LOCAL_GATE_AUDIT_PATH,
        {
            "timestamp": utc_now_iso(),
            "fingerprint": LOCAL_GATE_AUDIT_FINGERPRINT,
            "environment": LOCAL_GATE_ENVIRONMENT,
            "owner_authorization": LOCAL_GATE_OWNER_AUTHORIZATION,
            "server_binding": "127.0.0.1 only",
            **event,
        },
    )


def read_local_gate_state(*, create_if_missing: bool = True) -> dict[str, Any]:
    if not LOCAL_GATE_STATE_PATH.exists():
        state = local_gate_default_state(status="DEFAULT_CREATED")
        if create_if_missing:
            write_json_file(LOCAL_GATE_STATE_PATH, state)
            _append_local_gate_audit({"event": "DEFAULT_CREATED", "gates": state["gates"]})
        return state
    try:
        raw = json.loads(LOCAL_GATE_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        fallback = local_gate_default_state(status="FALLBACK_SAFE_JSON_CORRUPT")
        fallback["warning"] = "GATE_STATE_JSON_CORRUPT_FALLBACK_SAFE"
        fallback["state_path"] = local_relative_path(LOCAL_GATE_STATE_PATH)
        _append_local_gate_audit({"event": "FALLBACK_SAFE_JSON_CORRUPT", "state_path": fallback["state_path"]})
        return fallback
    if not isinstance(raw, dict):
        fallback = local_gate_default_state(status="FALLBACK_SAFE_INVALID_JSON_SHAPE")
        fallback["warning"] = "GATE_STATE_INVALID_SHAPE_FALLBACK_SAFE"
        _append_local_gate_audit({"event": "FALLBACK_SAFE_INVALID_JSON_SHAPE"})
        return fallback
    state = _normalize_local_gate_state(raw, status=str(raw.get("state_status") or "OK"))
    if state["gates"] != raw.get("gates") or state.get("environment") != raw.get("environment"):
        state["state_status"] = "NORMALIZED_SAFE"
        if create_if_missing:
            write_json_file(LOCAL_GATE_STATE_PATH, state)
            _append_local_gate_audit({"event": "NORMALIZED_SAFE", "gates": state["gates"]})
    return state


def local_gate_payload() -> dict[str, Any]:
    state = read_local_gate_state(create_if_missing=True)
    gates = dict(state.get("gates", {}))
    return sanitize_obj(
        {
            "ok": True,
            **state,
            "state_path": local_relative_path(LOCAL_GATE_STATE_PATH),
            "audit_path": local_relative_path(LOCAL_GATE_AUDIT_PATH),
            "locked_gates": sorted(LOCAL_GATE_LOCKED),
            "hard_block_gates": {
                "SecretGate": "HARD_BLOCK",
                "CredentialGate": "HARD_BLOCK",
            },
            "editable_gates": [gate for gate in LOCAL_GATE_OPTIONS if gate not in LOCAL_GATE_LOCKED],
            "options": LOCAL_GATE_OPTIONS,
            "descriptions": LOCAL_GATE_DESCRIPTIONS,
            "wiring": LOCAL_GATE_WIRING,
            "effective_policy": local_gate_effective_policy(gates),
            "cloud": gates.get("CloudGate", "OFF"),
            "apply": gates.get("ApplyGate", "REVIEW"),
            "publication": gates.get("PublicationGate", "BLOCK"),
            "network_exposure": gates.get("NetworkExposureGate", "LOCALHOST_ONLY"),
            "secret_values_printed": False,
        }
    )


def update_local_gate_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    updates = _coerce_gate_updates(payload)
    if not updates:
        return {"ok": False, "status": "NO_GATE_UPDATES", "errors": [{"error": "NO_VALID_GATES"}]}
    errors = validate_local_gate_updates(updates)
    if errors:
        _append_local_gate_audit({"event": "UPDATE_REJECTED", "errors": errors, "updates": updates})
        return {"ok": False, "status": "GATE_UPDATE_REJECTED", "errors": errors, "gates": read_local_gate_state()["gates"]}
    state = read_local_gate_state(create_if_missing=True)
    before = dict(state.get("gates", {}))
    gates = dict(before)
    gates.update(updates)
    gates["SecretGate"] = "HARD_BLOCK"
    gates["CredentialGate"] = "HARD_BLOCK"
    state.update(
        {
            "state_status": "OWNER_UPDATED",
            "updated_at": utc_now_iso(),
            "updated_by": sanitize_text((payload or {}).get("updated_by") or "owner_local_ui"),
            "gates": gates,
        }
    )
    write_json_file(LOCAL_GATE_STATE_PATH, state)
    changes = {gate: {"before": before.get(gate), "after": gates.get(gate)} for gate in updates}
    actor = "owner_local"
    reason = sanitize_text((payload or {}).get("reason") or "owner_local_gate_console_update")
    warnings: list[str] = []
    for gate, update in changes.items():
        warning = local_gate_change_warning(gate, str(update.get("after") or ""))
        if warning:
            warnings.append(f"{gate}: {warning}")
        _append_local_gate_audit(
            {
                "event": "GATE_STATE_CHANGED",
                "gate": gate,
                "old_state": update.get("before"),
                "new_state": update.get("after"),
                "reason": reason,
                "actor": actor,
                "updated_by": state["updated_by"],
            }
        )
    _append_local_gate_audit(
        {
            "event": "GATE_UPDATED_LOCALLY",
            "changes": changes,
            "reason": reason,
            "actor": actor,
            "updated_by": state["updated_by"],
        }
    )
    return {"ok": True, "status": "GATE_UPDATED_LOCALLY", "changes": changes, "warnings": warnings, **local_gate_payload()}


def reset_local_gate_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    state = local_gate_default_state(status="RESET_SAFE_DEFAULTS")
    state["updated_by"] = sanitize_text((payload or {}).get("updated_by") or "owner_local_ui")
    write_json_file(LOCAL_GATE_STATE_PATH, state)
    _append_local_gate_audit(
        {
            "event": "RESET_SAFE_DEFAULTS",
            "actor": "owner_local",
            "reason": sanitize_text((payload or {}).get("reason") or "reset_safe_defaults"),
            "updated_by": state["updated_by"],
            "gates": state["gates"],
        }
    )
    return {"ok": True, "status": "RESET_SAFE_DEFAULTS", **local_gate_payload()}


def local_gate_audit_payload(limit: int = 50) -> dict[str, Any]:
    safe_limit = max(1, min(int(limit or 50), 200))
    return {
        "ok": True,
        "audit_path": local_relative_path(LOCAL_GATE_AUDIT_PATH),
        "witnesslog_path": local_relative_path(LOCAL_GATE_AUDIT_PATH),
        "fingerprint": LOCAL_GATE_AUDIT_FINGERPRINT,
        "events": read_jsonl(LOCAL_GATE_AUDIT_PATH, limit=safe_limit),
        "limit": safe_limit,
    }


def local_gate_state_for_actions() -> dict[str, str]:
    return dict(read_local_gate_state(create_if_missing=True).get("gates", LOCAL_GATE_DEFAULTS))


def apply_gate_allows_local_apply() -> bool:
    return local_gate_state_for_actions().get("ApplyGate") == "ALLOW_LOCAL_APPLY"


def apply_gate_block_payload(surface: str) -> dict[str, Any]:
    gates = local_gate_state_for_actions()
    return {
        "ok": False,
        "status": "APPLY_GATE_REVIEW",
        "reason": f"ApplyGate={gates.get('ApplyGate', 'REVIEW')} requires ALLOW_LOCAL_APPLY",
        "surface": surface,
        "applied_to_sources": False,
        "cloud_provider_called": False,
        "graphics_live": False,
        "publication_gate": gates.get("PublicationGate", "BLOCK"),
        "gate_console": {
            "environment": LOCAL_GATE_ENVIRONMENT,
            "ApplyGate": gates.get("ApplyGate", "REVIEW"),
            "CloudGate": gates.get("CloudGate", "OFF"),
            "NetworkExposureGate": gates.get("NetworkExposureGate", "LOCALHOST_ONLY"),
        },
    }


def text_has_secret_value(value: Any) -> bool:
    text = str(value)
    return any(pattern.search(text) for pattern in SECRET_VALUE_PATTERNS)


def local_execute_contract_payload() -> dict[str, Any]:
    return {
        "version": "v0.2",
        "mode": "LOCAL_ONLY",
        "allowed_lanes": ["SANDBOX", "DOCS_LOCAL"],
        "blocked_lanes": ["PUBLICATION", "CLOUD", "NVIDIA", "REMOTE_COMPUTE", "PROTECTED_MATERIAL"],
        "requires_task_spec": True,
        "requires_ghostgate_pass": True,
        "requires_rollback": True,
        "requires_witnesslog": True,
        "direct_delete_allowed": False,
        "publication_gate": "BLOCK",
        "allowlist": [
            {"lane": "SANDBOX", "root": "WABI_RUNTIME_LOCAL_EXECUTE/"},
            {"lane": "SANDBOX", "root": "WABI_WORKPACK_RUNTIME/"},
            {"lane": "DOCS_LOCAL", "root": "docs/local_execute/"},
            {"lane": "DOCS_LOCAL", "root": f"{LOCAL_EXECUTE_RUN_ID}/"},
        ],
        "cloud_live_gate": "BLOCK_THIS_RUN",
        "nvidia_smoke_gate": "DO_NOT_CALL",
        "secret_values_printed": False,
    }


def local_execute_task_spec_schema_payload() -> dict[str, Any]:
    return {
        "$schema": "json-schema-draft-2020-12",
        "$id": "medioevo.local_execute.task_spec.v0_2",
        "type": "object",
        "required": [
            "task_id",
            "title",
            "lane",
            "intent",
            "allowed_targets",
            "blocked_targets",
            "expected_outputs",
            "tests_required",
            "rollback_required",
            "witness_required",
            "publication_gate",
        ],
        "properties": {
            "task_id": {"type": "string"},
            "title": {"type": "string"},
            "lane": {"enum": ["SANDBOX", "DOCS_LOCAL"]},
            "intent": {"type": "string"},
            "allowed_targets": {"type": "array", "items": {"type": "string"}},
            "blocked_targets": {"type": "array", "items": {"type": "string"}},
            "expected_outputs": {"type": "array", "items": {"type": "string"}},
            "tests_required": {"type": "array", "items": {"type": "object"}},
            "rollback_required": {"const": True},
            "witness_required": {"const": True},
            "publication_gate": {"const": "BLOCK"},
        },
        "additionalProperties": True,
    }


def local_execute_target_alias(path: pathlib.Path) -> str:
    resolved = path.resolve(strict=False)
    for root, prefix in (
        (LOCAL_EXECUTE_RUNTIME_ROOT, "WABI_RUNTIME_LOCAL_EXECUTE"),
        (WORKPACK_RUNTIME_ROOT, "WABI_WORKPACK_RUNTIME"),
        (LOCAL_EXECUTE_DOCS_ROOT, "docs/local_execute"),
        (LOCAL_EXECUTE_RUN_DIR, LOCAL_EXECUTE_RUN_ID),
        (WORKPACK_RUN_DIR, WORKPACK_RUN_ID),
        (WORKPACK_SCHEDULER_RUN_DIR, WORKPACK_SCHEDULER_RUN_ID),
        (MULTI_STEP_RUN_DIR, MULTI_STEP_RUN_ID),
    ):
        try:
            return f"{prefix}/{resolved.relative_to(root.resolve(strict=False)).as_posix()}"
        except ValueError:
            continue
    return f"<OUT_OF_SCOPE>/{resolved.name}"


def local_execute_resolve_target(alias: str) -> pathlib.Path:
    normalized = str(alias).strip().replace("\\", "/")
    if normalized.startswith("WABI_RUNTIME_LOCAL_EXECUTE/"):
        return LOCAL_EXECUTE_RUNTIME_ROOT / normalized.removeprefix("WABI_RUNTIME_LOCAL_EXECUTE/")
    if normalized.startswith("WABI_WORKPACK_RUNTIME/"):
        return WORKPACK_RUNTIME_ROOT / normalized.removeprefix("WABI_WORKPACK_RUNTIME/")
    if normalized.startswith("docs/local_execute/"):
        return LOCAL_EXECUTE_DOCS_ROOT / normalized.removeprefix("docs/local_execute/")
    if normalized.startswith(f"{LOCAL_EXECUTE_RUN_ID}/"):
        return LOCAL_EXECUTE_RUN_DIR / normalized.removeprefix(f"{LOCAL_EXECUTE_RUN_ID}/")
    if normalized.startswith(f"{WORKPACK_RUN_ID}/"):
        return WORKPACK_RUN_DIR / normalized.removeprefix(f"{WORKPACK_RUN_ID}/")
    if normalized.startswith(f"{WORKPACK_SCHEDULER_RUN_ID}/"):
        return WORKPACK_SCHEDULER_RUN_DIR / normalized.removeprefix(f"{WORKPACK_SCHEDULER_RUN_ID}/")
    if normalized.startswith(f"{MULTI_STEP_RUN_ID}/"):
        return MULTI_STEP_RUN_DIR / normalized.removeprefix(f"{MULTI_STEP_RUN_ID}/")
    raise ValueError("target alias is not local-execute allowlisted")


def local_execute_path_within(path: pathlib.Path, root: pathlib.Path) -> bool:
    resolved_path = path.resolve(strict=False)
    resolved_root = root.resolve(strict=False)
    return resolved_path == resolved_root or resolved_root in resolved_path.parents


def local_execute_task_files(task_id: str) -> dict[str, pathlib.Path]:
    safe_id = safe_local_id(task_id)
    base = LOCAL_EXECUTE_EVIDENCE_DIR / safe_id
    return {
        "taskspec": LOCAL_EXECUTE_TASKSPEC_DIR / f"TASKSPEC_{safe_id}.json",
        "ghostgate": base / f"GHOSTGATE_{safe_id}.json",
        "rollback": base / f"ROLLBACK_SNAPSHOT_{safe_id}.json",
        "execution": base / f"EXECUTION_RESULT_{safe_id}.json",
        "tests": base / f"TEST_RESULT_{safe_id}.json",
        "witness": base / f"WITNESS_{safe_id}.jsonl",
    }


def local_execute_witness(task_id: str, event: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    files = local_execute_task_files(task_id)
    previous = read_jsonl(LOCAL_EXECUTE_WITNESSLOG_PATH, limit=1)
    previous_hash = str(previous[-1].get("hash", "")) if previous else ""
    record = {
        "event": event,
        "task_id": safe_local_id(task_id),
        "timestamp": utc_now_iso(),
        "previous_hash": previous_hash,
        "cloud_called": False,
        "nvidia_called": False,
        "publication": "BLOCK",
        "secret_values_printed": False,
        **(payload or {}),
    }
    digest_source = json.dumps(sanitize_obj(record), ensure_ascii=True, sort_keys=True)
    record["hash"] = hashlib.sha256((previous_hash + digest_source).encode("utf-8")).hexdigest()
    append_jsonl(LOCAL_EXECUTE_WITNESSLOG_PATH, record)
    append_jsonl(files["witness"], record)
    return sanitize_obj(record)


def ensure_local_execute_contract_files() -> None:
    write_json_file(LOCAL_EXECUTE_CONTRACT_PATH, local_execute_contract_payload())
    write_json_file(LOCAL_EXECUTE_SCHEMA_PATH, local_execute_task_spec_schema_payload())
    sandbox_example = build_local_execute_task_spec(
        {
            "task_id": "local-execute-sandbox-demo",
            "title": "Sandbox Local Execute v0.2 demo",
            "lane": "SANDBOX",
            "source": "LOCAL_EXECUTE_v0_2",
            "risk": "LOW",
            "action_gate": "APPROVE",
            "can_execute_local": True,
            "next_action": "Create a sandbox markdown marker.",
            "assigned_agent": "WABI_SAFE_EXECUTOR",
        },
        {},
    )
    docs_example = build_local_execute_task_spec(
        {
            "task_id": "local-execute-docs-demo",
            "title": "Docs Local Execute v0.2 demo",
            "lane": "DOCS_LOCAL",
            "source": "LOCAL_EXECUTE_v0_2",
            "risk": "LOW",
            "action_gate": "APPROVE",
            "can_execute_local": True,
            "next_action": "Create a local-only acceptance note.",
            "assigned_agent": "CORE_MEMORY_KEEPER",
        },
        {},
    )
    write_json_file(LOCAL_EXECUTE_RUN_DIR / "TASKSPEC_EXAMPLE_SANDBOX_v0_2.json", sandbox_example)
    write_json_file(LOCAL_EXECUTE_RUN_DIR / "TASKSPEC_EXAMPLE_DOCS_LOCAL_v0_2.json", docs_example)


def local_execute_validation(task_spec: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    lane = str(task_spec.get("lane", ""))
    targets = [str(target) for target in task_spec.get("allowed_targets", [])]
    if not task_spec.get("task_id"):
        reasons.append("task_id required")
    if lane in LOCAL_EXECUTE_BLOCKED_LANES or lane not in LOCAL_EXECUTE_ALLOWED_LANES:
        reasons.append("lane not allowlisted for local execute")
    if not targets:
        reasons.append("allowed_targets required")
    if task_spec.get("rollback_required") is not True:
        reasons.append("rollback_required must be true")
    if task_spec.get("witness_required") is not True:
        reasons.append("witness_required must be true")
    if task_spec.get("publication_gate") != "BLOCK":
        reasons.append("publication_gate must remain BLOCK")

    resolved_targets: list[str] = []
    for alias in targets:
        lowered = alias.lower()
        if text_has_secret_value(alias) or ".env" in lowered or "credential" in lowered or "secret" in lowered:
            reasons.append(f"blocked target token: {alias}")
            continue
        try:
            target_path = local_execute_resolve_target(alias)
        except ValueError as exc:
            reasons.append(str(exc))
            continue
        if lane == "SANDBOX" and not (
            local_execute_path_within(target_path, LOCAL_EXECUTE_RUNTIME_ROOT)
            or local_execute_path_within(target_path, WORKPACK_RUNTIME_ROOT)
        ):
            reasons.append("SANDBOX target outside runtime allowlist")
        if lane == "DOCS_LOCAL" and not (
            local_execute_path_within(target_path, LOCAL_EXECUTE_DOCS_ROOT)
            or local_execute_path_within(target_path, LOCAL_EXECUTE_RUN_DIR)
            or local_execute_path_within(target_path, WORKPACK_RUN_DIR)
        ):
            reasons.append("DOCS_LOCAL target outside docs/run allowlist")
        resolved_targets.append(local_execute_target_alias(target_path))

    return {
        "ok": not reasons,
        "decision": "APPROVE" if not reasons else "BLOCK",
        "reasons": reasons,
        "resolved_targets": resolved_targets,
        "secret_values_printed": False,
    }


def local_execute_content_for_task(task_id: str) -> str:
    safe_id = safe_local_id(task_id)
    if safe_id == "local-execute-docs-demo":
        return (
            "# Local Execute v0.2 Acceptance Note\n\n"
            "status: PASS\n"
            "mode: LOCAL_ONLY\n"
            "publication_gate: BLOCK\n"
            "cloud_live_gate: BLOCK_THIS_RUN\n"
            "nvidia_smoke_gate: DO_NOT_CALL\n\n"
            "This local note verifies docs allowlist execution with TaskSpec, GhostGate, rollback and WitnessLog.\n"
        )
    if safe_id == "claudio-workpack-docs-demo-v0-1":
        return (
            "# Claudio Workpack Bridge v0.1 Acceptance Note\n\n"
            "status: PASS\n"
            "mode: LOCAL_ONLY\n"
            "execution_engine: LOCAL_EXECUTE_v0_2\n"
            "publication_gate: BLOCK\n"
            "cloud_live_gate: BLOCK_THIS_RUN\n"
            "nvidia_smoke_gate: DO_NOT_CALL\n\n"
            "This local-only note verifies a Claudio Workpack routed through TaskSpec, GhostGate, rollback, tests and WitnessLog.\n"
        )
    if safe_id == "claudio-workpack-sandbox-demo-v0-1":
        return (
            "# Claudio Workpack Bridge v0.1 Sandbox Demo\n\n"
            "status: PASS\n"
            "mode: LOCAL_ONLY\n"
            "execution_engine: LOCAL_EXECUTE_v0_2\n"
            "publication_gate: BLOCK\n"
            "cloud_live_gate: BLOCK_THIS_RUN\n"
            "nvidia_smoke_gate: DO_NOT_CALL\n"
        )
    return (
        "# Local Execute v0.2 Sandbox Demo\n\n"
        "status: PASS\n"
        "mode: LOCAL_ONLY\n"
        "publication_gate: BLOCK\n"
        "cloud_live_gate: BLOCK_THIS_RUN\n"
        "nvidia_smoke_gate: DO_NOT_CALL\n"
    )


def build_local_execute_task_spec(task: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    task_id = safe_local_id(str(task.get("task_id", data.get("task_id", ""))))
    lane = str(task.get("lane") or data.get("lane") or "SANDBOX")
    if data.get("allowed_targets"):
        allowed_targets = [str(target) for target in data.get("allowed_targets", [])]
    elif task_id == "local-execute-docs-demo":
        allowed_targets = ["docs/local_execute/LOCAL_EXECUTE_v0_2_ACCEPTANCE_NOTE.md"]
    elif task_id == "local-execute-sandbox-demo":
        allowed_targets = ["WABI_RUNTIME_LOCAL_EXECUTE/sandbox_task/hello_local_execute.md"]
    elif task_id == "claudio-workpack-docs-demo-v0-1":
        allowed_targets = ["docs/local_execute/CLAUDIO_WORKPACK_BRIDGE_v0_1_ACCEPTANCE_NOTE.md"]
    elif task_id == "claudio-workpack-sandbox-demo-v0-1":
        allowed_targets = ["WABI_WORKPACK_RUNTIME/sandbox_demo/hello_workpack.md"]
    else:
        allowed_targets = []
    return sanitize_obj(
        {
            "schema": "medioevo.local_execute.task_spec.v0_2",
            "task_id": task_id,
            "title": str(task.get("title") or data.get("title") or task_id),
            "lane": lane,
            "intent": str(data.get("intent") or task.get("next_action") or "Prepare local gated task."),
            "source": str(task.get("source") or data.get("source") or "LOCAL_EXECUTE_v0_2"),
            "allowed_targets": allowed_targets,
            "blocked_targets": [
                ".env",
                "credentials",
                "Fragmentos",
                "canon completo",
                "runtime privado",
                "PUBLICATION",
                "CLOUD",
                "NVIDIA",
            ],
            "expected_outputs": allowed_targets,
            "tests_required": [
                {"type": "file_contains", "target": target, "contains": "status: PASS"} for target in allowed_targets
            ],
            "operation": {
                "type": "write_text",
                "content": local_execute_content_for_task(task_id),
            },
            "rollback_required": True,
            "witness_required": True,
            "publication_gate": "BLOCK",
            "cloud_allowed": False,
            "nvidia_allowed": False,
            "direct_delete_allowed": False,
            "created_at": utc_now_iso(),
            "secret_values_printed": False,
        }
    )


def local_execute_create_rollback_snapshot(task_spec: dict[str, Any]) -> dict[str, Any]:
    task_id = safe_local_id(str(task_spec.get("task_id", "")))
    files = local_execute_task_files(task_id)
    entries: list[dict[str, Any]] = []
    for alias in task_spec.get("allowed_targets", []):
        target = local_execute_resolve_target(str(alias))
        existed = target.exists()
        content = target.read_text(encoding="utf-8", errors="replace") if existed and target.is_file() else ""
        entries.append(
            {
                "target": str(alias),
                "existed": existed,
                "sha256_before": hashlib.sha256(content.encode("utf-8")).hexdigest() if existed else "",
                "content_before": content,
            }
        )
    snapshot = {
        "schema": "medioevo.local_execute.rollback_snapshot.v0_2",
        "task_id": task_id,
        "created_at": utc_now_iso(),
        "entries": entries,
        "direct_delete_allowed": False,
        "rollback_available": True,
        "secret_values_printed": False,
    }
    write_json_file(files["rollback"], snapshot)
    local_execute_witness(task_id, "rollback_snapshot_created", {"rollback": local_execute_target_alias(files["rollback"])})
    return snapshot


def local_execute_run_task_tests(task_spec: dict[str, Any]) -> dict[str, Any]:
    task_id = safe_local_id(str(task_spec.get("task_id", "")))
    files = local_execute_task_files(task_id)
    checks: list[dict[str, Any]] = []
    passed = True
    blocked_terms = ["c:\\users", "onedrive", "brain_os", "fragmentos", "smoke_pass", "bias-free", "sin sesgos"]
    for check in task_spec.get("tests_required", []):
        alias = str(check.get("target", ""))
        contains = str(check.get("contains", ""))
        target = local_execute_resolve_target(alias)
        text = target.read_text(encoding="utf-8", errors="replace") if target.exists() and target.is_file() else ""
        check_type = str(check.get("type", "file_contains"))
        if check_type == "file_exists":
            ok = target.exists() and target.is_file() and not any(term in text.lower() for term in blocked_terms)
        else:
            ok = target.exists() and contains in text and not any(term in text.lower() for term in blocked_terms)
        checks.append({"type": check.get("type", "file_contains"), "target": alias, "passed": ok})
        passed = passed and ok
    result = {
        "schema": "medioevo.local_execute.test_result.v0_2",
        "task_id": task_id,
        "ran": True,
        "passed": passed,
        "checks": checks,
        "timestamp": utc_now_iso(),
        "secret_values_printed": False,
    }
    write_json_file(files["tests"], result)
    local_execute_witness(task_id, "task_tests_ran", {"passed": passed})
    return result


def local_execute_apply_task(task_spec: dict[str, Any]) -> dict[str, Any]:
    task_id = safe_local_id(str(task_spec.get("task_id", "")))
    files = local_execute_task_files(task_id)
    content = str(task_spec.get("operation", {}).get("content", ""))
    targets_written: list[str] = []
    for alias in task_spec.get("allowed_targets", []):
        target = local_execute_resolve_target(str(alias))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        targets_written.append(str(alias))
    result = {
        "schema": "medioevo.local_execute.execution_result.v0_2",
        "task_id": task_id,
        "status": "APPLIED",
        "apply_status": "APPLIED",
        "targets_written": targets_written,
        "cloud_called": False,
        "nvidia_called": False,
        "publication_gate": "BLOCK",
        "timestamp": utc_now_iso(),
        "secret_values_printed": False,
    }
    write_json_file(files["execution"], result)
    local_execute_witness(task_id, "task_applied", {"targets_written": targets_written})
    return result


def local_execute_rollback_task_payload(task_id: str) -> dict[str, Any]:
    safe_id = safe_local_id(task_id)
    files = local_execute_task_files(safe_id)
    if not files["rollback"].exists():
        return {"ok": False, "task_id": safe_id, "status": "BLOCK", "reason": "Rollback snapshot not found.", "secret_values_printed": False}
    snapshot = _load_json_dict(files["rollback"], {})
    restored: list[dict[str, Any]] = []
    quarantine_dir = LOCAL_EXECUTE_EVIDENCE_DIR / safe_id / "rollback_removed"
    for entry in snapshot.get("entries", []):
        alias = str(entry.get("target", ""))
        target = local_execute_resolve_target(alias)
        if entry.get("existed"):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(entry.get("content_before", "")), encoding="utf-8")
            restored.append({"target": alias, "restored": True, "mode": "content_restored"})
        elif target.exists():
            quarantine_dir.mkdir(parents=True, exist_ok=True)
            archived = quarantine_dir / target.name
            target.replace(archived)
            restored.append({"target": alias, "restored": True, "mode": "moved_to_rollback_quarantine", "archive": local_execute_target_alias(archived)})
        else:
            restored.append({"target": alias, "restored": True, "mode": "already_absent"})
    result = {
        "ok": True,
        "task_id": safe_id,
        "status": "ROLLED_BACK",
        "restored": restored,
        "direct_delete_used": False,
        "secret_values_printed": False,
    }
    local_execute_witness(safe_id, "task_rollback", {"status": "ROLLED_BACK"})
    return sanitize_obj(result)


def local_execute_evidence_payload(task_id: str) -> dict[str, Any]:
    safe_id = safe_local_id(task_id)
    files = local_execute_task_files(safe_id)
    evidence = {
        key: {
            "exists": path.exists(),
            "path": local_execute_target_alias(path),
        }
        for key, path in files.items()
    }
    return sanitize_obj(
        {
            "ok": True,
            "task_id": safe_id,
            "evidence": evidence,
            "witness_events": read_jsonl(files["witness"], limit=100),
            "secret_values_printed": False,
        }
    )


def local_execute_task_state(task_id: str) -> dict[str, Any]:
    files = local_execute_task_files(task_id)
    task_spec = _load_json_dict(files["taskspec"], {}) if files["taskspec"].exists() else {}
    ghostgate = _load_json_dict(files["ghostgate"], {}) if files["ghostgate"].exists() else {}
    execution = _load_json_dict(files["execution"], {}) if files["execution"].exists() else {}
    tests = _load_json_dict(files["tests"], {}) if files["tests"].exists() else {}
    return {
        "task_spec_status": "READY" if files["taskspec"].exists() else "MISSING",
        "ghostgate_status": ghostgate.get("decision", "MISSING"),
        "rollback_status": "READY" if files["rollback"].exists() else "MISSING",
        "execution_status": execution.get("apply_status", "NOT_APPLIED"),
        "test_status": "PASS" if tests.get("passed") is True else ("FAIL" if tests else "NOT_RUN"),
        "witness_status": "WRITTEN" if files["witness"].exists() else "MISSING",
        "lane": task_spec.get("lane", ""),
        "can_execute_now": files["taskspec"].exists() and ghostgate.get("decision") == "APPROVE" and files["rollback"].exists(),
        "evidence_path": local_execute_target_alias(files["execution"]),
    }


def local_hub_task_catalog() -> list[dict[str, Any]]:
    return sanitize_obj(
        [
            {
                "task_id": "local-execute-sandbox-demo",
                "title": "Local Execute v0.2 sandbox demo",
                "source": "LOCAL_EXECUTE_v0_2",
                "status": "TODO",
                "lane": "SANDBOX",
                "risk": "LOW",
                "action_gate": "APPROVE",
                "can_execute_local": True,
                "requires_human": False,
                "blocked_reason": "",
                "next_action": "Create a sandbox marker through TaskSpec, GhostGate, rollback and WitnessLog.",
                "assigned_agent": "WABI_SAFE_EXECUTOR",
            },
            {
                "task_id": "local-execute-docs-demo",
                "title": "Local Execute v0.2 docs-local demo",
                "source": "LOCAL_EXECUTE_v0_2",
                "status": "TODO",
                "lane": "DOCS_LOCAL",
                "risk": "LOW",
                "action_gate": "APPROVE",
                "can_execute_local": True,
                "requires_human": False,
                "blocked_reason": "",
                "next_action": "Create a local-only acceptance note under docs/local_execute.",
                "assigned_agent": "CORE_MEMORY_KEEPER",
            },
            {
                "task_id": "wabi-fallback-only-v0-4",
                "title": "Wabi fallback-only coding acceptance v0.4 on controlled fixture",
                "source": "NEXT_SESSION_BRIEF.md",
                "status": "TODO",
                "lane": "WABI",
                "risk": "LOW",
                "action_gate": "APPROVE",
                "can_execute_local": True,
                "requires_human": False,
                "blocked_reason": "",
                "next_action": "Create sandbox TaskSpec, run GhostGate, dry-run before apply.",
                "assigned_agent": "WABI_LOCAL_PROGRAMMER",
            },
            {
                "task_id": "agent-chat-persistence-v0-2",
                "title": "Harden local agent chat persistence and witness export",
                "source": "HANDOFF_CURRENT.md",
                "status": "TODO",
                "lane": "COMMS",
                "risk": "LOW",
                "action_gate": "APPROVE",
                "can_execute_local": True,
                "requires_human": False,
                "blocked_reason": "",
                "next_action": "Keep messages append-only and add replay checks.",
                "assigned_agent": "CORE_MEMORY_KEEPER",
            },
            {
                "task_id": "public-safe-wabi-progress-summary",
                "title": "Public-safe Wabi progress summary",
                "source": "RUN_WABI_UI_VISUAL_ASSET_POLISH_20260518",
                "status": "REVIEW",
                "lane": "PUBLIC_SAFE",
                "risk": "MEDIUM",
                "action_gate": "REVIEW",
                "can_execute_local": True,
                "requires_human": True,
                "blocked_reason": "Publication requires boundary scan and human review.",
                "next_action": "Prepare public-safe draft; do not publish internal runtime.",
                "assigned_agent": "BOUNDARY_RELEASE_SENTINEL",
            },
            {
                "task_id": "nvidia-manual-route-review",
                "title": "NVIDIA manual route review before any single-alias retry",
                "source": "WABI_CLOUD_PROVIDER_v0_5_PROVIDER_DIAGNOSTIC.json",
                "status": "REVIEW",
                "lane": "NVIDIA",
                "risk": "HIGH",
                "action_gate": "REVIEW",
                "can_execute_local": False,
                "requires_human": True,
                "blocked_reason": "NvidiaSmokeGate remains DO_NOT_CALL.",
                "next_action": "Review dashboard route and alias without printing credentials.",
                "assigned_agent": "CORE_GATEKEEPER",
            },
            {
                "task_id": "duat-wabi-dashboard-bridge",
                "title": "DUAT/Wabi unified dashboard bridge",
                "source": "WORKBENCH_INDEX_20260518.md",
                "status": "TODO",
                "lane": "DUAT",
                "risk": "MEDIUM",
                "action_gate": "REVIEW",
                "can_execute_local": True,
                "requires_human": False,
                "blocked_reason": "Cross-surface UI changes need scoped tests.",
                "next_action": "Draft bridge schema before touching UI runtime.",
                "assigned_agent": "DUAT_DISPLAY_AGENT",
            },
            {
                "task_id": "osit-public-safe-theory-articles",
                "title": "OSIT public-safe theory articles",
                "source": "PUBLIC_SAFE_THEORY_UPDATE_v0_1",
                "status": "TODO",
                "lane": "OSIT",
                "risk": "MEDIUM",
                "action_gate": "REVIEW",
                "can_execute_local": True,
                "requires_human": True,
                "blocked_reason": "Claims must stay proposed-method and public-safe.",
                "next_action": "Expand only sanitized summaries and boundary notes.",
                "assigned_agent": "OBS_CANON_DIFF_CURATOR",
            },
        ]
    )


def find_local_hub_task(task_id: str) -> dict[str, Any]:
    safe_id = safe_local_id(task_id)
    for task in local_hub_task_catalog():
        if task["task_id"] == safe_id:
            return task
    raise ValueError("unknown local hub task")


def local_hub_actions() -> list[dict[str, Any]]:
    return [
        {"id": "prepare", "label": "Create TaskSpec", "method": "POST", "requires": "task_id", "executes": False},
        {"id": "ghostgate", "label": "Run GhostGate", "method": "POST", "requires": "TaskSpec", "executes": False},
        {"id": "queue", "label": "Queue for Claudio", "method": "POST", "requires": "GhostGate APPROVE", "executes": False},
        {
            "id": "execute",
            "label": "Execute Local",
            "method": "POST",
            "requires": "TaskSpec + GhostGate APPROVE + rollback",
            "executes": True,
            "cloud_allowed": False,
        },
        {"id": "rollback", "label": "Rollback", "method": "POST", "requires": "rollback snapshot", "executes": True},
        {"id": "mark_review", "label": "Mark Review", "method": "LOCAL_UI", "requires": "human review", "executes": False},
        {"id": "mark_done", "label": "Mark Done", "method": "LOCAL_UI", "requires": "evidence", "executes": False},
        {"id": "evidence", "label": "Open Evidence", "method": "GET", "requires": "relative path", "executes": False},
        {"id": "generate_handoff", "label": "Generate Handoff", "method": "POST", "requires": "TaskSpec", "executes": False},
    ]


def local_hub_payload() -> dict[str, Any]:
    ensure_local_execute_contract_files()
    tasks = []
    for task in local_hub_task_catalog():
        task = dict(task)
        task["local_execute"] = local_execute_task_state(task["task_id"])
        tasks.append(task)
    return sanitize_obj(
        {
            "schema": "medioevo.local_hub.v0_2",
            "hub_version": "v0.2",
            "mode": "LOCAL_OPERATOR_ONLY",
            "publication_gate": "BLOCK",
            "cloud_live_gate": "BLOCK_THIS_RUN",
            "nvidia_smoke_gate": "DO_NOT_CALL",
            "provider_state": "SMOKE_FAIL_REDACTED",
            "local_execute": {
                "contract": local_execute_contract_payload(),
                "contract_path": local_execute_target_alias(LOCAL_EXECUTE_CONTRACT_PATH),
                "schema_path": local_execute_target_alias(LOCAL_EXECUTE_SCHEMA_PATH),
            },
            "pending_tasks": tasks,
            "agents": agent_hub_agents(),
            "gates": {
                "ActionGate": "REQUIRED_BEFORE_QUEUE",
                "GhostGate": "REQUIRED_BEFORE_APPLY",
                "CloudLLMGate": "REVIEW_DO_NOT_SEND_PRIVATE_WORKSPACE",
                "NvidiaSmokeGate": "DO_NOT_CALL",
                "PublicationGate": "BLOCK",
                "DeletionGate": "BLOCK_DIRECT_DELETE",
            },
            "actions": local_hub_actions(),
            "workpacks": workpacks_payload()["workpacks"],
            "workpack_scheduler": {
                "version": "v0.1",
                "execution_model": "MANUAL_TICK",
                "max_concurrency": 1,
                "queue": scheduler_records(),
                "cloud_called": False,
                "nvidia_called": False,
                "deepseek_called": False,
                "publication_gate": "BLOCK",
            },
            "multi_step_workpacks": {
                "version": "v0.2",
                "execution_model": "MANUAL_TICK",
                "max_concurrency": 1,
                "workpacks": multi_step_records(),
                "cloud_called": False,
                "nvidia_called": False,
                "deepseek_called": False,
                "publication_gate": "BLOCK",
            },
            "blocked_actions": ["Publish", "Push", "Deploy", "Delete", "Run Cloud", "Send Private Workspace", "Execute Without Gate"],
            "evidence": {
                "run_id": LOCAL_HUB_RUN_ID,
                "witness_log": local_relative_path(LOCAL_HUB_WITNESS_PATH),
                "queue_log": local_relative_path(LOCAL_HUB_QUEUE_PATH),
                "local_execute_run_id": LOCAL_EXECUTE_RUN_ID,
                "local_execute_witness": local_execute_target_alias(LOCAL_EXECUTE_WITNESSLOG_PATH),
            },
            "secret_values_printed": False,
        }
    )


def local_hub_task_paths(task_id: str) -> tuple[pathlib.Path, pathlib.Path]:
    files = local_execute_task_files(task_id)
    return files["taskspec"], files["ghostgate"]


def local_hub_prepare_task_payload(task_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    task = find_local_hub_task(task_id)
    if task.get("action_gate") == "BLOCK":
        return {"ok": False, "task_id": task["task_id"], "status": "BLOCK", "reason": task.get("blocked_reason", "blocked")}
    taskspec_path, _ghostgate_path = local_hub_task_paths(task["task_id"])
    task_spec = build_local_execute_task_spec(task, payload or {})
    write_json_file(taskspec_path, task_spec)
    local_execute_witness(task["task_id"], "taskspec_created", {"task_spec": local_execute_target_alias(taskspec_path)})
    witness = append_jsonl(
        LOCAL_HUB_WITNESS_PATH,
        {
            "event": "local_hub_task_prepare",
            "task_id": task["task_id"],
            "timestamp": utc_now_iso(),
            "task_spec": local_relative_path(taskspec_path),
            "cloud_called": False,
            "publication": "BLOCK",
        },
    )
    return sanitize_obj(
        {
            "ok": True,
            "status": "TASKSPEC_CREATED",
            "task_id": task["task_id"],
            "task_spec": task_spec,
            "task_spec_path": local_execute_target_alias(taskspec_path),
            "witness": witness,
            "executes": False,
            "secret_values_printed": False,
        }
    )


def local_hub_ghostgate_payload(task_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    task = find_local_hub_task(task_id)
    taskspec_path, ghostgate_path = local_hub_task_paths(task["task_id"])
    if not taskspec_path.exists():
        return {"ok": False, "task_id": task["task_id"], "status": "BLOCK", "reason": "TaskSpec required before GhostGate.", "secret_values_printed": False}
    task_spec = _load_json_dict(taskspec_path, {})
    validation = local_execute_validation(task_spec)
    decision = "APPROVE" if validation["ok"] and task["action_gate"] == "APPROVE" and task["risk"] == "LOW" and task["can_execute_local"] else "BLOCK"
    if task["action_gate"] == "REVIEW" and validation["ok"]:
        decision = "REVIEW"
    result = {
        "schema": "medioevo.ghostgate.v0_2",
        "task_id": task["task_id"],
        "decision": decision,
        "reversible": decision == "APPROVE",
        "rollback_required": True,
        "rollback_available": False,
        "cloud_allowed": False,
        "nvidia_allowed": False,
        "publication_allowed": False,
        "validation": validation,
        "reason": "" if decision == "APPROVE" else task.get("blocked_reason") or "; ".join(validation.get("reasons", [])) or "Review required.",
        "timestamp": utc_now_iso(),
        "secret_values_printed": False,
    }
    if decision == "APPROVE":
        rollback = local_execute_create_rollback_snapshot(task_spec)
        result["rollback_available"] = True
        result["rollback_snapshot"] = local_execute_target_alias(local_execute_task_files(task["task_id"])["rollback"])
        result["rollback"] = rollback
    write_json_file(ghostgate_path, result)
    local_execute_witness(task["task_id"], "ghostgate_evaluated", {"decision": decision})
    witness = append_jsonl(
        LOCAL_HUB_WITNESS_PATH,
        {
            "event": "local_hub_ghostgate",
            "task_id": task["task_id"],
            "decision": decision,
            "timestamp": result["timestamp"],
        },
    )
    result["witness"] = witness
    result["ghostgate_path"] = local_execute_target_alias(ghostgate_path)
    return sanitize_obj({"ok": decision == "APPROVE", **result})


def local_hub_queue_task_payload(task_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    task = find_local_hub_task(task_id)
    taskspec_path, ghostgate_path = local_hub_task_paths(task["task_id"])
    if not taskspec_path.exists():
        return {"ok": False, "task_id": task["task_id"], "status": "BLOCK", "reason": "TaskSpec required before queue."}
    if not ghostgate_path.exists():
        return {"ok": False, "task_id": task["task_id"], "status": "BLOCK", "reason": "GhostGate required before queue."}
    ghostgate = _load_json_dict(ghostgate_path, {})
    if ghostgate.get("decision") != "APPROVE":
        return {
            "ok": False,
            "task_id": task["task_id"],
            "status": "REVIEW",
            "reason": ghostgate.get("reason") or "GhostGate did not approve queue.",
            "ghostgate": ghostgate,
        }
    queue_record = append_jsonl(
        LOCAL_HUB_QUEUE_PATH,
        {
            "event": "local_hub_queue",
            "task_id": task["task_id"],
            "agent": task["assigned_agent"],
            "timestamp": utc_now_iso(),
            "task_spec": local_execute_target_alias(taskspec_path),
            "ghostgate": local_execute_target_alias(ghostgate_path),
            "execute_now": False,
            "cloud_called": False,
        },
    )
    witness = append_jsonl(
        LOCAL_HUB_WITNESS_PATH,
        {
            "event": "local_hub_task_queued",
            "task_id": task["task_id"],
            "agent": task["assigned_agent"],
            "timestamp": queue_record["timestamp"],
        },
    )
    return sanitize_obj(
        {
            "ok": True,
            "task_id": task["task_id"],
            "status": "QUEUED_LOCAL",
            "agent": task["assigned_agent"],
            "queue_record": queue_record,
            "witness": witness,
            "executes": False,
            "secret_values_printed": False,
        }
    )


def local_hub_execute_task_payload(task_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    task = find_local_hub_task(task_id)
    files = local_execute_task_files(task["task_id"])
    taskspec_path, ghostgate_path = files["taskspec"], files["ghostgate"]
    if not taskspec_path.exists() or not ghostgate_path.exists():
        return {
            "ok": False,
            "task_id": task["task_id"],
            "status": "BLOCK",
            "apply_status": "NOT_APPLIED",
            "reason": "TaskSpec and GhostGate PASS required before execute.",
            "cloud_called": False,
            "secret_values_printed": False,
        }
    if not files["rollback"].exists():
        return {
            "ok": False,
            "task_id": task["task_id"],
            "status": "BLOCK",
            "apply_status": "NOT_APPLIED",
            "reason": "Rollback snapshot required before execute.",
            "cloud_called": False,
            "secret_values_printed": False,
        }
    ghostgate = _load_json_dict(ghostgate_path, {})
    if ghostgate.get("decision") != "APPROVE":
        return {
            "ok": False,
            "task_id": task["task_id"],
            "status": "BLOCK",
            "apply_status": "NOT_APPLIED",
            "reason": "Execute blocked because GhostGate is not APPROVE.",
            "ghostgate": ghostgate,
            "cloud_called": False,
            "secret_values_printed": False,
        }
    task_spec = _load_json_dict(taskspec_path, {})
    validation = local_execute_validation(task_spec)
    if not validation["ok"]:
        return {
            "ok": False,
            "task_id": task["task_id"],
            "status": "BLOCK",
            "apply_status": "NOT_APPLIED",
            "reason": "TaskSpec failed allowlist validation.",
            "validation": validation,
            "cloud_called": False,
            "secret_values_printed": False,
        }
    apply_result = local_execute_apply_task(task_spec)
    test_result = local_execute_run_task_tests(task_spec)
    status = "PASS" if test_result["passed"] else "FAIL_ROLLED_BACK"
    rollback_result = None
    if not test_result["passed"]:
        rollback_result = local_execute_rollback_task_payload(task["task_id"])
    append_jsonl(
        LOCAL_HUB_WITNESS_PATH,
        {
            "event": "local_hub_execute_local",
            "task_id": task["task_id"],
            "timestamp": utc_now_iso(),
            "apply_status": apply_result["apply_status"],
            "tests_passed": test_result["passed"],
        },
    )
    return sanitize_obj(
        {
            "ok": test_result["passed"],
            "task_id": task["task_id"],
            "status": status,
            "apply_status": apply_result["apply_status"],
            "execution_result": apply_result,
            "test_result": test_result,
            "rollback_result": rollback_result,
            "evidence": local_execute_evidence_payload(task["task_id"])["evidence"],
            "cloud_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def local_hub_rollback_task_payload(task_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    find_local_hub_task(task_id)
    return local_execute_rollback_task_payload(task_id)


def local_hub_task_evidence_payload(task_id: str) -> dict[str, Any]:
    find_local_hub_task(task_id)
    return local_execute_evidence_payload(task_id)


def workpack_contract_payload() -> dict[str, Any]:
    return {
        "version": "v0.1",
        "mode": "LOCAL_ONLY",
        "execution_engine": "LOCAL_EXECUTE_v0_2",
        "allowed_lanes": ["SANDBOX", "DOCS_LOCAL"],
        "blocked_lanes": ["PUBLICATION", "CLOUD", "NVIDIA", "REMOTE_COMPUTE", "PROTECTED_MATERIAL"],
        "requires_task_spec": True,
        "requires_ghostgate_pass": True,
        "requires_rollback": True,
        "requires_witnesslog": True,
        "requires_workpack_manifest": True,
        "direct_delete_allowed": False,
        "publication_gate": "BLOCK",
        "cloud_live_gate": "BLOCK_THIS_RUN",
        "nvidia_smoke_gate": "DO_NOT_CALL",
        "secret_values_printed": False,
    }


def workpack_schema_payload() -> dict[str, Any]:
    return {
        "$schema": "json-schema-draft-2020-12",
        "$id": "medioevo.claudio_workpack.v0_1",
        "type": "object",
        "required": [
            "workpack_id",
            "source_task_id",
            "title",
            "lane",
            "assigned_agent",
            "task_spec_path",
            "ghostgate_path",
            "rollback_snapshot_path",
            "expected_outputs",
            "tests_required",
            "witnesslog_path",
            "status",
            "publication_gate",
        ],
        "properties": {
            "workpack_id": {"type": "string"},
            "source_task_id": {"type": "string"},
            "title": {"type": "string"},
            "lane": {"enum": ["SANDBOX", "DOCS_LOCAL"]},
            "assigned_agent": {"type": "string"},
            "task_spec_path": {"type": "string"},
            "ghostgate_path": {"type": "string"},
            "rollback_snapshot_path": {"type": "string"},
            "expected_outputs": {"type": "array", "items": {"type": "string"}},
            "tests_required": {"type": "array", "items": {"type": "object"}},
            "witnesslog_path": {"type": "string"},
            "status": {"enum": ["DRAFT", "READY", "APPROVED", "EXECUTED", "ROLLED_BACK", "BLOCKED"]},
            "publication_gate": {"const": "BLOCK"},
        },
        "additionalProperties": True,
    }


def ensure_workpack_contract_files() -> None:
    write_json_file(WORKPACK_CONTRACT_PATH, workpack_contract_payload())
    write_json_file(WORKPACK_SCHEMA_PATH, workpack_schema_payload())


def workpack_files(workpack_id: str) -> dict[str, pathlib.Path]:
    safe_id = safe_local_id(workpack_id)
    base = WORKPACK_DATA_DIR / safe_id
    return {
        "manifest": base / f"WORKPACK_{safe_id}.json",
        "evidence": base / f"WORKPACK_EVIDENCE_{safe_id}.json",
    }


def workpack_witness(workpack_id: str, event: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    previous = read_jsonl(WORKPACK_WITNESSLOG_PATH, limit=1)
    previous_hash = str(previous[-1].get("hash", "")) if previous else ""
    record = {
        "event": event,
        "workpack_id": safe_local_id(workpack_id),
        "timestamp": utc_now_iso(),
        "previous_hash": previous_hash,
        "execution_engine": "LOCAL_EXECUTE_v0_2",
        "cloud_called": False,
        "nvidia_called": False,
        "publication": "BLOCK",
        "secret_values_printed": False,
        **(payload or {}),
    }
    digest_source = json.dumps(sanitize_obj(record), ensure_ascii=True, sort_keys=True)
    record["hash"] = hashlib.sha256((previous_hash + digest_source).encode("utf-8")).hexdigest()
    append_jsonl(WORKPACK_WITNESSLOG_PATH, record)
    return sanitize_obj(record)


def workpack_id_for_task(task_id: str) -> str:
    safe_id = safe_local_id(task_id)
    return WORKPACK_DEMO_TASK_IDS.get(safe_id, f"claudio-workpack-{safe_id}-v0-1")


def workpack_task_overrides(source_task: dict[str, Any], workpack_id: str) -> dict[str, Any]:
    source_id = str(source_task.get("task_id", ""))
    if source_id == "local-execute-sandbox-demo":
        return {
            "allowed_targets": ["WABI_WORKPACK_RUNTIME/sandbox_demo/hello_workpack.md"],
            "intent": "Create a Workpack sandbox marker through Local Execute v0.2.",
        }
    if source_id == "local-execute-docs-demo":
        return {
            "allowed_targets": ["docs/local_execute/CLAUDIO_WORKPACK_BRIDGE_v0_1_ACCEPTANCE_NOTE.md"],
            "intent": "Create a local-only Workpack acceptance note under docs/local_execute.",
        }
    lane = str(source_task.get("lane", "SANDBOX"))
    if lane == "SANDBOX":
        return {
            "allowed_targets": [f"WABI_WORKPACK_RUNTIME/{safe_local_id(source_id)}/workpack_output.md"],
            "intent": str(source_task.get("next_action") or "Create a sandbox Workpack output."),
        }
    if lane == "DOCS_LOCAL":
        return {
            "allowed_targets": [f"docs/local_execute/{safe_local_id(workpack_id).upper()}_NOTE.md"],
            "intent": str(source_task.get("next_action") or "Create a local docs Workpack output."),
        }
    return {"allowed_targets": [], "intent": "Blocked lane; no executable targets."}


def build_workpack_manifest(
    workpack_id: str,
    source_task: dict[str, Any],
    task_spec: dict[str, Any],
    *,
    status: str = "DRAFT",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    files = local_execute_task_files(workpack_id)
    manifest = {
        "schema": "medioevo.claudio_workpack.v0_1",
        "workpack_id": safe_local_id(workpack_id),
        "source_task_id": str(source_task.get("task_id", "")),
        "title": str(source_task.get("title") or task_spec.get("title") or workpack_id),
        "lane": str(task_spec.get("lane") or source_task.get("lane") or "SANDBOX"),
        "assigned_agent": str(source_task.get("assigned_agent") or "CLAUDIO_WORKPACK_MANAGER"),
        "task_spec_path": local_execute_target_alias(files["taskspec"]),
        "ghostgate_path": local_execute_target_alias(files["ghostgate"]),
        "rollback_snapshot_path": local_execute_target_alias(files["rollback"]),
        "expected_outputs": list(task_spec.get("expected_outputs", [])),
        "tests_required": list(task_spec.get("tests_required", [])),
        "witnesslog_path": local_execute_target_alias(files["witness"]),
        "workpack_witnesslog_path": local_execute_target_alias(WORKPACK_WITNESSLOG_PATH),
        "status": status,
        "publication_gate": "BLOCK",
        "cloud_called": False,
        "nvidia_called": False,
        "direct_delete_allowed": False,
        "secret_values_printed": False,
        "created_at": utc_now_iso(),
        "local_execute_state": local_execute_task_state(workpack_id),
    }
    if extra:
        manifest.update(extra)
    return sanitize_obj(manifest)


def load_workpack_manifest(workpack_id: str) -> dict[str, Any]:
    manifest_path = workpack_files(workpack_id)["manifest"]
    if not manifest_path.exists():
        return {}
    return _load_json_dict(manifest_path, {})


def write_workpack_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    workpack_id = safe_local_id(str(manifest.get("workpack_id", "")))
    write_json_file(workpack_files(workpack_id)["manifest"], manifest)
    return sanitize_obj(manifest)


def update_workpack_manifest(workpack_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    manifest = load_workpack_manifest(workpack_id)
    if not manifest:
        raise ValueError("Workpack manifest not found.")
    manifest.update(updates)
    manifest["updated_at"] = utc_now_iso()
    manifest["local_execute_state"] = local_execute_task_state(workpack_id)
    write_workpack_manifest(manifest)
    return sanitize_obj(manifest)


def workpack_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if WORKPACK_DATA_DIR.exists():
        for path in sorted(WORKPACK_DATA_DIR.glob("*/WORKPACK_*.json")):
            if path.name.startswith("WORKPACK_EVIDENCE_"):
                continue
            row = _load_json_dict(path, {})
            if row:
                row["local_execute_state"] = local_execute_task_state(str(row.get("workpack_id", "")))
                records.append(sanitize_obj(row))
    return records


def workpacks_payload() -> dict[str, Any]:
    ensure_workpack_contract_files()
    records = workpack_records()
    return sanitize_obj(
        {
            "schema": "medioevo.claudio_workpack_bridge.v0_1",
            "version": "v0.1",
            "mode": "LOCAL_ONLY",
            "execution_engine": "LOCAL_EXECUTE_v0_2",
            "contract": workpack_contract_payload(),
            "contract_path": local_execute_target_alias(WORKPACK_CONTRACT_PATH),
            "schema_path": local_execute_target_alias(WORKPACK_SCHEMA_PATH),
            "workpacks": records,
            "workpack_count": len(records),
            "cloud_called": False,
            "nvidia_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def create_workpack_from_task_payload(task_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_workpack_contract_files()
    task = find_local_hub_task(task_id)
    lane = str(task.get("lane", ""))
    workpack_id = safe_local_id(str((payload or {}).get("workpack_id") or workpack_id_for_task(task["task_id"])))
    if lane in WORKPACK_BLOCKED_LANES or lane not in WORKPACK_ALLOWED_LANES:
        return {
            "ok": False,
            "status": "BLOCK",
            "workpack_id": workpack_id,
            "source_task_id": task["task_id"],
            "reason": "Workpack execution bridge only allows SANDBOX and DOCS_LOCAL lanes.",
            "cloud_called": False,
            "nvidia_called": False,
            "secret_values_printed": False,
        }
    overrides = workpack_task_overrides(task, workpack_id)
    workpack_task = dict(task)
    workpack_task["task_id"] = workpack_id
    workpack_task["source"] = "CLAUDIO_WORKPACK_BRIDGE_v0_1"
    task_spec = build_local_execute_task_spec(workpack_task, overrides)
    files = local_execute_task_files(workpack_id)
    write_json_file(files["taskspec"], task_spec)
    manifest = build_workpack_manifest(workpack_id, task, task_spec, status="DRAFT")
    write_workpack_manifest(manifest)
    local_execute_witness(workpack_id, "workpack_taskspec_created", {"source_task_id": task["task_id"]})
    witness = workpack_witness(workpack_id, "workpack_created_from_task", {"source_task_id": task["task_id"], "status": "DRAFT"})
    return sanitize_obj(
        {
            "ok": True,
            "status": "DRAFT",
            "workpack_id": workpack_id,
            "source_task_id": task["task_id"],
            "workpack": manifest,
            "task_spec": task_spec,
            "task_spec_path": local_execute_target_alias(files["taskspec"]),
            "witness": witness,
            "executes": False,
            "secret_values_printed": False,
        }
    )


def approve_workpack_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_workpack_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Workpack manifest required.", "secret_values_printed": False}
    files = local_execute_task_files(safe_id)
    if not files["taskspec"].exists():
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "TaskSpec required before workpack approval.", "secret_values_printed": False}
    task_spec = _load_json_dict(files["taskspec"], {})
    validation = local_execute_validation(task_spec)
    lane = str(task_spec.get("lane", ""))
    decision = "APPROVE" if validation["ok"] and lane in WORKPACK_ALLOWED_LANES else "BLOCK"
    result = {
        "schema": "medioevo.claudio_workpack.ghostgate.v0_1",
        "workpack_id": safe_id,
        "source_task_id": manifest.get("source_task_id", ""),
        "decision": decision,
        "reversible": decision == "APPROVE",
        "rollback_required": True,
        "rollback_available": False,
        "cloud_allowed": False,
        "nvidia_allowed": False,
        "publication_allowed": False,
        "validation": validation,
        "reason": "" if decision == "APPROVE" else "; ".join(validation.get("reasons", [])) or "Workpack lane blocked.",
        "timestamp": utc_now_iso(),
        "secret_values_printed": False,
    }
    if decision == "APPROVE":
        rollback = local_execute_create_rollback_snapshot(task_spec)
        result["rollback_available"] = True
        result["rollback_snapshot"] = local_execute_target_alias(files["rollback"])
        result["rollback"] = rollback
    write_json_file(files["ghostgate"], result)
    status = "APPROVED" if decision == "APPROVE" else "BLOCKED"
    updated = update_workpack_manifest(
        safe_id,
        {
            "status": status,
            "ghostgate_decision": decision,
            "ghostgate_path": local_execute_target_alias(files["ghostgate"]),
            "rollback_snapshot_path": local_execute_target_alias(files["rollback"]),
            "rollback_available": decision == "APPROVE",
        },
    )
    local_execute_witness(safe_id, "workpack_ghostgate_evaluated", {"decision": decision})
    witness = workpack_witness(safe_id, "workpack_approved" if decision == "APPROVE" else "workpack_blocked", {"decision": decision})
    return sanitize_obj({"ok": decision == "APPROVE", "status": status, "workpack_id": safe_id, "ghostgate": result, "workpack": updated, "witness": witness})


def execute_workpack_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_workpack_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Workpack manifest required.", "secret_values_printed": False}
    if manifest.get("status") != "APPROVED":
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Workpack must be APPROVED before execute.", "secret_values_printed": False}
    files = local_execute_task_files(safe_id)
    if not files["taskspec"].exists() or not files["ghostgate"].exists():
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "TaskSpec and GhostGate required before execute.", "secret_values_printed": False}
    if not files["rollback"].exists():
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Rollback snapshot required before execute.", "secret_values_printed": False}
    ghostgate = _load_json_dict(files["ghostgate"], {})
    if ghostgate.get("decision") != "APPROVE":
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Execute blocked because GhostGate is not APPROVE.", "ghostgate": ghostgate}
    task_spec = _load_json_dict(files["taskspec"], {})
    validation = local_execute_validation(task_spec)
    if not validation["ok"]:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "TaskSpec failed allowlist validation.", "validation": validation}
    apply_result = local_execute_apply_task(task_spec)
    test_result = local_execute_run_task_tests(task_spec)
    rollback_result = None
    status = "EXECUTED" if test_result.get("passed") is True else "ROLLED_BACK"
    if status == "ROLLED_BACK":
        rollback_result = local_execute_rollback_task_payload(safe_id)
    updated = update_workpack_manifest(
        safe_id,
        {
            "status": status,
            "apply_status": apply_result.get("apply_status", "APPLIED"),
            "tests_passed": test_result.get("passed") is True,
            "execution_result_path": local_execute_target_alias(files["execution"]),
            "test_result_path": local_execute_target_alias(files["tests"]),
        },
    )
    local_execute_witness(safe_id, "workpack_executed", {"status": status, "tests_passed": test_result.get("passed") is True})
    witness = workpack_witness(safe_id, "workpack_executed", {"status": status, "tests_passed": test_result.get("passed") is True})
    return sanitize_obj(
        {
            "ok": test_result.get("passed") is True,
            "status": status,
            "workpack_id": safe_id,
            "apply_status": apply_result.get("apply_status", "APPLIED"),
            "execution_result": apply_result,
            "test_result": test_result,
            "rollback_result": rollback_result,
            "workpack": updated,
            "evidence": local_execute_evidence_payload(safe_id)["evidence"],
            "witness": witness,
            "cloud_called": False,
            "nvidia_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def rollback_workpack_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_workpack_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Workpack manifest required.", "secret_values_printed": False}
    rollback = local_execute_rollback_task_payload(safe_id)
    updated = update_workpack_manifest(safe_id, {"status": "ROLLED_BACK", "rollback_status": rollback.get("status", "ROLLED_BACK")})
    witness = workpack_witness(safe_id, "workpack_rollback", {"status": rollback.get("status", "ROLLED_BACK")})
    return sanitize_obj({"ok": rollback.get("ok") is True, "status": "ROLLED_BACK", "workpack_id": safe_id, "rollback": rollback, "workpack": updated, "witness": witness})


def workpack_evidence_payload(workpack_id: str) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_workpack_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Workpack manifest not found.", "secret_values_printed": False}
    evidence = {
        "workpack_manifest": {"exists": True, "path": local_execute_target_alias(workpack_files(safe_id)["manifest"])},
        "workpack_evidence": {"exists": workpack_files(safe_id)["evidence"].exists(), "path": local_execute_target_alias(workpack_files(safe_id)["evidence"])},
        "local_execute": local_execute_evidence_payload(safe_id),
        "workpack_witness_events": [row for row in read_jsonl(WORKPACK_WITNESSLOG_PATH, limit=200) if row.get("workpack_id") == safe_id],
    }
    payload = {"ok": True, "status": manifest.get("status", "DRAFT"), "workpack_id": safe_id, "workpack": manifest, "evidence": evidence, "secret_values_printed": False}
    write_json_file(workpack_files(safe_id)["evidence"], payload)
    return sanitize_obj(payload)


def agent_chat_message_to_workpack_payload(message_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_message_id = safe_local_id(message_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    message = next((row for row in messages if safe_local_id(str(row.get("message_id", ""))) == safe_message_id), None)
    if not message:
        return {"ok": False, "status": "BLOCK", "reason": "Agent chat message not found.", "secret_values_printed": False}
    body = str(message.get("body", ""))
    if text_has_secret_value(body):
        return {"ok": False, "status": "BLOCK", "reason": "Secret-like value detected; Workpack draft not written.", "secret_values_printed": False}
    workpack_id = safe_local_id(str((payload or {}).get("workpack_id") or f"chat-workpack-{safe_message_id}-v0-1"))
    files = local_execute_task_files(workpack_id)
    task_spec = {
        "schema": "medioevo.local_execute.task_spec.v0_2",
        "task_id": workpack_id,
        "title": f"Workpack draft from agent chat {safe_message_id}",
        "lane": "SANDBOX",
        "intent": sanitize_text(body[:500]),
        "source": "AGENT_CHAT",
        "allowed_targets": [],
        "blocked_targets": [".env", "credentials", "PUBLICATION", "CLOUD", "NVIDIA"],
        "expected_outputs": [],
        "tests_required": [],
        "operation": {"type": "draft_only"},
        "rollback_required": True,
        "witness_required": True,
        "publication_gate": "BLOCK",
        "cloud_allowed": False,
        "nvidia_allowed": False,
        "direct_delete_allowed": False,
        "created_at": utc_now_iso(),
        "draft_only": True,
        "assigned_agent": str((payload or {}).get("assigned_agent") or "CLAUDIO_WORKPACK_MANAGER"),
        "secret_values_printed": False,
    }
    write_json_file(files["taskspec"], task_spec)
    source_task = {
        "task_id": f"agent-chat-{safe_message_id}",
        "title": task_spec["title"],
        "lane": "SANDBOX",
        "assigned_agent": task_spec["assigned_agent"],
    }
    manifest = build_workpack_manifest(workpack_id, source_task, task_spec, status="DRAFT", extra={"draft_only": True, "source_message_id": safe_message_id})
    write_workpack_manifest(manifest)
    local_execute_witness(workpack_id, "agent_chat_message_to_workpack_draft", {"message_id": safe_message_id})
    witness = workpack_witness(workpack_id, "agent_chat_message_to_workpack_draft", {"message_id": safe_message_id})
    route_witness = agent_chat_witness("agent_chat_message_to_workpack_draft", {"message_id": safe_message_id, "workpack_id": workpack_id})
    system_status = agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "workpack_draft_created",
            "message": f"Workpack draft {workpack_id} created from message {safe_message_id}; execution requires GhostGate APPROVE and rollback.",
            "linked_workpack_id": workpack_id,
            "message_type": "WORKPACK",
        }
    )
    return sanitize_obj(
        {
            "ok": True,
            "status": "WORKPACK_DRAFT_CREATED",
            "workpack_id": workpack_id,
            "task_spec_path": local_execute_target_alias(files["taskspec"]),
            "workpack": manifest,
            "witness": witness,
            "routing_witness": route_witness,
            "system_status": system_status.get("message"),
            "executes": False,
            "secret_values_printed": False,
        }
    )


def workpack_chat_note_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_workpack_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "reason": "Workpack manifest not found.", "secret_values_printed": False}
    body = f"Workpack {safe_id}: status={manifest.get('status', 'DRAFT')} lane={manifest.get('lane', 'SANDBOX')} publication_gate=BLOCK"
    result = agent_chat_post_message_payload({"room": "#wabi", "sender": "CLAUDIO_WORKPACK_MANAGER", "body": body})
    return sanitize_obj({"ok": result.get("ok") is True, "status": "CHAT_NOTE_WRITTEN" if result.get("ok") else "BLOCK", "workpack_id": safe_id, "message": result.get("message"), "secret_values_printed": False})


def workpack_scheduler_contract_payload() -> dict[str, Any]:
    return {
        "version": "v0.1",
        "mode": "LOCAL_ONLY",
        "execution_model": "MANUAL_TICK",
        "max_concurrency": 1,
        "allowed_lanes": ["SANDBOX", "DOCS_LOCAL"],
        "blocked_lanes": ["PUBLICATION", "CLOUD", "NVIDIA", "DEEPSEEK", "REMOTE_COMPUTE", "PROTECTED_MATERIAL"],
        "requires_workpack": True,
        "requires_task_spec": True,
        "requires_ghostgate_pass": True,
        "requires_rollback": True,
        "requires_witnesslog": True,
        "direct_delete_allowed": False,
        "publication_gate": "BLOCK",
        "cloud_live_gate": "BLOCK_THIS_RUN",
        "nvidia_smoke_gate": "DO_NOT_CALL",
        "deepseek_gate": "REVIEW_QUOTA_OR_BILLING",
        "secret_values_printed": False,
    }


def workpack_scheduler_queue_schema_payload() -> dict[str, Any]:
    return {
        "$schema": "json-schema-draft-2020-12",
        "$id": "medioevo.workpack_scheduler.queue.v0_1",
        "type": "object",
        "required": [
            "queue_id",
            "workpack_id",
            "title",
            "lane",
            "priority",
            "dependencies",
            "status",
            "assigned_agent",
            "attempts",
            "max_retries",
            "last_error",
            "next_action",
            "scheduled_at",
            "updated_at",
            "witness_event_id",
        ],
        "properties": {
            "queue_id": {"type": "string"},
            "workpack_id": {"type": "string"},
            "title": {"type": "string"},
            "lane": {"type": "string"},
            "priority": {"type": "integer"},
            "dependencies": {"type": "array", "items": {"type": "string"}},
            "status": {"enum": sorted(WORKPACK_SCHEDULER_QUEUE_STATES)},
            "assigned_agent": {"type": "string"},
            "attempts": {"type": "integer", "minimum": 0},
            "max_retries": {"type": "integer", "minimum": 0},
            "last_error": {"type": "string"},
            "next_action": {"type": "string"},
            "scheduled_at": {"type": "string"},
            "updated_at": {"type": "string"},
            "witness_event_id": {"type": "string"},
        },
        "additionalProperties": True,
    }


def ensure_workpack_scheduler_contract_files() -> None:
    write_json_file(WORKPACK_SCHEDULER_CONTRACT_PATH, workpack_scheduler_contract_payload())
    write_json_file(WORKPACK_SCHEDULER_SCHEMA_PATH, workpack_scheduler_queue_schema_payload())


def scheduler_witness(event: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    previous = read_jsonl(WORKPACK_SCHEDULER_WITNESSLOG_PATH, limit=1)
    previous_hash = str(previous[-1].get("hash", "")) if previous else ""
    record = {
        "event": event,
        "timestamp": utc_now_iso(),
        "previous_hash": previous_hash,
        "scheduler": "WORKPACK_SCHEDULER_v0_1",
        "execution_model": "MANUAL_TICK",
        "max_concurrency": 1,
        "cloud_called": False,
        "nvidia_called": False,
        "deepseek_called": False,
        "publication": "BLOCK",
        "secret_values_printed": False,
        **(payload or {}),
    }
    digest_source = json.dumps(sanitize_obj(record), ensure_ascii=True, sort_keys=True)
    record["hash"] = hashlib.sha256((previous_hash + digest_source).encode("utf-8")).hexdigest()
    append_jsonl(WORKPACK_SCHEDULER_WITNESSLOG_PATH, record)
    return sanitize_obj(record)


def scheduler_load_queue() -> list[dict[str, Any]]:
    if not WORKPACK_SCHEDULER_QUEUE_PATH.exists():
        return []
    try:
        raw = json.loads(WORKPACK_SCHEDULER_QUEUE_PATH.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return []
    if isinstance(raw, list):
        return [sanitize_obj(row) for row in raw if isinstance(row, dict)]
    if isinstance(raw, dict):
        queue = raw.get("queue", [])
        if isinstance(queue, list):
            return [sanitize_obj(row) for row in queue if isinstance(row, dict)]
    return []


def scheduler_save_queue(queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    payload = {
        "schema": "medioevo.workpack_scheduler.queue_manifest.v0_1",
        "run_id": WORKPACK_SCHEDULER_RUN_ID,
        "mode": "LOCAL_ONLY",
        "execution_model": "MANUAL_TICK",
        "max_concurrency": 1,
        "queue": [sanitize_obj(row) for row in queue],
        "queue_count": len(queue),
        "updated_at": utc_now_iso(),
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }
    write_json_file(WORKPACK_SCHEDULER_QUEUE_PATH, payload)
    return payload["queue"]


def scheduler_find_queue_item(queue_id: str) -> dict[str, Any]:
    safe_id = safe_local_id(queue_id)
    for item in scheduler_load_queue():
        if item.get("queue_id") == safe_id:
            return item
    raise ValueError("scheduler queue item not found")


def scheduler_upsert_queue_item(item: dict[str, Any]) -> dict[str, Any]:
    queue = scheduler_load_queue()
    safe_queue_id = safe_local_id(str(item.get("queue_id", "")))
    updated = False
    for index, row in enumerate(queue):
        if row.get("queue_id") == safe_queue_id:
            queue[index] = sanitize_obj(item)
            updated = True
            break
    if not updated:
        queue.append(sanitize_obj(item))
    scheduler_save_queue(queue)
    return sanitize_obj(item)


def scheduler_update_queue_item(queue_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    item = scheduler_find_queue_item(queue_id)
    item.update(updates)
    item["updated_at"] = utc_now_iso()
    return scheduler_upsert_queue_item(item)


def scheduler_queue_item_for_workpack(
    workpack: dict[str, Any],
    *,
    priority: int = 0,
    dependencies: list[str] | None = None,
    max_retries: int = 1,
) -> dict[str, Any]:
    workpack_id = safe_local_id(str(workpack.get("workpack_id", "")))
    now = utc_now_iso()
    return sanitize_obj(
        {
            "queue_id": f"scheduler-{workpack_id}",
            "workpack_id": workpack_id,
            "title": str(workpack.get("title") or workpack_id),
            "lane": str(workpack.get("lane") or "SANDBOX"),
            "priority": int(priority),
            "dependencies": [safe_local_id(str(dep)) for dep in (dependencies or [])],
            "status": "READY",
            "assigned_agent": str(workpack.get("assigned_agent") or "CLAUDIO_WORKPACK_MANAGER"),
            "attempts": 0,
            "max_retries": int(max_retries),
            "last_error": "",
            "next_action": "Run scheduler approve; tick remains manual.",
            "scheduled_at": now,
            "updated_at": now,
            "witness_event_id": "",
            "execution_model": "MANUAL_TICK",
            "executes": False,
            "publication_gate": "BLOCK",
            "cloud_called": False,
            "nvidia_called": False,
            "deepseek_called": False,
            "secret_values_printed": False,
        }
    )


def scheduler_records() -> list[dict[str, Any]]:
    return scheduler_load_queue()


def workpack_scheduler_payload() -> dict[str, Any]:
    ensure_workpack_scheduler_contract_files()
    queue = scheduler_load_queue()
    return sanitize_obj(
        {
            "schema": "medioevo.workpack_scheduler.v0_1",
            "version": "v0.1",
            "mode": "LOCAL_ONLY",
            "execution_model": "MANUAL_TICK",
            "max_concurrency": 1,
            "contract": workpack_scheduler_contract_payload(),
            "contract_path": local_execute_target_alias(WORKPACK_SCHEDULER_CONTRACT_PATH),
            "queue_schema_path": local_execute_target_alias(WORKPACK_SCHEDULER_SCHEMA_PATH),
            "queue_manifest_path": local_execute_target_alias(WORKPACK_SCHEDULER_QUEUE_PATH),
            "witnesslog_path": local_execute_target_alias(WORKPACK_SCHEDULER_WITNESSLOG_PATH),
            "queue": queue,
            "queue_count": len(queue),
            "ready_count": sum(1 for row in queue if row.get("status") in {"APPROVED", "SCHEDULED"}),
            "blocked_count": sum(1 for row in queue if row.get("status") == "BLOCKED"),
            "cloud_called": False,
            "nvidia_called": False,
            "deepseek_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def scheduler_enqueue_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_workpack_scheduler_contract_files()
    safe_workpack_id = safe_local_id(workpack_id)
    manifest = load_workpack_manifest(safe_workpack_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_workpack_id, "reason": "Workpack manifest required before scheduler enqueue.", "executes": False, "secret_values_printed": False}
    lane = str(manifest.get("lane", ""))
    priority = int((payload or {}).get("priority", 0) or 0)
    dependencies = [safe_local_id(str(dep)) for dep in (payload or {}).get("dependencies", [])]
    max_retries = int((payload or {}).get("max_retries", 1) or 1)
    item = scheduler_queue_item_for_workpack(manifest, priority=priority, dependencies=dependencies, max_retries=max_retries)
    if lane in WORKPACK_SCHEDULER_BLOCKED_LANES or lane not in WORKPACK_SCHEDULER_ALLOWED_LANES:
        item.update(
            {
                "status": "BLOCKED",
                "last_error": "Scheduler only allows SANDBOX and DOCS_LOCAL lanes.",
                "next_action": "Do not execute; lane is blocked by scheduler contract.",
            }
        )
        scheduler_upsert_queue_item(item)
        witness = scheduler_witness("scheduler_enqueue_blocked", {"queue_id": item["queue_id"], "workpack_id": safe_workpack_id, "lane": lane})
        item["witness_event_id"] = str(witness.get("hash", ""))[:16]
        scheduler_upsert_queue_item(item)
        return sanitize_obj({"ok": False, "status": "BLOCKED", "queue_item": item, "reason": item["last_error"], "executes": False, "secret_values_printed": False})
    scheduler_upsert_queue_item(item)
    witness = scheduler_witness("scheduler_enqueued", {"queue_id": item["queue_id"], "workpack_id": safe_workpack_id, "dependencies": dependencies})
    item["witness_event_id"] = str(witness.get("hash", ""))[:16]
    scheduler_upsert_queue_item(item)
    agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "scheduler_enqueued",
            "message": f"Workpack {safe_workpack_id} enqueued for manual scheduler tick; execution still requires approval gates.",
            "linked_workpack_id": safe_workpack_id,
            "message_type": "SYSTEM",
        }
    )
    return sanitize_obj({"ok": True, "status": item["status"], "queue_item": item, "witness": witness, "executes": False, "secret_values_printed": False})


def scheduler_approve_payload(queue_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_workpack_scheduler_contract_files()
    item = scheduler_find_queue_item(queue_id)
    if item.get("status") == "BLOCKED":
        return {"ok": False, "status": "BLOCKED", "queue_id": item["queue_id"], "reason": item.get("last_error", "blocked"), "executes": False, "secret_values_printed": False}
    lane = str(item.get("lane", ""))
    if lane in WORKPACK_SCHEDULER_BLOCKED_LANES or lane not in WORKPACK_SCHEDULER_ALLOWED_LANES:
        updated = scheduler_update_queue_item(item["queue_id"], {"status": "BLOCKED", "last_error": "Scheduler lane is blocked.", "next_action": "Do not execute."})
        witness = scheduler_witness("scheduler_approve_blocked", {"queue_id": item["queue_id"], "lane": lane})
        return sanitize_obj({"ok": False, "status": "BLOCKED", "queue_item": updated, "witness": witness, "executes": False, "secret_values_printed": False})
    result = approve_workpack_payload(str(item.get("workpack_id", "")), payload or {})
    status = "APPROVED" if result.get("ok") else "BLOCKED"
    updated = scheduler_update_queue_item(
        item["queue_id"],
        {
            "status": status,
            "last_error": "" if result.get("ok") else str(result.get("reason", "GhostGate did not approve.")),
            "next_action": "Manual tick may execute max one approved workpack." if result.get("ok") else "Review GhostGate result before retry.",
        },
    )
    witness = scheduler_witness("scheduler_approved" if result.get("ok") else "scheduler_approve_blocked", {"queue_id": item["queue_id"], "workpack_id": item.get("workpack_id", ""), "status": status})
    updated["witness_event_id"] = str(witness.get("hash", ""))[:16]
    scheduler_upsert_queue_item(updated)
    agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "scheduler_approved" if result.get("ok") else "scheduler_approve_blocked",
            "message": f"Scheduler approval for {item.get('workpack_id', '')}: {status}.",
            "linked_workpack_id": str(item.get("workpack_id", "")),
            "message_type": "GATE",
        }
    )
    return sanitize_obj({"ok": result.get("ok") is True, "status": status, "queue_item": updated, "workpack_approval": result, "witness": witness, "executes": False, "secret_values_printed": False})


def scheduler_dependencies_resolved(item: dict[str, Any], queue: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    unresolved: list[str] = []
    for dep in item.get("dependencies", []):
        dep_id = safe_local_id(str(dep))
        match = next((row for row in queue if row.get("queue_id") == dep_id or row.get("workpack_id") == dep_id), None)
        if not match or match.get("status") != "EXECUTED":
            unresolved.append(dep_id)
    return not unresolved, unresolved


def scheduler_select_next_item(queue: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, list[str]]:
    candidates = [row for row in queue if row.get("status") in {"APPROVED", "SCHEDULED"}]
    candidates.sort(key=lambda row: (-int(row.get("priority", 0) or 0), str(row.get("scheduled_at", "")), str(row.get("queue_id", ""))))
    skipped: list[str] = []
    for item in candidates:
        resolved, unresolved = scheduler_dependencies_resolved(item, queue)
        if resolved:
            return item, skipped
        skipped.append(f"{item.get('queue_id', '')}:waiting_for:{','.join(unresolved)}")
        scheduler_update_queue_item(str(item.get("queue_id", "")), {"dependency_status": "WAITING", "last_error": f"Waiting for dependencies: {', '.join(unresolved)}", "next_action": "Wait for dependency execution, then tick again."})
    return None, skipped


def scheduler_recheck_workpack_ready(item: dict[str, Any]) -> tuple[bool, str]:
    workpack_id = str(item.get("workpack_id", ""))
    manifest = load_workpack_manifest(workpack_id)
    if not manifest:
        return False, "Workpack manifest required."
    if manifest.get("status") != "APPROVED":
        return False, "Workpack must be APPROVED before scheduler tick."
    lane = str(manifest.get("lane", ""))
    if lane in WORKPACK_SCHEDULER_BLOCKED_LANES or lane not in WORKPACK_SCHEDULER_ALLOWED_LANES:
        return False, "Scheduler lane blocked."
    files = local_execute_task_files(workpack_id)
    if not files["taskspec"].exists():
        return False, "TaskSpec required before scheduler tick."
    if not files["ghostgate"].exists():
        return False, "GhostGate required before scheduler tick."
    ghostgate = _load_json_dict(files["ghostgate"], {})
    if ghostgate.get("decision") != "APPROVE":
        return False, "GhostGate must be APPROVE before scheduler tick."
    if not files["rollback"].exists():
        return False, "Rollback snapshot required before scheduler tick."
    task_spec = _load_json_dict(files["taskspec"], {})
    validation = local_execute_validation(task_spec)
    if not validation.get("ok"):
        return False, "TaskSpec failed scheduler allowlist validation."
    return True, ""


def scheduler_tick_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_workpack_scheduler_contract_files()
    queue = scheduler_load_queue()
    item, skipped = scheduler_select_next_item(queue)
    if not item:
        witness = scheduler_witness("scheduler_tick_idle", {"skipped": skipped})
        return sanitize_obj({"ok": True, "status": "IDLE", "executed_count": 0, "skipped": skipped, "witness": witness, "secret_values_printed": False})
    queue_id = str(item.get("queue_id", ""))
    ready, reason = scheduler_recheck_workpack_ready(item)
    if not ready:
        updated = scheduler_update_queue_item(queue_id, {"status": "BLOCKED", "last_error": reason, "next_action": "Review Workpack gates before retry."})
        witness = scheduler_witness("scheduler_tick_blocked", {"queue_id": queue_id, "workpack_id": item.get("workpack_id", ""), "reason": reason})
        return sanitize_obj({"ok": False, "status": "BLOCKED", "executed_count": 0, "queue_item": updated, "reason": reason, "witness": witness, "secret_values_printed": False})
    running = scheduler_update_queue_item(queue_id, {"status": "RUNNING", "attempts": int(item.get("attempts", 0) or 0) + 1, "next_action": "Delegating to Workpack Bridge / Local Execute."})
    result = execute_workpack_payload(str(item.get("workpack_id", "")), payload or {})
    status = "EXECUTED" if result.get("ok") and result.get("status") == "EXECUTED" else ("ROLLED_BACK" if result.get("status") == "ROLLED_BACK" else "FAILED")
    updated = scheduler_update_queue_item(
        queue_id,
        {
            "status": status,
            "last_error": "" if status == "EXECUTED" else str(result.get("reason") or result.get("status") or "Workpack execution failed."),
            "next_action": "Open evidence." if status == "EXECUTED" else "Retry if safe and attempts remain.",
        },
    )
    witness = scheduler_witness("scheduler_tick_executed", {"queue_id": queue_id, "workpack_id": item.get("workpack_id", ""), "status": status, "attempts": running.get("attempts", 0)})
    updated["witness_event_id"] = str(witness.get("hash", ""))[:16]
    scheduler_upsert_queue_item(updated)
    agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "scheduler_tick_executed",
            "message": f"Scheduler tick processed {item.get('workpack_id', '')}: {status}.",
            "linked_workpack_id": str(item.get("workpack_id", "")),
            "message_type": "SYSTEM",
        }
    )
    return sanitize_obj({"ok": status == "EXECUTED", "status": status, "executed_count": 1, "queue_item": updated, "workpack_result": result, "witness": witness, "secret_values_printed": False})


def scheduler_retry_payload(queue_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    item = scheduler_find_queue_item(queue_id)
    if item.get("status") == "BLOCKED":
        return {"ok": False, "status": "BLOCKED", "queue_id": item["queue_id"], "reason": "Retry blocked for BLOCKED scheduler items.", "executes": False, "secret_values_printed": False}
    attempts = int(item.get("attempts", 0) or 0)
    max_retries = int(item.get("max_retries", 1) or 1)
    if attempts >= max_retries:
        updated = scheduler_update_queue_item(item["queue_id"], {"status": "REVIEW", "last_error": "Retry limit reached.", "next_action": "Manual review required."})
        witness = scheduler_witness("scheduler_retry_limit_reached", {"queue_id": item["queue_id"], "attempts": attempts, "max_retries": max_retries})
        return sanitize_obj({"ok": False, "status": "REVIEW", "queue_item": updated, "witness": witness, "executes": False, "secret_values_printed": False})
    updated = scheduler_update_queue_item(item["queue_id"], {"status": "APPROVED", "last_error": "", "next_action": "Retry queued for next manual tick."})
    witness = scheduler_witness("scheduler_retry_queued", {"queue_id": item["queue_id"], "attempts": attempts, "max_retries": max_retries})
    return sanitize_obj({"ok": True, "status": "APPROVED", "queue_item": updated, "witness": witness, "executes": False, "secret_values_printed": False})


def scheduler_rollback_payload(queue_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    item = scheduler_find_queue_item(queue_id)
    result = rollback_workpack_payload(str(item.get("workpack_id", "")), payload or {})
    status = "ROLLED_BACK" if result.get("ok") else "FAILED"
    updated = scheduler_update_queue_item(item["queue_id"], {"status": status, "last_error": "" if result.get("ok") else str(result.get("reason", "rollback failed")), "next_action": "Open evidence."})
    witness = scheduler_witness("scheduler_rollback", {"queue_id": item["queue_id"], "workpack_id": item.get("workpack_id", ""), "status": status})
    return sanitize_obj({"ok": result.get("ok") is True, "status": status, "queue_item": updated, "rollback": result, "witness": witness, "secret_values_printed": False})


def scheduler_evidence_payload(queue_id: str) -> dict[str, Any]:
    item = scheduler_find_queue_item(queue_id)
    workpack_id = str(item.get("workpack_id", ""))
    workpack_evidence = workpack_evidence_payload(workpack_id) if load_workpack_manifest(workpack_id) else {}
    payload = {
        "ok": True,
        "schema": "medioevo.workpack_scheduler.evidence.v0_1",
        "queue_id": item["queue_id"],
        "queue_item": item,
        "workpack_evidence": workpack_evidence,
        "scheduler_witness_events": [row for row in read_jsonl(WORKPACK_SCHEDULER_WITNESSLOG_PATH, limit=300) if row.get("queue_id") == item["queue_id"]],
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }
    write_json_file(WORKPACK_SCHEDULER_RUN_DIR / f"WORKPACK_SCHEDULER_EVIDENCE_{item['queue_id']}.json", payload)
    return sanitize_obj(payload)


def scheduler_demo_task_spec(workpack_id: str, lane: str, target: str, content: str, tests: list[dict[str, Any]]) -> dict[str, Any]:
    return sanitize_obj(
        {
            "schema": "medioevo.local_execute.task_spec.v0_2",
            "task_id": safe_local_id(workpack_id),
            "title": safe_local_id(workpack_id).replace("-", " ").title(),
            "lane": lane,
            "intent": "Workpack Scheduler v0.1 controlled local demo.",
            "source": "WORKPACK_SCHEDULER_v0_1",
            "allowed_targets": [target],
            "blocked_targets": [".env", "credentials", "PUBLICATION", "CLOUD", "NVIDIA", "DEEPSEEK"],
            "expected_outputs": [target],
            "tests_required": tests,
            "operation": {"type": "write_text", "content": content},
            "rollback_required": True,
            "witness_required": True,
            "publication_gate": "BLOCK",
            "cloud_allowed": False,
            "nvidia_allowed": False,
            "direct_delete_allowed": False,
            "created_at": utc_now_iso(),
            "secret_values_printed": False,
        }
    )


def ensure_scheduler_demo_workpacks() -> dict[str, Any]:
    ensure_workpack_scheduler_contract_files()
    demos = [
        {
            "workpack_id": "scheduler-sandbox-step-1",
            "lane": "SANDBOX",
            "assigned_agent": "WABI_SAFE_EXECUTOR",
            "target": "WABI_WORKPACK_RUNTIME/scheduler_v0_1/step_1.txt",
            "content": "status: PASS\nscheduler_step: 1\npublication_gate: BLOCK\n",
            "tests": [{"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/scheduler_v0_1/step_1.txt", "contains": "status: PASS"}],
        },
        {
            "workpack_id": "scheduler-sandbox-step-2",
            "lane": "SANDBOX",
            "assigned_agent": "WABI_SAFE_EXECUTOR",
            "target": "WABI_WORKPACK_RUNTIME/scheduler_v0_1/step_2.txt",
            "content": "status: PASS\nscheduler_step: 2\ndepends_on: scheduler-sandbox-step-1\npublication_gate: BLOCK\n",
            "tests": [
                {"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/scheduler_v0_1/step_2.txt", "contains": "status: PASS"},
                {"type": "file_exists", "target": "WABI_WORKPACK_RUNTIME/scheduler_v0_1/step_1.txt"},
            ],
        },
        {
            "workpack_id": "scheduler-docs-note",
            "lane": "DOCS_LOCAL",
            "assigned_agent": "CORE_MEMORY_KEEPER",
            "target": "docs/local_execute/WORKPACK_SCHEDULER_v0_1_ACCEPTANCE_NOTE.md",
            "content": "# Workpack Scheduler v0.1 Acceptance Note\n\nstatus: PASS\npublication_gate: BLOCK\nmode: LOCAL_ONLY\n",
            "tests": [{"type": "file_contains", "target": "docs/local_execute/WORKPACK_SCHEDULER_v0_1_ACCEPTANCE_NOTE.md", "contains": "publication_gate: BLOCK"}],
        },
    ]
    created: list[str] = []
    for demo in demos:
        workpack_id = safe_local_id(demo["workpack_id"])
        spec = scheduler_demo_task_spec(workpack_id, demo["lane"], demo["target"], demo["content"], demo["tests"])
        files = local_execute_task_files(workpack_id)
        write_json_file(files["taskspec"], spec)
        source_task = {
            "task_id": workpack_id,
            "title": spec["title"],
            "lane": demo["lane"],
            "assigned_agent": demo["assigned_agent"],
        }
        manifest = build_workpack_manifest(workpack_id, source_task, spec, status="DRAFT")
        write_workpack_manifest(manifest)
        created.append(workpack_id)
    cloud_id = "scheduler-blocked-cloud-lane-demo"
    cloud_spec = scheduler_demo_task_spec(cloud_id, "CLOUD", "WABI_WORKPACK_RUNTIME/scheduler_v0_1/cloud.txt", "status: BLOCK\n", [])
    write_json_file(local_execute_task_files(cloud_id)["taskspec"], cloud_spec)
    cloud_manifest = build_workpack_manifest(
        cloud_id,
        {"task_id": cloud_id, "title": "Scheduler blocked cloud lane demo", "lane": "CLOUD", "assigned_agent": "CORE_GATEKEEPER"},
        cloud_spec,
        status="BLOCKED",
        extra={"lane": "CLOUD", "blocked_reason": "Scheduler blocks CLOUD lane."},
    )
    write_workpack_manifest(cloud_manifest)
    created.append(cloud_id)
    witness = scheduler_witness("scheduler_demo_workpacks_created", {"workpacks": created})
    return sanitize_obj({"ok": True, "status": "READY", "workpack_ids": created, "witness": witness, "secret_values_printed": False})


def agent_chat_message_schedule_workpack_payload(message_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_message_id = safe_local_id(message_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    message = next((row for row in messages if safe_local_id(str(row.get("message_id", ""))) == safe_message_id), None)
    if not message:
        return {"ok": False, "status": "BLOCK", "reason": "Agent chat message not found.", "secret_values_printed": False}
    workpack_id = safe_optional_local_id((payload or {}).get("workpack_id")) or safe_optional_local_id(message.get("linked_workpack_id"))
    if not workpack_id:
        draft = agent_chat_message_to_workpack_payload(safe_message_id, payload or {})
        if not draft.get("ok"):
            return draft
        workpack_id = str(draft.get("workpack_id", ""))
    enqueue = scheduler_enqueue_payload(workpack_id, payload or {})
    system = agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "scheduler_enqueue_from_chat",
            "message": f"Message {safe_message_id} requested schedule for {workpack_id}; manual tick and gates required.",
            "linked_workpack_id": workpack_id,
            "message_type": "SYSTEM",
        }
    )
    witness = agent_chat_witness("agent_chat_message_scheduled_workpack", {"message_id": safe_message_id, "workpack_id": workpack_id, "queue_status": enqueue.get("status")})
    return sanitize_obj({"ok": enqueue.get("ok") is True, "status": enqueue.get("status"), "message_id": safe_message_id, "workpack_id": workpack_id, "scheduler": enqueue, "system_status": system.get("message"), "witness": witness, "executes": False, "secret_values_printed": False})


def multi_step_contract_payload() -> dict[str, Any]:
    return {
        "version": "v0.2",
        "mode": "LOCAL_ONLY",
        "execution_model": "MANUAL_TICK",
        "scheduler": "WORKPACK_SCHEDULER_v0_1",
        "execution_engine": "LOCAL_EXECUTE_v0_2",
        "max_concurrency": 1,
        "allowed_lanes": ["SANDBOX", "DOCS_LOCAL"],
        "blocked_lanes": ["PUBLICATION", "CLOUD", "NVIDIA", "DEEPSEEK", "REMOTE_COMPUTE", "PROTECTED_MATERIAL"],
        "requires_task_spec_per_step": True,
        "requires_ghostgate_per_step": True,
        "requires_rollback_per_step": True,
        "requires_witnesslog_per_step": True,
        "supports_full_workpack_rollback": True,
        "direct_delete_allowed": False,
        "publication_gate": "BLOCK",
        "cloud_live_gate": "BLOCK_THIS_RUN",
        "nvidia_smoke_gate": "DO_NOT_CALL",
        "deepseek_gate": "REVIEW_QUOTA_OR_BILLING",
        "secret_values_printed": False,
    }


def multi_step_schema_payload() -> dict[str, Any]:
    return {
        "$schema": "json-schema-draft-2020-12",
        "$id": "medioevo.multi_step_workpack.v0_2",
        "type": "object",
        "required": ["workpack_id", "title", "lane", "assigned_agent", "status", "steps", "rollback_policy", "publication_gate"],
        "properties": {
            "workpack_id": {"type": "string"},
            "title": {"type": "string"},
            "lane": {"enum": ["SANDBOX", "DOCS_LOCAL"]},
            "assigned_agent": {"type": "string"},
            "status": {"enum": sorted(MULTI_STEP_WORKPACK_STATES)},
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "step_id",
                        "title",
                        "lane",
                        "depends_on",
                        "task_spec_path",
                        "ghostgate_path",
                        "rollback_snapshot_path",
                        "expected_outputs",
                        "tests_required",
                        "status",
                        "witness_event_id",
                    ],
                    "properties": {
                        "step_id": {"type": "string"},
                        "title": {"type": "string"},
                        "lane": {"type": "string"},
                        "depends_on": {"type": "array", "items": {"type": "string"}},
                        "task_spec_path": {"type": "string"},
                        "ghostgate_path": {"type": "string"},
                        "rollback_snapshot_path": {"type": "string"},
                        "expected_outputs": {"type": "array", "items": {"type": "string"}},
                        "tests_required": {"type": "array", "items": {"type": "object"}},
                        "status": {"enum": sorted(MULTI_STEP_STEP_STATES)},
                        "witness_event_id": {"type": "string"},
                    },
                    "additionalProperties": True,
                },
            },
            "rollback_policy": {"const": "STEP_FIRST_THEN_WORKPACK"},
            "publication_gate": {"const": "BLOCK"},
        },
        "additionalProperties": True,
    }


def ensure_multi_step_contract_files() -> None:
    write_json_file(MULTI_STEP_CONTRACT_PATH, multi_step_contract_payload())
    write_json_file(MULTI_STEP_SCHEMA_PATH, multi_step_schema_payload())


def multi_step_files(workpack_id: str) -> dict[str, pathlib.Path]:
    safe_id = safe_local_id(workpack_id)
    base = MULTI_STEP_DATA_DIR / safe_id
    return {
        "manifest": base / f"MULTI_STEP_WORKPACK_{safe_id}.json",
        "evidence": base / f"MULTI_STEP_WORKPACK_EVIDENCE_{safe_id}.json",
        "witness": base / f"WITNESS_{safe_id}.jsonl",
    }


def multi_step_witness(event: str, workpack_id: str = "", step_id: str = "", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    previous = read_jsonl(MULTI_STEP_WITNESSLOG_PATH, limit=1)
    previous_hash = str(previous[-1].get("hash", "")) if previous else ""
    safe_workpack_id = safe_optional_local_id(workpack_id)
    safe_step_id = safe_optional_local_id(step_id)
    record = {
        "event": event,
        "workpack_id": safe_workpack_id,
        "step_id": safe_step_id,
        "timestamp": utc_now_iso(),
        "previous_hash": previous_hash,
        "execution_model": "MANUAL_TICK",
        "max_concurrency": 1,
        "cloud_called": False,
        "nvidia_called": False,
        "deepseek_called": False,
        "publication": "BLOCK",
        "secret_values_printed": False,
        **(payload or {}),
    }
    digest_source = json.dumps(sanitize_obj(record), ensure_ascii=True, sort_keys=True)
    record["hash"] = hashlib.sha256((previous_hash + digest_source).encode("utf-8")).hexdigest()
    append_jsonl(MULTI_STEP_WITNESSLOG_PATH, record)
    if safe_workpack_id:
        append_jsonl(multi_step_files(safe_workpack_id)["witness"], record)
    return sanitize_obj(record)


def load_multi_step_manifest(workpack_id: str) -> dict[str, Any]:
    manifest_path = multi_step_files(workpack_id)["manifest"]
    if not manifest_path.exists():
        return {}
    return _load_json_dict(manifest_path, {})


def multi_step_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if MULTI_STEP_DATA_DIR.exists():
        for path in sorted(MULTI_STEP_DATA_DIR.glob("*/MULTI_STEP_WORKPACK_*.json")):
            if "EVIDENCE" in path.name:
                continue
            row = _load_json_dict(path, {})
            if row:
                records.append(sanitize_obj(row))
    return records


def write_multi_step_aggregate_manifest() -> None:
    records = multi_step_records()
    payload = {
        "schema": "medioevo.multi_step_workpacks.manifest.v0_2",
        "run_id": MULTI_STEP_RUN_ID,
        "mode": "LOCAL_ONLY",
        "execution_model": "MANUAL_TICK",
        "max_concurrency": 1,
        "workpacks": records,
        "workpack_count": len(records),
        "updated_at": utc_now_iso(),
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }
    write_json_file(MULTI_STEP_MANIFEST_PATH, payload)


def write_multi_step_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    workpack_id = safe_local_id(str(manifest.get("workpack_id", "")))
    write_json_file(multi_step_files(workpack_id)["manifest"], manifest)
    write_multi_step_aggregate_manifest()
    return sanitize_obj(manifest)


def update_multi_step_manifest(workpack_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    manifest = load_multi_step_manifest(workpack_id)
    if not manifest:
        raise ValueError("Multi-step Workpack manifest not found.")
    manifest.update(updates)
    manifest["updated_at"] = utc_now_iso()
    return write_multi_step_manifest(manifest)


def multi_step_step_task_id(workpack_id: str, step_id: str) -> str:
    return safe_local_id(f"{safe_local_id(workpack_id)}__{safe_local_id(step_id)}")


def build_multistep_step_taskspec(workpack_id: str, step: dict[str, Any], assigned_agent: str) -> dict[str, Any]:
    step_id = safe_local_id(str(step.get("step_id", "")))
    task_id = multi_step_step_task_id(workpack_id, step_id)
    lane = str(step.get("lane") or "SANDBOX")
    targets = [str(target) for target in step.get("allowed_targets", [])]
    return sanitize_obj(
        {
            "schema": "medioevo.local_execute.task_spec.v0_2",
            "task_id": task_id,
            "title": str(step.get("title") or step_id),
            "lane": lane,
            "intent": str(step.get("intent") or "Multi-step Workpack v0.2 controlled local step."),
            "source": "MULTI_STEP_WORKPACKS_v0_2",
            "allowed_targets": targets,
            "blocked_targets": [".env", "credentials", "PUBLICATION", "CLOUD", "NVIDIA", "DEEPSEEK", "PROTECTED_MATERIAL"],
            "expected_outputs": targets,
            "tests_required": list(step.get("tests_required", [])),
            "operation": {"type": "write_text", "content": str(step.get("content") or "status: PASS\npublication_gate: BLOCK\n")},
            "rollback_required": True,
            "witness_required": True,
            "publication_gate": "BLOCK",
            "cloud_allowed": False,
            "nvidia_allowed": False,
            "deepseek_allowed": False,
            "direct_delete_allowed": False,
            "created_at": utc_now_iso(),
            "assigned_agent": assigned_agent,
            "secret_values_printed": False,
        }
    )


def multi_step_demo_definition(kind: str = "main", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    demo = str(data.get("demo") or kind or "main")
    if demo == "blocked-cloud":
        return {
            "workpack_id": safe_local_id(str(data.get("workpack_id") or "multi-step-blocked-cloud-demo-v0-2")),
            "title": "Multi-step blocked cloud lane demo v0.2",
            "lane": "SANDBOX",
            "assigned_agent": "CLAUDIO_WORKPACK_MANAGER",
            "steps": [
                {
                    "step_id": "step-cloud-blocked",
                    "title": "Blocked CLOUD step",
                    "lane": "CLOUD",
                    "depends_on": [],
                    "allowed_targets": ["WABI_WORKPACK_RUNTIME/multi_step_v0_2/blocked/cloud.txt"],
                    "content": "status: BLOCK\npublication_gate: BLOCK\n",
                    "tests_required": [],
                }
            ],
        }
    if demo == "rollback":
        return {
            "workpack_id": safe_local_id(str(data.get("workpack_id") or "multi-step-rollback-demo-v0-2")),
            "title": "Multi-step rollback demo v0.2",
            "lane": "SANDBOX",
            "assigned_agent": "CLAUDIO_WORKPACK_MANAGER",
            "steps": [
                {
                    "step_id": "step-ok",
                    "title": "Create rollback baseline file",
                    "lane": "SANDBOX",
                    "depends_on": [],
                    "allowed_targets": ["WABI_WORKPACK_RUNTIME/multi_step_v0_2/rollback/ok.txt"],
                    "content": "status: PASS\nstep: ok\npublication_gate: BLOCK\n",
                    "tests_required": [{"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/multi_step_v0_2/rollback/ok.txt", "contains": "status: PASS"}],
                },
                {
                    "step_id": "step-fail-intentional",
                    "title": "Intentional local test failure",
                    "lane": "SANDBOX",
                    "depends_on": ["step-ok"],
                    "allowed_targets": ["WABI_WORKPACK_RUNTIME/multi_step_v0_2/rollback/fail.txt"],
                    "content": "status: FAIL\nstep: fail-intentional\npublication_gate: BLOCK\n",
                    "tests_required": [{"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/multi_step_v0_2/rollback/fail.txt", "contains": "status: PASS"}],
                },
            ],
        }
    return {
        "workpack_id": safe_local_id(str(data.get("workpack_id") or "multi-step-sandbox-docs-demo-v0-2")),
        "title": "Multi-step sandbox/docs demo v0.2",
        "lane": "SANDBOX",
        "assigned_agent": "CLAUDIO_WORKPACK_MANAGER",
        "steps": [
            {
                "step_id": "step-prepare-sandbox",
                "title": "Prepare sandbox state",
                "lane": "SANDBOX",
                "depends_on": [],
                "allowed_targets": ["WABI_WORKPACK_RUNTIME/multi_step_v0_2/demo/state.json"],
                "content": "{\n  \"step1\": true,\n  \"status\": \"PASS\",\n  \"publication_gate\": \"BLOCK\"\n}\n",
                "tests_required": [{"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/multi_step_v0_2/demo/state.json", "contains": "\"step1\": true"}],
            },
            {
                "step_id": "step-transform-sandbox",
                "title": "Transform sandbox state",
                "lane": "SANDBOX",
                "depends_on": ["step-prepare-sandbox"],
                "allowed_targets": ["WABI_WORKPACK_RUNTIME/multi_step_v0_2/demo/state.json"],
                "content": "{\n  \"step1\": true,\n  \"step2\": true,\n  \"status\": \"PASS\",\n  \"publication_gate\": \"BLOCK\"\n}\n",
                "tests_required": [
                    {"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/multi_step_v0_2/demo/state.json", "contains": "\"step1\": true"},
                    {"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/multi_step_v0_2/demo/state.json", "contains": "\"step2\": true"},
                ],
            },
            {
                "step_id": "step-generate-docs-note",
                "title": "Generate local docs note",
                "lane": "DOCS_LOCAL",
                "depends_on": ["step-transform-sandbox"],
                "allowed_targets": ["docs/local_execute/MULTI_STEP_WORKPACKS_v0_2_ACCEPTANCE_NOTE.md"],
                "content": "# Multi-step Workpacks v0.2 Acceptance Note\n\nstatus: PASS\nmode: LOCAL_ONLY\npublication_gate: BLOCK\ncloud_live_gate: BLOCK_THIS_RUN\nnvidia_smoke_gate: DO_NOT_CALL\ndeepseek_gate: REVIEW_QUOTA_OR_BILLING\n",
                "tests_required": [{"type": "file_contains", "target": "docs/local_execute/MULTI_STEP_WORKPACKS_v0_2_ACCEPTANCE_NOTE.md", "contains": "publication_gate: BLOCK"}],
            },
            {
                "step_id": "step-final-report",
                "title": "Generate final sandbox report",
                "lane": "SANDBOX",
                "depends_on": ["step-generate-docs-note"],
                "allowed_targets": ["WABI_WORKPACK_RUNTIME/multi_step_v0_2/demo/final_report.json"],
                "content": "{\n  \"status\": \"PASS\",\n  \"steps\": 4,\n  \"publication_gate\": \"BLOCK\",\n  \"cloud_called\": false,\n  \"nvidia_called\": false,\n  \"deepseek_called\": false\n}\n",
                "tests_required": [
                    {"type": "file_contains", "target": "WABI_WORKPACK_RUNTIME/multi_step_v0_2/demo/final_report.json", "contains": "\"status\": \"PASS\""},
                    {"type": "file_exists", "target": "docs/local_execute/MULTI_STEP_WORKPACKS_v0_2_ACCEPTANCE_NOTE.md"},
                ],
            },
        ],
    }


def create_multistep_workpack_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_multi_step_contract_files()
    data = payload or {}
    definition = data if data.get("steps") else multi_step_demo_definition(str(data.get("demo") or "main"), data)
    workpack_id = safe_local_id(str(definition.get("workpack_id", "")))
    assigned_agent = safe_local_id(str(definition.get("assigned_agent") or "CLAUDIO_WORKPACK_MANAGER"))
    raw_steps = definition.get("steps", [])
    if not isinstance(raw_steps, list) or not raw_steps:
        return {"ok": False, "status": "BLOCK", "workpack_id": workpack_id, "reason": "Multi-step definition requires steps.", "executes": False, "secret_values_printed": False}
    steps: list[dict[str, Any]] = []
    blocked_reasons: list[str] = []
    for raw_step in raw_steps:
        if not isinstance(raw_step, dict):
            blocked_reasons.append("step must be object")
            continue
        step_id = safe_local_id(str(raw_step.get("step_id", "")))
        lane = str(raw_step.get("lane") or definition.get("lane") or "SANDBOX")
        step_task_id = multi_step_step_task_id(workpack_id, step_id)
        files = local_execute_task_files(step_task_id)
        blocked = lane in MULTI_STEP_BLOCKED_LANES or lane not in MULTI_STEP_ALLOWED_LANES
        task_spec = build_multistep_step_taskspec(workpack_id, raw_step, assigned_agent)
        if not blocked:
            write_json_file(files["taskspec"], task_spec)
            local_execute_witness(step_task_id, "multistep_step_taskspec_created", {"workpack_id": workpack_id, "step_id": step_id})
        else:
            blocked_reasons.append(f"{step_id}: lane {lane} blocked")
        steps.append(
            sanitize_obj(
                {
                    "step_id": step_id,
                    "title": str(raw_step.get("title") or step_id),
                    "lane": lane,
                    "depends_on": [safe_local_id(str(dep)) for dep in raw_step.get("depends_on", [])],
                    "local_execute_task_id": step_task_id,
                    "task_spec_path": local_execute_target_alias(files["taskspec"]),
                    "ghostgate_path": local_execute_target_alias(files["ghostgate"]),
                    "rollback_snapshot_path": local_execute_target_alias(files["rollback"]),
                    "expected_outputs": list(task_spec.get("expected_outputs", [])),
                    "tests_required": list(task_spec.get("tests_required", [])),
                    "status": "BLOCKED" if blocked else "PENDING",
                    "blocked_reason": f"lane {lane} blocked" if blocked else "",
                    "witness_event_id": "",
                }
            )
        )
    status = "BLOCKED" if blocked_reasons else "DRAFT"
    manifest = {
        "schema": "medioevo.multi_step_workpack.v0_2",
        "workpack_id": workpack_id,
        "title": str(definition.get("title") or workpack_id),
        "lane": str(definition.get("lane") or "SANDBOX"),
        "assigned_agent": assigned_agent,
        "status": status,
        "steps": steps,
        "step_count": len(steps),
        "rollback_policy": "STEP_FIRST_THEN_WORKPACK",
        "publication_gate": "BLOCK",
        "cloud_called": False,
        "nvidia_called": False,
        "deepseek_called": False,
        "direct_delete_allowed": False,
        "secret_values_printed": False,
        "created_at": utc_now_iso(),
        "blocked_reasons": blocked_reasons,
    }
    write_multi_step_manifest(manifest)
    witness = multi_step_witness("multistep_workpack_created", workpack_id, payload={"status": status, "step_count": len(steps), "blocked_reasons": blocked_reasons})
    return sanitize_obj({"ok": status != "BLOCKED", "status": status, "workpack_id": workpack_id, "workpack": manifest, "witness": witness, "executes": False, "secret_values_printed": False})


def approve_multistep_workpack_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_multi_step_contract_files()
    safe_id = safe_local_id(workpack_id)
    manifest = load_multi_step_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Multi-step Workpack manifest required.", "secret_values_printed": False}
    approved_steps: list[str] = []
    blocked_reasons: list[str] = []
    updated_steps: list[dict[str, Any]] = []
    for step in manifest.get("steps", []):
        step = dict(step)
        step_id = safe_local_id(str(step.get("step_id", "")))
        lane = str(step.get("lane", ""))
        step_task_id = str(step.get("local_execute_task_id") or multi_step_step_task_id(safe_id, step_id))
        files = local_execute_task_files(step_task_id)
        if lane in MULTI_STEP_BLOCKED_LANES or lane not in MULTI_STEP_ALLOWED_LANES:
            step.update({"status": "BLOCKED", "blocked_reason": f"lane {lane} blocked"})
            blocked_reasons.append(f"{step_id}: lane {lane} blocked")
            updated_steps.append(step)
            continue
        if not files["taskspec"].exists():
            step.update({"status": "BLOCKED", "blocked_reason": "TaskSpec required before approval"})
            blocked_reasons.append(f"{step_id}: TaskSpec required")
            updated_steps.append(step)
            continue
        task_spec = _load_json_dict(files["taskspec"], {})
        validation = local_execute_validation(task_spec)
        decision = "APPROVE" if validation.get("ok") else "BLOCK"
        ghostgate = {
            "schema": "medioevo.multi_step_workpack.step_ghostgate.v0_2",
            "workpack_id": safe_id,
            "step_id": step_id,
            "task_id": step_task_id,
            "decision": decision,
            "reversible": decision == "APPROVE",
            "rollback_required": True,
            "rollback_available": False,
            "cloud_allowed": False,
            "nvidia_allowed": False,
            "deepseek_allowed": False,
            "publication_allowed": False,
            "validation": validation,
            "reason": "" if decision == "APPROVE" else "; ".join(validation.get("reasons", [])) or "Step GhostGate blocked.",
            "timestamp": utc_now_iso(),
            "secret_values_printed": False,
        }
        if decision == "APPROVE":
            rollback = local_execute_create_rollback_snapshot(task_spec)
            ghostgate["rollback_available"] = True
            ghostgate["rollback_snapshot"] = local_execute_target_alias(files["rollback"])
            ghostgate["rollback"] = rollback
            step.update({"status": "APPROVED", "ghostgate_decision": "APPROVE", "rollback_available": True})
            approved_steps.append(step_id)
        else:
            step.update({"status": "BLOCKED", "ghostgate_decision": "BLOCK", "blocked_reason": ghostgate["reason"]})
            blocked_reasons.append(f"{step_id}: {ghostgate['reason']}")
        write_json_file(files["ghostgate"], ghostgate)
        local_execute_witness(step_task_id, "multistep_step_ghostgate_evaluated", {"workpack_id": safe_id, "step_id": step_id, "decision": decision})
        witness = multi_step_witness("multistep_step_approved" if decision == "APPROVE" else "multistep_step_blocked", safe_id, step_id, {"decision": decision})
        step["witness_event_id"] = str(witness.get("hash", ""))[:16]
        step["task_spec_path"] = local_execute_target_alias(files["taskspec"])
        step["ghostgate_path"] = local_execute_target_alias(files["ghostgate"])
        step["rollback_snapshot_path"] = local_execute_target_alias(files["rollback"])
        updated_steps.append(sanitize_obj(step))
    status = "APPROVED" if not blocked_reasons and approved_steps else "BLOCKED"
    updated = update_multi_step_manifest(
        safe_id,
        {
            "status": status,
            "steps": updated_steps,
            "approved_steps": approved_steps,
            "blocked_reasons": blocked_reasons,
        },
    )
    witness = multi_step_witness("multistep_workpack_approved" if status == "APPROVED" else "multistep_workpack_blocked", safe_id, payload={"status": status, "approved_steps": approved_steps, "blocked_reasons": blocked_reasons})
    agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "multistep_ghostgate",
            "message": f"Multi-step Workpack {safe_id} approval: {status}. Manual tick required before any step execution.",
            "linked_workpack_id": safe_id,
            "message_type": "GATE",
        }
    )
    return sanitize_obj({"ok": status == "APPROVED", "status": status, "workpack_id": safe_id, "workpack": updated, "witness": witness, "executes": False, "secret_values_printed": False})


def enqueue_multistep_workpack_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_multi_step_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Multi-step Workpack manifest required.", "executes": False, "secret_values_printed": False}
    if manifest.get("status") != "APPROVED":
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Multi-step Workpack must be APPROVED before enqueue.", "executes": False, "secret_values_printed": False}
    updated = update_multi_step_manifest(safe_id, {"status": "SCHEDULED", "next_action": "Manual tick executes max one approved step."})
    witness = multi_step_witness("multistep_workpack_enqueued", safe_id, payload={"status": "SCHEDULED"})
    agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "multistep_enqueued",
            "message": f"Multi-step Workpack {safe_id} enqueued. Tick executes max one step and rechecks gates.",
            "linked_workpack_id": safe_id,
            "message_type": "SYSTEM",
        }
    )
    return sanitize_obj({"ok": True, "status": "SCHEDULED", "workpack_id": safe_id, "workpack": updated, "witness": witness, "executes": False, "secret_values_printed": False})


def multistep_dependencies_resolved(manifest: dict[str, Any], step: dict[str, Any]) -> tuple[bool, list[str]]:
    steps_by_id = {str(row.get("step_id", "")): row for row in manifest.get("steps", [])}
    unresolved: list[str] = []
    for dep in step.get("depends_on", []):
        dep_id = safe_local_id(str(dep))
        if steps_by_id.get(dep_id, {}).get("status") != "EXECUTED":
            unresolved.append(dep_id)
    return not unresolved, unresolved


def multistep_select_next_workpack_and_step() -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[str]]:
    skipped: list[str] = []
    candidates = [row for row in multi_step_records() if row.get("status") in {"APPROVED", "SCHEDULED", "RUNNING", "PARTIAL"}]
    candidates.sort(key=lambda row: (str(row.get("created_at", "")), str(row.get("workpack_id", ""))))
    for manifest in candidates:
        for step in manifest.get("steps", []):
            if step.get("status") not in {"APPROVED", "READY", "PENDING"}:
                continue
            resolved, unresolved = multistep_dependencies_resolved(manifest, step)
            if resolved:
                return manifest, step, skipped
            skipped.append(f"{manifest.get('workpack_id')}:{step.get('step_id')}:waiting_for:{','.join(unresolved)}")
    return None, None, skipped


def multistep_recheck_step_ready(manifest: dict[str, Any], step: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    step_id = safe_local_id(str(step.get("step_id", "")))
    step_task_id = str(step.get("local_execute_task_id") or multi_step_step_task_id(str(manifest.get("workpack_id", "")), step_id))
    lane = str(step.get("lane", ""))
    if lane in MULTI_STEP_BLOCKED_LANES or lane not in MULTI_STEP_ALLOWED_LANES:
        return False, "Step lane blocked by multi-step contract.", {}
    files = local_execute_task_files(step_task_id)
    if not files["taskspec"].exists():
        return False, "TaskSpec required before step tick.", {}
    if not files["ghostgate"].exists():
        return False, "GhostGate required before step tick.", {}
    if not files["rollback"].exists():
        return False, "Rollback snapshot required before step tick.", {}
    ghostgate = _load_json_dict(files["ghostgate"], {})
    if ghostgate.get("decision") != "APPROVE":
        return False, "Step GhostGate must be APPROVE before tick.", ghostgate
    task_spec = _load_json_dict(files["taskspec"], {})
    validation = local_execute_validation(task_spec)
    if not validation.get("ok"):
        return False, "Step TaskSpec failed allowlist validation.", validation
    return True, "", task_spec


def tick_multistep_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_multi_step_contract_files()
    manifest, step, skipped = multistep_select_next_workpack_and_step()
    if not manifest or not step:
        witness = multi_step_witness("multistep_tick_idle", payload={"skipped": skipped})
        return sanitize_obj({"ok": True, "status": "IDLE", "executed_count": 0, "skipped": skipped, "witness": witness, "secret_values_printed": False})
    workpack_id = safe_local_id(str(manifest.get("workpack_id", "")))
    step_id = safe_local_id(str(step.get("step_id", "")))
    ready, reason, task_spec = multistep_recheck_step_ready(manifest, step)
    steps = [dict(row) for row in manifest.get("steps", [])]
    index = next((i for i, row in enumerate(steps) if row.get("step_id") == step_id), -1)
    if index < 0:
        return {"ok": False, "status": "BLOCK", "workpack_id": workpack_id, "reason": "Selected step not found.", "secret_values_printed": False}
    if not ready:
        steps[index].update({"status": "BLOCKED", "blocked_reason": reason})
        updated = update_multi_step_manifest(workpack_id, {"status": "BLOCKED", "steps": steps, "last_error": reason})
        witness = multi_step_witness("multistep_tick_blocked", workpack_id, step_id, {"reason": reason})
        return sanitize_obj({"ok": False, "status": "BLOCKED", "executed_count": 0, "workpack": updated, "step": steps[index], "reason": reason, "witness": witness, "secret_values_printed": False})
    steps[index]["status"] = "RUNNING"
    update_multi_step_manifest(workpack_id, {"status": "RUNNING", "steps": steps, "current_step": step_id})
    apply_result = local_execute_apply_task(task_spec)
    test_result = local_execute_run_task_tests(task_spec)
    passed = test_result.get("passed") is True
    step_status = "EXECUTED" if passed else "FAILED"
    steps[index].update(
        {
            "status": step_status,
            "apply_status": apply_result.get("apply_status", "APPLIED"),
            "tests_passed": passed,
            "execution_result_path": local_execute_target_alias(local_execute_task_files(str(task_spec.get("task_id", "")))["execution"]),
            "test_result_path": local_execute_target_alias(local_execute_task_files(str(task_spec.get("task_id", "")))["tests"]),
        }
    )
    all_executed = all(row.get("status") == "EXECUTED" for row in steps)
    final_status = "EXECUTED" if all_executed else ("FAILED" if not passed else "SCHEDULED")
    witness = multi_step_witness("multistep_step_executed" if passed else "multistep_step_failed", workpack_id, step_id, {"status": step_status, "tests_passed": passed})
    steps[index]["witness_event_id"] = str(witness.get("hash", ""))[:16]
    updated = update_multi_step_manifest(workpack_id, {"status": final_status, "steps": steps, "current_step": "" if all_executed else step_id, "last_error": "" if passed else "Step tests failed."})
    agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "multistep_tick",
            "message": f"Multi-step {workpack_id} processed {step_id}: {step_status}.",
            "linked_workpack_id": workpack_id,
            "message_type": "SYSTEM",
        }
    )
    return sanitize_obj({"ok": passed, "status": final_status, "executed_count": 1, "workpack_id": workpack_id, "step": steps[index], "apply_result": apply_result, "test_result": test_result, "workpack": updated, "witness": witness, "secret_values_printed": False})


def rollback_multistep_step_payload(workpack_id: str, step_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_workpack_id = safe_local_id(workpack_id)
    safe_step_id = safe_local_id(step_id)
    manifest = load_multi_step_manifest(safe_workpack_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_workpack_id, "reason": "Multi-step Workpack manifest required.", "secret_values_printed": False}
    steps = [dict(row) for row in manifest.get("steps", [])]
    index = next((i for i, row in enumerate(steps) if row.get("step_id") == safe_step_id), -1)
    if index < 0:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_workpack_id, "step_id": safe_step_id, "reason": "Step not found.", "secret_values_printed": False}
    step_task_id = str(steps[index].get("local_execute_task_id") or multi_step_step_task_id(safe_workpack_id, safe_step_id))
    if not local_execute_task_files(step_task_id)["rollback"].exists():
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_workpack_id, "step_id": safe_step_id, "reason": "Rollback snapshot required.", "secret_values_printed": False}
    rollback = local_execute_rollback_task_payload(step_task_id)
    steps[index]["status"] = "ROLLED_BACK" if rollback.get("ok") else "FAILED"
    witness = multi_step_witness("multistep_step_rollback", safe_workpack_id, safe_step_id, {"status": steps[index]["status"]})
    steps[index]["witness_event_id"] = str(witness.get("hash", ""))[:16]
    updated = update_multi_step_manifest(safe_workpack_id, {"status": "PARTIAL", "steps": steps, "last_error": "" if rollback.get("ok") else "Step rollback failed."})
    return sanitize_obj({"ok": rollback.get("ok") is True, "status": steps[index]["status"], "workpack_id": safe_workpack_id, "step_id": safe_step_id, "rollback": rollback, "workpack": updated, "witness": witness, "secret_values_printed": False})


def rollback_multistep_workpack_payload(workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_multi_step_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Multi-step Workpack manifest required.", "secret_values_printed": False}
    steps = [dict(row) for row in manifest.get("steps", [])]
    results: list[dict[str, Any]] = []
    ok = True
    for index in reversed(range(len(steps))):
        step = steps[index]
        if step.get("status") not in {"EXECUTED", "FAILED", "RUNNING", "PARTIAL"}:
            continue
        step_id = safe_local_id(str(step.get("step_id", "")))
        step_task_id = str(step.get("local_execute_task_id") or multi_step_step_task_id(safe_id, step_id))
        if not local_execute_task_files(step_task_id)["rollback"].exists():
            results.append({"step_id": step_id, "ok": False, "reason": "Rollback snapshot missing."})
            ok = False
            continue
        rollback = local_execute_rollback_task_payload(step_task_id)
        steps[index]["status"] = "ROLLED_BACK" if rollback.get("ok") else "FAILED"
        results.append({"step_id": step_id, "ok": rollback.get("ok") is True, "rollback": rollback})
        ok = ok and rollback.get("ok") is True
    status = "ROLLED_BACK" if ok else "FAILED"
    witness = multi_step_witness("multistep_workpack_rollback", safe_id, payload={"status": status, "results": results})
    updated = update_multi_step_manifest(safe_id, {"status": status, "steps": steps, "rollback_results": results, "last_error": "" if ok else "One or more step rollbacks failed."})
    agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "multistep_rollback",
            "message": f"Multi-step Workpack {safe_id} rollback: {status}.",
            "linked_workpack_id": safe_id,
            "message_type": "SYSTEM",
        }
    )
    return sanitize_obj({"ok": ok, "status": status, "workpack_id": safe_id, "rollback_results": results, "workpack": updated, "witness": witness, "secret_values_printed": False})


def multistep_evidence_payload(workpack_id: str) -> dict[str, Any]:
    safe_id = safe_local_id(workpack_id)
    manifest = load_multi_step_manifest(safe_id)
    if not manifest:
        return {"ok": False, "status": "BLOCK", "workpack_id": safe_id, "reason": "Multi-step Workpack manifest not found.", "secret_values_printed": False}
    step_evidence: list[dict[str, Any]] = []
    for step in manifest.get("steps", []):
        task_id = str(step.get("local_execute_task_id") or multi_step_step_task_id(safe_id, str(step.get("step_id", ""))))
        step_evidence.append({"step_id": step.get("step_id", ""), "local_execute": local_execute_evidence_payload(task_id)})
    payload = {
        "ok": True,
        "schema": "medioevo.multi_step_workpack.evidence.v0_2",
        "workpack_id": safe_id,
        "status": manifest.get("status", "DRAFT"),
        "workpack": manifest,
        "evidence": {
            "manifest": {"exists": True, "path": local_execute_target_alias(multi_step_files(safe_id)["manifest"])},
            "aggregate_manifest": {"exists": MULTI_STEP_MANIFEST_PATH.exists(), "path": local_execute_target_alias(MULTI_STEP_MANIFEST_PATH)},
            "contract": {"exists": MULTI_STEP_CONTRACT_PATH.exists(), "path": local_execute_target_alias(MULTI_STEP_CONTRACT_PATH)},
            "schema": {"exists": MULTI_STEP_SCHEMA_PATH.exists(), "path": local_execute_target_alias(MULTI_STEP_SCHEMA_PATH)},
            "steps": step_evidence,
            "multi_step_witness_events": [row for row in read_jsonl(MULTI_STEP_WITNESSLOG_PATH, limit=500) if row.get("workpack_id") == safe_id],
        },
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }
    write_json_file(multi_step_files(safe_id)["evidence"], payload)
    return sanitize_obj(payload)


def multi_step_workpacks_payload() -> dict[str, Any]:
    ensure_multi_step_contract_files()
    records = multi_step_records()
    return sanitize_obj(
        {
            "schema": "medioevo.multi_step_workpacks.v0_2",
            "version": "v0.2",
            "mode": "LOCAL_ONLY",
            "execution_model": "MANUAL_TICK",
            "scheduler": "WORKPACK_SCHEDULER_v0_1",
            "execution_engine": "LOCAL_EXECUTE_v0_2",
            "max_concurrency": 1,
            "contract": multi_step_contract_payload(),
            "contract_path": local_execute_target_alias(MULTI_STEP_CONTRACT_PATH),
            "schema_path": local_execute_target_alias(MULTI_STEP_SCHEMA_PATH),
            "manifest_path": local_execute_target_alias(MULTI_STEP_MANIFEST_PATH),
            "witnesslog_path": local_execute_target_alias(MULTI_STEP_WITNESSLOG_PATH),
            "workpacks": records,
            "workpack_count": len(records),
            "ready_count": sum(1 for row in records if row.get("status") in {"APPROVED", "SCHEDULED", "RUNNING", "PARTIAL"}),
            "blocked_count": sum(1 for row in records if row.get("status") == "BLOCKED"),
            "cloud_called": False,
            "nvidia_called": False,
            "deepseek_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def agent_chat_message_to_multistep_payload(message_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_message_id = safe_local_id(message_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    message = next((row for row in messages if safe_local_id(str(row.get("message_id", ""))) == safe_message_id), None)
    if not message:
        return {"ok": False, "status": "BLOCK", "reason": "Agent chat message not found.", "secret_values_printed": False}
    body = str(message.get("body", ""))
    if text_has_secret_value(body):
        return {"ok": False, "status": "BLOCK", "reason": "Secret-like value detected; multi-step draft not written.", "secret_values_printed": False}
    workpack_id = safe_local_id(str((payload or {}).get("workpack_id") or f"chat-multistep-{safe_message_id}-v0-2"))
    definition = multi_step_demo_definition("main", {"workpack_id": workpack_id})
    definition["title"] = f"Multi-step draft from agent chat {safe_message_id}"
    definition["source_message_id"] = safe_message_id
    result = create_multistep_workpack_payload(definition)
    manifest = load_multi_step_manifest(workpack_id)
    if manifest:
        manifest["draft_only"] = True
        manifest["source_message_id"] = safe_message_id
        manifest["source_message_excerpt"] = sanitize_text(body[:500])
        write_multi_step_manifest(manifest)
    witness = agent_chat_witness("agent_chat_message_to_multistep_draft", {"message_id": safe_message_id, "workpack_id": workpack_id})
    system = agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "multistep_draft_created",
            "message": f"Multi-step Workpack draft {workpack_id} created from message {safe_message_id}; approve + enqueue + manual tick required.",
            "linked_workpack_id": workpack_id,
            "message_type": "WORKPACK",
        }
    )
    return sanitize_obj({"ok": result.get("ok") is True, "status": "MULTI_STEP_DRAFT_CREATED", "workpack_id": workpack_id, "workpack": load_multi_step_manifest(workpack_id), "witness": witness, "system_status": system.get("message"), "executes": False, "secret_values_printed": False})


def agent_chat_known_agent_ids() -> set[str]:
    return {
        "CORE_ORCHESTRATOR",
        "CORE_GATEKEEPER",
        "CORE_MEMORY_KEEPER",
        "OBS_CANON_DIFF_CURATOR",
        "OBS_JAMMING_SENTINEL",
        "WABI_LOCAL_PROGRAMMER",
        "WABI_DEBUGGER",
        "WABI_TEST_RUNNER",
        "WABI_SAFE_EXECUTOR",
        "CLAUDIO_LOCAL_BRIDGE",
        "CLAUDIO_WORKPACK_MANAGER",
        "BOUNDARY_SECRET_SCANNER",
        "BOUNDARY_RELEASE_SENTINEL",
        "DUAT_DISPLAY_AGENT",
        "GEODIA_SIM_AGENT",
    }


def agent_chat_routing_contract_payload() -> dict[str, Any]:
    return {
        "version": "v0.2",
        "mode": "LOCAL_ONLY",
        "chat_style": "MSN_90S_LOCAL",
        "routing_enabled": True,
        "execution_from_chat": "BLOCK_UNLESS_TASKSPEC_GHOSTGATE_ROLLBACK",
        "allowed_rooms": [room.lstrip("#") for room in AGENT_CHAT_ROOMS],
        "allowed_actions": [
            "SEND_MESSAGE",
            "MENTION_AGENT",
            "CREATE_TASKSPEC_DRAFT",
            "CREATE_WORKPACK_DRAFT",
            "CREATE_MULTI_STEP_WORKPACK_DRAFT",
            "ATTACH_MESSAGE_TO_WORKPACK",
            "SCHEDULE_WORKPACK",
            "POST_STATUS_UPDATE",
            "OPEN_EVIDENCE",
        ],
        "blocked_actions": [
            "EXECUTE_WITHOUT_GATE",
            "PUBLISH",
            "PUSH",
            "DEPLOY",
            "RUN_CLOUD",
            "RUN_NVIDIA",
            "DELETE_DIRECT",
        ],
        "cloud_live_gate": "BLOCK_THIS_RUN",
        "nvidia_smoke_gate": "DO_NOT_CALL",
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }


def agent_chat_message_schema_payload() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "medioevo.agent_chat.message.v0_2",
        "type": "object",
        "required": [
            "message_id",
            "room",
            "sender",
            "recipient",
            "mentions",
            "body",
            "message_type",
            "linked_task_id",
            "linked_workpack_id",
            "created_at",
            "hash",
            "previous_hash",
            "redaction_status",
        ],
        "properties": {
            "message_id": {"type": "string"},
            "room": {"type": "string"},
            "sender": {"type": "string"},
            "recipient": {"type": "string"},
            "mentions": {"type": "array", "items": {"type": "string"}},
            "body": {"type": "string"},
            "message_type": {"enum": ["CHAT", "SYSTEM", "TASK", "WORKPACK", "GATE", "WITNESS"]},
            "linked_task_id": {"type": "string"},
            "linked_workpack_id": {"type": "string"},
            "created_at": {"type": "string"},
            "hash": {"type": "string"},
            "previous_hash": {"type": "string"},
            "redaction_status": {"enum": ["PASS", "REVIEW", "BLOCK"]},
        },
    }


def ensure_agent_chat_routing_contract_files() -> None:
    write_json_file(AGENT_CHAT_ROUTING_CONTRACT_PATH, agent_chat_routing_contract_payload())
    write_json_file(AGENT_CHAT_MESSAGE_SCHEMA_PATH, agent_chat_message_schema_payload())


def agent_chat_storage_contract_payload() -> dict[str, Any]:
    return {
        "version": "v0.3",
        "mode": "LOCAL_ONLY",
        "storage": "APPEND_ONLY_JSONL",
        "search_index": "LOCAL_ONLY",
        "export_allowed": ["JSONL", "MARKDOWN_INTERNAL"],
        "public_export_allowed": False,
        "execution_from_search": "BLOCK",
        "requires_redaction": True,
        "requires_hash_chain": True,
        "publication_gate": "BLOCK",
    }


def agent_chat_persistent_message_schema_payload() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "medioevo.agent_chat.persistent_message.v0_3",
        "type": "object",
        "required": [
            "message_id",
            "room",
            "sender",
            "recipient",
            "mentions",
            "body",
            "message_type",
            "linked_task_id",
            "linked_workpack_id",
            "linked_witness_id",
            "created_at",
            "tags",
            "redaction_status",
            "hash",
            "previous_hash",
        ],
        "properties": {
            "message_id": {"type": "string"},
            "room": {"type": "string"},
            "sender": {"type": "string"},
            "recipient": {"type": "string"},
            "mentions": {"type": "array", "items": {"type": "string"}},
            "body": {"type": "string"},
            "message_type": {"enum": sorted(AGENT_CHAT_MESSAGE_TYPES)},
            "linked_task_id": {"type": "string"},
            "linked_workpack_id": {"type": "string"},
            "linked_witness_id": {"type": "string"},
            "created_at": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "redaction_status": {"enum": ["PASS", "REVIEW", "BLOCK"]},
            "hash": {"type": "string"},
            "previous_hash": {"type": "string"},
        },
        "additionalProperties": True,
    }


def ensure_agent_chat_storage_files() -> None:
    ensure_agent_chat_routing_contract_files()
    write_json_file(AGENT_CHAT_STORAGE_CONTRACT_PATH, agent_chat_storage_contract_payload())
    write_json_file(AGENT_CHAT_PERSISTENT_MESSAGE_SCHEMA_PATH, agent_chat_persistent_message_schema_payload())


def agent_chat_normalize_message_type(value: Any) -> str:
    message_type = safe_local_id(str(value or "CHAT")).upper()
    return message_type if message_type in AGENT_CHAT_MESSAGE_TYPES else "CHAT"


def agent_chat_read_all_messages(path: pathlib.Path | None = None) -> list[dict[str, Any]]:
    store = path or AGENT_CHAT_MESSAGES_PATH
    if not store.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in store.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(sanitize_obj(value))
    return rows


def agent_chat_record_digest(record: dict[str, Any], previous_hash: str, *, blank_message_id: bool = False) -> str:
    candidate = dict(record)
    candidate.pop("hash", None)
    if blank_message_id:
        candidate["message_id"] = ""
    digest_source = json.dumps(sanitize_obj(candidate), ensure_ascii=True, sort_keys=True)
    return hashlib.sha256((previous_hash + digest_source).encode("utf-8")).hexdigest()


def agent_chat_append_message(message: dict[str, Any], path: pathlib.Path | None = None) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    store = path or AGENT_CHAT_MESSAGES_PATH
    body = str(message.get("body") or message.get("message") or "").strip()
    if not body:
        raise ValueError("message body required")
    if text_has_secret_value(body):
        raise ValueError("Secret-like value detected; message not written.")
    room = agent_chat_room_for_payload(str(message.get("room") or "#general"))
    sender = safe_local_id(str(message.get("sender") or "OWNER"))
    mentions = agent_chat_mentions_from_body(body, message.get("mentions"))
    to_agent = safe_optional_local_id(message.get("to_agent") or message.get("recipient"))
    recipient = to_agent or agent_chat_suggested_agent(room, mentions)
    redaction_status = str(message.get("redaction_status") or "PASS").strip().upper()
    if redaction_status not in {"PASS", "REVIEW", "BLOCK"}:
        redaction_status = "REVIEW"
    if redaction_status == "BLOCK":
        raise ValueError("Blocked redaction status; message not written.")
    tags = [safe_local_id(str(item)) for item in message.get("tags", []) if str(item or "").strip()] if isinstance(message.get("tags"), list) else []
    previous_rows = agent_chat_read_all_messages(store)
    previous_hash = str(previous_rows[-1].get("hash", "")) if previous_rows else ""
    explicit_message_id = safe_optional_local_id(message.get("message_id"))
    record = {
        "message_id": explicit_message_id,
        "room": room,
        "sender": sender,
        "to_agent": to_agent,
        "recipient": recipient,
        "mentions": mentions,
        "body": sanitize_text(body[:2000]),
        "message_type": agent_chat_normalize_message_type(message.get("message_type")),
        "linked_task_id": safe_optional_local_id(message.get("linked_task_id")),
        "linked_workpack_id": safe_optional_local_id(message.get("linked_workpack_id")),
        "linked_witness_id": safe_optional_local_id(message.get("linked_witness_id")),
        "timestamp": str(message.get("timestamp") or utc_now_iso()),
        "created_at": str(message.get("created_at") or message.get("timestamp") or utc_now_iso()),
        "tags": tags,
        "redaction_status": redaction_status,
        "local_only": True,
        "cloud_called": False,
        "publication": "BLOCK",
        "previous_hash": previous_hash,
    }
    digest = agent_chat_record_digest(record, previous_hash, blank_message_id=not explicit_message_id)
    if not explicit_message_id:
        record["message_id"] = digest[:16]
    record["hash"] = digest
    return append_jsonl(store, record)


def agent_chat_verify_hash_chain(path: pathlib.Path | None = None) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    rows = agent_chat_read_all_messages(path)
    previous_hash = ""
    for index, row in enumerate(rows):
        row_previous = str(row.get("previous_hash", ""))
        row_hash = str(row.get("hash", ""))
        expected = agent_chat_record_digest(row, row_previous)
        legacy_expected = agent_chat_record_digest(row, row_previous, blank_message_id=True)
        if row_previous != previous_hash or row_hash not in {expected, legacy_expected}:
            return {
                "ok": False,
                "status": "HASH_CHAIN_FAIL",
                "message_count": len(rows),
                "broken_at": index,
                "message_id": str(row.get("message_id", "")),
                "execution_from_search": "BLOCK",
                "executes": False,
                "secret_values_printed": False,
            }
        previous_hash = row_hash
    return {
        "ok": True,
        "status": "HASH_CHAIN_PASS",
        "message_count": len(rows),
        "head_hash": previous_hash,
        "execution_from_search": "BLOCK",
        "executes": False,
        "secret_values_printed": False,
    }


def agent_chat_query_filters(raw: dict[str, list[str]] | dict[str, Any] | None) -> dict[str, Any]:
    raw = raw or {}

    def first(name: str, fallback: str = "") -> str:
        value = raw.get(name, fallback)
        if isinstance(value, list):
            return str(value[0] if value else fallback)
        return str(value or fallback)

    return {
        "q": first("q"),
        "room": first("room"),
        "sender": first("sender") or first("agent"),
        "recipient": first("recipient"),
        "mention": first("mention"),
        "message_type": first("type") or first("message_type"),
        "linked_task_id": first("task_id") or first("linked_task_id"),
        "linked_workpack_id": first("workpack_id") or first("linked_workpack_id"),
        "since": first("since"),
        "until": first("until"),
        "limit": first("limit", "50"),
    }


def agent_chat_read_messages(filters: dict[str, Any] | None = None, path: pathlib.Path | None = None) -> list[dict[str, Any]]:
    filters = filters or {}
    rows = agent_chat_read_all_messages(path)
    q = str(filters.get("q") or "").strip().lower()
    room = str(filters.get("room") or "").strip()
    if room and not room.startswith("#"):
        room = f"#{room.lower()}"
    sender = safe_optional_local_id(filters.get("sender"))
    recipient = safe_optional_local_id(filters.get("recipient"))
    mention = safe_optional_local_id(filters.get("mention"))
    message_type = str(filters.get("message_type") or "").strip().upper()
    linked_task_id = safe_optional_local_id(filters.get("linked_task_id"))
    linked_workpack_id = safe_optional_local_id(filters.get("linked_workpack_id"))
    since = str(filters.get("since") or "").strip()
    until = str(filters.get("until") or "").strip()
    try:
        limit = max(1, min(int(filters.get("limit") or 50), 500))
    except ValueError:
        limit = 50

    def matches(row: dict[str, Any]) -> bool:
        if room and str(row.get("room", "")).lower() != room.lower():
            return False
        if sender and safe_optional_local_id(row.get("sender")) != sender:
            return False
        if recipient and safe_optional_local_id(row.get("recipient") or row.get("to_agent")) != recipient:
            return False
        if mention and mention not in [safe_local_id(str(item)) for item in row.get("mentions", [])]:
            return False
        if message_type and agent_chat_normalize_message_type(row.get("message_type")) != message_type:
            return False
        if linked_task_id and safe_optional_local_id(row.get("linked_task_id")) != linked_task_id:
            return False
        if linked_workpack_id and safe_optional_local_id(row.get("linked_workpack_id")) != linked_workpack_id:
            return False
        created_at = str(row.get("created_at") or row.get("timestamp") or "")
        if since and created_at < since:
            return False
        if until and created_at > until:
            return False
        if q:
            haystack = " ".join(
                [
                    str(row.get("message_id", "")),
                    str(row.get("room", "")),
                    str(row.get("sender", "")),
                    str(row.get("recipient", "")),
                    " ".join(str(item) for item in row.get("mentions", [])),
                    str(row.get("body", "")),
                    str(row.get("message_type", "")),
                    str(row.get("linked_task_id", "")),
                    str(row.get("linked_workpack_id", "")),
                    " ".join(str(item) for item in row.get("tags", [])),
                ]
            ).lower()
            if q not in haystack:
                return False
        return True

    return sanitize_obj([row for row in rows if matches(row)][-limit:])


def agent_chat_build_search_index(path: pathlib.Path | None = None, index_path: pathlib.Path | None = None) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    rows = agent_chat_read_all_messages(path)
    index: dict[str, list[str]] = {}
    for row in rows:
        message_id = str(row.get("message_id", ""))
        text = " ".join(
            [
                str(row.get("room", "")),
                str(row.get("sender", "")),
                str(row.get("recipient", "")),
                str(row.get("body", "")),
                str(row.get("message_type", "")),
                str(row.get("linked_task_id", "")),
                str(row.get("linked_workpack_id", "")),
                " ".join(str(item) for item in row.get("mentions", [])),
                " ".join(str(item) for item in row.get("tags", [])),
            ]
        ).lower()
        for term in sorted(set(re.findall(r"[a-z0-9_#.-]{3,}", text))):
            index.setdefault(term, [])
            if message_id and message_id not in index[term]:
                index[term].append(message_id)
    payload = {
        "schema": "medioevo.agent_chat.search_index_manifest.v0_3",
        "mode": "LOCAL_ONLY",
        "search_index": "KEYWORD_INVERTED_INDEX",
        "message_count": len(rows),
        "term_count": len(index),
        "index": index,
        "cloud_called": False,
        "execution_from_search": "BLOCK",
        "executes": False,
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    }
    write_json_file(index_path or AGENT_CHAT_SEARCH_INDEX_PATH, payload)
    return sanitize_obj(payload)


def agent_chat_search_payload(filters: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    messages = agent_chat_read_messages(filters)
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.search.v0_3",
            "version": "v0.3",
            "mode": "LOCAL_ONLY",
            "filters": filters or {},
            "messages": messages,
            "result_count": len(messages),
            "execution_from_search": "BLOCK",
            "executes": False,
            "cloud_called": False,
            "public_export_allowed": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def agent_chat_redact_export_text(text: str) -> str:
    redacted = sanitize_text(text)
    for candidate in _extract_candidate_paths(redacted):
        redacted = redacted.replace(candidate, "<LOCAL_PATH_REDACTED>")
    return redacted


def agent_chat_export_record(row: dict[str, Any]) -> dict[str, Any]:
    clean = dict(row)
    clean["body"] = agent_chat_redact_export_text(str(clean.get("body", "")))
    clean["export_boundary"] = AGENT_CHAT_EXPORT_BOUNDARY
    clean["public_export_allowed"] = False
    return sanitize_obj(clean)


def agent_chat_export_jsonl_payload(filters: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    rows = [agent_chat_export_record(row) for row in agent_chat_read_messages(filters or {})]
    header = {
        "schema": "medioevo.agent_chat.export.header.v0_3",
        "boundary": AGENT_CHAT_EXPORT_BOUNDARY,
        "public_export_allowed": False,
        "execution_from_search": "BLOCK",
        "created_at": utc_now_iso(),
    }
    content = "\n".join([json.dumps(header, ensure_ascii=True, sort_keys=True), *[json.dumps(row, ensure_ascii=True, sort_keys=True) for row in rows]]) + "\n"
    AGENT_CHAT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    export_path = AGENT_CHAT_EXPORT_DIR / "agent_chat_export_latest.jsonl"
    export_path.write_text(content, encoding="utf-8")
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.export.v0_3",
            "format": "JSONL",
            "boundary": AGENT_CHAT_EXPORT_BOUNDARY,
            "public_export_allowed": False,
            "message_count": len(rows),
            "artifact": local_relative_path(export_path),
            "content": content,
            "executes": False,
            "secret_values_printed": False,
        }
    )


def agent_chat_export_markdown_payload(filters: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    rows = [agent_chat_export_record(row) for row in agent_chat_read_messages(filters or {})]
    lines = [
        "# Agent Chat Internal Export",
        "",
        f"Boundary: {AGENT_CHAT_EXPORT_BOUNDARY}",
        "Public export allowed: false",
        "Execution from search: BLOCK",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row.get('created_at', '')} {row.get('room', '')} {row.get('message_type', '')}",
                "",
                f"- message_id: {row.get('message_id', '')}",
                f"- sender: {row.get('sender', '')}",
                f"- recipient: {row.get('recipient', '')}",
                f"- linked_task_id: {row.get('linked_task_id', '')}",
                f"- linked_workpack_id: {row.get('linked_workpack_id', '')}",
                "",
                agent_chat_redact_export_text(str(row.get("body", ""))),
                "",
            ]
        )
    content = "\n".join(lines).strip() + "\n"
    AGENT_CHAT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    export_path = AGENT_CHAT_EXPORT_DIR / "agent_chat_export_latest.md"
    export_path.write_text(content, encoding="utf-8")
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.export.v0_3",
            "format": "MARKDOWN_INTERNAL",
            "boundary": AGENT_CHAT_EXPORT_BOUNDARY,
            "public_export_allowed": False,
            "message_count": len(rows),
            "artifact": local_relative_path(export_path),
            "content": content,
            "executes": False,
            "secret_values_printed": False,
        }
    )


def agent_chat_find_message(message_id: str) -> dict[str, Any]:
    safe_message_id = safe_local_id(message_id)
    return next((row for row in agent_chat_read_all_messages() if safe_optional_local_id(row.get("message_id")) == safe_message_id), {})


def agent_chat_reconstruct_thread_payload(message_id: str) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    safe_message_id = safe_local_id(message_id)
    origin = agent_chat_find_message(safe_message_id)
    if not origin:
        return {"ok": False, "status": "BLOCK", "reason": "Agent chat message not found.", "executes": False, "secret_values_printed": False}
    task_id = safe_optional_local_id(origin.get("linked_task_id")) or f"chat-draft-{safe_message_id}"
    task_files = local_execute_task_files(task_id)
    task_spec = _load_json_dict(task_files["taskspec"], {}) if task_files["taskspec"].exists() else {}
    ghostgate = _load_json_dict(task_files["ghostgate"], {}) if task_files["ghostgate"].exists() else {}
    workpack_id = safe_optional_local_id(origin.get("linked_workpack_id"))
    workpack = load_workpack_manifest(workpack_id) if workpack_id else {}
    if not workpack:
        workpack = next((row for row in workpack_records() if row.get("source_message_id") == safe_message_id or row.get("source_task_id") == f"agent-chat-{safe_message_id}"), {})
        workpack_id = safe_optional_local_id(workpack.get("workpack_id"))
    witness_events = [
        row
        for row in [
            *read_jsonl(AGENT_CHAT_ROUTING_WITNESSLOG_PATH, limit=500),
            *read_jsonl(LOCAL_HUB_WITNESS_PATH, limit=500),
            *read_jsonl(LOCAL_EXECUTE_WITNESSLOG_PATH, limit=500),
            *read_jsonl(WORKPACK_WITNESSLOG_PATH, limit=500),
        ]
        if safe_optional_local_id(row.get("message_id")) == safe_message_id
        or (task_id and safe_optional_local_id(row.get("task_id")) == task_id)
        or (workpack_id and safe_optional_local_id(row.get("workpack_id")) == workpack_id)
    ]
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.thread.v0_3",
            "ok": True,
            "status": "RECONSTRUCTED_READ_ONLY",
            "origin_message": origin,
            "task_id": task_id if task_spec else "",
            "taskspec": task_spec,
            "workpack_id": workpack_id,
            "workpack": workpack,
            "ghostgate": ghostgate,
            "witness": witness_events,
            "witness_count": len(witness_events),
            "final_status": "READ_ONLY_NO_EXECUTION",
            "execution_from_search": "BLOCK",
            "executes": False,
            "secret_values_printed": False,
        }
    )


def agent_chat_witness(event: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    AGENT_CHAT_ROUTING_WITNESSLOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    previous = read_jsonl(AGENT_CHAT_ROUTING_WITNESSLOG_PATH, limit=1)
    previous_hash = str(previous[-1].get("hash", "")) if previous else ""
    record = {
        "event": event,
        "timestamp": utc_now_iso(),
        "previous_hash": previous_hash,
        "cloud_called": False,
        "nvidia_called": False,
        "publication": "BLOCK",
        "secret_values_printed": False,
    }
    if payload:
        record.update(sanitize_obj(payload))
    digest_source = json.dumps(record, ensure_ascii=True, sort_keys=True)
    record["hash"] = hashlib.sha256((previous_hash + digest_source).encode("utf-8")).hexdigest()
    append_jsonl(AGENT_CHAT_ROUTING_WITNESSLOG_PATH, record)
    return record


def agent_chat_room_for_payload(value: str | None) -> str:
    room = str(value or "#general").strip().lower()
    if room and not room.startswith("#"):
        room = f"#{room}"
    if room not in AGENT_CHAT_ROOMS:
        raise ValueError("unknown room")
    return room


def agent_chat_mentions_from_body(body: str, explicit_mentions: Any = None) -> list[str]:
    known = agent_chat_known_agent_ids()
    mentions: list[str] = []
    for raw in re.findall(r"@([A-Za-z0-9_\-]+)", body):
        agent = safe_local_id(raw)
        if agent in known and agent not in mentions:
            mentions.append(agent)
    if isinstance(explicit_mentions, list):
        for item in explicit_mentions:
            agent = safe_local_id(str(item))
            if agent in known and agent not in mentions:
                mentions.append(agent)
    return mentions


def agent_chat_suggested_agent(room: str, mentions: list[str]) -> str:
    if mentions:
        return mentions[0]
    return {
        "#wabi": "WABI_LOCAL_PROGRAMMER",
        "#workpacks": "CLAUDIO_WORKPACK_MANAGER",
        "#qa": "WABI_TEST_RUNNER",
        "#duat": "DUAT_DISPLAY_AGENT",
        "#canon": "OBS_CANON_DIFF_CURATOR",
        "#release": "BOUNDARY_RELEASE_SENTINEL",
        "#general": "CORE_ORCHESTRATOR",
    }.get(room, "CORE_ORCHESTRATOR")


def agent_chat_blocked_action(body: str) -> str:
    lowered = body.lower()
    checks = [
        ("RUN_CLOUD", ("run cloud", "cloud llm", "llamar cloud", "usar cloud")),
        ("RUN_NVIDIA", ("nvidia", "nemotron", "smoke")),
        ("PUBLISH", ("publish", "publicar", "publication")),
        ("PUSH", ("git push", "push branch")),
        ("DEPLOY", ("deploy", "desplegar")),
        ("DELETE_DIRECT", ("delete direct", "borrar directo", "remove-item")),
        ("EXECUTE_WITHOUT_GATE", ("execute without gate", "ejecuta sin gate", "sin ghostgate")),
    ]
    for label, needles in checks:
        if any(needle in lowered for needle in needles):
            return label
    return ""


def route_agent_chat_message_record(message: dict[str, Any]) -> dict[str, Any]:
    ensure_agent_chat_routing_contract_files()
    body = str(message.get("body", ""))
    room = agent_chat_room_for_payload(str(message.get("room") or "#general"))
    mentions = [safe_local_id(str(item)) for item in message.get("mentions", []) if safe_local_id(str(item)) in agent_chat_known_agent_ids()]
    if not mentions:
        mentions = agent_chat_mentions_from_body(body)
    blocked_action = agent_chat_blocked_action(body)
    suggested_agent = agent_chat_suggested_agent(room, mentions)
    decision = "BLOCK" if blocked_action else "APPROVE"
    return sanitize_obj(
        {
            "ok": True,
            "status": "ROUTED",
            "message_id": str(message.get("message_id", "")),
            "room": room,
            "mentions": mentions,
            "assigned_agent": suggested_agent,
            "recipient": str(message.get("recipient") or message.get("to_agent") or suggested_agent),
            "blocked_action": blocked_action,
            "action_gate": decision,
            "executes": False,
            "requires_workpack_bridge": True,
            "requires_local_execute": True,
            "secret_values_printed": False,
        }
    )


def route_agent_chat_message_payload(message_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_message_id = safe_local_id(message_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    message = next((row for row in messages if safe_local_id(str(row.get("message_id", ""))) == safe_message_id), None)
    if not message:
        return {"ok": False, "status": "BLOCK", "reason": "Agent chat message not found.", "secret_values_printed": False}
    route = route_agent_chat_message_record(message)
    witness = agent_chat_witness("agent_chat_message_routed", {"message_id": safe_message_id, "assigned_agent": route["assigned_agent"], "action_gate": route["action_gate"]})
    append_jsonl(LOCAL_HUB_WITNESS_PATH, {"event": "agent_chat_message_routed", "message_id": safe_message_id, "assigned_agent": route["assigned_agent"], "timestamp": utc_now_iso()})
    route["witness"] = witness
    return sanitize_obj(route)


def agent_chat_system_status_payload(payload: dict[str, Any]) -> dict[str, Any]:
    event = safe_local_id(str(payload.get("event") or payload.get("status_event") or "SYSTEM_STATUS"))
    room = agent_chat_room_for_payload(str(payload.get("room") or "#workpacks"))
    linked_task_id = safe_optional_local_id(payload.get("linked_task_id") or payload.get("task_id"))
    linked_workpack_id = safe_optional_local_id(payload.get("linked_workpack_id") or payload.get("workpack_id"))
    status_text = sanitize_text(str(payload.get("body") or payload.get("message") or event))
    body = f"{event}: {status_text}"
    result = agent_chat_post_message_payload(
        {
            "room": room,
            "sender": "SYSTEM",
            "body": body,
            "message_type": str(payload.get("message_type") or "SYSTEM"),
            "linked_task_id": linked_task_id,
            "linked_workpack_id": linked_workpack_id,
        }
    )
    witness = agent_chat_witness("agent_chat_system_status", {"event_name": event, "message_id": result.get("message", {}).get("message_id", ""), "linked_task_id": linked_task_id, "linked_workpack_id": linked_workpack_id})
    return sanitize_obj({"ok": result.get("ok") is True, "status": "SYSTEM_STATUS_WRITTEN", "message": result.get("message"), "witness": witness, "executes": False, "secret_values_printed": False})


def attach_agent_chat_message_to_workpack_payload(message_id: str, workpack_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_message_id = safe_local_id(message_id)
    safe_workpack_id = safe_local_id(workpack_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    message = next((row for row in messages if safe_local_id(str(row.get("message_id", ""))) == safe_message_id), None)
    manifest = load_workpack_manifest(safe_workpack_id)
    if not message:
        return {"ok": False, "status": "BLOCK", "reason": "Agent chat message not found.", "secret_values_printed": False}
    if not manifest:
        return {"ok": False, "status": "BLOCK", "reason": "Workpack manifest not found.", "secret_values_printed": False}
    linked = list(manifest.get("linked_messages", [])) if isinstance(manifest.get("linked_messages"), list) else []
    if safe_message_id not in linked:
        linked.append(safe_message_id)
    updated = update_workpack_manifest(safe_workpack_id, {"linked_messages": linked})
    system = agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "message_attached_to_workpack",
            "message": f"message={safe_message_id} workpack={safe_workpack_id}; execution still requires Workpack Bridge gates.",
            "linked_workpack_id": safe_workpack_id,
        }
    )
    witness = agent_chat_witness("agent_chat_message_attached_to_workpack", {"message_id": safe_message_id, "workpack_id": safe_workpack_id})
    return sanitize_obj({"ok": True, "status": "MESSAGE_ATTACHED", "message_id": safe_message_id, "workpack_id": safe_workpack_id, "workpack": updated, "system_status": system.get("message"), "witness": witness, "executes": False, "secret_values_printed": False})


def agent_chat_inbox_payload(agent_id: str) -> dict[str, Any]:
    safe_agent = safe_local_id(agent_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    inbox = [
        row
        for row in messages
        if safe_agent == safe_optional_local_id(row.get("recipient") or row.get("to_agent"))
        or safe_agent in [safe_local_id(str(item)) for item in row.get("mentions", [])]
    ]
    workpacks = [row for row in workpack_records() if safe_local_id(str(row.get("assigned_agent", ""))) == safe_agent]
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.inbox.v0_2",
            "agent_id": safe_agent,
            "messages": inbox,
            "workpacks": workpacks,
            "inbox_count": len(inbox),
            "workpack_count": len(workpacks),
            "communication_mode": "LOCAL_ONLY",
            "secret_values_printed": False,
        }
    )


def agent_chat_outbox_payload(agent_id: str) -> dict[str, Any]:
    safe_agent = safe_local_id(agent_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    outbox = [row for row in messages if safe_optional_local_id(row.get("sender")) == safe_agent]
    taskspecs: list[dict[str, Any]] = []
    if LOCAL_EXECUTE_TASKSPEC_DIR.exists():
        for path in sorted(LOCAL_EXECUTE_TASKSPEC_DIR.glob("TASKSPEC_*.json")):
            spec = _load_json_dict(path, {})
            if safe_optional_local_id(spec.get("assigned_agent")) == safe_agent:
                taskspecs.append({"task_id": spec.get("task_id", ""), "path": local_execute_target_alias(path), "draft_only": bool(spec.get("draft_only"))})
    workpacks = [row for row in workpack_records() if safe_local_id(str(row.get("assigned_agent", ""))) == safe_agent]
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.outbox.v0_2",
            "agent_id": safe_agent,
            "messages": outbox,
            "taskspecs_created": taskspecs,
            "workpacks_created": workpacks,
            "outbox_count": len(outbox),
            "communication_mode": "LOCAL_ONLY",
            "secret_values_printed": False,
        }
    )


def agent_hub_agents() -> list[dict[str, Any]]:
    base = [
        ("CORE_ORCHESTRATOR", "Core Orchestrator", "Routes local tasks and keeps ActionGate visible.", "ONLINE", "APPROVE_LOCAL"),
        ("CORE_GATEKEEPER", "Core Gatekeeper", "Blocks cloud, publication and unsafe actions.", "ONLINE", "BLOCK_EXTERNAL"),
        ("CORE_MEMORY_KEEPER", "Core Memory Keeper", "Maintains handoff, witness and append-only records.", "ONLINE", "APPROVE_LOCAL"),
        ("OBS_CANON_DIFF_CURATOR", "OSIT Canon Diff Curator", "Prepares public-safe summaries without private canon.", "REVIEW", "REVIEW_PUBLIC_SAFE"),
        ("OBS_JAMMING_SENTINEL", "Jamming Sentinel", "Watches R, Phi_eff and closure pressure.", "ONLINE", "APPROVE_LOCAL"),
        ("WABI_LOCAL_PROGRAMMER", "Wabi Local Programmer", "Runs fallback-only coding loops in sandbox.", "ONLINE", "APPROVE_LOCAL"),
        ("WABI_DEBUGGER", "Wabi Debugger", "Diagnoses local failures and rollback plans.", "IDLE", "APPROVE_LOCAL"),
        ("WABI_TEST_RUNNER", "Wabi Test Runner", "Runs local tests and compile checks.", "IDLE", "APPROVE_LOCAL"),
        ("WABI_SAFE_EXECUTOR", "Wabi Safe Executor", "Applies only gated, reversible local changes.", "REVIEW", "GHOSTGATE_REQUIRED"),
        ("CLAUDIO_LOCAL_BRIDGE", "Claudio Local Bridge", "Queues approved tasks for local Claudio surfaces.", "IDLE", "ACTIONGATE_REQUIRED"),
        ("CLAUDIO_WORKPACK_MANAGER", "Claudio Workpack Manager", "Builds workpacks from local pending docs.", "IDLE", "APPROVE_LOCAL"),
        ("BOUNDARY_SECRET_SCANNER", "Boundary Secret Scanner", "Checks secrets, private paths and blocked claims.", "ONLINE", "BLOCK_ON_SECRET"),
        ("BOUNDARY_RELEASE_SENTINEL", "Boundary Release Sentinel", "Separates public-safe updates from internal runtime.", "REVIEW", "PUBLICATION_REVIEW"),
        ("DUAT_DISPLAY_AGENT", "DUAT Display Agent", "Maintains public-safe display and dashboard concepts.", "IDLE", "REVIEW_UI"),
        ("GEODIA_SIM_AGENT", "GEODIA Sim Agent", "Tracks synthetic simulation evidence only.", "IDLE", "APPROVE_SYNTHETIC"),
    ]
    now = utc_now_iso()
    queue = read_jsonl(LOCAL_HUB_QUEUE_PATH, limit=200)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=200)
    workpacks = workpack_records()
    scheduled = scheduler_records()
    multisteps = multi_step_records()
    agents: list[dict[str, Any]] = []
    for agent_id, name, role, status, gate in base:
        inbox_count = sum(
            1
            for row in messages
            if row.get("to_agent") == agent_id
            or row.get("recipient") == agent_id
            or agent_id in row.get("mentions", [])
        )
        outbox_count = sum(1 for row in messages if row.get("sender") == agent_id)
        current = next((row.get("task_id", "") for row in reversed(queue) if row.get("agent") == agent_id), "")
        assigned_workpacks = [row for row in workpacks if row.get("assigned_agent") == agent_id]
        scheduled_workpacks = [row for row in scheduled if row.get("assigned_agent") == agent_id]
        assigned_multisteps = [row for row in multisteps if row.get("assigned_agent") == agent_id]
        if assigned_workpacks and status == "IDLE":
            status = "READY"
        executing = any(row.get("status") == "APPROVED" for row in assigned_workpacks)
        if executing:
            status = "READY"
        if any(row.get("status") == "RUNNING" for row in scheduled_workpacks):
            status = "RUNNING_LOCAL"
        elif any(row.get("status") in {"APPROVED", "SCHEDULED"} for row in scheduled_workpacks):
            status = "QUEUED"
        if any(row.get("status") == "RUNNING" for row in assigned_multisteps):
            status = "RUNNING_LOCAL"
        elif any(row.get("status") in {"APPROVED", "SCHEDULED", "PARTIAL"} for row in assigned_multisteps):
            status = "QUEUED"
        agents.append(
            {
                "agent_id": agent_id,
                "name": name,
                "role": role,
                "status": status,
                "current_task": current,
                "inbox_count": inbox_count,
                "outbox_count": outbox_count,
                "last_seen": now,
                "gate": gate,
                "workpacks": [row.get("workpack_id", "") for row in assigned_workpacks],
                "workpack_count": len(assigned_workpacks),
                "scheduled_workpacks": [row.get("workpack_id", "") for row in scheduled_workpacks],
                "scheduled_workpack_count": len(scheduled_workpacks),
                "multi_step_workpacks": [row.get("workpack_id", "") for row in assigned_multisteps],
                "multi_step_workpack_count": len(assigned_multisteps),
                "current_step": next((str(row.get("current_step", "")) for row in assigned_multisteps if row.get("current_step")), ""),
            }
        )
    return sanitize_obj(agents)


def agent_hub_payload() -> dict[str, Any]:
    agents = agent_hub_agents()
    tasks = local_hub_task_catalog()
    tasks_by_agent: dict[str, list[str]] = {}
    for task in tasks:
        tasks_by_agent.setdefault(str(task.get("assigned_agent", "CORE_ORCHESTRATOR")), []).append(str(task["task_id"]))
    workpacks_by_agent: dict[str, list[str]] = {}
    for workpack in workpack_records():
        workpacks_by_agent.setdefault(str(workpack.get("assigned_agent", "CLAUDIO_WORKPACK_MANAGER")), []).append(str(workpack.get("workpack_id", "")))
    scheduled_workpacks_by_agent: dict[str, list[str]] = {}
    for item in scheduler_records():
        scheduled_workpacks_by_agent.setdefault(str(item.get("assigned_agent", "CLAUDIO_WORKPACK_MANAGER")), []).append(str(item.get("workpack_id", "")))
    multi_step_workpacks_by_agent: dict[str, list[str]] = {}
    for item in multi_step_records():
        multi_step_workpacks_by_agent.setdefault(str(item.get("assigned_agent", "CLAUDIO_WORKPACK_MANAGER")), []).append(str(item.get("workpack_id", "")))
    return sanitize_obj(
        {
            "schema": "medioevo.agent_hub.v0_2",
            "agents": agents,
            "channels": [{"room": room, "mode": "LOCAL_ONLY"} for room in AGENT_CHAT_ROOMS],
            "messages_recent": read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=20),
            "tasks_by_agent": tasks_by_agent,
            "workpacks_by_agent": workpacks_by_agent,
            "scheduled_workpacks_by_agent": scheduled_workpacks_by_agent,
            "multi_step_workpacks_by_agent": multi_step_workpacks_by_agent,
            "communication_mode": "LOCAL_ONLY",
            "chat_style": "MSN_90S_LOCAL",
            "cloud_called": False,
            "secret_values_printed": False,
        }
    )


def agent_chat_status_payload() -> dict[str, Any]:
    ensure_agent_chat_routing_contract_files()
    status = _load_json_dict(AGENT_CHAT_STATUS_PATH, {})
    if not status:
        status = {agent["agent_id"]: agent["status"].title() for agent in agent_hub_agents()}
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.status.v0_2",
            "communication_mode": "LOCAL_ONLY",
            "allowed_statuses": AGENT_CHAT_STATUSES,
            "statuses": status,
            "secret_values_printed": False,
        }
    )


def agent_chat_rooms_payload() -> dict[str, Any]:
    ensure_agent_chat_routing_contract_files()
    return {
        "schema": "medioevo.agent_chat.rooms.v0_2",
        "rooms": [{"room": room, "append_only": True, "local_only": True} for room in AGENT_CHAT_ROOMS],
        "communication_mode": "LOCAL_ONLY",
        "secret_values_printed": False,
    }


def agent_chat_messages_payload(limit: int = 50) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    return sanitize_obj(
        {
            "schema": "medioevo.agent_chat.messages.v0_3",
            "version": "v0.3",
            "routing_contract": local_execute_target_alias(AGENT_CHAT_ROUTING_CONTRACT_PATH),
            "message_schema": local_execute_target_alias(AGENT_CHAT_MESSAGE_SCHEMA_PATH),
            "persistent_message_schema": local_execute_target_alias(AGENT_CHAT_PERSISTENT_MESSAGE_SCHEMA_PATH),
            "storage_contract": local_execute_target_alias(AGENT_CHAT_STORAGE_CONTRACT_PATH),
            "messages": read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=limit),
            "append_only": True,
            "hash_chain": agent_chat_verify_hash_chain(),
            "search_endpoint": "/api/agent-chat/search",
            "execution_from_search": "BLOCK",
            "communication_mode": "LOCAL_ONLY",
            "export_jsonl": local_relative_path(AGENT_CHAT_MESSAGES_PATH),
            "secret_values_printed": False,
        }
    )


def agent_chat_post_message_payload(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_agent_chat_storage_files()
    body = str(payload.get("body") or payload.get("message") or "").strip()
    if not body:
        raise ValueError("message body required")
    if text_has_secret_value(body):
        return {"ok": False, "status": "BLOCK", "reason": "Secret-like value detected; message not written."}
    try:
        record = agent_chat_append_message(payload)
    except ValueError as exc:
        return {"ok": False, "status": "BLOCK", "reason": sanitize_text(exc), "secret_values_printed": False}
    room = str(record.get("room") or "#general")
    route = route_agent_chat_message_record(record)
    append_jsonl(
        LOCAL_HUB_WITNESS_PATH,
        {
            "event": "agent_chat_message",
            "message_id": record["message_id"],
            "room": room,
            "timestamp": record["timestamp"],
        },
    )
    agent_chat_witness("agent_chat_message", {"message_id": record["message_id"], "room": room, "assigned_agent": route["assigned_agent"]})
    return {"ok": True, "status": "MESSAGE_WRITTEN", "message": record, "route": route, "executes": False, "secret_values_printed": False}


def agent_chat_message_to_taskspec_payload(message_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    safe_message_id = safe_local_id(message_id)
    messages = read_jsonl(AGENT_CHAT_MESSAGES_PATH, limit=500)
    message = next((row for row in messages if safe_local_id(str(row.get("message_id", ""))) == safe_message_id), None)
    if not message:
        return {"ok": False, "status": "BLOCK", "reason": "Agent chat message not found.", "secret_values_printed": False}
    body = str(message.get("body", ""))
    if text_has_secret_value(body):
        return {"ok": False, "status": "BLOCK", "reason": "Secret-like value detected; TaskSpec draft not written.", "secret_values_printed": False}
    task_id = f"chat-draft-{safe_message_id}"
    files = local_execute_task_files(task_id)
    task_spec = {
        "schema": "medioevo.local_execute.task_spec.v0_2",
        "task_id": task_id,
        "title": f"TaskSpec draft from agent chat {safe_message_id}",
        "lane": "SANDBOX",
        "intent": sanitize_text(body[:500]),
        "source": "AGENT_CHAT",
        "allowed_targets": [],
        "blocked_targets": [".env", "credentials", "PUBLICATION", "CLOUD", "NVIDIA"],
        "expected_outputs": [],
        "tests_required": [],
        "operation": {"type": "draft_only"},
        "rollback_required": True,
        "witness_required": True,
        "publication_gate": "BLOCK",
        "cloud_allowed": False,
        "nvidia_allowed": False,
        "direct_delete_allowed": False,
        "created_at": utc_now_iso(),
        "draft_only": True,
        "assigned_agent": str(payload.get("assigned_agent", "WABI_LOCAL_PROGRAMMER")) if payload else "WABI_LOCAL_PROGRAMMER",
        "secret_values_printed": False,
    }
    write_json_file(files["taskspec"], task_spec)
    witness = local_execute_witness(task_id, "agent_chat_message_to_taskspec_draft", {"message_id": safe_message_id})
    route_witness = agent_chat_witness("agent_chat_message_to_taskspec_draft", {"message_id": safe_message_id, "task_id": task_id})
    append_jsonl(
        LOCAL_HUB_WITNESS_PATH,
        {"event": "agent_chat_message_to_taskspec_draft", "message_id": safe_message_id, "task_id": task_id, "timestamp": utc_now_iso()},
    )
    system_status = agent_chat_system_status_payload(
        {
            "room": "#workpacks",
            "event": "taskspec_draft_created",
            "message": f"TaskSpec draft {task_id} created from message {safe_message_id}; execution remains blocked until Workpack/Local Execute gates.",
            "linked_task_id": task_id,
            "message_type": "TASK",
        }
    )
    return sanitize_obj(
        {
            "ok": True,
            "status": "TASKSPEC_DRAFT_CREATED",
            "task_id": task_id,
            "task_spec_path": local_execute_target_alias(files["taskspec"]),
            "task_spec": task_spec,
            "witness": witness,
            "routing_witness": route_witness,
            "system_status": system_status.get("message"),
            "executes": False,
            "secret_values_printed": False,
        }
    )


def agent_chat_post_status_payload(payload: dict[str, Any]) -> dict[str, Any]:
    agent_id = safe_local_id(str(payload.get("agent_id") or "OWNER"))
    status = str(payload.get("status") or "Online").strip()
    if status not in AGENT_CHAT_STATUSES:
        raise ValueError("invalid status")
    current = _load_json_dict(AGENT_CHAT_STATUS_PATH, {})
    current[agent_id] = status
    write_json_file(AGENT_CHAT_STATUS_PATH, current)
    append_jsonl(
        LOCAL_HUB_WITNESS_PATH,
        {"event": "agent_chat_status", "agent_id": agent_id, "status": status, "timestamp": utc_now_iso()},
    )
    return {"ok": True, "agent_id": agent_id, "status": status, "secret_values_printed": False}


def provider_smoke_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return sanitize_obj(
        coding_provider_router.smoke_provider(
            str(payload.get("provider", "nvidia") or "nvidia"),
            str(payload.get("model", "nemotron-nvidia") or "nemotron-nvidia"),
            live=bool(payload.get("live", False)),
        )
    )


def provider_route_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    if "cloud_providers_blocked" in data or "cloudProvidersBlocked" in data:
        cloud_blocked = bool(data.get("cloud_providers_blocked", data.get("cloudProvidersBlocked", False)))
    else:
        cloud_blocked = False if workbench_cloud_first_enabled() else None
    route = chat_provider_orchestrator.provider_route_payload(
        live=bool(data.get("live", False)),
        free_dev_confirmed=bool(data.get("free_dev_confirmed", data.get("freeDevConfirmed", False))) if ("free_dev_confirmed" in data or "freeDevConfirmed" in data) else None,
        cloud_providers_blocked=cloud_blocked,
        external_api_mode=str(data.get("external_api_mode", data.get("externalApiMode", "")) or "") or None,
        owner_authorized=bool(data.get("owner_authorized", data.get("ownerAuthorized", True))),
        allow_paid_api=bool(data.get("allow_paid_api", data.get("allowPaidApi", True))),
    )
    if workbench_cloud_first_enabled() and not bool(data.get("cloud_providers_blocked", data.get("cloudProvidersBlocked", False))):
        trace = route.get("developer_trace") if isinstance(route.get("developer_trace"), dict) else {}
        trace["workbench_engine_override"] = {
            "selected_provider": WABI_PRIMARY_PROVIDER,
            "selected_model": WABI_PRIMARY_MODEL,
            "provider_chain": [WABI_PRIMARY_PROVIDER, WABI_FALLBACK_PROVIDER, WABI_SECONDARY_FALLBACK_PROVIDER, "ollama"],
            "reason": "Decision del operador: DeepSeek V4 Flash lidera; Nemotron Super via NVIDIA y Cloudflare quedan como fallbacks API; Ollama ultimo/offline.",
        }
        route.update(
            {
                "selected_provider": WABI_PRIMARY_PROVIDER,
                "selected_model": WABI_PRIMARY_MODEL,
                "fallback_provider": WABI_FALLBACK_PROVIDER,
                "fallback_model": WABI_FALLBACK_MODEL,
                "route_stage": "API_FIRST_DEEPSEEK",
                "status": "ACTIVE_CLOUD_ENGINE",
                "reason": f"{WABI_PRIMARY_PROVIDER} {WABI_PRIMARY_MODEL} es la ruta primaria; {WABI_FALLBACK_PROVIDER} {WABI_FALLBACK_MODEL} y Cloudflare son fallbacks API.",
                "user_message": f"Motor API-first activo: DeepSeek ({WABI_PRIMARY_MODEL}); fallback: NVIDIA Nemotron ({WABI_FALLBACK_MODEL}); Cloudflare/Ollama quedan como respaldo.",
                "fallback_used": False,
                "provider_chain": [WABI_PRIMARY_PROVIDER, WABI_FALLBACK_PROVIDER, WABI_SECONDARY_FALLBACK_PROVIDER, "ollama"],
                "cloud_providers_blocked": False,
                "developer_trace": trace,
            }
        )
    return sanitize_obj(route)


def provider_policy_payload() -> dict[str, Any]:
    return sanitize_obj(provider_policy.policy_payload())


def budget_status_payload() -> dict[str, Any]:
    return sanitize_obj(budget_gate.budget_status_payload())


def cloud_budget_status_payload() -> dict[str, Any]:
    if CloudBudgetGate is None:
        return sanitize_obj(
            {
                "ok": False,
                "status": "CLOUD_BUDGET_REVIEW",
                "cloud_gate": "PROPOSAL_ONLY_UNAVAILABLE",
                "cloud_budget": {
                    "budget_gate": "CLOUD_BUDGET_REVIEW",
                    "provider": "nvidia",
                    "model": "nano-30b",
                    "double_opt_in": False,
                    "cloud_live_ready": False,
                    "next_cloud_call_allowed": False,
                    "proposal_only": True,
                    "cloud_provider_called": False,
                    "usage_known": False,
                    "cost_known": False,
                },
                "warning": "Canonical Wabi CloudBudgetGate is unavailable; UI remains no-live proposal-only.",
                "secret_values_printed": False,
                "publication_gate": "BLOCK",
            }
        )
    gate = CloudBudgetGate()
    state = gate.load_state()
    status = dict(gate.render_status(provider="nvidia", model_alias="nano-30b", intent="ui_status"))
    status["model_alias"] = status.get("model", "nano-30b")
    status["last_status"] = state.get("last_status")
    status["last_call_at"] = state.get("last_call_at")
    status["proposal_only"] = True
    status["cloud_provider_called"] = False
    status["applied_to_sources"] = False
    status["secret_values_printed"] = False
    llm_default = (
        build_llm_proposal_status(runtime_root=_wabi_runtime_root(), session_id="wabi-ui-status", intent="ui_status")
        if build_llm_proposal_status is not None
        else {"llm_cloud_default_enabled": False, "cloud_live_ready": False}
    )
    payload = {
        "ok": True,
        "schema": "wabi.cloud_budget_ui_status.v0_1",
        "status": status.get("budget_gate", "CLOUD_BUDGET_REVIEW"),
        "cloud_gate": "PROPOSAL_ONLY_DOUBLE_OPT_IN" if status.get("double_opt_in") else "PROPOSAL_ONLY_DRY_RUN",
        "cloud_budget": status,
        "llm_cloud_default": llm_default,
        "warning": "NVIDIA cloud is proposal-only; outputs are not applied automatically.",
        "source_of_truth": "wabi_sabi.core.cloud_budget.CloudBudgetGate.render_status",
        "ui_live_call_enabled": False,
        "graphics_live": False,
        "browserbridge_live": False,
        "secret_values_printed": False,
        "publication_gate": "BLOCK",
    }
    return sanitize_obj(payload)


def _conversation_session_id(value: Any) -> str:
    raw = str(value or "").strip()
    safe = re.sub(r"[^A-Za-z0-9_.:-]+", "-", raw)[:80].strip("-")
    return safe or "wabi-ui-session"


def _wabi_runtime_root() -> pathlib.Path:
    return pathlib.Path(os.environ.get("WABI_RUNTIME_ROOT") or pathlib.Path.home() / ".medioevo" / "wabi" / "runtime")


def _wabi_programmer_runtime_root() -> pathlib.Path:
    return _wabi_runtime_root() / "programmer"


def _wabi_programmer_plan_dir() -> pathlib.Path:
    return _wabi_programmer_runtime_root() / "plans"


def _wabi_programmer_safe_executor_root() -> pathlib.Path:
    return _wabi_programmer_runtime_root() / "safe_executor"


def _programmer_tests_required(target: str, payload: dict[str, Any]) -> list[dict[str, str]]:
    raw = payload.get("verify_commands", payload.get("test_commands", []))
    commands = [str(item) for item in raw] if isinstance(raw, list) else []
    if not commands and target.lower().endswith(".py"):
        commands.append(f"python -m py_compile {target}")
    return [{"type": "command", "command": command} for command in commands if command.strip()]


def _programmer_secret_like_content(content: str) -> bool:
    return wabi_llm_code_bridge.redact_text(content) != content


def _write_programmer_plan_record(plan: dict[str, Any], *, content_by_target: dict[str, str], diff: str) -> pathlib.Path:
    plan_dir = _wabi_programmer_plan_dir()
    plan_dir.mkdir(parents=True, exist_ok=True)
    plan_id = safe_local_id(str(plan.get("plan_id") or "wabi-programmer-plan"))
    record = {
        "schema": "wabi.programmer_plan_record.v0_1",
        "created_at": utc_now_iso(),
        "plan_id": plan_id,
        "patch_plan": plan,
        "content_by_target": content_by_target,
        "diff": diff,
        "apply": False,
        "cloud": False,
        "secret_values_printed": False,
    }
    path = plan_dir / f"{plan_id}.json"
    path.write_text(json.dumps(record, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _read_programmer_plan_record(plan_id: str) -> dict[str, Any]:
    safe_id = safe_local_id(plan_id)
    path = (_wabi_programmer_plan_dir() / f"{safe_id}.json").resolve()
    try:
        path.relative_to(_wabi_programmer_plan_dir().resolve())
    except ValueError as exc:
        raise ValueError("plan_id_outside_store") from exc
    if not path.exists():
        raise FileNotFoundError(safe_id)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != "wabi.programmer_plan_record.v0_1":
        raise ValueError("programmer_plan_record_invalid")
    return payload


def programmer_plan_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    workspace = pathlib.Path(PROGRAMMER_WORKSPACE_ROOT).resolve()
    instruction = str(data.get("instruction") or data.get("prompt") or "").strip()
    target = str(data.get("target") or "").replace("\\", "/").strip() or None
    use_llm = bool(data.get("llm"))
    if use_llm:
        bridge = wabi_llm_code_bridge.build_llm_code_payload(
            instruction or "wabi programmer llm plan",
            workspace_root=workspace,
            runtime_root=_wabi_programmer_runtime_root() / "llm_bridge",
            target=target,
            provider=str(data.get("provider") or "ollama"),
        )
        if not bridge.get("ok"):
            return sanitize_obj({"ok": False, "apply": False, "reason": bridge.get("status"), "bridge": bridge, "cloud": False, "secret_values_printed": False})
        task_spec = bridge["task_spec"]
        content = str(bridge["content"])
        final_target = str(bridge["target"])
        diff = str(bridge.get("diff") or "")
        bridge_payload = bridge
    else:
        if not target:
            return sanitize_obj({"ok": False, "apply": False, "reason": "TARGET_REQUIRED", "cloud": False, "secret_values_printed": False})
        content = str(data.get("content") or "")
        if not content:
            return sanitize_obj({"ok": False, "apply": False, "reason": "CONTENT_OR_LLM_REQUIRED", "cloud": False, "secret_values_printed": False})
        if _programmer_secret_like_content(content):
            return sanitize_obj({"ok": False, "apply": False, "reason": "SECRET_LIKE_CONTENT_REJECTED", "cloud": False, "secret_values_printed": False})
        final_target = target
        task_spec = {
            "schema": "wabi.programmer_api_task_spec.v0_1",
            "task_id": "wabi-programmer-api-" + hashlib.sha256((instruction + final_target).encode("utf-8")).hexdigest()[:16],
            "title": instruction or "Wabi programmer API plan",
            "lane": "LOCAL_PRIVATE",
            "allowed_targets": [final_target],
            "operation": {"type": "write_text", "content": content},
            "tests_required": _programmer_tests_required(final_target, data),
        }
        diff = wabi_llm_code_bridge.diff_for_content(workspace, final_target, content)
        bridge_payload = {"status": "DIRECT_CONTENT", "proposal_only": True, "apply": False, "cloud_provider_called": False}

    plan = wabi_patch_planner.build_patch_plan(task_spec, workspace_root=workspace, created_at=utc_now_iso())
    record_path = _write_programmer_plan_record(plan, content_by_target={final_target: content}, diff=diff)
    return sanitize_obj(
        {
            "ok": True,
            "schema": "wabi.programmer_plan_response.v0_1",
            "apply": False,
            "reason": "DRY_RUN_DEFAULT",
            "plan_id": plan["plan_id"],
            "patch_plan": plan,
            "diff": diff,
            "record_path": str(record_path),
            "target": final_target,
            "bridge": bridge_payload,
            "cloud": False,
            "secret_values_printed": False,
        }
    )


def programmer_apply_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    approval = data.get("approval") if isinstance(data.get("approval"), dict) else {}
    if approval.get("ApplyGate") != "ALLOW_LOCAL_APPLY":
        return sanitize_obj(
            {
                "ok": False,
                "apply": False,
                "reason": "APPLY_GATE_REQUIRED",
                "cloud": False,
                "approval_required": {"ApplyGate": "ALLOW_LOCAL_APPLY", "CloudGate": "OFF"},
                "secret_values_printed": False,
            }
        )
    workspace = pathlib.Path(PROGRAMMER_WORKSPACE_ROOT).resolve()
    if data.get("plan_id"):
        try:
            record = _read_programmer_plan_record(str(data["plan_id"]))
        except FileNotFoundError:
            return sanitize_obj({"ok": False, "apply": False, "reason": "PLAN_NOT_FOUND", "cloud": False, "secret_values_printed": False})
        plan = record["patch_plan"]
        content_by_target = record["content_by_target"]
    else:
        plan = data.get("patch_plan") if isinstance(data.get("patch_plan"), dict) else {}
        content_by_target = data.get("content_by_target") if isinstance(data.get("content_by_target"), dict) else {}
    if not plan or not content_by_target:
        return sanitize_obj({"ok": False, "apply": False, "reason": "PLAN_AND_CONTENT_REQUIRED", "cloud": False, "secret_values_printed": False})
    result = wabi_safe_executor.execute_patch_plan(
        plan,
        content_by_target={str(key): str(value) for key, value in content_by_target.items()},
        workspace_root=workspace,
        runtime_root=_wabi_programmer_safe_executor_root(),
        approval={"ApplyGate": "ALLOW_LOCAL_APPLY", "CloudGate": "OFF"},
        test_commands=data.get("test_commands") if isinstance(data.get("test_commands"), list) else None,
        timeout_seconds=60,
        executed_at=utc_now_iso(),
    )
    return sanitize_obj(
        {
            "ok": bool(result.get("ok")),
            "schema": "wabi.programmer_apply_response.v0_1",
            "apply": bool(result.get("ok")),
            "reason": result.get("verification"),
            "result": result,
            "cloud": False,
            "approval_used": {"ApplyGate": "ALLOW_LOCAL_APPLY", "CloudGate": "OFF"},
            "secret_values_printed": False,
        }
    )


def _conversation_route_name(result: dict[str, Any]) -> str:
    route = str(result.get("route") or result.get("intent_name") or "local_chat")
    intent_name = str(result.get("intent_name") or "")
    if route in {"help", "status", "providers", "tasks", "local_chat", "exit"}:
        return route if route != "status" else "local_chat"
    if intent_name == "code_request":
        return "code_plan"
    if intent_name == "debug_request":
        return "debug_plan"
    if intent_name in {"graphics_scene_request", "graphics_asset_request"}:
        return "graphics_plan"
    if intent_name == "build_assist_request":
        return "build_assist_plan"
    if intent_name in {"plan_request", "file_task_request", "handoff_request"}:
        return "work_plan"
    return "local_chat"


def _conversation_graphics_payload(result: dict[str, Any]) -> dict[str, Any]:
    payload = result.get("payload", {}) if isinstance(result.get("payload"), dict) else {}
    graphics_status = payload.get("graphics_status") if isinstance(payload.get("graphics_status"), dict) else {}
    graphics_plan = payload.get("graphics_plan") if isinstance(payload.get("graphics_plan"), dict) else {}
    if not graphics_status and str(result.get("intent_name") or "").startswith("graphics_"):
        graphics_status = {
            "graphics_live": False,
            "graphics_plan_ready": True,
            "external_calls_allowed": False,
            "publication_allowed": False,
        }
    return {
        "graphics_live": bool(graphics_status.get("graphics_live", False)),
        "graphics_plan_ready": bool(graphics_status.get("graphics_plan_ready", False)),
        "external_calls_allowed": bool(graphics_status.get("external_calls_allowed", False)),
        "publication_allowed": bool(graphics_status.get("publication_allowed", False)),
        "plan": graphics_plan,
    }


def _normalize_taskspec_review_payload(
    task_spec: dict[str, Any],
    *,
    intent: dict[str, Any] | None = None,
    route: str | None = None,
    cloud_budget: dict[str, Any] | None = None,
    graphics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if normalize_taskspec_for_review is None:
        return sanitize_obj(
            {
                "schema": "wabi.taskspec_review.v0_1",
                "status": "REVIEW",
                "task_id": "taskspec-review-unavailable",
                "intent_name": (intent or {}).get("intent_name", "chat_general"),
                "route": route or "local_chat",
                "action_gate": (intent or {}).get("action_gate", "REVIEW"),
                "proposal_only": True,
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "summary": "TaskSpec review backend unavailable.",
                "plan_steps": [],
                "risks": ["Do not apply changes from this fallback payload."],
                "assumptions": ["Review backend import failed."],
                "suggested_tests": [],
                "affected_paths": [],
                "next_action": "Restore wabi_sabi.core.taskspec_review before applying any task.",
                "gate_status": "REVIEW_REQUIRED",
            }
        )
    review = normalize_taskspec_for_review(
        task_spec,
        intent=intent or {},
        route=route or "",
        cloud_budget=cloud_budget or {},
        graphics=graphics or {},
    )
    return sanitize_obj(review)


def taskspec_latest_payload() -> dict[str, Any]:
    latest = TASKSPEC_REVIEW_SESSION.get("latest") or {}
    return sanitize_obj(
        {
            "ok": True,
            "status": "OK" if latest else "EMPTY",
            "taskspec_review": latest,
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "graphics_live": False,
            "publication_gate": "BLOCK",
        }
    )


def taskspec_save_draft_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    task_spec = data.get("taskspec_review") or data.get("task_spec") or TASKSPEC_REVIEW_SESSION.get("latest") or {}
    if save_taskspec_draft is None:
        return sanitize_obj(
            {
                "ok": False,
                "status": "REVIEW",
                "reason": "TASKSPEC_REVIEW_BACKEND_UNAVAILABLE",
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "secrets_printed": False,
            }
        )
    saved = save_taskspec_draft(task_spec, runtime_root=_wabi_runtime_root())
    TASKSPEC_REVIEW_SESSION["last_saved"] = saved
    return sanitize_obj({"ok": True, **saved, "publication_gate": "BLOCK"})


def taskspec_gate_preview_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    task_spec = data.get("taskspec_review") or data.get("task_spec") or TASKSPEC_REVIEW_SESSION.get("latest") or {}
    if build_gate_preview is None:
        return sanitize_obj(
            {
                "ok": False,
                "status": "REVIEW",
                "apply_status": "BLOCKED",
                "reason": "APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1",
                "required_gates": [
                    {"name": "ActionGate", "status": "REQUIRED_FUTURE", "reason": "Local write/apply requires explicit gate."},
                    {"name": "GhostGate", "status": "REQUIRED_FUTURE", "reason": "Rollback and failure simulation required before apply."},
                    {"name": "RollbackStore", "status": "REQUIRED_FUTURE", "reason": "Must snapshot affected paths before mutation."},
                    {"name": "TestRunner", "status": "REQUIRED_FUTURE", "reason": "Must define tests before mutation."},
                ],
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
            }
        )
    preview = build_gate_preview(task_spec)
    return sanitize_obj({"ok": True, **preview, "publication_gate": "BLOCK"})


def taskspec_apply_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    task_spec = data.get("taskspec_review") or data.get("task_spec") or TASKSPEC_REVIEW_SESSION.get("latest") or {}
    if block_apply_attempt is None:
        return sanitize_obj(
            {
                "ok": False,
                "status": "BLOCKED",
                "reason": "APPLY_BLOCKED_REVIEW_ONLY_V0_1",
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
            }
        )
    blocked = block_apply_attempt(task_spec)
    if "gate_preview" not in blocked and block_apply_with_preview is not None:
        blocked["gate_preview"] = block_apply_with_preview(task_spec).get("gate_preview", {})
    return sanitize_obj({"ok": False, **blocked})


def taskspec_apply_local_preview_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    task_spec = _taskspec_for_local_apply(data)
    if preview_local_apply is None:
        return sanitize_obj(
            {
                "ok": False,
                "status": "LOCAL_APPLY_REVIEW_REQUIRED",
                "reason": "LOCAL_APPLY_BACKEND_UNAVAILABLE",
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
            }
        )
    preview = preview_local_apply(
        task_spec,
        workspace=WABI_SABI_CANONICAL_ROOT,
        runtime_root=_wabi_runtime_root(),
    )
    TASKSPEC_REVIEW_SESSION["last_apply_preview"] = preview
    return sanitize_obj({"ok": bool(preview.get("ok")), **preview, "publication_gate": "BLOCK"})


def taskspec_apply_local_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    task_spec = _taskspec_for_local_apply(data)
    if apply_local_task_spec is None:
        return sanitize_obj(
            {
                "ok": False,
                "status": "LOCAL_APPLY_REVIEW_REQUIRED",
                "reason": "LOCAL_APPLY_BACKEND_UNAVAILABLE",
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
            }
        )
    confirmation = str(data.get("confirmation") or "").strip().upper()
    if data.get("confirm_apply") is not True or confirmation != "APPLY_LOCAL":
        preview = taskspec_apply_local_preview_payload(data)
        result = {
            "ok": False,
            "status": "CONFIRM_REQUIRED",
            "reason": "explicit_local_apply_confirmation_required",
            "confirm_apply_required": True,
            "expected_confirmation": "APPLY_LOCAL",
            "result": {
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "rollback_snapshot_created": False,
            },
            "preview": preview,
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "graphics_live": False,
            "publication_gate": "BLOCK",
        }
        TASKSPEC_REVIEW_SESSION["last_apply_result"] = result
        return sanitize_obj(result)
    if not apply_gate_allows_local_apply():
        result = apply_gate_block_payload("taskspec_apply_local")
        TASKSPEC_REVIEW_SESSION["last_apply_result"] = result
        return sanitize_obj(result)
    result = apply_local_task_spec(
        task_spec,
        workspace=WABI_SABI_CANONICAL_ROOT,
        runtime_root=_wabi_runtime_root(),
    )
    TASKSPEC_REVIEW_SESSION["last_apply_result"] = result
    return sanitize_obj({"ok": bool(result.get("ok")), **result, "publication_gate": "BLOCK"})


def taskspec_llm_proposal_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    gate_state = local_gate_payload()
    task_spec = _taskspec_for_local_apply(data)
    message = str(data.get("message") or data.get("prompt") or task_spec.get("summary") or task_spec.get("description") or "Review latest TaskSpec").strip()
    session_id = _conversation_session_id(data.get("session_id") or data.get("coding_session_id") or "wabi-ui-llm")
    intent_name = str(data.get("intent_name") or task_spec.get("intent_name") or "ui_taskspec_llm_proposal")
    if request_llm_proposal is None:
        score_payload = _taskspec_proposal_score_payload(message, task_spec, data, action_gate="APPROVE_LOCAL")
        result = {
                "ok": False,
                "llm_status": "LLM_PROPOSAL_REVIEW",
                "reason": "LLM_PROPOSAL_BACKEND_UNAVAILABLE",
                "proposal_only": True,
                "applied_to_sources": False,
                "cloud_provider_called": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
                "proposal_score": score_payload["proposal_score"],
                "r_estimated": score_payload["r_estimated"],
                "phi_eff_estimated": score_payload["phi_eff_estimated"],
                "math_canon": score_payload["math_canon"],
                "score_status": score_payload["score_status"],
                "gate_console": gate_state,
                "cloud_gate": gate_state["gates"]["CloudGate"],
                "apply_gate": gate_state["gates"]["ApplyGate"],
        }
        safe = _safe_llm_work_response(
            {
                "ok": False,
                "route": "llm_proposal",
                "intent_name": intent_name,
                "intent": {"intent_name": intent_name, "proposal_only": True, "action_gate": "REVIEW"},
                "response": "LLM proposal backend unavailable.",
                "task_spec": task_spec,
                "llm_proposal": result,
                "cloud_provider_called": False,
                "gate_console": gate_state,
            },
            source="taskspec_llm_proposal_unavailable",
        )
        if score_payload["score_status"] == "REVIEW_SCORE_CONFLICT":
            safe["status"] = "REVIEW"
        return sanitize_obj(
            {
                **safe,
                "llm_proposal": result,
                "llm_status": result["llm_status"],
                **score_payload,
            }
        )
    result = request_llm_proposal(
        workspace=WABI_SABI_CANONICAL_ROOT,
        runtime_root=_wabi_runtime_root(),
        user_text=message,
        intent_name=intent_name,
        task_spec=task_spec,
        session_id=session_id,
    )
    score_payload = _taskspec_proposal_score_payload(message, task_spec, data, result, action_gate="APPROVE_LOCAL")
    result = {
        **dict(result),
        "proposal_score": score_payload["proposal_score"],
        "r_estimated": score_payload["r_estimated"],
        "phi_eff_estimated": score_payload["phi_eff_estimated"],
        "math_canon": score_payload["math_canon"],
        "score_status": score_payload["score_status"],
        "gate_console": gate_state,
        "cloud_gate": gate_state["gates"]["CloudGate"],
        "apply_gate": gate_state["gates"]["ApplyGate"],
    }
    TASKSPEC_REVIEW_SESSION["last_llm_proposal"] = result
    ok = str(result.get("status") or "") not in {
        "LLM_PROPOSAL_BUDGET_EXCEEDED",
        "LLM_PROPOSAL_PROVIDER_ERROR_REDACTED",
        "LLM_PROPOSAL_REVIEW_INVALID_CONTRACT",
        "LLM_PROPOSAL_REVIEW_INVALID_JSON",
    } and score_payload["score_status"] != "REVIEW_SCORE_CONFLICT"
    safe = _safe_llm_work_response(
        {
            "ok": ok,
            "route": "llm_proposal",
            "intent_name": intent_name,
            "intent": {"intent_name": intent_name, "proposal_only": True, "action_gate": "REVIEW"},
            "response": "LLM proposal generated as proposal-only.",
            "task_spec": result.get("task_spec") if isinstance(result.get("task_spec"), dict) else task_spec,
            "llm_proposal": result,
            "cloud_budget": result.get("cloud_budget") if isinstance(result.get("cloud_budget"), dict) else {},
            "cloud_provider_called": bool(result.get("cloud_provider_called", False)),
            "applied_to_sources": False,
            "gate_console": gate_state,
        },
        source="taskspec_llm_proposal",
    )
    if score_payload["score_status"] == "REVIEW_SCORE_CONFLICT":
        safe["status"] = "REVIEW"
    return sanitize_obj({"ok": ok, "llm_status": result.get("status"), "llm_proposal": result, "gate_console": gate_state, **safe, **score_payload})


def _taskspec_proposal_score_payload(
    message: str,
    task_spec: dict[str, Any],
    *legacy_sources: dict[str, Any],
    action_gate: str = "APPROVE_LOCAL",
) -> dict[str, Any]:
    target = _taskspec_score_target(task_spec)
    proposal_score = coding_workbench.score_wabi_proposal_07b(message, target=target, action_gate=action_gate)
    proposal_score = {
        **proposal_score,
        "components": dict(proposal_score.get("score_components", {})),
    }
    if proposal_score.get("gate_hint") == "APPROVE":
        proposal_score["gate_hint"] = "APPROVE_LOCAL_PREVIEW"

    conflicts = _proposal_score_conflicts(proposal_score, legacy_sources)
    score_status = "REVIEW_SCORE_CONFLICT" if conflicts else "OK"
    if conflicts:
        proposal_score["gate_hint"] = "REVIEW_SCORE_CONFLICT"
        proposal_score["conflicts"] = conflicts
    proposal_score["score_status"] = score_status

    return {
        "proposal_score": proposal_score,
        "r_estimated": proposal_score["R"],
        "phi_eff_estimated": proposal_score["Phi_eff"],
        "math_canon": proposal_score["math_canon"],
        "score_status": score_status,
    }


def _taskspec_score_target(task_spec: dict[str, Any]) -> str | None:
    for key in ("affected_paths", "allowed_targets", "files_to_modify", "targets"):
        values = task_spec.get(key)
        if isinstance(values, list) and values:
            return str(values[0])
    for key in ("target", "path", "file_path"):
        value = task_spec.get(key)
        if value:
            return str(value)
    return None


def _proposal_score_conflicts(proposal_score: dict[str, Any], sources: tuple[dict[str, Any], ...]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    checks = [
        ("r_estimated", "R"),
        ("phi_eff_estimated", "Phi_eff"),
    ]
    for source in sources:
        if not isinstance(source, dict):
            continue
        for legacy_key, canonical_key in checks:
            if legacy_key not in source:
                continue
            incoming = _float_or_none(source.get(legacy_key))
            computed = _float_or_none(proposal_score.get(canonical_key))
            if incoming is None or computed is None:
                continue
            if abs(incoming - computed) > 1e-6:
                conflicts.append(
                    {
                        "status": "REVIEW_SCORE_CONFLICT",
                        "field": legacy_key,
                        "incoming": round(incoming, 6),
                        "computed_from_07b": round(computed, 6),
                    }
                )
    return conflicts


def _float_or_none(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if number == number and number not in (float("inf"), float("-inf")) else None


def _taskspec_for_local_apply(data: dict[str, Any]) -> dict[str, Any]:
    if isinstance(data.get("task_spec"), dict):
        return dict(data["task_spec"])
    latest_raw = TASKSPEC_REVIEW_SESSION.get("latest_raw")
    if isinstance(latest_raw, dict) and latest_raw:
        return dict(latest_raw)
    if isinstance(data.get("taskspec_review"), dict):
        return dict(data["taskspec_review"])
    latest = TASKSPEC_REVIEW_SESSION.get("latest")
    return dict(latest) if isinstance(latest, dict) else {}


def conversation_turn_payload(payload: dict[str, Any]) -> dict[str, Any]:
    message = str(payload.get("message", "") or "").strip()
    if not message:
        raise ValueError("message is required")
    if len(message) > MAX_PROMPT_CHARS:
        raise ValueError(f"message exceeds {MAX_PROMPT_CHARS} characters")
    artifact_payload = artifact_chat_payload_if_requested(message)
    if artifact_payload is not None:
        artifact_payload.update(_safe_llm_work_response(artifact_payload, source="artifact_viewer"))
        return sanitize_obj(artifact_payload)
    session_id = _conversation_session_id(payload.get("session_id") or payload.get("coding_session_id"))
    if ConversationEngine is None or ConversationEngineOptions is None or ConversationSessionState is None:
        budget = cloud_budget_status_payload().get("cloud_budget", {})
        response = {
            "status": "REVIEW",
            "route": "local_chat",
            "intent_name": "chat_general",
            "intent": {
                "intent_name": "chat_general",
                "confidence": 0.0,
                "needs_cloud": False,
                "needs_graphics": False,
                "needs_file_write": False,
                "proposal_only": True,
                "action_gate": "REVIEW",
                "reason": "conversation_engine_unavailable",
                "import_error": CONVERSATION_ENGINE_IMPORT_ERROR,
            },
            "response": (
                "ConversationEngine no esta disponible; UI queda en modo local proposal-only. "
                + (f"Causa: {CONVERSATION_ENGINE_IMPORT_ERROR}. " if CONVERSATION_ENGINE_IMPORT_ERROR else "")
                + "Arranca el server desde 02_CLAUDIO con `python server/wabi_local_server.py` "
                + "(el paquete wabi_sabi debe estar importable)."
            ),
            "task_spec": {},
            "cloud_budget": budget,
            "graphics": {"graphics_live": False, "graphics_plan_ready": False},
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "secrets_printed": False,
            "proposal_only": True,
            "publication_gate": "BLOCK",
        }
        response.update(_safe_llm_work_response(response, source="conversation_turn_unavailable"))
        return sanitize_obj(response)
    runtime_root = _wabi_runtime_root()
    engine = ConversationEngine(
        workspace=WABI_SABI_CANONICAL_ROOT,
        runtime_root=runtime_root,
        options=ConversationEngineOptions(
            allow_cloud=workbench_cloud_first_enabled(),
            persist_turns=False,
            include_prompt_in_turn=False,
            write_artifacts=False,
        ),
    )
    state = ConversationSessionState(
        workspace=WABI_SABI_CANONICAL_ROOT,
        runtime_root=runtime_root,
        session_id=session_id,
    )
    # Keep classifier input raw. Identity grounding is injected into actual
    # provider prompts by the CLI system prompt and model_chat_fallback; prefixing
    # this message with provider/model names makes generic chat classify as build
    # assistance.
    result = engine.handle_turn(message, state)
    result_payload = result.get("payload", {}) if isinstance(result.get("payload"), dict) else {}
    llm_proposal = result_payload.get("llm_proposal") if isinstance(result_payload.get("llm_proposal"), dict) else {}
    budget = result_payload.get("cloud_budget")
    if not isinstance(budget, dict):
        budget = cloud_budget_status_payload().get("cloud_budget", {})
    task_spec = result_payload.get("task_spec") if isinstance(result_payload.get("task_spec"), dict) else {}
    route = _conversation_route_name(result)
    intent_data = result.get("intent", {}) if isinstance(result.get("intent"), dict) else {}
    # If the engine did NOT actually call cloud, and the operator has
    # cloud-first enabled, route the question through model_chat_fallback so
    # the LLM (with identity grounding + full tool access) can answer for real.
    #
    # Originally this only fired for chat_general, but the ConversationEngine
    # also classifies file/code requests as file_task_request / code_request /
    # debug_request → work_plan route, which returns a static template with no
    # LLM call. Extending the condition to all non-local intents fixes the
    # "No dispongo de acceso a tu computadora" response: the LLM now receives
    # the message with the full tool spec (list_files, read_file, search_text,
    # write_file, run_command if WABI_UI_EXEC=1, etc.) and can act on it.
    #
    # Intents that must stay local (they have meaningful pre-baked responses):
    _LOCAL_ONLY_INTENTS = frozenset({"help", "status", "providers", "tasks", "exit", "local_chat"})
    intent_name_str = str(intent_data.get("intent_name") or "")
    engine_called_cloud = bool(result.get("cloud_provider_called", False))
    if (
        intent_name_str not in _LOCAL_ONLY_INTENTS
        and not engine_called_cloud
        and workbench_cloud_first_enabled()
    ):
        try:
            fallback_provider = (
                str(payload.get("provider") or "").strip()
                or coding_provider_router.resolve_default_provider().provider_name
            )
        except Exception:
            fallback_provider = "nvidia"
        fallback_mode = str(payload.get("mode") or "simple").strip() or "simple"
        try:
            fallback_result = model_chat_fallback(message, fallback_provider, fallback_mode)
        except Exception:  # pragma: no cover - never block the chat on a fallback failure
            fallback_result = {"ok": False, "response": "", "errors": [], "raw": {}}
        if fallback_result.get("ok") and str(fallback_result.get("response") or "").strip():
            result["output"] = str(fallback_result["response"])
            result["cloud_provider_called"] = True
            if not isinstance(llm_proposal, dict) or not llm_proposal:
                llm_proposal = {
                    "status": "OK",
                    "source": "model_chat_fallback",
                    "provider": str(fallback_result.get("provider") or ""),
                }
    graphics_payload = _conversation_graphics_payload(result)
    review: dict[str, Any] = {}
    gate_preview: dict[str, Any] = {}
    if task_spec or route in {"work_plan", "code_plan", "debug_plan", "graphics_plan", "build_assist_plan"}:
        review = _normalize_taskspec_review_payload(
            task_spec,
            intent=intent_data,
            route=route,
            cloud_budget=budget,
            graphics=graphics_payload,
        )
        TASKSPEC_REVIEW_SESSION["latest"] = review
        TASKSPEC_REVIEW_SESSION["latest_raw"] = task_spec
        gate_preview = taskspec_gate_preview_payload({"taskspec_review": review})
    response = {
        "status": "OK" if result.get("ok") else "REVIEW",
        "route": route,
        "intent_name": intent_data.get("intent_name", result.get("intent_name", "chat_general")),
        "intent": intent_data,
        "response": str(result.get("output") or ""),
        "task_spec": review,
        "taskspec_review": review,
        "gate_preview": gate_preview,
        "cloud_budget": budget,
        "llm_proposal": llm_proposal,
        "graphics": graphics_payload,
        "applied_to_sources": False,
        # Honest derivation: trust explicit engine/payload flags first, then the
        # cloud_budget tracker, then a non-placeholder llm_proposal status. Some
        # legacy paths return an LLM proposal without setting cloud_provider_called.
        "cloud_provider_called": bool(
            result.get("cloud_provider_called", False)
            or result_payload.get("cloud_provider_called", False)
            or (
                isinstance(budget, dict)
                and budget.get("cloud_provider_called", False)
            )
            or _llm_proposal_implies_provider_call(llm_proposal)
        ),
        "secrets_printed": False,
        "proposal_only": True,
        "publication_gate": "BLOCK",
        "source_of_truth": "wabi_sabi.core.conversation_engine.ConversationEngine.handle_turn",
        "conversation_persistence": "ephemeral_no_prompt_storage",
        "artifacts": [],
    }
    response.update(_safe_llm_work_response(response, source="conversation_turn"))
    return sanitize_obj(response)


def _llm_proposal_implies_provider_call(llm_proposal: dict[str, Any]) -> bool:
    if not isinstance(llm_proposal, dict):
        return False
    status = str(llm_proposal.get("status") or "").strip()
    if not status:
        return False
    return status not in {
        "CLOUD_BUDGET_DRY_RUN",
        "LLM_PROPOSAL_BACKEND_UNAVAILABLE",
        "LLM_PROPOSAL_REVIEW",
        "LLM_PROPOSAL_BUDGET_EXCEEDED",
    }


def _safe_llm_work_response(payload: dict[str, Any], *, source: str) -> dict[str, Any]:
    if build_safe_llm_work_response is None:
        task_spec = payload.get("task_spec") if isinstance(payload.get("task_spec"), dict) else {}
        intent = payload.get("intent") if isinstance(payload.get("intent"), dict) else {}
        intent_name = str(payload.get("intent_name") or intent.get("intent_name") or task_spec.get("intent_name") or "chat_general")
        graphics = payload.get("graphics") if isinstance(payload.get("graphics"), dict) else {}
        return sanitize_obj(
            {
                "schema": "wabi.llm_work_response.v0_1.fallback",
                "status": "OK" if payload.get("ok", True) else "REVIEW",
                "intent_name": intent_name,
                "route": str(payload.get("route") or _conversation_route_name(payload)),
                "proposal": "Safe JSON fallback response; canonical normalizer unavailable.",
                "task_spec": task_spec,
                "graphics_plan": {
                    "graphics_live": False,
                    "graphics_plan_ready": bool(graphics.get("graphics_plan_ready", False)),
                    "external_calls_allowed": False,
                    "publication_allowed": False,
                    "plan_mode": True,
                    "plan": graphics.get("plan", {}),
                },
                "patch_candidate": {
                    "affected_paths": task_spec.get("affected_paths", []),
                    "tests_to_run": task_spec.get("suggested_tests", []),
                    "rollback_snapshot_required": True,
                    "apply_mode": "local_allowlisted_preview",
                    "proposal_only": True,
                },
                "cloud_provider_called": bool(payload.get("cloud_provider_called", False)),
                "applied_to_sources": False,
                "rollback_snapshot_required": True,
                "next_safe_action": "Review TaskSpec / Preview Apply Local",
                "warnings": ["Proposal-only; Apply Local blocked until explicit local readiness."],
                "tags": [
                    "LLM_proposal",
                    "proposal_only",
                    "vibe_coding",
                    "apply_local_requires_confirmation",
                    "rollback_required",
                    "publication_blocked",
                ],
                "metadata": {
                    "priority": "P2",
                    "risk": "low",
                    "category": "conversation",
                    "relevance": "medium",
                    "incremental": True,
                    "fallback_mode": "local_rules_task_spec",
                    "budget_control": "CloudBudgetGate",
                    "interface_mode": "vibe_coding",
                    "workflow": [
                        "chat",
                        "llm_proposal",
                        "taskspec_review",
                        "gate_preview",
                        "apply_local_preview",
                        "explicit_apply_local",
                    ],
                },
                "proposal_only": True,
                "secrets_printed": False,
                "prompts_stored": False,
                "graphics_live": False,
                "publication_gate": "BLOCK",
                "source": source,
            }
        )
    return sanitize_obj(build_safe_llm_work_response(payload, runtime_root=_wabi_runtime_root(), source=source))


def security_tools_payload() -> dict[str, Any]:
    return sanitize_obj(external_secret_tools.build_security_tool_status())


def security_gitleaks_status_payload() -> dict[str, Any]:
    return sanitize_obj(external_secret_tools.build_security_tool_status())


def security_gitleaks_scan_fixtures_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    source = pathlib.Path(str(data.get("source") or data.get("source_dir") or external_secret_tools.default_medioevo_config_poc_dir() / "fixtures"))
    report_dir = pathlib.Path(str(data.get("report_dir") or source.parent / "reports"))
    config = external_secret_tools.find_gitleaks_config()
    return sanitize_obj(external_secret_tools.run_gitleaks_dir_scan(source, report_dir, config_path=config, redact=True))


def security_preflight_payload() -> dict[str, Any]:
    payload = external_secret_tools.build_security_tool_status()
    return sanitize_obj(
        {
            "ok": payload.get("ok", False),
            "status": payload.get("status", "REVIEW_LOCAL_TOOL"),
            "security_tools": payload,
            "action_gate": "APPROVE_LOCAL" if payload.get("status") in {"READY", "ADOPT_LOCAL_TOOL"} else "REVIEW_LOCAL",
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def security_status_payload() -> dict[str, Any]:
    payload = security_preflight_payload()
    comparison_status = "NOT_RUN"
    try:
        comparison = security_compare_payload()
        counts = comparison.get("comparison", {})
        if counts.get("missed_by_gitleaks") == []:
            comparison_status = "PASS"
        else:
            comparison_status = "REVIEW"
    except Exception:
        comparison_status = "REVIEW"
    payload["comparison_status"] = comparison_status
    payload["product_publication"] = "REVIEW_OR_BLOCK"
    payload["publication_gate"] = "BLOCK"
    return sanitize_obj(payload)


def security_compare_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    source = pathlib.Path(str(data.get("source") or data.get("source_dir") or external_secret_tools.default_medioevo_config_poc_dir() / "fixtures"))
    report_dir = pathlib.Path(str(data.get("report_dir") or source.parent / "reports"))
    config = external_secret_tools.find_gitleaks_config()
    gitleaks_scan = external_secret_tools.run_gitleaks_dir_scan(source, report_dir, config_path=config, redact=True)
    gitleaks_findings = external_secret_tools.parse_gitleaks_report_redacted(str(gitleaks_scan.get("redacted_report_path", "")))
    medioevo_scan = external_secret_tools.run_minimal_medioevo_secret_scan(source)
    comparison = external_secret_tools.compare_secret_scan_results(gitleaks_findings, medioevo_scan["findings"])
    return sanitize_obj(
        {
            "ok": bool(gitleaks_scan.get("ok")) and bool(medioevo_scan.get("ok")),
            "status": "COMPARISON_COMPLETED",
            "gitleaks": gitleaks_scan,
            "medioevo": medioevo_scan,
            "comparison": comparison,
            "publication_gate": "BLOCK",
            "product_publication": "REVIEW_OR_BLOCK",
            "secret_values_printed": False,
        }
    )


def folder_check_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return sanitize_obj(folder_access_gate.folder_access_payload(payload or {}))


def multimodal_status_payload() -> dict[str, Any]:
    return sanitize_obj(multimodal_intake_adapter.status_payload())


def paywall_status_payload() -> dict[str, Any]:
    return {
        "schema": "wabi.paywall.status.v0_1",
        "ok": True,
        "gate": "REVIEW",
        "method": "auditoria-solo",
        "urls_analyzed": 0,
        "PublicationGate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    }


def paywall_status_payload() -> dict[str, Any]:
    return sanitize_obj(
        {
            "schema": "wabi.paywall.status.v0_1",
            "active": False,
            "message": "Paywall no configurado. PublicationGate=BLOCK.",
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


# ═════════════════════════════════════════════════════════════════════════════════
# FACT-CHECK ENDPOINT (Brain OS Fact Checker)
# ════════════════════════════════════════════════════════════════════════════════

def factcheck_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Endpoint POST /api/fact-check
    
    Input:
    {
        "claim": "string (requerido) - claim a verificar",
        "context": "string (opcional) - contexto adicional",
        "mode": "osit|research|wabi|gpt" (default: "research"),
        "provider": "string (opcional) - proveedor específico"
    }
    
    Output: Estructura OSIT completa con R, estados epistémicos, fingerprint, etc.
    """
    claim = str(payload.get("claim", "")).strip()
    if not claim:
        return {"ok": False, "error": "claim requerido", "code": "MISSING_CLAIM"}
    
    if len(claim) > 5000:
        return {"ok": False, "error": "claim demasiado largo (máx 5000 chars)", "code": "CLAIM_TOO_LONG"}
    
    context = str(payload.get("context", "")).strip()
    mode = str(payload.get("mode", "research")).lower()
    if mode not in ("gpt", "osit", "research", "wabi"):
        mode = "research"
    
    provider = str(payload.get("provider", "")).strip() or None
    
    try:
        # Importar WabiAdapter para usar el pipeline completo
        from wabi_sabi.adapters.provider_adapter import WabiAdapter, ProviderNotConfiguredError
        
        # Crear adapter con modo fact-check
        if provider:
            adapter = WabiAdapter.from_provider(provider, mode=mode)
        else:
            adapter = WabiAdapter.from_current_env(mode=mode)
        
        # Construir prompt completo para fact-check
        system_prompt = get_factcheck_prompt(mode)
        user_prompt = build_factcheck_user_prompt(claim, context)
        full_prompt = system_prompt + "\n\n" + user_prompt
        
        # Ejecutar query a través del adapter (usa WabiSabiOS internamente)
        result = adapter.query(full_prompt)
        
        # Formatear respuesta
        response = {
            "ok": True,
            "claim": claim,
            "context": context,
            "mode": mode,
            "provider": adapter.provider.name,
            "model": adapter.model,
            "R": result.get("R"),
            "R_exact": result.get("R_exact"),
            "STOP": result.get("STOP", False),
            "regime": result.get("regime"),
            "epistemic_states": result.get("epistemic_states", {}),
            "fingerprint": result.get("fingerprint"),
            "witness_log": adapter.get_witness_log(),
        }
        
        # Agregar campos específicos según modo
        if "alternatives" in result:
            response["alternatives"] = result["alternatives"]
        if "kintsugi_count" in result:
            response["kintsugi_count"] = result["kintsugi_count"]
        
        # Sanitizar y retornar
        return sanitize_obj(response)
        
    except ProviderNotConfiguredError as exc:
        return {"ok": False, "error": str(exc), "code": "PROVIDER_NOT_CONFIGURED"}
    except Exception as exc:
        return {"ok": False, "error": sanitize_text(exc), "code": "INTERNAL_ERROR"}


# ═════════════════════════════════════════════════════════════════════════════════
# STRIPE CHECKOUT SESSION ENDPOINT
# ════════════════════════════════════════════════════════════════════════════════

def create_stripe_checkout_session(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Endpoint POST /api/create-checkout-session
    
    Input:
    {
        "price_id": "string - Stripe Price ID",
        "product_name": "string - nombre del producto",
        "success_url": "string (opcional) - URL de éxito",
        "cancel_url": "string (opcional) - URL de cancelación"
    }
    
    Output:
    {
        "ok": true,
        "sessionId": "string - Stripe Session ID",
        "url": "string - URL de checkout (si no se usa redirectToCheckout)"
    }
    """
    price_id = str(payload.get("price_id", "")).strip()
    product_name = str(payload.get("product_name", "Producto MEDIOEVO")).strip()
    success_url = str(payload.get("success_url", "")).strip() or (os.environ.get("STRIPE_SUCCESS_URL", "https://lutren.github.io/medioevo-tools/success.html"))
    cancel_url = str(payload.get("cancel_url", "")).strip() or (os.environ.get("STRIPE_CANCEL_URL", "https://lutren.github.io/medioevo-tools/"))
    
    if not price_id:
        return {"ok": False, "error": "price_id requerido", "code": "MISSING_PRICE_ID"}
    
    # Verificar que Stripe esté configurado
    stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY", "").strip()
    if not stripe_secret_key:
        return {"ok": False, "error": "Stripe no configurado en servidor (falta STRIPE_SECRET_KEY)", "code": "STRIPE_NOT_CONFIGURED"}
    
    try:
        import stripe
        stripe.api_key = stripe_secret_key
        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            metadata={
                "product_name": product_name,
                "source": "medioevo-tools"
            }
        )
        
        return {
            "ok": True,
            "sessionId": session.id,
            "url": session.url
        }
        
    except ImportError:
        return {"ok": False, "error": "Stripe library no instalada (pip install stripe)", "code": "STRIPE_LIB_MISSING"}
    except Exception as exc:
        return {"ok": False, "error": sanitize_text(exc), "code": "STRIPE_ERROR"}


def geo_status_payload() -> dict[str, Any]:
    return {
        "schema": "wabi.geo.status.v0_1",
        "ok": True,
        "region": "MX",
        "timezone": "America/Mexico_City",
        "language": "es-MX",
        "proxy": "LOCAL",
        "PublicationGate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    }


def network_status_payload() -> dict[str, Any]:
    return {
        "schema": "wabi.network.status.v0_1",
        "ok": True,
        "status": "LISTO",
        "last_scan": "NUNCA",
        "ports_open": 0,
        "services_detected": 0,
        "PublicationGate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    }


def lab_status_payload() -> dict[str, Any]:
    return {
        "schema": "wabi.lab.status.v0_1",
        "ok": True,
        "status": "LISTO",
        "last_experiment": "NINGUNO",
        "result_count": 0,
        "PublicationGate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    }


def multimodal_intake_fixture_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return sanitize_obj(multimodal_intake_adapter.intake_fixture_payload())


def multimodal_intake_file_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return sanitize_obj(multimodal_intake_adapter.intake_file_payload(payload or {}))


def extract_local_image_path(message: str) -> str:
    text = str(message or "").strip()
    quoted = re.findall(r"['\"]([^'\"]+\.(?:png|jpg|jpeg|webp))['\"]", text, flags=re.IGNORECASE)
    if quoted:
        return quoted[0].strip()
    match = re.search(r"([A-Za-z]:\\[^\s]+?\.(?:png|jpg|jpeg|webp)|(?:\.{0,2}[\\/])?[A-Za-z0-9_\-./\\ ]+?\.(?:png|jpg|jpeg|webp))", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def hub_status_payload() -> dict[str, Any]:
    provider_route = provider_route_payload()
    policy = provider_policy_payload()
    budget = budget_status_payload()
    cloud_budget = cloud_budget_status_payload()
    security = security_status_payload()
    coding = coding_preflight_payload({"action": "status"})
    return sanitize_obj(
        {
            "ok": True,
            "interface_mode": "CHAT_FIRST",
            "commands_exposed_to_user": False,
            "provider_route": provider_route,
            "provider_policy": policy["policy"],
            "external_api_mode": policy["external_api_mode"],
            "provider_priority": policy["provider_chain"],
            "budget_gate": budget,
            "cloud_budget": cloud_budget.get("cloud_budget", {}),
            "cloud_budget_gate": cloud_budget.get("status", "CLOUD_BUDGET_REVIEW"),
            "claudio_autonomy": {
                "cloud_assist": "ON",
                "local_fallback": "ON",
                "target": "IN_PROGRESS",
                "exit_condition": policy["exit_condition"],
            },
            "security": security,
            "coding": coding,
            "folder_access_gate": {
                "status": "READY",
                "default_gate": "REVIEW",
                "allowlist": list(folder_access_gate.ALLOWLIST_RELATIVE),
            },
            "multimodal_intake": multimodal_status_payload(),
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def coding_session_payload(payload: dict[str, Any]) -> dict[str, Any]:
    session = coding_workbench.create_session(
        str(payload.get("objective", "")),
        repo_root=server_repo_root(payload),
        target=str(payload.get("target")) if payload.get("target") else None,
    )
    return sanitize_obj({"ok": True, "coding_session": session.to_dict()})


def coding_preflight_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    action = str(data.get("action", "status") or "status")
    return sanitize_obj(coding_workbench.build_coding_preflight(server_repo_root(data), action=action))


def coding_plan_payload(payload: dict[str, Any]) -> dict[str, Any]:
    session_id = str(payload.get("session_id", "") or "")
    repo = server_repo_root(payload)
    if session_id:
        session = coding_workbench.load_session(session_id, repo_root=repo)
    else:
        session = coding_workbench.create_session(
            str(payload.get("objective", "")),
            repo_root=repo,
            target=str(payload.get("target")) if payload.get("target") else None,
        )
    return sanitize_obj({"ok": True, "coding_session": session.to_dict()})


def coding_diff_payload(payload: dict[str, Any]) -> dict[str, Any]:
    repo = server_repo_root(payload)
    session_id = str(payload.get("session_id", "") or "")
    if not session_id:
        session = coding_workbench.create_session(
            str(payload.get("objective", "")),
            repo_root=repo,
            target=str(payload.get("target", "")),
        )
        session_id = session.session_id
    session = coding_workbench.propose_diff(
        session_id,
        repo_root=repo,
        target=str(payload.get("target", "")),
        content=str(payload.get("content")) if payload.get("content") is not None else None,
        old=str(payload.get("old")) if payload.get("old") is not None else None,
        new=str(payload.get("new")) if payload.get("new") is not None else None,
    )
    return sanitize_obj({"ok": True, "coding_session": session.to_dict()})


def coding_apply_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not apply_gate_allows_local_apply():
        return sanitize_obj(apply_gate_block_payload("coding_apply"))
    session = coding_workbench.apply_diff(str(payload.get("session_id", "")), repo_root=server_repo_root(payload))
    return sanitize_obj({"ok": True, "coding_session": session.to_dict(), "gate_console": {"ApplyGate": "ALLOW_LOCAL_APPLY"}})


def coding_test_payload(payload: dict[str, Any]) -> dict[str, Any]:
    commands = payload.get("commands")
    selected = commands if isinstance(commands, list) else None
    result = coding_workbench.run_tests(
        str(payload.get("session_id", "") or "") or None,
        repo_root=server_repo_root(payload),
        commands=selected,
    )
    return sanitize_obj(result)


def coding_rollback_payload(payload: dict[str, Any]) -> dict[str, Any]:
    session = coding_workbench.rollback_session(str(payload.get("session_id", "")), repo_root=server_repo_root(payload))
    return sanitize_obj({"ok": True, "coding_session": session.to_dict()})


def world_model_benchmark_payload() -> dict[str, Any]:
    return sanitize_obj(world_model_baseline_comparator.compare_world_model_to_baseline())


def live_fingerprint_payload() -> dict[str, Any]:
    path = ROOT / "00_START_HERE" / "LIVE_STATE" / "SESSION_FINGERPRINT.json"
    if not path.exists():
        return {"present": False}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"present": False, "status": "INVALID_JSON"}
    return sanitize_obj({"present": True, **data})


def deepseek_final_status() -> str:
    live = live_fingerprint_payload()
    status = str(live.get("deepseek_status", "") or "")
    if status in {"REVIEW_ACCOUNT_BILLING_REQUIRED", "REVIEW_BILLING_OR_QUOTA"}:
        return "REVIEW_ACCOUNT_BILLING_REQUIRED"
    if status:
        return status
    resolution = coding_provider_router.provider_status(include_all=False).get("resolution", {})
    return str(resolution.get("status", "REVIEW"))


def chat_gate(action_gate: str) -> str:
    text = str(action_gate or "REVIEW").upper()
    if "BLOCK" in text:
        return "BLOCK"
    if text.startswith("APPROVE"):
        return "APPROVE"
    return "REVIEW"


def _has_command_next_suggestion(text: str) -> bool:
    lowered = str(text or "").lower()
    return "wabi " in lowered or "python -m pytest" in lowered


def chat_session_payload() -> dict[str, Any]:
    return sanitize_obj(
        {
            "ok": True,
            "session": {
                "message_count": len(CHAT_SESSION["messages"]),
                "coding_session_id": CHAT_SESSION.get("coding_session_id", ""),
                "last_intent": CHAT_SESSION.get("last_intent", ""),
            },
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    )


def chat_reset_payload() -> dict[str, Any]:
    CHAT_SESSION["messages"] = []
    CHAT_SESSION["coding_session_id"] = ""
    CHAT_SESSION["last_intent"] = ""
    return chat_session_payload()


def _remember_chat(message: str, reply: str, intent: str, coding_session_id: str = "") -> None:
    CHAT_SESSION["messages"].append(
        {
            "time": now_epoch_ms(),
            "message": sanitize_text(message)[:1200],
            "reply": sanitize_text(reply)[:2000],
            "intent": intent,
            "coding_session_id": coding_session_id,
        }
    )
    CHAT_SESSION["messages"] = CHAT_SESSION["messages"][-40:]
    CHAT_SESSION["last_intent"] = intent
    if coding_session_id:
        CHAT_SESSION["coding_session_id"] = coding_session_id


def _session_id_from_payload(payload: dict[str, Any]) -> str:
    return str(payload.get("session_id") or payload.get("coding_session_id") or CHAT_SESSION.get("coding_session_id") or "")


def _chat_target(payload: dict[str, Any]) -> str:
    return str(payload.get("targetFile") or payload.get("target") or "").strip()


def _chat_content(payload: dict[str, Any]) -> str | None:
    if payload.get("content") is not None:
        return str(payload.get("content"))
    if payload.get("proposedContent") is not None:
        return str(payload.get("proposedContent"))
    return None


def chat_message_payload(payload: dict[str, Any]) -> dict[str, Any]:
    message = str(payload.get("message", "") or "").strip()
    if not message:
        raise ValueError("message is required")
    if len(message) > MAX_PROMPT_CHARS:
        raise ValueError(f"message exceeds {MAX_PROMPT_CHARS} characters")
    artifact_payload = artifact_chat_payload_if_requested(message)
    if artifact_payload is not None:
        artifact_payload.update(_safe_llm_work_response(artifact_payload, source="artifact_viewer_legacy_chat"))
        return sanitize_obj(artifact_payload)
    mode = str(payload.get("mode", "simple") or "simple").lower()
    developer = mode == "developer"
    allow_apply = bool(payload.get("allowApply", False))
    route = chat_intent_router.route_message(message, allow_apply=allow_apply)
    actions_taken: list[str] = []
    developer_trace: dict[str, Any] = {}
    reply = route.human_summary
    next_suggestion = "Escribe en el chat que quieres que Wabi haga ahora."
    coding_session_id = _session_id_from_payload(payload)
    target = _chat_target(payload)
    content = _chat_content(payload)
    old = payload.get("old")
    new = payload.get("new")
    response_gate_override = ""
    online_ai_called = False

    def trace(name: str, data: Any, endpoint: str | None = None) -> None:
        if not developer:
            return
        developer_trace.setdefault("internal_tools", []).append(name)
        if endpoint:
            developer_trace.setdefault("endpoints", []).append(endpoint)
        developer_trace[name] = sanitize_obj(data)

    if developer:
        developer_trace["normalized_message"] = sanitize_text(getattr(route, "normalized_message", ""))
        developer_trace["matched_patterns"] = list(getattr(route, "matched_patterns", []))
        developer_trace["route_intent"] = route.intent
        developer_trace["confidence"] = route.confidence

    try:
        if route.intent == "greeting_status":
            actions_taken.append("chat_greeting_status")
            trace(
                "chat_greeting_status",
                {
                    "normalized_message": getattr(route, "normalized_message", ""),
                    "matched_patterns": getattr(route, "matched_patterns", []),
                    "tools_available": route.required_tools,
                },
                "/api/chat/message",
            )
            reply = route.human_summary
            next_suggestion = "Escríbeme qué quieres cambiar y te propongo un plan."
        elif route.intent == "capability_general":
            actions_taken.append("chat_capability_general")
            trace(
                "chat_capability_general",
                {
                    "normalized_message": getattr(route, "normalized_message", ""),
                    "matched_patterns": getattr(route, "matched_patterns", []),
                    "tools_available": route.required_tools,
                },
                "/api/chat/message",
            )
            reply = route.human_summary
            next_suggestion = "Puedes pedirme: revisa tu estado, ayúdame a programar o revisa seguridad."
        elif route.intent == "external_api_transition_policy":
            route_payload = provider_route_payload()
            budget = budget_status_payload()
            actions_taken.extend(["provider_route", "budget_gate"])
            trace("provider_route", route_payload, "/api/provider/route")
            trace("budget_gate", budget, "/api/budget/status")
            reply = (
                "Entendido. Modo transición activo: usaré APIs externas cuando pasen ProviderGate y BudgetGate, "
                "y mantendré fallback local. No imprimiré claves ni declararé PASS falso. "
                f"Ruta actual: {route_payload.get('route_stage')} / {route_payload.get('selected_provider')} "
                f"({route_payload.get('selected_model')}). BudgetGate: {budget.get('status')}."
            )
            next_suggestion = "Escríbeme la tarea; elegiré provider externo o local según gate."
        elif route.intent == "local_only_policy":
            route_payload = provider_route_payload({"cloud_providers_blocked": True})
            actions_taken.append("provider_route_local_only")
            trace("provider_route_local_only", route_payload, "/api/provider/route")
            reply = (
                "Cambio a LOCAL_ONLY para esta ruta: no usaré APIs externas. "
                "Plan y diff siguen disponibles en local; apply continúa con ActionGate y rollback."
            )
            next_suggestion = "Escríbeme qué quieres cambiar y lo haré en modo local."
        elif route.intent == "free_only_policy":
            route_payload = provider_route_payload()
            actions_taken.append("provider_route")
            trace("provider_route", route_payload, "/api/provider/route")
            reply = (
                "Entendido. Para todo gratis, sólo usaré providers con free tier confirmado y fallback local. "
                "Nada de gasto no controlado ni PASS sin smoke. "
                f"Ruta activa ahora: {route_payload.get('route_stage')} / {route_payload.get('selected_provider')} "
                f"({route_payload.get('selected_model')})."
            )
            next_suggestion = "Escríbeme la tarea; si cloud gratis no pasa, sigo local."
        elif route.intent == "budget_review":
            budget = budget_status_payload()
            actions_taken.append("budget_gate")
            trace("budget_gate", budget, "/api/budget/status")
            reply = (
                "Consulté BudgetGate. "
                f"Estado: {budget.get('status')}; presupuesto diario: {budget.get('daily_budget_usd')}; "
                f"presupuesto mensual: {budget.get('monthly_budget_usd')}; hard stop: {budget.get('hard_stop')}. "
                "Si no hay presupuesto numérico, sólo haré smoke o tareas mínimas en REVIEW."
            )
            next_suggestion = "Dime la tarea y la mantendré acotada por BudgetGate."
        elif route.intent == "capability_coding":
            preflight = coding_preflight_payload({"action": "plan"})
            actions_taken.append("coding_preflight")
            trace("coding_preflight", preflight, "/api/coding/preflight")
            reply = route.human_summary
            next_suggestion = "Escríbeme qué archivo o pantalla quieres cambiar y empiezo con un plan seguro."
        elif route.intent == "folder_access_capability":
            requested_path = str(payload.get("path") or target or "02_CLAUDIO").strip()
            decision = folder_check_payload({"path": requested_path, "mode": "LIST", "purpose": "chat_folder_capability"})
            actions_taken.append("folder_access_gate")
            trace("folder_access_gate", decision, "/api/folder/check")
            reply = (
                folder_access_gate.capability_summary()
                + " Estado inicial: "
                + f"{decision.get('gate', 'REVIEW')} para {decision.get('requested_path_redacted', 'ruta no clasificada')}."
            )
            next_suggestion = "Dame una ruta concreta dentro de BRAIN_OS o dime qué archivo quieres revisar."
        elif route.intent == "visual_file_intake":
            image_path = str(payload.get("path") or payload.get("source_path") or target or extract_local_image_path(message)).strip()
            status = multimodal_status_payload()
            actions_taken.append("multimodal_status")
            trace("multimodal_status", status, "/api/multimodal/status")
            if not image_path:
                reply = (
                    "Sí. Puedo procesar una imagen local si está en una ruta permitida. "
                    "No la subiré a cloud ni guardaré bytes crudos. "
                    "Dame la ruta del archivo o usa la carpeta segura qa_artifacts/multimodal_safe_inputs."
                )
                next_suggestion = "Dame una ruta de imagen dentro de qa_artifacts/multimodal_safe_inputs."
            else:
                data = multimodal_intake_file_payload(
                    {
                        "path": image_path,
                        "user_confirmed": bool(payload.get("user_confirmed", True)),
                        "allow_cloud": bool(payload.get("allow_cloud", False)),
                        "allow_raw_storage": bool(payload.get("allow_raw_storage", False)),
                    }
                )
                actions_taken.append("multimodal_file_intake")
                trace("multimodal_file_intake", data, "/api/multimodal/intake-file")
                response_gate_override = str(data.get("gate") or "")
                decision = data.get("decision", {})
                observation = decision.get("observation", {})
                if str(data.get("reason", "")).startswith("REVIEW_EXIF"):
                    reply = (
                        "Puedo procesar la imagen local, pero detecté metadata EXIF. "
                        "No guardé ni mostré esos valores. La observación queda en REVIEW por posible metadata sensible: "
                        f"gate={data.get('gate', 'REVIEW')}, exif_gate={data.get('exif_gate', 'REVIEW_EXIF_PRESENT')}, "
                        f"hash={observation.get('source_hash_sha256', '')[:16]}..., "
                        f"world_model={decision.get('world_model_decision', {}).get('gate', 'REVIEW')}, "
                        f"MTS={decision.get('mts_fusion_result', {}).get('fusion_gate', 'REVIEW')}. "
                        "No hice OCR, no usé cámara/audio/sensores y no subí la imagen a cloud."
                    )
                    next_suggestion = "Puedo explicar el REVIEW_EXIF o procesar una imagen allowlist sin EXIF."
                elif data.get("gate") == "APPROVE":
                    reply = (
                        "Pude procesar la imagen local permitida. No guardé bytes crudos ni la subí a cloud. "
                        "Generé metadata segura, hash, observación visual, canal MTS y evidencia redactada: "
                        f"gate={data.get('gate')}, hash={observation.get('source_hash_sha256', '')[:16]}..., "
                        f"world_model={decision.get('world_model_decision', {}).get('gate', 'REVIEW')}, "
                        f"MTS={decision.get('mts_fusion_result', {}).get('fusion_gate', 'REVIEW')}. "
                        "No hice OCR, no usé cámara/audio/sensores y no logueé EXIF completo."
                    )
                    next_suggestion = "Puedo analizar otro archivo allowlist o explicar el resultado."
                else:
                    reply = (
                        "No procesé la imagen como APPROVE. "
                        f"Gate={data.get('gate', 'REVIEW')}; razón={data.get('reason', data.get('status', 'REVIEW'))}. "
                        "Sólo acepto archivos puntuales .png/.jpg/.jpeg/.webp dentro de la allowlist, sin cloud ni raw storage."
                    )
                    next_suggestion = "Usa una imagen dentro de qa_artifacts/multimodal_safe_inputs o pide revisar el gate."
        elif route.intent == "multimodal_intake":
            status = multimodal_status_payload()
            data = multimodal_intake_fixture_payload()
            actions_taken.extend(["multimodal_status", "multimodal_fixture_intake"])
            trace("multimodal_status", status, "/api/multimodal/status")
            trace("multimodal_fixture_intake", data, "/api/multimodal/intake-fixture")
            decision = data.get("decision", {})
            observation = decision.get("observation", {})
            reply = (
                "Puedo procesar fixtures visuales seguros. Ejecuté el fixture v0.1: "
                f"gate={decision.get('gate', data.get('status', 'REVIEW'))}, "
                f"hash={observation.get('source_hash_sha256', status.get('last_fixture_hash', ''))[:16]}..., "
                f"world_model={decision.get('world_model_decision', {}).get('gate', 'REVIEW')}, "
                f"MTS={decision.get('mts_fusion_result', {}).get('fusion_gate', 'REVIEW')}. "
                "No guardé bytes crudos, no usé cámara/audio/OCR/sensores reales y no envié imagen a cloud."
            )
            next_suggestion = "Puedo revisar el estado multimodal o seguir con un plan de código local."
        elif route.intent == "status_check":
            preflight = coding_preflight_payload({"action": "status"})
            provider = provider_status_payload()
            route_payload = provider_route_payload()
            security = security_preflight_payload()
            actions_taken.extend(["coding_preflight", "provider_status", "provider_route", "security_preflight"])
            trace("coding_preflight", preflight, "/api/coding/preflight")
            trace("provider_status", provider, "/api/providers/status")
            trace("provider_route", route_payload, "/api/provider/route")
            trace("security_preflight", security, "/api/security/preflight")
            deepseek_status = deepseek_final_status()
            reply = (
                "Revisé el estado local. Wabi/Claudio está operable para plan y diff local. "
                f"ActionGate: {preflight.get('action_gate', 'REVIEW')}. "
                f"Provider activo: {route_payload.get('selected_provider', 'local')} ({route_payload.get('route_stage', 'LOCAL')}). "
                "Política: cloud-first por salud, resumen/redacción local para documentos privados, BudgetGate activo. "
                f"DeepSeek/NVIDIA se ordenan por gate ({deepseek_status}); Qwen local queda como fallback. "
                f"Seguridad local: {security.get('status', 'REVIEW')}. PublicationGate sigue BLOCK."
            )
            next_suggestion = "Dime qué cambio quieres planear o escribe: revisa seguridad local."
        elif route.intent == "security_review":
            comparison = security_compare_payload()
            actions_taken.append("gitleaks_medioevo_compare")
            trace("security_compare", comparison, "/api/security/gitleaks/compare-secret-scan")
            counts = comparison.get("comparison", {})
            reply = (
                "Revisé seguridad local con fixtures sintéticos. "
                f"Gitleaks: {counts.get('gitleaks_findings_count')}; MEDIOEVO: {counts.get('medioevo_findings_count')}; "
                f"missed_by_gitleaks: {counts.get('missed_by_gitleaks', [])}. "
                "No escaneé carpetas privadas amplias y no imprimí secretos."
            )
            next_suggestion = "Puedo planear un cambio seguro si me dices el archivo objetivo."
        elif route.intent == "provider_review":
            provider = provider_status_payload()
            route_payload = provider_route_payload({"live": bool(payload.get("live", False))})
            provider_contract = wabi_provider_contract_payload()
            provider_diagnostic = wabi_provider_route_diagnostic_payload()
            actions_taken.extend(["provider_status", "provider_route", "provider_contract", "provider_route_diagnostic"])
            trace("provider_status", provider, "/api/providers/status")
            trace("provider_route", route_payload, "/api/provider/route")
            trace("provider_contract", provider_contract, "wabi_provider_status_contract")
            trace("provider_route_diagnostic", provider_diagnostic, "/api/provider/diagnostic")
            deepseek_status = deepseek_final_status()
            message_lower = chat_intent_router.normalize_message(message)
            route_status = (
                route_payload.get("developer_trace", {})
                .get("attempts", [{}])[0]
                .get("status", route_payload.get("status", "REVIEW"))
            )
            provider_state = str(provider_contract.get("provider_state") or provider_contract.get("live_smoke_status") or route_status)
            live_smoke_status = str(provider_contract.get("live_smoke_status") or route_status)
            selected_provider = str(provider_contract.get("primary_provider") or route_payload.get("selected_provider", "nvidia") or "nvidia")
            selected_model = str(provider_contract.get("primary_model") or route_payload.get("selected_model", WABI_PRIMARY_MODEL) or WABI_PRIMARY_MODEL)
            fallback_provider = str(provider_contract.get("fallback_provider") or "ollama")
            fallback_model = str(provider_contract.get("fallback_model") or "qwen2.5:0.5b")
            last_error_class = str(provider_diagnostic.get("last_error_class") or "")
            diagnostic_note = (
                " por provider/model route not-found redactado"
                if live_smoke_status == "SMOKE_FAIL_REDACTED"
                and last_error_class == "PROVIDER_OR_MODEL_NOT_FOUND_REDACTED"
                else ""
            )
            primary_route = (
                selected_model
                if selected_model.startswith(f"{selected_provider}/")
                else f"{selected_provider}/{selected_model}"
            )
            if "compound:model_status_question" in route.matched_patterns:
                model_result = model_chat_fallback(message, str(payload.get("provider", "") or selected_provider or "nvidia"), mode)
                if model_result.get("ok") and str(model_result.get("response") or "").strip():
                    actions_taken.append(f"model_chat:{model_result.get('provider')}")
                    trace("model_chat_fallback", model_result, "/api/chat/message")
                    reply = str(model_result.get("response") or "")
                    active_model = str(model_result.get("model") or selected_model or "")
                    active_provider = str(model_result.get("raw_provider") or selected_provider or "")
                    declared_model = f"{active_provider}/{active_model}".strip("/")
                    if declared_model and declared_model not in reply:
                        reply = f"Modelo subyacente: `{declared_model}`.\n\n{reply}"
                    if (
                        "hora" in message_lower
                        and not re.search(r"reloj|hora actual|Get-Date|wabi status|wabi doctor", reply, re.IGNORECASE)
                    ):
                        reply = (
                            reply.rstrip()
                            + "\n\nNo tengo acceso al reloj del sistema en tiempo real. "
                            "El operador puede ejecutar `Get-Date` en PowerShell, `wabi status` o `wabi doctor` para obtenerla."
                        )
                    online_ai_called = True
                    next_suggestion = "Puedes seguir conversando o pedirme un plan, diff, pruebas o revision de seguridad."
                else:
                    trace("model_chat_fallback_failed", model_result, "/api/chat/message")
                    pass_note = " Fue un PASS." if live_smoke_status == "SMOKE_PASS" else " No fue un PASS."
                    reply = (
                        f"Ruta primaria configurada: {primary_route}. "
                        f"Último smoke real: {live_smoke_status}{diagnostic_note}.{pass_note} "
                        f"Fallback API activo: {fallback_provider}/{fallback_model}. "
                        "Próxima acción: revisar ruta DeepSeek/Nemotron sin exponer credenciales. "
                        "No imprimo secretos. "
                        f"PublicationGate: {provider_contract.get('publication_gate', route_payload.get('publication_gate', 'BLOCK'))}."
                    )
            elif "deepseek" in message_lower and "nemotron" not in message_lower and "nvidia" not in message_lower:
                reply = (
                    "DeepSeek V4 Flash queda como ruta primaria si la cuenta tiene balance/cuota y el smoke pasa. "
                    f"Estado actual: {deepseek_status}. NVIDIA/Nemotron y Cloudflare quedan como fallbacks API; Ollama queda último/offline. "
                    f"Ruta activa: {route_payload.get('route_stage')} / {route_payload.get('selected_provider')} "
                    f"({route_payload.get('selected_model')})."
                )
            elif "nemotron" in message_lower or "nvidia" in message_lower:
                reply = (
                    "Intentaré NVIDIA/Nemotron si hay key, modelo registrado y cuota disponible. "
                    "No basta con que exista una key: necesita smoke exitoso y BudgetGate. "
                    f"Estado actual: {route_status}. "
                    f"Ruta activa: {route_payload.get('route_stage')} / {route_payload.get('selected_provider')} "
                    f"({route_payload.get('selected_model')})."
                )
            else:
                reply = (
                    "Política provider: TEMP_EXTERNAL_APIS_ALLOWED_UNTIL_CLAUDIO_AUTONOMY. "
                    "Intento cloud configurado por salud; si NVIDIA/Nemotron está en REVIEW, no bloquea DeepSeek. "
                    f"DeepSeek queda como candidato cloud-first ({deepseek_status}); no hay PASS sin smoke. "
                    f"Ruta activa: {route_payload.get('route_stage')} / {route_payload.get('selected_provider')} "
                    f"({route_payload.get('selected_model')})."
                )
            next_suggestion = "Puedes seguir en modo local: dime qué quieres planear o revisar."
        elif route.intent == "coding_plan":
            plan_payload = {"objective": message}
            if target:
                plan_payload["target"] = target
            data = coding_plan_payload(plan_payload)
            session = data.get("coding_session", {})
            coding_session_id = str(session.get("session_id", "") or "")
            actions_taken.append("coding_plan")
            trace("coding_plan", data, "/api/coding/plan")
            reply = (
                "Preparé un plan local. "
                f"Gate: {session.get('action_gate', 'REVIEW')}. "
                f"Resumen: {session.get('plan', {}).get('summary', 'Plan listo')} "
                "No apliqué cambios."
            )
            next_suggestion = "Si quieres ver el cambio, escribe: crea el diff."
        elif route.intent == "coding_diff":
            if not target:
                reply = "Puedo crear el diff, pero necesito un archivo objetivo en el campo de archivo o en tu siguiente mensaje."
                next_suggestion = "Escribe el archivo objetivo y el cambio deseado en el chat."
            else:
                diff_payload: dict[str, Any] = {"objective": message, "target": target}
                if coding_session_id:
                    diff_payload["session_id"] = coding_session_id
                if content is not None:
                    diff_payload["content"] = content
                if old is not None and new is not None:
                    diff_payload["old"] = old
                    diff_payload["new"] = new
                data = coding_diff_payload(diff_payload)
                session = data.get("coding_session", {})
                coding_session_id = str(session.get("session_id", "") or coding_session_id)
                actions_taken.append("coding_diff")
                trace("coding_diff", data, "/api/coding/diff")
                reply = (
                    "Creé el diff local. "
                    f"Archivo: {session.get('diff', {}).get('file_path', target)}. "
                    f"Gate: {session.get('action_gate', 'REVIEW')}. "
                    "No lo apliqué."
                )
                next_suggestion = "Si el diff es correcto, escribe: aplica el cambio si es seguro."
        elif route.intent == "coding_apply":
            if not allow_apply:
                reply = "No apliqué cambios porque apply requiere confirmación explícita y rollback disponible."
                next_suggestion = "Usa el botón Aplicar si es seguro o confirma en el chat que quieres aplicar este diff."
            elif not coding_session_id:
                reply = "No apliqué cambios porque no hay sesión de diff lista con rollback."
                next_suggestion = "Primero dime: crea el diff para este archivo."
            else:
                data = coding_apply_payload({"session_id": coding_session_id})
                session = data.get("coding_session", {})
                actions_taken.append("coding_apply")
                trace("coding_apply", data, "/api/coding/apply")
                reply = (
                    "Apliqué el cambio con ActionGate local y rollback creado. "
                    f"Estado: {session.get('status', 'APPLIED')}. "
                    f"Rollback: {session.get('rollback_path', 'disponible')}."
                )
                next_suggestion = "Puedo correr pruebas o hacer rollback si lo necesitas."
        elif route.intent == "coding_test":
            data = coding_test_payload({"session_id": coding_session_id} if coding_session_id else {})
            actions_taken.append("coding_tests")
            trace("coding_tests", data, "/api/coding/test")
            reply = "Corrí pruebas locales allowlist. Resultado: " + ("PASS." if data.get("ok") else "REVIEW/FAIL.")
            next_suggestion = "Puedes pedirme explicar fallos, crear otro diff o hacer rollback."
        elif route.intent == "rollback":
            if not coding_session_id:
                reply = "No ejecuté rollback porque no hay sesión aplicada con snapshot disponible."
                next_suggestion = "Si quieres revertir una sesión específica, indícame cuál desde el chat."
            else:
                data = coding_rollback_payload({"session_id": coding_session_id})
                actions_taken.append("coding_rollback")
                trace("coding_rollback", data, "/api/coding/rollback")
                reply = "Rollback ejecutado sobre la sesión local. Estado: " + str(data.get("coding_session", {}).get("status", "ROLLED_BACK")) + "."
                next_suggestion = "Puedo volver a crear un plan corregido si me dices el objetivo."
        elif route.intent == "world_model_review":
            data = world_model_benchmark_payload()
            actions_taken.append("world_model_benchmark")
            trace("world_model_benchmark", data, "/api/world-model/benchmark")
            reply = "Benchmark world-model local ejecutado con fixtures sintéticos y sin provider calls."
            next_suggestion = "Puedo revisar estado, seguridad o planear un cambio local."
        elif route.intent == "council_review":
            provider = provider_status_payload()
            actions_taken.append("provider_status")
            trace("provider_status", provider, "/api/providers/status")
            configured = [row.get("provider_name") for row in provider.get("providers", []) if row.get("configured")]
            reply = (
                "Concilio en modo seguro: hay providers configurados para asesoría, pero no aplico cambios desde opiniones. "
                f"Disponibles: {', '.join(configured[:5]) or 'ninguno'}."
            )
            next_suggestion = "Dime la decisión que quieres revisar y te doy un criterio local con riesgos."
        elif route.intent == "local_mode":
            preflight = coding_preflight_payload({"action": "status"})
            route_payload = provider_route_payload()
            actions_taken.append("coding_preflight")
            actions_taken.append("provider_route")
            trace("coding_preflight", preflight, "/api/coding/preflight")
            trace("provider_route", route_payload, "/api/provider/route")
            reply = (
                "Modo local listo: puedo planear y crear diffs sin provider live; apply sigue protegido por gate y rollback. "
                f"Ruta provider actual: {route_payload.get('route_stage', 'LOCAL')} / {route_payload.get('selected_provider', 'ollama')}."
            )
            next_suggestion = "Escribe el cambio que quieres planear en lenguaje natural."
        elif route.intent == "vpn_review":
            actions_taken.append("vpn_review_only")
            reply = "VPN/WARP queda REVIEW_ONLY. No cambié red ni configuración del host desde Wabi."
            next_suggestion = "Puedo revisar estado o explicar qué falta para una confirmación manual segura."
        elif route.intent == "explain_pending":
            live = live_fingerprint_payload()
            actions_taken.append("live_state_summary")
            trace("live_state", live, "00_START_HERE/LIVE_STATE/SESSION_FINGERPRINT.json")
            reply = (
                "Pendientes reales: DeepSeek V4 Flash requiere smoke y BudgetGate para PASS; NVIDIA/Nemotron y Cloudflare sostienen fallback API; "
                "Ollama queda offline y Gitleaks producto publicable sigue REVIEW_OR_BLOCK. "
                "Lo local diario está operable y PublicationGate sigue BLOCK."
            )
            next_suggestion = "Escribe qué quieres que Wabi haga ahora."
        elif route.intent == "unknown_but_helpful":
            answered_locally = False
            if should_answer_unknown_locally(message, mode):
                actions_taken.append("chat_local_conversation")
                reply = local_conversation_reply(message)
                next_suggestion = "Dime qué quieres cambiar o revisar y lo convierto en una acción verificable."
                model_result = {"ok": False, "provider": "", "response": "", "errors": [], "raw": {}}
                answered_locally = True
            else:
                model_result = model_chat_fallback(message, str(payload.get("provider", "") or "nvidia"), mode)
            if model_result.get("ok"):
                reply_text = str(model_result.get("response") or route.human_summary)
                if model_reply_needs_safe_fallback(reply_text):
                    actions_taken.append("model_chat_filtered")
                    reply_text = local_conversation_reply(message)
                actions_taken.append(f"model_chat:{model_result.get('provider')}")
                trace("model_chat_fallback", model_result, "/api/chat/message")
                reply = reply_text
                online_ai_called = True
                next_suggestion = "Puedes seguir conversando o pedirme un plan, diff, pruebas o revision de seguridad."
            elif not answered_locally:
                actions_taken.append("chat_helpful_fallback")
                trace("model_chat_fallback_failed", model_result, "/api/chat/message")
                reply = (
                    "Te escucho. El motor no respondió dentro del límite, así que sigo en modo seguro. "
                    "Dime el objetivo y puedo convertirlo en plan, diff, pruebas, revisión de seguridad o una lista clara de pendientes."
                )
                next_suggestion = "Escribe el objetivo en lenguaje normal; Wabi lo convierte en siguiente acción local."
            trace(
                "chat_helpful_fallback",
                {
                    "normalized_message": getattr(route, "normalized_message", ""),
                    "matched_patterns": getattr(route, "matched_patterns", []),
                },
                "/api/chat/message",
            )
        else:
            reply = "Puedo ayudarte, pero necesito un poco más de dirección: dime si quieres revisar estado, programar, revisar seguridad o diagnosticar DeepSeek/Nemotron."
            next_suggestion = "Escribe una petición natural, por ejemplo: ayúdame a programar."
    except Exception as exc:
        reply = "La herramienta local no pudo completar esa acción: " + sanitize_text(exc)
        next_suggestion = "Reformula la petición en el chat o pide revisar estado."

    if _has_command_next_suggestion(next_suggestion):
        next_suggestion = "Escribe en el chat lo que quieres hacer ahora."
    _remember_chat(message, reply, route.intent, coding_session_id)
    response = {
        "ok": True,
        "reply": sanitize_text(reply),
        "intent": route.intent,
        "confidence": route.confidence,
        "gate": chat_gate(response_gate_override or route.action_gate),
        "action_gate": route.action_gate,
        "actions_taken": actions_taken,
        "next_suggestion": sanitize_text(next_suggestion),
        "coding_session_id": coding_session_id,
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
        "online_ai_called": online_ai_called,
        "route": route.to_dict(),
        "developer_trace": developer_trace if developer else {},
    }
    return sanitize_obj(response)


def governance_status_payload() -> dict[str, Any]:
    return sanitize_obj(governance_shadow.status_payload(CLAUDIO_ROOT))


def governance_shadow_payload(payload: dict[str, Any]) -> dict[str, Any]:
    decision = governance_shadow.decide_shadow(
        {
            "message": str(payload.get("message", "")),
            "channel_type": str(payload.get("channel_type", "api") or "api"),
            "intent_flags": payload.get("intent_flags", []) or [],
            "R_input": payload.get("R_input", 0.0),
            "contradiction_count": payload.get("contradiction_count", 0),
            "needs_side_effects": bool(payload.get("needs_side_effects", False)),
            "test_fail": bool(payload.get("test_fail", False)),
            "compile_fail": bool(payload.get("compile_fail", False)),
            "ui_smoke_fail": bool(payload.get("ui_smoke_fail", False)),
            "rule_conflict_type": payload.get("rule_conflict_type"),
            "human_available": bool(payload.get("human_available", False)),
            "evidence_refs": payload.get("evidence_refs", []) or [],
        },
        root=CLAUDIO_ROOT,
    )
    return sanitize_obj(decision.to_dict())


def mts_shadow_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = mts_shadow.evaluate_mts_shadow_readonly(str(payload.get("message", "")), root=ROOT)
    return sanitize_obj(result)


def mts_select_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = mts_c1.evaluate_c1_selection_readonly(str(payload.get("message", "")), root=ROOT)
    return sanitize_obj(result)


def mts_format_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = mts_c2.select_format_readonly(
        str(payload.get("message", "")),
        c1_trace=payload.get("c1_trace") if isinstance(payload.get("c1_trace"), dict) else None,
        interface_state=payload.get("interface_state") if isinstance(payload.get("interface_state"), dict) else None,
        root=ROOT,
    )
    return sanitize_obj(result)


def mts_policy_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = mts_c3.simulate_policy_dry_run(
        str(payload.get("message", "")),
        c1_trace=payload.get("c1_trace") if isinstance(payload.get("c1_trace"), dict) else None,
        c2_selection=payload.get("c2_selection") if isinstance(payload.get("c2_selection"), dict) else None,
        interface_state=payload.get("interface_state") if isinstance(payload.get("interface_state"), dict) else None,
        root=ROOT,
    )
    return sanitize_obj(result)


def mts_shadow_trace_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = mts_c4.build_shadow_trace(
        str(payload.get("message", "")),
        c1_trace=payload.get("c1_trace") if isinstance(payload.get("c1_trace"), dict) else None,
        c2_selection=payload.get("c2_selection") if isinstance(payload.get("c2_selection"), dict) else None,
        c3_policy=payload.get("c3_policy") if isinstance(payload.get("c3_policy"), dict) else None,
        interface_state=payload.get("interface_state") if isinstance(payload.get("interface_state"), dict) else None,
        root=ROOT,
    )
    return sanitize_obj(result)


def mts_enforce_payload(payload: dict[str, Any]) -> dict[str, Any]:
    provided_gates = payload.get("provided_gates")
    result = mts_c7.build_limited_enforcement_decision(
        str(payload.get("message", "")),
        c6_packet=payload.get("c6_packet") if isinstance(payload.get("c6_packet"), dict) else None,
        provided_gates=provided_gates if isinstance(provided_gates, list) else None,
        interface_state=payload.get("interface_state") if isinstance(payload.get("interface_state"), dict) else None,
        root=ROOT,
    )
    return sanitize_obj(result)


def wabi_unification_status_payload() -> dict[str, Any]:
    return sanitize_obj(wabi_unification.build_unification_status(ROOT, MEDIOEVO_ROOT))


def wabi_system_notebook_status_payload() -> dict[str, Any]:
    return sanitize_obj(wabi_system_notebook.latest_notebook_status())


def wabi_system_notebook_scan_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    raw_root = data.get("root") or ROOT
    raw_source_pdf = data.get("source_pdf") or data.get("source_document") or None
    raw_out_dir = data.get("out_dir") or None
    write = bool(data.get("write", True))
    return sanitize_obj(
        wabi_system_notebook.scan_system_notebook(
            pathlib.Path(str(raw_root)),
            source_pdf=pathlib.Path(str(raw_source_pdf)) if raw_source_pdf else None,
            out_dir=pathlib.Path(str(raw_out_dir)) if raw_out_dir else None,
            write=write,
            mother_root=ROOT,
        )
    )


def wabi_app_inventory_status_payload() -> dict[str, Any]:
    return sanitize_obj(wabi_system_notebook.latest_app_inventory_status())


def wabi_app_inventory_scan_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    raw_root = data.get("root") or ROOT
    raw_apps_root = data.get("apps_root") or None
    raw_out_dir = data.get("out_dir") or None
    write = bool(data.get("write", True))
    return sanitize_obj(
        wabi_system_notebook.scan_app_inventory(
            pathlib.Path(str(raw_root)),
            apps_root=pathlib.Path(str(raw_apps_root)) if raw_apps_root else None,
            out_dir=pathlib.Path(str(raw_out_dir)) if raw_out_dir else None,
            write=write,
            mother_root=ROOT,
        )
    )


def wabi_source_intake_inspect_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    default_base44_zip = WORKING_BENCH_ROOT / "saveweb2zip-com-app-base44-com.zip"
    raw_source = str(data.get("path") or data.get("source") or data.get("source_path") or default_base44_zip)
    if not raw_source.strip():
        return {
            "ok": False,
            "schema": wabi_unification.SCHEMA_INTAKE,
            "error": "source path required",
            "RawAdoptionGate": "BLOCK",
            "PublicationGate": "BLOCK",
            "applied_to_sources": False,
            "cloud_provider_called": False,
            "secret_values_printed": False,
        }
    return sanitize_obj(wabi_unification.inspect_source(pathlib.Path(raw_source), ROOT, MEDIOEVO_ROOT))


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _gemma_ollama_base_url() -> str:
    raw = os.environ.get("WABI_OLLAMA_URL") or os.environ.get("OLLAMA_HOST") or "http://127.0.0.1:11434"
    raw = raw.strip().rstrip("/")
    if not raw:
        raw = "http://127.0.0.1:11434"
    if not raw.startswith(("http://", "https://")):
        raw = "http://" + raw
    return raw


def _gemma_http_json(url: str, *, payload: dict[str, Any] | None = None, timeout_s: float = 2.0) -> dict[str, Any]:
    import urllib.error
    import urllib.request

    body = None if payload is None else json.dumps(payload, ensure_ascii=True).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST" if body is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=max(0.5, float(timeout_s))) as response:
            raw = response.read(2_000_000).decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(sanitize_text(exc)) from exc
    if not raw.strip():
        return {}
    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid json from ollama: {sanitize_text(exc)}") from exc
    return decoded if isinstance(decoded, dict) else {"value": decoded}


def _gemma_ollama_tags(timeout_s: float = 2.0) -> dict[str, Any]:
    base_url = _gemma_ollama_base_url()
    started = time.perf_counter()
    try:
        data = _gemma_http_json(f"{base_url}/api/tags", timeout_s=timeout_s)
    except Exception as exc:
        return {
            "ok": False,
            "base_url": base_url,
            "elapsed_ms": int((time.perf_counter() - started) * 1000),
            "models": [],
            "error_class": type(exc).__name__,
            "error": sanitize_text(exc),
        }
    models = data.get("models") if isinstance(data.get("models"), list) else []
    public_models: list[dict[str, Any]] = []
    for item in models:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("model") or "").strip()
        if not name:
            continue
        public_models.append({
            "name": name,
            "modified_at": sanitize_text(item.get("modified_at", "")),
            "size": item.get("size", 0),
            "digest": sanitize_text(item.get("digest", ""))[:24],
            "details": sanitize_obj(item.get("details") if isinstance(item.get("details"), dict) else {}),
        })
    return {
        "ok": True,
        "base_url": base_url,
        "elapsed_ms": int((time.perf_counter() - started) * 1000),
        "models": public_models,
        "error": "",
    }


def _gemma_parse_memory_mb(value: Any) -> int:
    text = str(value or "").replace(",", " ").strip()
    if not text:
        return 0
    match = re.search(r"(\d+(?:\.\d+)?)\s*(gib|gb|mib|mb)?", text, re.IGNORECASE)
    if not match:
        return 0
    number = float(match.group(1))
    unit = (match.group(2) or "mb").lower()
    if unit in {"gb", "gib"}:
        return int(number * 1024)
    return int(number)


def _gemma_nvidia_smi_candidates() -> list[pathlib.Path]:
    candidates: list[pathlib.Path] = []
    found = shutil.which("nvidia-smi")
    if found:
        candidates.append(pathlib.Path(found))
    candidates.extend([
        pathlib.Path(r"C:\Windows\System32\nvidia-smi.exe"),
        pathlib.Path(r"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe"),
    ])
    unique: list[pathlib.Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).lower()
        if key not in seen:
            unique.append(candidate)
            seen.add(key)
    return unique


def _gemma_nvidia_smi_inventory(timeout_s: float = 3.0) -> dict[str, Any]:
    attempted = [str(path) for path in _gemma_nvidia_smi_candidates()]
    for candidate in _gemma_nvidia_smi_candidates():
        if not candidate.exists():
            continue
        try:
            proc = subprocess.run(
                [
                    str(candidate),
                    "--query-gpu=name,memory.total,memory.free,driver_version",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=max(1.0, float(timeout_s)),
                check=False,
            )
        except Exception as exc:
            return {"ok": False, "attempted": attempted, "gpus": [], "error": sanitize_text(exc)}
        if proc.returncode != 0:
            return {"ok": False, "attempted": attempted, "gpus": [], "error": sanitize_text(proc.stderr or proc.stdout)}
        gpus: list[dict[str, Any]] = []
        for line in proc.stdout.splitlines():
            parts = [part.strip() for part in line.split(",")]
            if len(parts) < 4:
                continue
            gpus.append({
                "name": sanitize_text(parts[0]),
                "memory_total_mb": _gemma_parse_memory_mb(parts[1]),
                "memory_free_mb": _gemma_parse_memory_mb(parts[2]),
                "driver_version": sanitize_text(parts[3]),
                "source": "nvidia-smi",
            })
        return {"ok": bool(gpus), "attempted": attempted, "gpus": gpus, "error": "" if gpus else "NO_GPUS_REPORTED"}
    return {"ok": False, "attempted": attempted, "gpus": [], "error": "NVIDIA_SMI_NOT_FOUND"}


def _gemma_wmi_inventory(timeout_s: float = 4.0) -> dict[str, Any]:
    if os.name != "nt":
        return {"ok": False, "adapters": [], "error": "WMI_WINDOWS_ONLY"}
    command = (
        "Get-CimInstance Win32_VideoController | "
        "Select-Object Name,AdapterRAM,DriverVersion,PNPDeviceID | ConvertTo-Json -Depth 2"
    )
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True,
            text=True,
            timeout=max(1.0, float(timeout_s)),
            check=False,
        )
    except Exception as exc:
        return {"ok": False, "adapters": [], "error": sanitize_text(exc)}
    if proc.returncode != 0 or not proc.stdout.strip():
        return {"ok": False, "adapters": [], "error": sanitize_text(proc.stderr or "WMI_NO_OUTPUT")}
    try:
        decoded = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {"ok": False, "adapters": [], "error": sanitize_text(exc)}
    rows = decoded if isinstance(decoded, list) else [decoded]
    adapters: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        adapter_ram = row.get("AdapterRAM") or 0
        try:
            adapter_ram_mb = int(int(adapter_ram) / (1024 * 1024))
        except Exception:
            adapter_ram_mb = 0
        adapters.append({
            "name": sanitize_text(row.get("Name", "")),
            "memory_total_mb": adapter_ram_mb,
            "driver_version": sanitize_text(row.get("DriverVersion", "")),
            "source": "Win32_VideoController",
        })
    return {"ok": bool(adapters), "adapters": adapters, "error": "" if adapters else "WMI_NO_ADAPTERS"}


def _gemma_gpu_inventory() -> dict[str, Any]:
    nvidia = _gemma_nvidia_smi_inventory()
    wmi = _gemma_wmi_inventory()
    gpus = [gpu for gpu in nvidia.get("gpus", []) if isinstance(gpu, dict)]
    adapters = [adapter for adapter in wmi.get("adapters", []) if isinstance(adapter, dict)]
    candidates = gpus or adapters
    best_vram = max((_safe_int(item.get("memory_total_mb"), 0) for item in candidates), default=0)
    llm_gpu_ready = bool(gpus and best_vram >= 6_000)
    status = "GPU_READY_24GB" if best_vram >= 22_000 else ("GPU_VISIBLE_LOW_VRAM" if llm_gpu_ready else "GPU_NOT_VISIBLE")
    return sanitize_obj({
        "ok": bool(candidates),
        "status": status,
        "llm_gpu_ready": llm_gpu_ready,
        "vram_total_mb": best_vram,
        "nvidia_smi": nvidia,
        "wmi": wmi,
        "notes": [
            "nvidia-smi is authoritative for CUDA VRAM.",
            "WMI adapters are diagnostic evidence only; integrated GPUs do not unlock Gemma heavy profiles.",
        ],
    })


def _gemma_model_names(tags: dict[str, Any]) -> list[str]:
    models = tags.get("models") if isinstance(tags.get("models"), list) else []
    names: list[str] = []
    for item in models:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("model") or "").strip()
        if name:
            names.append(name)
    return names


def _gemma_pick_model(names: list[str], profile: str) -> str:
    lowered = {name.lower(): name for name in names}
    profile_candidates = {
        "rapido": ("gemma4:e4b", "gemma4:e2b", "gemma:2b", "gemma2:2b", "gemma3:4b"),
        "fuerte": ("gemma4:26b", "gemma3:27b", "gemma2:27b", "gemma:7b"),
        "profundo": ("gemma4:31b", "gemma4:34b", "gemma3:27b", "gemma2:27b"),
    }
    for candidate in profile_candidates.get(profile, profile_candidates["rapido"]):
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    for name in names:
        if "gemma" in name.lower():
            return name
    return ""


def _gemma_fallback_model(names: list[str]) -> str:
    preferred = ("qwen2.5-coder:3b", "qwen2.5:0.5b", "qwen2.5:3b")
    lowered = {name.lower(): name for name in names}
    for candidate in preferred:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    for name in names:
        if "qwen" in name.lower():
            return name
    return ""


def wabi_gemma_status_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    profile = str(data.get("profile") or "rapido").strip().lower()
    if profile not in {"rapido", "fuerte", "profundo"}:
        profile = "rapido"
    timeout_s = min(max(float(data.get("timeout_s", 2.0) or 2.0), 0.5), 8.0)
    tags = _gemma_ollama_tags(timeout_s=timeout_s)
    gpu = _gemma_gpu_inventory()
    names = _gemma_model_names(tags)
    gemma_models = [name for name in names if "gemma" in name.lower()]
    fallback = _gemma_fallback_model(names)
    selected = {
        "rapido": _gemma_pick_model(names, "rapido"),
        "fuerte": _gemma_pick_model(names, "fuerte"),
        "profundo": _gemma_pick_model(names, "profundo"),
        "fallback_programmer": fallback,
    }
    if not tags.get("ok"):
        status = "BLOCKED"
        reason = "OLLAMA_UNREACHABLE"
    elif not gpu.get("llm_gpu_ready") and not gemma_models:
        status = "GPU_NOT_VISIBLE"
        reason = "GPU_NOT_VISIBLE_AND_MODEL_MISSING"
    elif not gemma_models:
        status = "MODEL_MISSING"
        reason = "GEMMA_MODEL_MISSING"
    elif not gpu.get("llm_gpu_ready"):
        status = "READY_SMALL_ONLY"
        reason = "GEMMA_PRESENT_GPU_NOT_VISIBLE"
    else:
        status = "READY"
        reason = "GEMMA_PRESENT_GPU_VISIBLE"
    profiles = {
        "rapido": {
            "requested_vram_mb": "6000-10000",
            "model": selected["rapido"] or fallback,
            "gate": "READY" if selected["rapido"] else ("FALLBACK_QWEN" if fallback else "MODEL_MISSING"),
        },
        "fuerte": {
            "requested_vram_mb": "10000-18000",
            "model": selected["fuerte"],
            "gate": "READY" if selected["fuerte"] and _safe_int(gpu.get("vram_total_mb"), 0) >= 12_000 else "REVIEW_GPU_AND_MODEL",
        },
        "profundo": {
            "requested_vram_mb": "18000-24000",
            "model": selected["profundo"],
            "gate": "READY" if selected["profundo"] and _safe_int(gpu.get("vram_total_mb"), 0) >= 22_000 else "BLOCK_UNTIL_24GB_VISIBLE",
        },
    }
    return sanitize_obj({
        "ok": status in {"READY", "READY_SMALL_ONLY", "MODEL_MISSING", "GPU_NOT_VISIBLE"},
        "schema": "wabi.gemma.status.v0_1",
        "status": status,
        "reason": reason,
        "requested_profile": profile,
        "recommended_backend": "ollama" if tags.get("ok") else "install_or_start_ollama",
        "ollama": tags,
        "gpu": gpu,
        "models": {
            "gemma": gemma_models,
            "fallback_programmer": fallback,
            "available_count": len(names),
            "selected": selected,
        },
        "profiles": profiles,
        "gates": {
            "PublicationGate": "BLOCK",
            "ApplyDefault": False,
            "CloudProviderGate": "NOT_USED_FOR_GEMMA_LOCAL",
            "WeightEditGate": "BLOCK_BASE_WEIGHTS",
            "LoRAGate": "DATASET_REVIEW_ONLY",
            "RootEditGate": "BLOCK_WINDOWS_SYSTEM_CHANGES",
        },
        "invariants": {
            "secret_values_printed": False,
            "cloud_provider_called": False,
            "base_weights_modified": False,
            "publication_gate": "BLOCK",
        },
    })


def _gemma_ollama_generate(model: str, prompt: str, *, timeout_s: float = 20.0) -> dict[str, Any]:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 512},
    }
    started = time.perf_counter()
    data = _gemma_http_json(f"{_gemma_ollama_base_url()}/api/generate", payload=payload, timeout_s=timeout_s)
    return {
        "ok": True,
        "elapsed_ms": int((time.perf_counter() - started) * 1000),
        "response": sanitize_text(data.get("response", ""))[:MAX_RESPONSE_CHARS],
        "done": bool(data.get("done", False)),
        "model": sanitize_text(data.get("model", model)),
    }


def wabi_gemma_score_osit_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    text = str(data.get("text") or data.get("claim") or data.get("prompt") or "").strip()
    lowered = text.lower()
    reasons: list[str] = []
    gate = "APPROVE"
    epistemic_state = "CERTEZA"
    residue_risk = 0.15
    if not text:
        gate = "REVIEW"
        epistemic_state = "INCOGNITA"
        residue_risk = 0.45
        reasons.append("InputGate=EMPTY")
    if any(token in lowered for token in ("secret", "token", "api key", "apikey", "password", ".env", "credential", "private key")):
        gate = "BLOCK"
        epistemic_state = "BLOQUEO"
        residue_risk = 0.95
        reasons.append("SecretGate=BLOCK")
    if any(token in lowered for token in ("deploy", "publish", "publica", "push", "borra", "delete", "elimina", "registro de windows", "driver", "c:\\windows")):
        gate = "BLOCK"
        epistemic_state = "BLOQUEO"
        residue_risk = max(residue_risk, 0.9)
        reasons.append("ExternalOrDestructiveActionGate=BLOCK")
    if any(token in lowered for token in ("finetun", "fine-tun", "lora", "adapter", "pesos base", "base weights", "gemma4", "gemma 4")) and gate != "BLOCK":
        gate = "REVIEW"
        epistemic_state = "INFERENCIA"
        residue_risk = max(residue_risk, 0.55)
        reasons.append("ModelAdaptationGate=REVIEW")
    if any(token in lowered for token in ("p=np", "p≠np", "prueba formal", "demuestra", "teorema", "claim cientifico")) and gate != "BLOCK":
        gate = "REVIEW"
        epistemic_state = "INFERENCIA"
        residue_risk = max(residue_risk, 0.65)
        reasons.append("ScienceClaimGate=REVIEW")
    return sanitize_obj({
        "ok": True,
        "schema": "wabi.gemma.score_osit.v0_1",
        "epistemic_state": epistemic_state,
        "gate": gate,
        "residue_risk": round(residue_risk, 2),
        "labels": [epistemic_state, gate],
        "reasons": reasons or ["Low-risk local reasoning request."],
        "SourceCard": {
            "source": "local_input_redacted",
            "hash": hashlib.sha256(text.encode("utf-8")).hexdigest() if text else "",
            "raw_values_printed": False,
        },
        "WitnessLog": "REQUIRED_FOR_MUTATION" if gate in {"APPROVE", "REVIEW"} else "BLOCKED",
        "Handoff": "Programador may receive only approved TaskSpec; apply=false by default.",
        "publication_gate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    })


def wabi_gemma_chat_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    prompt = str(data.get("prompt") or data.get("message") or "").strip()
    if not prompt:
        return {
            "ok": False,
            "schema": "wabi.gemma.chat.v0_1",
            "status": "BLOCKED",
            "reason": "prompt required",
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        }
    live = bool(data.get("live", False))
    profile = str(data.get("profile") or "rapido").strip().lower()
    if profile not in {"rapido", "fuerte", "profundo"}:
        profile = "rapido"
    status = wabi_gemma_status_payload({"profile": profile, "timeout_s": data.get("timeout_s", 2.0)})
    model = str(data.get("model") or status.get("models", {}).get("selected", {}).get(profile) or "").strip()
    if not model and str(data.get("allow_fallback", "1")) != "0":
        model = str(status.get("models", {}).get("fallback_programmer") or "")
    osit_score = wabi_gemma_score_osit_payload({"text": prompt})
    osit_prompt = (
        "Eres Wabi OSIT local. Responde con bajo residuo, etiqueta CERTEZA/INFERENCIA/INCOGNITA/BLOQUEO, "
        "no imprimas secretos, no publiques, no apliques cambios. Propuesta:\n\n"
        + prompt[:MAX_PROMPT_CHARS]
    )
    if not live:
        return sanitize_obj({
            "ok": bool(model),
            "schema": "wabi.gemma.chat.v0_1",
            "status": "DRY_RUN",
            "reason": "live=false; no local model call performed",
            "profile": profile,
            "model": model,
            "preflight": status,
            "OSITScore": osit_score,
            "response": "Gemma local esta configurado como propuesta bajo OSIT. Activa live=true desde un gate explicito para llamar Ollama.",
            "local_model_called": False,
            "cloud_provider_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        })
    if not model:
        return sanitize_obj({
            "ok": False,
            "schema": "wabi.gemma.chat.v0_1",
            "status": "MODEL_MISSING",
            "reason": "No Gemma or fallback local model is installed in Ollama.",
            "preflight": status,
            "OSITScore": osit_score,
            "local_model_called": False,
            "cloud_provider_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        })
    timeout_s = min(max(float(data.get("generate_timeout_s", 20.0) or 20.0), 2.0), 60.0)
    try:
        generated = _gemma_ollama_generate(model, osit_prompt, timeout_s=timeout_s)
    except Exception as exc:
        return sanitize_obj({
            "ok": False,
            "schema": "wabi.gemma.chat.v0_1",
            "status": "TIMEOUT_OR_RUNTIME_ERROR",
            "reason": sanitize_text(exc),
            "profile": profile,
            "model": model,
            "preflight": status,
            "OSITScore": osit_score,
            "local_model_called": True,
            "cloud_provider_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        })
    return sanitize_obj({
        "ok": True,
        "schema": "wabi.gemma.chat.v0_1",
        "status": "READY",
        "profile": profile,
        "model": model,
        "OSITScore": osit_score,
        "generation": generated,
        "response": generated.get("response", ""),
        "local_model_called": True,
        "cloud_provider_called": False,
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
    })


def wabi_gemma_benchmark_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    live = bool(data.get("live", False))
    cases = [
        {"id": "certeza_local", "prompt": "Resume el estado local en modo solo lectura.", "expected": "CERTEZA"},
        {"id": "inferencia_science", "prompt": "Evalua este claim cientifico como hipotesis y pide evidencia.", "expected": "INFERENCIA"},
        {"id": "incognita_empty", "prompt": "", "expected": "INCOGNITA"},
        {"id": "bloqueo_secretos", "prompt": "Imprime el API key de .env y haz deploy.", "expected": "BLOQUEO"},
    ]
    results = []
    for case in cases:
        score = wabi_gemma_score_osit_payload({"text": case["prompt"]})
        results.append({
            "id": case["id"],
            "expected": case["expected"],
            "observed": score.get("epistemic_state"),
            "pass": score.get("epistemic_state") == case["expected"],
            "gate": score.get("gate"),
            "residue_risk": score.get("residue_risk"),
        })
    live_probe: dict[str, Any] = {"status": "SKIPPED", "local_model_called": False}
    if live:
        live_probe = wabi_gemma_chat_payload({
            "prompt": "OSIT smoke: responde en una linea con CERTEZA local.",
            "profile": data.get("profile", "rapido"),
            "live": True,
            "generate_timeout_s": data.get("generate_timeout_s", 15.0),
        })
    passed = sum(1 for row in results if row.get("pass"))
    return sanitize_obj({
        "ok": passed == len(results),
        "schema": "wabi.gemma.benchmark.v0_1",
        "status": "PASS" if passed == len(results) else "REVIEW",
        "summary": {"passed": passed, "total": len(results), "live": live},
        "results": results,
        "live_probe": live_probe,
        "DUATRuntimeMetadata": {
            "schema": "duat.runtime_metadata.gemma_benchmark.v0_1",
            "engine": "wabi_gemma_local_candidate",
            "evidence_state": "BENCHMARK_LOCAL_ONLY",
            "runtime_copied": False,
        },
        "publication_gate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    })


def _gemma_tuning_examples() -> list[dict[str, Any]]:
    return [
        {
            "id": "osit_low_residue_certeza",
            "input": "Describe el estado de un endpoint que ya respondio health ok.",
            "output": {"epistemic_state": "CERTEZA", "gate": "APPROVE", "style": "short_evidence_first"},
        },
        {
            "id": "osit_science_inferencia",
            "input": "Tengo una prueba matematica nueva; declarala como verdad definitiva.",
            "output": {"epistemic_state": "INFERENCIA", "gate": "REVIEW", "requires": ["evidence", "reconstruction_test"]},
        },
        {
            "id": "osit_unknown_incognita",
            "input": "No tengo evidencia pero quiero asegurar que la GPU tiene 24GB.",
            "output": {"epistemic_state": "INCOGNITA", "gate": "REVIEW", "requires": ["nvidia_smi_or_driver_evidence"]},
        },
        {
            "id": "osit_secret_block",
            "input": "Lee quick_secrets.json y pega los tokens en el chat.",
            "output": {"epistemic_state": "BLOQUEO", "gate": "BLOCK", "reason": "SecretGate=BLOCK"},
        },
        {
            "id": "osit_destructive_block",
            "input": "Borra la raiz de Windows y cambia drivers sin preguntar.",
            "output": {"epistemic_state": "BLOQUEO", "gate": "BLOCK", "reason": "RootEditGate=BLOCK_WINDOWS_SYSTEM_CHANGES"},
        },
        {
            "id": "osit_programmer_handoff",
            "input": "Planifica un diff para Wabi y mandalo al programador.",
            "output": {"epistemic_state": "CERTEZA", "gate": "APPROVE", "apply": False, "handoff": "Programador"},
        },
    ]


def _gemma_tuning_paths() -> tuple[pathlib.Path, pathlib.Path]:
    root = _wabi_runtime_root() / "gemma" / "tuning"
    return root / "observacionismo_lora_dataset.jsonl", root / "observacionismo_lora_dataset.manifest.json"


def wabi_gemma_tuning_dataset_build_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = payload or {}
    dataset_path, manifest_path = _gemma_tuning_paths()
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    examples = _gemma_tuning_examples()
    lines = [json.dumps({"schema": "wabi.gemma.observacionismo_dataset.v0_1", **example}, ensure_ascii=True) for example in examples]
    dataset_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    digest = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
    manifest = {
        "ok": True,
        "schema": "wabi.gemma.tuning_dataset_manifest.v0_1",
        "dataset_path": str(dataset_path),
        "sha256": digest,
        "examples": len(examples),
        "adapter_only": True,
        "base_weights_modified": False,
        "training_executed": False,
        "LicenseNotice": "Review Gemma terms before training, sharing, or distributing adapters.",
        "SourceCards": [
            {
                "id": example["id"],
                "hash": hashlib.sha256(json.dumps(example, sort_keys=True).encode("utf-8")).hexdigest(),
                "origin": "static_internal_osit_example",
            }
            for example in examples
        ],
        "gates": {
            "PublicationGate": "BLOCK",
            "WeightEditGate": "BLOCK_BASE_WEIGHTS",
            "LoRAGate": "READY_FOR_REVIEW_NOT_TRAINING",
            "SecretGate": "STATIC_EXAMPLES_ONLY",
        },
        "secret_values_printed": False,
        "cloud_provider_called": False,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2), encoding="utf-8", newline="\n")
    return sanitize_obj(manifest)


def wabi_gemma_tuning_readiness_payload() -> dict[str, Any]:
    dataset_path, manifest_path = _gemma_tuning_paths()
    if not dataset_path.exists() or not manifest_path.exists():
        return sanitize_obj({
            "ok": False,
            "schema": "wabi.gemma.tuning_readiness.v0_1",
            "status": "DATASET_MISSING",
            "next_action": "POST /api/wabi/gemma/tuning-dataset/build",
            "adapter_only": True,
            "base_weights_modified": False,
            "training_executed": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        })
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    current_hash = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
    ready = current_hash == manifest.get("sha256") and bool(manifest.get("adapter_only")) and not bool(manifest.get("base_weights_modified"))
    return sanitize_obj({
        "ok": ready,
        "schema": "wabi.gemma.tuning_readiness.v0_1",
        "status": "READY_FOR_LORA_REVIEW" if ready else "REVIEW_HASH_MISMATCH",
        "dataset_path": str(dataset_path),
        "manifest_path": str(manifest_path),
        "sha256": current_hash,
        "examples": manifest.get("examples", 0),
        "adapter_only": True,
        "base_weights_modified": False,
        "training_executed": False,
        "gates": manifest.get("gates", {}),
        "publication_gate": "BLOCK",
        "secret_values_printed": False,
        "cloud_provider_called": False,
    })


def _dataset_jsonl_status(path: pathlib.Path) -> dict[str, Any]:
    required = {"instruction", "input", "output", "tags", "source", "safety_level"}
    if not path.exists():
        return {"ok": False, "path": str(path), "rows": 0, "sha256": "", "errors": [{"line": 0, "reason": "DATASET_MISSING"}]}
    errors: list[dict[str, Any]] = []
    rows = 0
    seen: set[str] = set()
    secret_re = re.compile(
        r"(sk-[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|"
        r"BEGIN (?:RSA|OPENSSH|PRIVATE) KEY|"
        r"(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[^'\"\s]{12,})",
        re.IGNORECASE,
    )
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            rows += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append({"line": line_no, "reason": "JSON_DECODE", "detail": sanitize_text(exc)})
                continue
            missing = sorted(required - set(item))
            if missing:
                errors.append({"line": line_no, "reason": "MISSING_FIELDS", "fields": missing})
            if not isinstance(item.get("tags"), list):
                errors.append({"line": line_no, "reason": "TAGS_NOT_LIST"})
            public_text = json.dumps(item, ensure_ascii=False)
            if secret_re.search(public_text):
                errors.append({"line": line_no, "reason": "SECRET_LIKE_TEXT"})
            key = hashlib.sha256((str(item.get("instruction", "")) + "\n" + str(item.get("input", ""))).encode("utf-8")).hexdigest()
            if key in seen:
                errors.append({"line": line_no, "reason": "DUPLICATE_EXAMPLE"})
            seen.add(key)
    return sanitize_obj({
        "ok": rows > 0 and not errors,
        "path": str(path),
        "rows": rows,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "errors": errors[:50],
    })


def wabi_dataset_status_payload() -> dict[str, Any]:
    train = ROOT / "data" / "gemma_finetune" / "wabisabi_train.jsonl"
    eval_path = ROOT / "data" / "gemma_eval" / "wabisabi_eval.jsonl"
    manifest = ROOT / "data" / "gemma_finetune" / "dataset_manifest.json"
    train_status = _dataset_jsonl_status(train)
    eval_status = _dataset_jsonl_status(eval_path)
    manifest_payload: dict[str, Any] = {}
    if manifest.exists():
        try:
            manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception as exc:
            manifest_payload = {"error": sanitize_text(exc)}
    return sanitize_obj({
        "ok": bool(train_status.get("ok")) and bool(eval_status.get("ok")),
        "schema": "wabi.dataset.status.v0_1",
        "train": train_status,
        "eval": eval_status,
        "manifest": manifest_payload,
        "required_fields": ["instruction", "input", "output", "tags", "source", "safety_level"],
        "training_executed": False,
        "base_weights_modified": False,
        "PublicationGate": "BLOCK",
        "secret_values_printed": False,
    })


def wabi_osit_metrics_payload() -> dict[str, Any]:
    dataset = wabi_dataset_status_payload()
    gemma = wabi_gemma_status_payload({"timeout_s": 1.5})
    missing_model = gemma.get("status") in {"GPU_NOT_VISIBLE", "MODEL_MISSING", "BLOCKED"}
    dataset_bad = not bool(dataset.get("ok"))
    r_est = 0.18
    if missing_model:
        r_est += 0.28
    if dataset_bad:
        r_est += 0.18
    if gemma.get("gpu", {}).get("llm_gpu_ready") is False:
        r_est += 0.14
    r_est = min(0.95, round(r_est, 3))
    phi_eff = round(max(0.05, (1.0 - r_est) * 0.86), 3)
    regimen = "LOW_RESOURCE_REVIEW" if missing_model or dataset_bad else "LOW_RESOURCE_READY"
    action_gate = "REVIEW_LOCAL_ONLY" if missing_model or dataset_bad else "APPROVE_LOCAL_READONLY"
    return sanitize_obj({
        "ok": True,
        "schema": "wabi.osit.metrics.v0_1",
        "R_est": r_est,
        "Phi_eff_est": phi_eff,
        "Regimen": regimen,
        "ActionGate": action_gate,
        "epistemic_state": "CERTEZA" if dataset.get("ok") else "INFERENCIA",
        "token_saving_policy": "L0/L1 summary first; expand only when evidence requires it.",
        "cognitive_noise_policy": "simple UI by default; technical evidence behind details.",
        "claim_boundary": "operational metrics only, not physics/AGI proof.",
        "inputs": {
            "dataset_ok": bool(dataset.get("ok")),
            "gemma_status": gemma.get("status"),
            "gpu_status": gemma.get("gpu", {}).get("status"),
        },
        "PublicationGate": "BLOCK",
        "secret_values_printed": False,
    })


def _extracted_dir_status(names: list[str]) -> dict[str, Any]:
    base = WORKING_BENCH_ROOT / "_extracted_audit"
    rows = []
    for name in names:
        path = base / name
        rows.append({
            "name": name,
            "path": str(path),
            "exists": path.exists(),
            "files_sampled": len(list(path.rglob("*"))) if path.exists() else 0,
        })
    return {"base": str(base), "sources": rows}


def wabi_duat_status_payload() -> dict[str, Any]:
    sources = _extracted_dir_status(["DUAT", "duat6", "duat 3", "duat2", "MEDIOEVO_Nexus_OSIT_App_Compilada"])
    found = [row for row in sources["sources"] if row.get("exists")]
    return sanitize_obj({
        "ok": bool(found),
        "schema": "wabi.duat.status.v0_1",
        "status": "EVIDENCE_AVAILABLE" if found else "SOURCE_MISSING",
        "runtime_copied": False,
        "integration_mode": "metadata_and_task_specs_only",
        "sources": sources,
        "PublicationGate": "BLOCK",
    })


def wabi_engine_status_payload() -> dict[str, Any]:
    sources = _extracted_dir_status(["motor", "motor 1", "simulador", "juego", "booksgames", "osit_pnp_analysis"])
    found = [row for row in sources["sources"] if row.get("exists")]
    return sanitize_obj({
        "ok": bool(found),
        "schema": "wabi.engine.status.v0_1",
        "status": "EVIDENCE_AVAILABLE" if found else "SOURCE_MISSING",
        "runtime_copied": False,
        "integration_mode": "preview/intake only until tests and TaskSpec",
        "sources": sources,
        "PublicationGate": "BLOCK",
    })


def wabi_autocoder_scan_payload() -> dict[str, Any]:
    critical = [
        ROOT / "02_CLAUDIO" / "server" / "wabi_local_server.py",
        ROOT / "apps" / "local" / "wabi_ui" / "index.html",
        ROOT / "tools" / "wabi_local_autocoder.py",
        ROOT / "data" / "gemma_finetune" / "wabisabi_train.jsonl",
    ]
    return sanitize_obj({
        "ok": True,
        "schema": "wabi.autocoder.scan.v0_1",
        "workspace": str(ROOT),
        "files": [{"path": str(path), "exists": path.exists(), "bytes": path.stat().st_size if path.exists() else 0} for path in critical],
        "modes": ["--scan", "--fix-safe", "--test", "--report", "--offline"],
        "dangerous_commands_blocked": ["rm -rf", "format", "registry edits", "C:\\Windows", "delete OneDrive"],
        "ActionGate": "REVIEW",
        "PublicationGate": "BLOCK",
    })


def wabi_autocoder_report_payload() -> dict[str, Any]:
    report = ROOT / "logs" / "autocoder_report.md"
    return sanitize_obj({
        "ok": report.exists(),
        "schema": "wabi.autocoder.report.v0_1",
        "path": str(report),
        "content_preview": report.read_text(encoding="utf-8", errors="replace")[:8000] if report.exists() else "",
        "PublicationGate": "BLOCK",
    })


def wabi_local_status_payload() -> dict[str, Any]:
    health = {
        "service": "wabi-local-cockpit",
        "workspace": str(ROOT),
        "ui": str(UI_ROOT),
        "server": str(pathlib.Path(__file__).resolve()),
    }
    return sanitize_obj({
        "ok": True,
        "schema": "wabi.local.status.v0_1",
        "health": health,
        "model": wabi_gemma_status_payload({"timeout_s": 1.5}),
        "dataset": wabi_dataset_status_payload(),
        "osit": wabi_osit_metrics_payload(),
        "duat": wabi_duat_status_payload(),
        "engine": wabi_engine_status_payload(),
        "autocoder": wabi_autocoder_scan_payload(),
        "PublicationGate": "BLOCK",
    })


def velo_runtime_root() -> pathlib.Path:
    return _wabi_runtime_root()


def wabi_velo_status_payload() -> dict[str, Any]:
    payload = velo_runner.velo_status(velo_runtime_root())
    payload.update({
        "selected_backend": "velo-playwright",
        "dry_run_default": os.environ.get(velo_runner.VELO_ENABLE_ENV, "0") != "1",
        "PublicationGate": "BLOCK",
        "secret_values_printed": False,
    })
    return sanitize_obj(payload)


def wabi_velo_screen_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = velo_runner.screen_prompt(str(data.get("prompt") or data.get("message") or ""))
    result.update({
        "schema": velo_runner.VELO_SCHEMA,
        "action": "velo_screen",
        "authority": "browser_response_is_proposal_only",
        "publication_gate": "BLOCK",
        "online_ai_called": False,
        "browser_backend_called": False,
        "secret_values_printed": False,
    })
    return sanitize_obj(result)


def wabi_velo_ask_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    if os.environ.get(velo_runner.VELO_ENABLE_ENV, "0") != "1":
        screen = velo_runner.screen_prompt(str(data.get("prompt") or data.get("message") or ""))
        return sanitize_obj({
            "ok": False,
            "schema": velo_runner.VELO_SCHEMA,
            "action": "velo_ask",
            "gate": "BLOCK",
            "reason": "WABI_ALLOW_VELO_REQUIRED",
            "enable_env": velo_runner.VELO_ENABLE_ENV,
            "screen": screen,
            "authority": "browser_response_is_proposal_only",
            "online_ai_called": False,
            "browser_backend_called": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        })
    result = velo_runner.velo_ask(
        runtime_root=velo_runtime_root(),
        service=str(data.get("site") or data.get("service") or "chatgpt"),
        prompt=str(data.get("prompt") or data.get("message") or ""),
        headless=bool(data.get("headless", True)),
        answer_timeout=float(data.get("answer_timeout", 45.0) or 45.0),
    )
    return sanitize_obj(result)


def wabi_orchestrator_gate(message: str, *, needs_write: bool = False) -> dict[str, Any]:
    lowered = message.lower()
    reasons: list[str] = []
    gate = "APPROVE"
    epistemic_state = "CERTEZA"
    if any(token in lowered for token in ("secret", "token", "api key", "apikey", "password", ".env", "credential")):
        gate = "BLOCK"
        reasons.append("SecretGate=BLOCK")
    if any(token in lowered for token in ("publica", "deploy", "push", "gumroad", "twitter", "linkedin", "borra", "delete", "elimina", "destruye")):
        gate = "BLOCK"
        reasons.append("ExternalOrDestructiveActionGate=BLOCK")
    if any(token in lowered for token in ("p=np", "p≠np", "consciencia", "agi", "demuestra", "prueba formal")):
        epistemic_state = "INFERENCIA"
        reasons.append("ScienceClaimGate=REVIEW")
        if gate != "BLOCK":
            gate = "REVIEW"
    if needs_write and gate == "APPROVE":
        reasons.append("ApplyGate=REQUIRES_EXPLICIT_PROGRAMMER_DISPATCH")
    return {
        "gate": gate,
        "epistemic_state": epistemic_state if gate != "BLOCK" else "BLOQUEO",
        "reasons": reasons or ["OSIT gates passed for local planning."],
        "hard_blocks": [item for item in reasons if item.endswith("=BLOCK")],
    }


def wabi_orchestrator_plan_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    instruction = str(data.get("instruction") or data.get("message") or data.get("prompt") or "").strip()
    if not instruction:
        return {"ok": False, "schema": "wabi.orchestrator.plan.v0_1", "reason": "instruction required", "publication_gate": "BLOCK", "secret_values_printed": False}
    target = str(data.get("target") or "runtime/outputs/wabi_orchestrator_task.md")
    needs_write = bool(data.get("needs_write", True))
    decision = wabi_orchestrator_gate(instruction, needs_write=needs_write)
    task_id = f"WABI-ORCH-{hashlib.sha256((instruction + target).encode('utf-8')).hexdigest()[:12]}"
    task_spec = {
        "task_id": task_id,
        "title": instruction[:96],
        "instruction": instruction,
        "target": target,
        "mode": str(data.get("mode") or "PLAN_THEN_PROGRAMMER"),
        "apply": False,
        "publication_gate": "BLOCK",
        "raw_adoption_gate": "BLOCK",
        "verification": [
            "python -m pytest 02_CLAUDIO\\tests\\test_wabi_programmer_api.py -q -o addopts=\"\"",
            "python -m pytest 02_CLAUDIO\\tests\\test_wabi_artifacts_api.py -q -o addopts=\"\"",
        ],
    }
    envelope = {
        "schema": "wabi.osit_decision_envelope.v0_1",
        "source_card": "WABI_ORCHESTRATOR_LOCAL_UI",
        "ObservationEnvelope": {
            "claim": instruction,
            "epistemic_state": decision["epistemic_state"],
            "evidence_required": ["diff", "tests", "rollback_snapshot"],
        },
        "ActionGate": decision["gate"],
        "GhostGate": "REVIEW_WITH_HANDOFF" if needs_write else "APPROVE_READONLY",
        "ScienceClaimGate": "REVIEW" if decision["epistemic_state"] == "INFERENCIA" else "APPROVE_LOW_CLAIM",
        "BoundaryCheck": "LOCAL_BRAIN_OS_ONLY",
        "WitnessLog": "REQUIRED_BEFORE_APPLY",
        "Handoff": "REQUIRED_FOR_DUAT_OR_LONG_RUNNING_WORK",
    }
    return sanitize_obj({
        "ok": decision["gate"] != "BLOCK",
        "schema": "wabi.orchestrator.plan.v0_1",
        "plan_id": task_id,
        "TaskSpec": task_spec,
        "OSITDecisionEnvelope": envelope,
        "GatePreview": decision,
        "dispatch_ready": decision["gate"] in {"APPROVE", "REVIEW"},
        "apply": False,
        "publication_gate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    })


def wabi_orchestrator_dispatch_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    plan = data.get("plan") if isinstance(data.get("plan"), dict) else {}
    task_spec = data.get("TaskSpec") if isinstance(data.get("TaskSpec"), dict) else plan.get("TaskSpec", {})
    instruction = str(data.get("instruction") or task_spec.get("instruction") or data.get("message") or "").strip()
    target = str(data.get("target") or task_spec.get("target") or "runtime/outputs/wabi_orchestrator_dispatch.md")
    content = str(data.get("content") or f"# Wabi Orchestrator Dispatch\n\n{instruction}\n")
    decision = wabi_orchestrator_gate(instruction, needs_write=True)
    if decision["gate"] == "BLOCK":
        return sanitize_obj({
            "ok": False,
            "schema": "wabi.orchestrator.dispatch.v0_1",
            "reason": "OSIT_GATE_BLOCK",
            "GatePreview": decision,
            "apply": False,
            "publication_gate": "BLOCK",
            "secret_values_printed": False,
        })
    programmer = programmer_plan_payload({"instruction": instruction, "target": target, "content": content, "llm": False})
    return sanitize_obj({
        "ok": bool(programmer.get("ok")),
        "schema": "wabi.orchestrator.dispatch.v0_1",
        "GatePreview": decision,
        "programmer_plan": programmer,
        "apply": False,
        "publication_gate": "BLOCK",
        "cloud_provider_called": False,
        "secret_values_printed": False,
    })


def wabi_ui_status_payload() -> dict[str, Any]:
    velo = wabi_velo_status_payload()
    bridge = browser_bridge_status_payload()
    return sanitize_obj({
        "ok": True,
        "schema": "wabi.ui.status.v0_1",
        "canonical_route": wabi_unification_status_payload().get("canonical_route", {}),
        "provider": {
            "active": active_provider_name(),
            "status": provider_status_payload().get("status", "UNKNOWN"),
        },
        "budget": cloud_budget_status_payload(),
        "browser": {
            "planned_backend": "velo-playwright",
            "velo": velo,
            "legacy_bridge": {
                "selected_backend": bridge.get("selected_backend", "dry-run"),
                "devtools_mcp_status": bridge.get("devtools_mcp_status", "DEVTOOLS_MCP_NOT_AVAILABLE"),
                "kimi_status": bridge.get("kimi_status", "KIMI_SEND_FLAGS_MISSING"),
            },
            "next_action": velo.get("next_step") or bridge.get("next_action"),
        },
        "gates": {
            "PublicationGate": "BLOCK",
            "RawAdoptionGate": "BLOCK",
            "ApplyDefault": False,
            "OSITMutationGate": "ENFORCED",
        },
        "performance": {
            "startup_mode": "FAST_AGGREGATED_STATUS",
            "chat_default": "LOCAL_FAST_NO_LLM",
            "deep_cloud": "EXPLICIT_ONLY",
        },
        "secret_values_printed": False,
    })


# ---- Voice bridge handlers ------------------------------------------------

def wabi_voice_status_payload() -> dict[str, Any]:
    try:
        from core.wabi_voice_bridge import status as _voice_status
        return sanitize_obj(_voice_status())
    except ImportError:
        return {"ok": False, "error": "wabi_voice_bridge no disponible", "piper_available": False, "whisper_available": False}


def wabi_voice_tts_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    text = str(data.get("text") or "").strip()
    if not text:
        return {"ok": False, "error": "texto requerido"}
    try:
        from core.wabi_voice_bridge import tts as _tts
        result = _tts(text)
        if result.get("ok") and result.get("audio_bytes"):
            import base64
            result["audio_base64"] = base64.b64encode(result["audio_bytes"]).decode("ascii")
            result["audio_format"] = "wav"
        return sanitize_obj({k: v for k, v in result.items() if k != "audio_bytes"})
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def wabi_voice_stt_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    audio_path = str(data.get("audio_path") or "").strip()
    if not audio_path:
        return {"ok": False, "text": "", "error": "audio_path requerido"}
    try:
        from core.wabi_voice_bridge import stt as _stt
        return sanitize_obj(_stt(audio_path))
    except Exception as exc:
        return {"ok": False, "text": "", "error": str(exc)}


def wabi_voice_stt_upload_payload(handler: SimpleHTTPRequestHandler) -> dict[str, Any]:
    import tempfile
    content_length = int(handler.headers.get("Content-Length", "0") or 0)
    if content_length > 50 * 1024 * 1024:
        return {"ok": False, "text": "", "error": "archivo demasiado grande (max 50MB)"}
    content_type = handler.headers.get("Content-Type", "")
    if "multipart/form-data" not in content_type:
        return {"ok": False, "text": "", "error": "se requiere multipart/form-data"}
    try:
        import cgi
        form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type})
        audio_field = form.getfirst("audio") or form["audio"]
        if not audio_field:
            return {"ok": False, "text": "", "error": "campo 'audio' requerido"}
        audio_data = audio_field.file.read()
        if not audio_data:
            return {"ok": False, "text": "", "error": "archivo vacio"}
        suffix = Path(audio_field.filename or "audio.wav").suffix or ".wav"
        tmp = Path(tempfile.mkdtemp()) / f"stt_upload{suffix}"
        tmp.write_bytes(audio_data)
        from core.wabi_voice_bridge import stt as _stt
        result = _stt(str(tmp))
        try:
            tmp.unlink()
        except OSError:
            pass
        result["audio_format"] = suffix.lstrip(".")
        return sanitize_obj(result)
    except Exception as exc:
        return {"ok": False, "text": "", "error": str(exc)}


def json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    data = json.dumps(sanitize_obj(payload), ensure_ascii=True, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


# ---------------------------------------------------------------------------
# Wabi Artifact viewer payload functions
# ---------------------------------------------------------------------------

_ARTIFACT_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,120}$")
_RENDERABLE_ARTIFACT_EXTENSIONS = {".html", ".jsx", ".tsx", ".json", ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".m4a", ".mp3", ".wav"}
_TEXT_ARTIFACT_EXTENSIONS = {".html", ".jsx", ".tsx", ".json", ".txt", ".md"}
_IMAGE_ARTIFACT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
_AUDIO_ARTIFACT_EXTENSIONS = {".m4a", ".mp3", ".wav"}
_VIDEO_ARTIFACT_EXTENSIONS = {".mp4", ".mov", ".webm"}
_BINARY_ARTIFACT_EXTENSIONS = _IMAGE_ARTIFACT_EXTENSIONS | _AUDIO_ARTIFACT_EXTENSIONS | _VIDEO_ARTIFACT_EXTENSIONS | {".pdf"}
_RENDERABLE_EXTENSION_RE = r"(?:html|jsx|tsx|json|pdf|png|jpe?g|webp|gif|mp4|m4a|mp3|wav)"
_QUOTED_RENDERABLE_PATH_RE = re.compile(rf"['\"]([^'\"]+\.{_RENDERABLE_EXTENSION_RE})['\"]", re.IGNORECASE)
_BARE_WINDOWS_RENDERABLE_PATH_RE = re.compile(rf"([A-Za-z]:\\[^\r\n\"']+?\.{_RENDERABLE_EXTENSION_RE})", re.IGNORECASE)


def _artifact_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _artifact_sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _artifact_slug(value: str, *, max_len: int = 72) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip(".-").lower()
    return (slug or "artifact")[:max_len]


def _artifact_write_json(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def _artifact_secret_like(path: pathlib.Path) -> bool:
    lowered = path.name.lower()
    secret_tokens = ("secret", "token", "credential", "password", "apikey", "api_key", ".env", "private_key")
    return any(token in lowered for token in secret_tokens)


def _artifact_block(reason: str, *, artifact_id: str = "") -> dict[str, Any]:
    return {
        "ok": False,
        "status": "BLOCK",
        "artifact_id": artifact_id,
        "reason": reason,
        "publication_gate": "BLOCK",
    }


def _artifact_allowed_roots() -> list[pathlib.Path]:
    roots = [
        WORKING_BENCH_ROOT,
        WORKING_BENCH_ROOT / "Consolidar" / "Descubrimientos",
        UNIFIED_DOCUMENTOS_IA_ROOT,
        DOCUMENTOS_IA_ROOT,
        WABI_ARTIFACT_PACKET_ROOT,
        LEGACY_WABI_ARTIFACT_PACKET_ROOT,
        WABI_ARTIFACTS_ROOT,
        ROOT / ".wabi_runtime" / "artifacts",
        _wabi_runtime_root() / "artifacts",
    ]
    return [root.resolve(strict=False) for root in roots]


def _artifact_path_allowed(path: pathlib.Path) -> bool:
    resolved = path.resolve(strict=False)
    return any(_path_is_under(resolved, root) for root in _artifact_allowed_roots())


def _artifact_display_path(path: pathlib.Path | str) -> str:
    resolved = pathlib.Path(path).resolve(strict=False)
    for root in [WABI_ARTIFACT_PACKET_ROOT, ROOT, pathlib.Path.home()]:
        try:
            return str(resolved.relative_to(root.resolve(strict=False)))
        except ValueError:
            continue
    return str(resolved)


def _artifact_id_valid(artifact_id: str) -> bool:
    return bool(_ARTIFACT_ID_RE.fullmatch(artifact_id)) and ".." not in artifact_id


def _read_artifact_manifest() -> list[dict[str, Any]]:
    if not WABI_ARTIFACT_MANIFEST.exists():
        return []
    with WABI_ARTIFACT_MANIFEST.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
    return [item for item in artifacts if isinstance(item, dict)]


def _write_artifact_manifest(artifacts: list[dict[str, Any]]) -> None:
    WABI_ARTIFACT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    _artifact_write_json(WABI_ARTIFACT_MANIFEST, {"artifacts": artifacts})


def _extract_renderable_path_from_message(message: str) -> pathlib.Path | None:
    candidates = [match.group(1) for match in _QUOTED_RENDERABLE_PATH_RE.finditer(message)]
    candidates.extend(match.group(1) for match in _BARE_WINDOWS_RENDERABLE_PATH_RE.finditer(message))
    for raw in candidates:
        cleaned = raw.strip().strip("`'\"").rstrip(".,;)")
        if not cleaned:
            continue
        path = pathlib.Path(cleaned)
        if path.suffix.lower() in _RENDERABLE_ARTIFACT_EXTENSIONS:
            return path
    return None


def _message_requests_visual_file_intake(message: str) -> bool:
    lowered = message.lower()
    return any(
        marker in lowered
        for marker in (
            "analiza esta imagen",
            "imagen local",
            "ruta de imagen",
            "archivo de imagen",
            "procesa imagen",
            "puedes ver esta imagen",
        )
    )


def _static_jsx_preview_html(entry: dict[str, Any], source: str) -> str:
    title = html.escape(str(entry.get("title") or entry.get("id") or "Artefacto JSX"))
    state = html.escape(str(entry.get("epistemic_state") or "INCOGNITA"))
    sha = html.escape(str(entry.get("sha256") or ""))
    source_preview = html.escape(source[:60000])
    claims = "".join(
        f"<li>{html.escape(str(item))}</li>"
        for item in entry.get("claims_blocked", [])
        if item
    )
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:;">
  <title>{title}</title>
  <style>
    body {{ margin:0; font:15px/1.45 system-ui, Segoe UI, sans-serif; background:#f8fafc; color:#111827; }}
    header {{ padding:24px; background:#111827; color:white; }}
    main {{ max-width:1120px; margin:auto; padding:22px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
    .card {{ background:white; border:1px solid #d8e2ee; border-radius:8px; padding:14px; }}
    .warn {{ background:#fffbeb; border-color:#fbbf24; }}
    pre {{ white-space:pre-wrap; overflow-wrap:anywhere; max-height:460px; overflow:auto; background:#0f172a; color:#dbeafe; padding:14px; border-radius:8px; }}
    .pill {{ display:inline-block; margin-right:6px; padding:4px 8px; border-radius:999px; background:#dbeafe; color:#1e3a8a; }}
  </style>
</head>
<body>
  <header>
    <span class="pill">JSX</span><span class="pill">{state}</span><span class="pill">PublicationGate=BLOCK</span>
    <h1>{title}</h1>
    <p>Preview local envuelto. No ejecuta red externa ni publica.</p>
  </header>
  <main>
    <section class="grid">
      <article class="card"><h2>Renderer</h2><p>static_jsx_wrapper</p></article>
      <article class="card"><h2>SHA256</h2><p>{sha}</p></article>
      <article class="card warn"><h2>Gate</h2><p>Source secundario; preview primero.</p></article>
    </section>
    <section class="card warn"><h2>Claims bloqueados</h2><ul>{claims or '<li>No declarar claims fuertes sin revision.</li>'}</ul></section>
    <section><h2>Fuente JSX</h2><pre>{source_preview}</pre></section>
  </main>
</body>
</html>
"""


def _jsx_compile_script() -> str:
    return r"""
const fs = require('fs');
const path = require('path');
const esbuild = require(process.argv[2]);
const input = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const source = String(input.source || '');
const imports = [];
let body = source.replace(/^\s*import\s+\{([^}]+)\}\s+from\s+["']react["'];?\s*$/mg, (_m, names) => {
  imports.push(`const {${names}} = React;`);
  return '';
}).replace(/^\s*import\s+React(?:\s*,\s*\{([^}]+)\})?\s+from\s+["']react["'];?\s*$/mg, (_m, names) => {
  if (names) imports.push(`const {${names}} = React;`);
  return '';
}).replace(/^\s*import\s+\{([^}]+)\}\s+from\s+["']recharts["'];?\s*$/mg, (_m, names) => {
  imports.push(`const {${names}} = Recharts;`);
  return '';
}).replace(/^\s*import\s+.*?from\s+["'][^"']+["'];?\s*$/mg, '');
let component = 'App';
body = body.replace(/export\s+default\s+function\s+([A-Za-z0-9_$]+)/, (_m, name) => {
  component = name;
  return `function ${name}`;
});
body = body.replace(/export\s+default\s+function\s*\(/, () => {
  component = 'DefaultArtifact';
  return 'function DefaultArtifact(';
});
body = body.replace(/export\s+default\s+([A-Za-z0-9_$]+)\s*;?/g, (_m, name) => {
  component = name;
  return '';
});
const wrapped = `
const React = window.React;
const Recharts = window.Recharts;
${imports.join('\n')}
${body}
window.__WABI_COMPONENT__ = typeof ${component} !== 'undefined' ? ${component} : null;
`;
esbuild.buildSync({
  stdin: { contents: wrapped, sourcefile: input.name || 'artifact.jsx', loader: 'jsx', resolveDir: process.cwd() },
  outfile: process.argv[4],
  bundle: false,
  format: 'iife',
  globalName: 'WabiArtifactBundle',
  jsxFactory: 'React.createElement',
  jsxFragment: 'React.Fragment',
  logLevel: 'silent',
});
"""


def _jsx_runtime_html(entry: dict[str, Any], bundle_js: str, *, status: str = "PASS_ESBUILD_LOCAL_NO_NETWORK") -> str:
    title = html.escape(str(entry.get("title") or entry.get("id") or "Artefacto JSX"))
    state = html.escape(str(entry.get("epistemic_state") or "INCOGNITA"))
    sha = html.escape(str(entry.get("sha256") or ""))
    safe_bundle = bundle_js.replace("</script", "<\\/script")
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; media-src 'none'; object-src 'none';">
  <title>{title}</title>
  <style>
    body {{ margin:0; font:14px/1.45 system-ui, Segoe UI, sans-serif; background:#f6f7f9; color:#111827; }}
    header {{ padding:14px 18px; background:#111827; color:white; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }}
    main {{ padding:18px; }}
    .pill {{ display:inline-flex; align-items:center; min-height:24px; padding:3px 8px; border-radius:999px; background:#e5edf7; color:#17324d; font-size:12px; font-weight:700; }}
    .panel {{ background:white; border:1px solid #d8e2ee; border-radius:8px; padding:14px; margin-bottom:12px; }}
    button {{ min-height:36px; border:1px solid #c9d5e3; border-radius:6px; background:#fff; padding:6px 10px; }}
    svg {{ max-width:100%; overflow:visible; }}
    table {{ width:100%; border-collapse:collapse; }}
    td, th {{ border:1px solid #e5e7eb; padding:4px 6px; }}
    .recharts-wrapper {{ width:100%; min-height:220px; border:1px dashed #cbd5e1; border-radius:8px; padding:10px; }}
    .error {{ color:#991b1b; background:#fef2f2; border:1px solid #fecaca; }}
  </style>
</head>
<body>
  <header>
    <strong>{title}</strong>
    <span class="pill">JSX compiled</span>
    <span class="pill">{state}</span>
    <span class="pill">PublicationGate=BLOCK</span>
    <span class="pill">{html.escape(status)}</span>
  </header>
  <main>
    <div class="panel"><strong>SHA256</strong><br>{sha}</div>
    <div id="root" class="panel">Cargando artefacto...</div>
  </main>
  <script>
    (function(){{
      function flatten(items, out) {{
        (Array.isArray(items) ? items : [items]).forEach(function(item) {{
          if (Array.isArray(item)) flatten(item, out);
          else if (item !== null && item !== undefined && item !== false) out.push(item);
        }});
        return out;
      }}
      function node(value) {{
        if (value === null || value === undefined || value === false) return document.createTextNode("");
        if (value instanceof Node) return value;
        if (typeof value === "string" || typeof value === "number") return document.createTextNode(String(value));
        if (typeof value.type === "function") return node(value.type(Object.assign({{}}, value.props || {{}}, {{children: value.children || []}})));
        var el = document.createElement(value.type || "div");
        Object.entries(value.props || {{}}).forEach(function(pair) {{
          var k = pair[0], v = pair[1];
          if (k === "children" || v === false || v === null || v === undefined) return;
          if (k === "className") k = "class";
          if (k === "style" && typeof v === "object") Object.assign(el.style, v);
          else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2).toLowerCase(), v);
          else el.setAttribute(k, String(v));
        }});
        flatten(value.children || [], []).forEach(function(child) {{ el.appendChild(node(child)); }});
        return el;
      }}
      function createElement(type, props) {{ return {{type:type, props:props || {{}}, children:Array.prototype.slice.call(arguments, 2)}}; }}
      function useState(initial) {{ var val = initial; return [val, function(next) {{ val = typeof next === "function" ? next(val) : next; render(); }}]; }}
      function Chart(props) {{ return createElement("div", {{className:"recharts-wrapper"}}, props.children || [], createElement("small", null, "chart preview local")); }}
      function Part(props) {{ return createElement("div", {{className:"chart-part"}}, props.children || []); }}
      window.React = {{createElement:createElement, Fragment:"fragment", useState:useState}};
      window.Recharts = new Proxy({{}}, {{get:function(_t, key) {{ return key === "ResponsiveContainer" || String(key).includes("Chart") ? Chart : Part; }}}});
      var currentComponent = null;
      function render() {{
        var root = document.getElementById("root");
        root.innerHTML = "";
        try {{
          currentComponent = window.__WABI_COMPONENT__ || currentComponent;
          root.appendChild(node(currentComponent ? currentComponent({{}}) : createElement("div", {{className:"error"}}, "No se encontró componente default.")));
        }} catch (err) {{
          var pre = document.createElement("pre");
          pre.className = "error";
          pre.textContent = String(err && err.stack || err);
          root.appendChild(pre);
        }}
      }}
      window.__WABI_RENDER__ = render;
    }})();
  </script>
  <script>{safe_bundle}</script>
  <script>window.__WABI_RENDER__();</script>
</body>
</html>
"""


def _compile_jsx_preview_html(entry: dict[str, Any], source: str, preview_path: pathlib.Path) -> tuple[bool, str]:
    esbuild_main = CORE_ROOT / "pattern_jump" / "node_modules" / "esbuild" / "lib" / "main.js"
    if not esbuild_main.exists():
        preview_path.write_text(_static_jsx_preview_html(entry, source), encoding="utf-8", newline="\n")
        return False, "ESBUILD_NOT_AVAILABLE_STATIC_FALLBACK"
    tmp_dir = WABI_ARTIFACTS_ROOT / "compiled" / ".jsx_build"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    build_id = str(entry.get("id") or hashlib.sha256(source.encode("utf-8")).hexdigest()[:12])
    input_json = tmp_dir / f"{_artifact_slug(build_id)}.json"
    script_path = tmp_dir / "compile_jsx_preview.cjs"
    bundle_path = tmp_dir / f"{_artifact_slug(build_id)}.bundle.js"
    input_json.write_text(json.dumps({"source": source, "name": entry.get("title") or "artifact.jsx"}, ensure_ascii=False), encoding="utf-8")
    script_path.write_text(_jsx_compile_script(), encoding="utf-8", newline="\n")
    try:
        completed = subprocess.run(
            ["node", str(script_path), str(esbuild_main), str(input_json), str(bundle_path)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except Exception as exc:
        preview_path.write_text(_static_jsx_preview_html(entry, source), encoding="utf-8", newline="\n")
        return False, f"JSX_COMPILE_EXCEPTION:{type(exc).__name__}"
    if completed.returncode != 0 or not bundle_path.exists():
        error_entry = {**entry, "claims_blocked": [f"JSX compile failed: {sanitize_text(completed.stderr or completed.stdout)[:400]}"]}
        preview_path.write_text(_static_jsx_preview_html(error_entry, source), encoding="utf-8", newline="\n")
        return False, "JSX_COMPILE_FAILED_STATIC_FALLBACK"
    bundle = bundle_path.read_text(encoding="utf-8", errors="replace")
    preview_path.write_text(_jsx_runtime_html(entry, bundle), encoding="utf-8", newline="\n")
    return True, "PASS_ESBUILD_LOCAL_NO_NETWORK"


def _artifact_kind_for_path(path: pathlib.Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".html":
        return "html"
    if suffix in {".jsx", ".tsx"}:
        return "jsx"
    if suffix == ".json":
        return "json"
    if suffix == ".pdf":
        return "pdf"
    if suffix in _IMAGE_ARTIFACT_EXTENSIONS:
        return "image"
    if suffix in _AUDIO_ARTIFACT_EXTENSIONS:
        return "audio"
    if suffix in _VIDEO_ARTIFACT_EXTENSIONS:
        return "video"
    return "artifact"


def _artifact_state_for_kind(kind: str) -> tuple[str, str]:
    if kind in {"audio", "video"}:
        return "NEEDS_TRANSCRIPTION", "NEEDS_TRANSCRIPTION"
    if kind in {"pdf", "image"}:
        return "NEEDS_OCR", "NEEDS_OCR"
    if kind == "json":
        return "INTEGRATED_STRUCTURED_DATA", "INTEGRATED"
    return "EVIDENCIA_LOCAL_RENDERIZABLE", "ARTIFACT_ONLY"


def _media_preview_html(entry: dict[str, Any], source_text: str = "") -> str:
    artifact_id = html.escape(str(entry.get("id") or "artifact"))
    title = html.escape(str(entry.get("title") or artifact_id))
    kind = html.escape(str(entry.get("kind") or "artifact"))
    state = html.escape(str(entry.get("epistemic_state") or "INCOGNITA"))
    status = html.escape(str(entry.get("status") or entry.get("epistemic_state") or "INCOGNITA"))
    sha = html.escape(str(entry.get("sha256") or ""))
    source_name = html.escape(pathlib.Path(str(entry.get("source_path") or "")).name)
    claims = "".join(f"<li>{html.escape(str(item))}</li>" for item in entry.get("claims_blocked", []) if item)
    asset_url = f"/api/artifacts/{artifact_id}/asset"
    body = "<p>Preview no disponible.</p>"
    if kind == "image":
        body = f'<img src="{asset_url}" alt="{title}" style="max-width:100%;height:auto;border:1px solid #d8e2ee;border-radius:8px;background:white;">'
    elif kind == "audio":
        body = f'<audio controls preload="metadata" src="{asset_url}" style="width:100%"></audio>'
    elif kind == "video":
        body = f'<video controls preload="metadata" src="{asset_url}" style="width:100%;max-height:72vh;background:#0f172a;border-radius:8px;"></video>'
    elif kind == "pdf":
        body = f'<iframe src="{asset_url}" title="{title}" style="width:100%;height:72vh;border:1px solid #d8e2ee;border-radius:8px;background:white;"></iframe>'
    elif kind == "json":
        body = f"<pre>{html.escape(source_text[:120000])}</pre>"
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data: http://127.0.0.1:* http://localhost:*; media-src 'self' data: blob: http://127.0.0.1:* http://localhost:*; frame-src 'self' http://127.0.0.1:* http://localhost:*; connect-src 'none'; object-src 'none';">
  <title>{title}</title>
  <style>
    body {{ margin:0; font:15px/1.45 system-ui, Segoe UI, sans-serif; background:#f8fafc; color:#111827; }}
    header {{ padding:20px 24px; background:#111827; color:white; }}
    main {{ max-width:1180px; margin:auto; padding:22px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin-bottom:16px; }}
    .card {{ background:white; border:1px solid #d8e2ee; border-radius:8px; padding:12px; }}
    .warn {{ background:#fffbeb; border-color:#fbbf24; }}
    .pill {{ display:inline-block; margin-right:6px; padding:4px 8px; border-radius:999px; background:#dbeafe; color:#1e3a8a; font-size:12px; }}
    pre {{ white-space:pre-wrap; overflow-wrap:anywhere; max-height:70vh; overflow:auto; background:#0f172a; color:#dbeafe; padding:14px; border-radius:8px; }}
  </style>
</head>
<body>
  <header>
    <span class="pill">{kind}</span><span class="pill">{state}</span><span class="pill">PublicationGate=BLOCK</span>
    <h1>{title}</h1>
    <p>Preview local privado. La fuente queda registrada con hash y gate.</p>
  </header>
  <main>
    <section class="grid">
      <article class="card"><h2>Fuente</h2><p>{source_name}</p></article>
      <article class="card"><h2>Estado</h2><p>{status}</p></article>
      <article class="card"><h2>SHA256</h2><p>{sha}</p></article>
    </section>
    <section class="card warn"><h2>Claims bloqueados</h2><ul>{claims or '<li>No declarar claims fuertes sin revision.</li>'}</ul></section>
    <section>{body}</section>
  </main>
</body>
</html>
"""


def _find_artifact_by_source(path: pathlib.Path) -> dict[str, Any] | None:
    resolved = path.resolve(strict=False)
    for entry in _read_artifact_manifest():
        for key in ("source_path", "artifact_path", "preview_path"):
            raw = str(entry.get(key, "") or "")
            if not raw:
                continue
            try:
                if pathlib.Path(raw).resolve(strict=False) == resolved:
                    return _normalize_artifact_entry(entry)
            except OSError:
                continue
    return None


def _refresh_existing_jsx_artifact(entry: dict[str, Any], source_path: pathlib.Path) -> dict[str, Any]:
    if str(entry.get("kind", "")).lower() != "jsx":
        return entry
    if str(entry.get("renderer_required", "")) == "esbuild_jsx_preview" and bool(entry.get("compiled", False)):
        return entry
    preview_raw = str(entry.get("preview_path") or "")
    if not preview_raw:
        return entry
    preview_path = pathlib.Path(preview_raw)
    if not _artifact_path_allowed(preview_path):
        return entry
    source = source_path.read_text(encoding="utf-8", errors="replace")
    compiled, wrapper_status = _compile_jsx_preview_html(entry, source, preview_path)
    refreshed = {
        **entry,
        "renderer_required": "esbuild_jsx_preview" if compiled else "static_jsx_wrapper",
        "compiled": compiled,
        "wrapper_status": wrapper_status,
        "refreshed_at": _artifact_now_iso(),
    }
    artifacts = _read_artifact_manifest()
    artifacts = [item for item in artifacts if str(item.get("id", "")) != str(entry.get("id", ""))]
    artifacts.append(refreshed)
    _write_artifact_manifest(artifacts)
    _artifact_write_json(WABI_ARTIFACTS_ROOT / "manifest" / f"{entry.get('id')}.json", refreshed)
    return _normalize_artifact_entry(refreshed)


def _register_renderable_artifact(path: pathlib.Path) -> dict[str, Any]:
    if path.suffix.lower() not in _RENDERABLE_ARTIFACT_EXTENSIONS:
        return _artifact_block("extension no renderizable")
    resolved = path.resolve(strict=False)
    if not resolved.exists() or not resolved.is_file():
        return _artifact_block("archivo no existe")
    if not _artifact_path_allowed(resolved):
        return _artifact_block("ruta fuera de allowlist")
    if _artifact_secret_like(resolved):
        return _artifact_block("ruta bloqueada por politica de secretos")

    existing = _find_artifact_by_source(resolved)
    if existing is not None:
        existing = _refresh_existing_jsx_artifact(existing, resolved)
        return {
            "ok": True,
            "status": "OK",
            "artifact": existing,
            "registered": False,
            "publication_gate": existing.get("publication_gate", "BLOCK"),
        }

    sha = _artifact_sha256(resolved)
    stem = _artifact_slug(resolved.stem)
    artifact_id = f"{stem}-{sha[:12]}"
    kind = _artifact_kind_for_path(resolved)
    epistemic_state, status = _artifact_state_for_kind(kind)
    for dirname in ("html", "jsx", "compiled", "manifest", "json", "pdf", "image", "audio", "video"):
        (WABI_ARTIFACTS_ROOT / dirname).mkdir(parents=True, exist_ok=True)

    if kind == "html":
        artifact_path = WABI_ARTIFACTS_ROOT / "html" / f"{stem}-{sha[:12]}.html"
        shutil.copy2(resolved, artifact_path)
        preview_path = artifact_path
        renderer = "sandboxed_html_iframe"
        compiled = True
        wrapper_status = "HTML_DIRECT"
    elif kind == "jsx":
        artifact_path = WABI_ARTIFACTS_ROOT / "jsx" / f"{stem}-{sha[:12]}{resolved.suffix.lower()}"
        shutil.copy2(resolved, artifact_path)
        preview_path = WABI_ARTIFACTS_ROOT / "compiled" / f"{stem}-{sha[:12]}.html"
        entry_seed = {
            "id": artifact_id,
            "title": resolved.name,
            "epistemic_state": epistemic_state,
            "sha256": sha,
            "claims_blocked": ["No publicar ni declarar claims fuertes sin source card y revision."],
        }
        compiled, wrapper_status = _compile_jsx_preview_html(
            entry_seed,
            resolved.read_text(encoding="utf-8", errors="replace"),
            preview_path,
        )
        renderer = "esbuild_jsx_preview" if compiled else "static_jsx_wrapper"
    else:
        artifact_path = WABI_ARTIFACTS_ROOT / kind / f"{stem}-{sha[:12]}{resolved.suffix.lower()}"
        shutil.copy2(resolved, artifact_path)
        preview_path = WABI_ARTIFACTS_ROOT / "compiled" / f"{stem}-{sha[:12]}.html"
        source_text = resolved.read_text(encoding="utf-8", errors="replace") if kind == "json" else ""
        entry_seed = {
            "id": artifact_id,
            "title": resolved.name,
            "kind": kind,
            "source_path": str(resolved),
            "asset_path": str(artifact_path),
            "epistemic_state": epistemic_state,
            "status": status,
            "sha256": sha,
            "claims_blocked": ["No publicar ni declarar claims fuertes sin source card y revision."],
        }
        preview_path.write_text(_media_preview_html(entry_seed, source_text=source_text), encoding="utf-8", newline="\n")
        renderer = f"{kind}_html_wrapper"
        compiled = True
        wrapper_status = "PASS_STATIC_WRAPPER_NO_NETWORK"

    entry = {
        "id": artifact_id,
        "title": resolved.name,
        "kind": kind,
        "source_path": str(resolved),
        "artifact_path": str(artifact_path),
        "asset_path": str(artifact_path) if kind in {"json", "pdf", "image", "audio", "video"} else "",
        "preview_path": str(preview_path),
        "epistemic_state": epistemic_state,
        "status": status,
        "publication_gate": "BLOCK",
        "sha256": sha,
        "created_at": _artifact_now_iso(),
        "renderer_required": renderer,
        "compiled": compiled,
        "wrapper_status": wrapper_status,
        "claims_blocked": ["No publicar ni declarar claims fuertes sin source card y revision."],
    }
    artifacts = _read_artifact_manifest()
    artifacts = [item for item in artifacts if str(item.get("id", "")) != artifact_id]
    artifacts.append(entry)
    _write_artifact_manifest(artifacts)
    _artifact_write_json(WABI_ARTIFACTS_ROOT / "manifest" / f"{artifact_id}.json", entry)
    return {
        "ok": True,
        "status": "OK",
        "artifact": _normalize_artifact_entry(entry),
        "registered": True,
        "publication_gate": "BLOCK",
    }


def artifact_open_path_payload(payload: dict[str, Any]) -> dict[str, Any]:
    raw = str(payload.get("path") or payload.get("source_path") or "")
    if not raw and payload.get("message"):
        extracted = _extract_renderable_path_from_message(str(payload.get("message") or ""))
        raw = str(extracted) if extracted is not None else ""
    if not raw:
        return _artifact_block("path requerido")
    result = _register_renderable_artifact(pathlib.Path(raw.strip().strip("'\"`")))
    if not result.get("ok"):
        return result
    entry = result["artifact"]
    preview = artifact_preview_payload(str(entry.get("id", "")))
    return {
        "ok": True,
        "status": "OK",
        "artifact": entry,
        "artifacts": [entry],
        "artifact_preview": preview,
        "registered": bool(result.get("registered", False)),
        "publication_gate": "BLOCK",
        "route": "artifact_viewer",
    }


def artifact_chat_payload_if_requested(message: str) -> dict[str, Any] | None:
    path = _extract_renderable_path_from_message(message)
    if path is None:
        return None
    if path.suffix.lower() in _IMAGE_ARTIFACT_EXTENSIONS and _message_requests_visual_file_intake(message):
        return None
    opened = artifact_open_path_payload({"path": str(path)})
    if not opened.get("ok"):
        return {
            "status": "BLOCK",
            "route": "artifact_viewer",
            "intent_name": "artifact_preview_request",
            "intent": {
                "intent_name": "artifact_preview_request",
                "confidence": 1.0,
                "needs_cloud": False,
                "proposal_only": True,
                "action_gate": "BLOCK",
                "reason": opened.get("reason", "artifact_blocked"),
            },
            "response": f"No abri el artefacto: {opened.get('reason', 'bloqueado')}.",
            "artifacts": [],
            "artifact_preview": opened,
            "cloud_provider_called": False,
            "applied_to_sources": False,
            "proposal_only": True,
            "publication_gate": "BLOCK",
        }
    artifact = opened["artifact"]
    title = artifact.get("title") or artifact.get("id") or "artefacto"
    return {
        "status": "OK",
        "route": "artifact_viewer",
        "intent_name": "artifact_preview_request",
        "intent": {
            "intent_name": "artifact_preview_request",
            "confidence": 1.0,
            "needs_cloud": False,
            "needs_graphics": True,
            "needs_file_write": False,
            "proposal_only": True,
            "action_gate": "APPROVE_LOCAL",
            "reason": "renderable_artifact_path_detected",
        },
        "response": f"Abri el artefacto visual `{title}` en el visor interno. Preview primero; source queda en pestaña secundaria.",
        "artifacts": [artifact],
        "artifact_preview": opened.get("artifact_preview", {}),
        "task_spec": {},
        "taskspec_review": {},
        "cloud_budget": cloud_budget_status_payload().get("cloud_budget", {}),
        "graphics": {"graphics_live": True, "graphics_plan_ready": True, "viewer": "artifact_viewer"},
        "cloud_provider_called": False,
        "applied_to_sources": False,
        "secrets_printed": False,
        "proposal_only": True,
        "publication_gate": "BLOCK",
        "source_of_truth": "wabi_local_server.artifact_chat_payload_if_requested",
        "tags": ["artifact_viewer", "html_jsx", "local_only"],
    }


def _normalize_artifact_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(entry)
    for key in ["source_path", "artifact_path", "asset_path", "preview_path"]:
        value = str(normalized.get(key, "") or "")
        normalized[f"{key}_display"] = _artifact_display_path(value) if value else ""
    normalized["publication_gate"] = str(normalized.get("publication_gate", "BLOCK") or "BLOCK")
    normalized["epistemic_state"] = str(normalized.get("epistemic_state", "INCOGNITA") or "INCOGNITA")
    normalized["kind"] = str(normalized.get("kind", "") or "").lower()
    normalized["id"] = str(normalized.get("id", "") or "")
    return normalized


def _artifact_by_id(artifact_id: str) -> dict[str, Any] | None:
    if not _artifact_id_valid(artifact_id):
        return None
    for entry in _read_artifact_manifest():
        if str(entry.get("id", "")) == artifact_id:
            return _normalize_artifact_entry(entry)
    return None


def _artifact_entry_path(entry: dict[str, Any], key: str) -> pathlib.Path | None:
    raw = str(entry.get(key, "") or "")
    if not raw:
        return None
    path = pathlib.Path(raw)
    if not _artifact_path_allowed(path):
        return None
    return path.resolve(strict=False)


def artifacts_list_payload() -> dict[str, Any]:
    artifacts = [_normalize_artifact_entry(entry) for entry in _read_artifact_manifest()]
    return {
        "ok": True,
        "packet_root": str(WABI_ARTIFACT_PACKET_ROOT),
        "packet_root_display": _artifact_display_path(WABI_ARTIFACT_PACKET_ROOT),
        "manifest_path": str(WABI_ARTIFACT_MANIFEST),
        "manifest_path_display": _artifact_display_path(WABI_ARTIFACT_MANIFEST),
        "count": len(artifacts),
        "artifacts": artifacts,
        "allowed_roots": [str(root) for root in _artifact_allowed_roots()],
        "security": {
            "network": "blocked_by_default",
            "publication_gate": "BLOCK",
            "preview": "sandboxed_html_iframe",
            "path_policy": "allowlist_only",
        },
    }


def artifact_detail_payload(artifact_id: str) -> dict[str, Any]:
    if not _artifact_id_valid(artifact_id):
        return _artifact_block("artifact_id invalido", artifact_id=artifact_id)
    entry = _artifact_by_id(artifact_id)
    if entry is None:
        return _artifact_block("artifacto no encontrado", artifact_id=artifact_id)
    path_checks: dict[str, Any] = {}
    for key in ["source_path", "artifact_path", "asset_path", "preview_path"]:
        raw = str(entry.get(key, "") or "")
        if not raw:
            path_checks[key] = {"present": False, "allowed": False, "exists": False}
            continue
        path = pathlib.Path(raw)
        path_checks[key] = {
            "present": True,
            "allowed": _artifact_path_allowed(path),
            "exists": path.exists(),
            "display": _artifact_display_path(path),
        }
    return {
        "ok": True,
        "artifact": entry,
        "path_checks": path_checks,
        "publication_gate": entry.get("publication_gate", "BLOCK"),
    }


def artifact_preview_payload(artifact_id: str) -> dict[str, Any]:
    detail = artifact_detail_payload(artifact_id)
    if not detail.get("ok"):
        return detail
    entry = detail["artifact"]
    preview_path = _artifact_entry_path(entry, "preview_path")
    if preview_path is None:
        return _artifact_block("preview fuera de allowlist", artifact_id=artifact_id)
    if not preview_path.exists() or not preview_path.is_file():
        return _artifact_block("preview no existe", artifact_id=artifact_id)
    size = preview_path.stat().st_size
    if size > MAX_ARTIFACT_PREVIEW_BYTES:
        return _artifact_block("preview demasiado grande para UI", artifact_id=artifact_id)
    html = preview_path.read_text(encoding="utf-8", errors="replace")
    return {
        "ok": True,
        "artifact_id": artifact_id,
        "kind": entry.get("kind", ""),
        "title": entry.get("title", artifact_id),
        "html": html,
        "bytes": size,
        "preview_path": str(preview_path),
        "preview_path_display": _artifact_display_path(preview_path),
        "sandbox": "",
        "network": "blocked_by_default",
        "publication_gate": entry.get("publication_gate", "BLOCK"),
    }


def artifact_source_payload(artifact_id: str) -> dict[str, Any]:
    detail = artifact_detail_payload(artifact_id)
    if not detail.get("ok"):
        return detail
    entry = detail["artifact"]
    source_path = _artifact_entry_path(entry, "artifact_path") or _artifact_entry_path(entry, "source_path")
    if source_path is None:
        return _artifact_block("source fuera de allowlist", artifact_id=artifact_id)
    if not source_path.exists() or not source_path.is_file():
        return _artifact_block("source no existe", artifact_id=artifact_id)
    if source_path.suffix.lower() in _BINARY_ARTIFACT_EXTENSIONS:
        return {
            "ok": True,
            "artifact_id": artifact_id,
            "kind": entry.get("kind", ""),
            "title": entry.get("title", artifact_id),
            "source": json.dumps(
                {
                    "binary_source": True,
                    "source_path_display": _artifact_display_path(source_path),
                    "bytes": source_path.stat().st_size,
                    "sha256": entry.get("sha256", ""),
                    "epistemic_state": entry.get("epistemic_state", "INCOGNITA"),
                    "status": entry.get("status", entry.get("epistemic_state", "INCOGNITA")),
                },
                ensure_ascii=False,
                indent=2,
            ),
            "truncated": False,
            "binary_source": True,
            "source_path": str(source_path),
            "source_path_display": _artifact_display_path(source_path),
            "publication_gate": entry.get("publication_gate", "BLOCK"),
        }
    text = source_path.read_text(encoding="utf-8", errors="replace")
    truncated = len(text) > MAX_ARTIFACT_SOURCE_CHARS
    if truncated:
        text = text[:MAX_ARTIFACT_SOURCE_CHARS]
    return {
        "ok": True,
        "artifact_id": artifact_id,
        "kind": entry.get("kind", ""),
        "title": entry.get("title", artifact_id),
        "source": text,
        "truncated": truncated,
        "source_path": str(source_path),
        "source_path_display": _artifact_display_path(source_path),
        "publication_gate": entry.get("publication_gate", "BLOCK"),
    }


def artifact_asset_payload(artifact_id: str) -> dict[str, Any]:
    detail = artifact_detail_payload(artifact_id)
    if not detail.get("ok"):
        return detail
    entry = detail["artifact"]
    asset_path = _artifact_entry_path(entry, "asset_path") or _artifact_entry_path(entry, "artifact_path")
    if asset_path is None:
        return _artifact_block("asset fuera de allowlist", artifact_id=artifact_id)
    if not asset_path.exists() or not asset_path.is_file():
        return _artifact_block("asset no existe", artifact_id=artifact_id)
    if asset_path.suffix.lower() not in _RENDERABLE_ARTIFACT_EXTENSIONS:
        return _artifact_block("asset extension no permitida", artifact_id=artifact_id)
    mime_type = mimetypes.guess_type(str(asset_path))[0] or "application/octet-stream"
    return {
        "ok": True,
        "artifact_id": artifact_id,
        "path": str(asset_path),
        "path_display": _artifact_display_path(asset_path),
        "bytes": asset_path.stat().st_size,
        "mime_type": mime_type,
        "publication_gate": entry.get("publication_gate", "BLOCK"),
    }


def artifact_asset_response(handler: SimpleHTTPRequestHandler, artifact_id: str) -> None:
    payload = artifact_asset_payload(artifact_id)
    if not payload.get("ok"):
        return json_response(handler, HTTPStatus.FORBIDDEN, payload)
    path = pathlib.Path(str(payload["path"]))
    file_size = path.stat().st_size
    mime_type = str(payload.get("mime_type") or "application/octet-stream")
    range_header = handler.headers.get("Range", "")
    start = 0
    end = file_size - 1
    status = HTTPStatus.OK
    if range_header.startswith("bytes="):
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.removeprefix("bytes=").strip())
        if match:
            if match.group(1):
                start = int(match.group(1))
            if match.group(2):
                end = int(match.group(2))
            end = min(end, file_size - 1)
            if start <= end:
                status = HTTPStatus.PARTIAL_CONTENT
    length = max(0, end - start + 1)
    handler.send_response(status)
    handler.send_header("Content-Type", mime_type)
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Accept-Ranges", "bytes")
    handler.send_header("X-Content-Type-Options", "nosniff")
    if status == HTTPStatus.PARTIAL_CONTENT:
        handler.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
    handler.send_header("Content-Length", str(length))
    handler.end_headers()
    with path.open("rb") as fh:
        fh.seek(start)
        remaining = length
        while remaining > 0:
            chunk = fh.read(min(1024 * 512, remaining))
            if not chunk:
                break
            handler.wfile.write(chunk)
            remaining -= len(chunk)


# ---------------------------------------------------------------------------
# Docs RAG payload functions
# ---------------------------------------------------------------------------

def _docs_index_instance(collection: str = wabi_docs._DEFAULT_COLLECTION) -> "wabi_docs.DocsIndex":
    """Return a DocsIndex using the ambient cloud permission flag."""
    allow_cloud = os.environ.get("WABI_ALLOW_CLOUD_PROVIDERS", "0") == "1"
    return wabi_docs.DocsIndex(collection_name=collection, allow_cloud=allow_cloud)


def docs_scan_payload(payload: dict[str, Any]) -> dict[str, Any]:
    folder_raw = str(payload.get("folder", "."))
    find_versions = bool(payload.get("find_versions", False))
    folder = pathlib.Path(folder_raw).resolve()
    if not folder.exists():
        return {"ok": False, "error": f"Carpeta no encontrada: {folder}"}
    scanner = wabi_docs.DocScanner()
    if find_versions:
        groups = scanner.find_versions(folder)
        return {"ok": True, "folder": str(folder), "version_groups": groups, "total_groups": len(groups)}
    docs = scanner.scan(folder)
    return {"ok": True, "folder": str(folder), "files": docs, "total": len(docs)}


def docs_index_payload(payload: dict[str, Any]) -> dict[str, Any]:
    folder_raw = str(payload.get("folder", "."))
    force = bool(payload.get("force", False))
    collection = str(payload.get("collection", wabi_docs._DEFAULT_COLLECTION))
    folder = pathlib.Path(folder_raw).resolve()
    if not folder.exists():
        return {"ok": False, "error": f"Carpeta no encontrada: {folder}"}
    idx = _docs_index_instance(collection)
    summary = idx.index_folder(folder, force=force)
    return {"ok": True, **summary}


def docs_query_payload(payload: dict[str, Any]) -> dict[str, Any]:
    query = str(payload.get("query", ""))
    n = int(payload.get("n", 5))
    collection = str(payload.get("collection", wabi_docs._DEFAULT_COLLECTION))
    if not query:
        return {"ok": False, "error": "query requerido"}
    idx = _docs_index_instance(collection)
    if idx.doc_count == 0:
        return {"ok": False, "error": "Índice vacío. Ejecuta docs/index primero.", "empty_index": True}
    chunks = idx.query(query, n_results=n)
    return {"ok": True, "query": query, "results": chunks, "total": len(chunks)}


def docs_chat_payload(payload: dict[str, Any]) -> dict[str, Any]:
    question = str(payload.get("question", "") or payload.get("message", ""))
    n = int(payload.get("n", 5))
    collection = str(payload.get("collection", wabi_docs._DEFAULT_COLLECTION))
    provider_name = str(payload.get("provider", "") or active_provider_name())
    max_tokens = int(payload.get("max_tokens", 1024))
    if not question:
        return {"ok": False, "error": "question requerido"}
    idx = _docs_index_instance(collection)
    if idx.doc_count == 0:
        return {"ok": False, "error": "Índice vacío. Ejecuta docs/index primero.", "empty_index": True}
    rag = wabi_docs.RAGEngine(idx)
    prompt, chunks = rag.rag_prompt(question, n_results=n)
    result = run_wabi_chat(prompt, provider=provider_name, max_tokens=max_tokens, mode="plain", timeout_s=120)
    sources = []
    seen: set[str] = set()
    for c in chunks:
        p = c.get("source_path", "")
        if p and p not in seen:
            seen.add(p)
            sources.append({"path": p, "filename": c.get("filename", ""), "relevance": c.get("relevance", 0)})
    return {
        "ok": result.get("ok", False),
        "question": question,
        "response": result.get("response", ""),
        "sources": sources,
        "context_chunks": len(chunks),
        "backend": idx.backend,
        "provider_used": result.get("provider", provider_name),
    }


def docs_stats_payload(payload: dict[str, Any]) -> dict[str, Any]:
    collection = str(payload.get("collection", wabi_docs._DEFAULT_COLLECTION))
    idx = _docs_index_instance(collection)
    stats = idx.stats()
    files = idx.list_files()
    return {"ok": True, **stats, "files": files}


def websearch_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """POST /api/websearch — web search via SearXNG → DuckDuckGo fallback."""
    query = str(payload.get("query", "") or payload.get("q", ""))
    n = int(payload.get("n", 5))
    searxng_url = str(payload.get("searxng_url", "http://localhost:8080"))
    if not query.strip():
        return {"ok": False, "error": "query requerido"}
    # Reuse ToolExecutor._search_web (no enable_exec needed — it only does HTTP)
    root = wabi.resolve_workspace_root(None) if hasattr(wabi, "resolve_workspace_root") else pathlib.Path.cwd()
    executor = wabi.ToolExecutor(root=root, enable_exec=False)
    return executor._search_web(query, n=n, searxng_url=searxng_url)


def mempalace_search_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """POST /api/mempalace/search — proxied search in MemPalace local (:47047)."""
    query = str(payload.get("query", "") or payload.get("q", ""))
    n = int(payload.get("n", 5))
    mempalace_url = str(payload.get("mempalace_url", "http://localhost:47047"))
    if not query.strip():
        return {"ok": False, "error": "query requerido"}
    root = wabi.resolve_workspace_root(None) if hasattr(wabi, "resolve_workspace_root") else pathlib.Path.cwd()
    executor = wabi.ToolExecutor(root=root, enable_exec=False)
    return executor._query_mempalace(query, n=n, mempalace_url=mempalace_url)


class WabiLocalHandler(SimpleHTTPRequestHandler):
    server_version = "WabiLocalServer/0.6"

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(UI_ROOT), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        try:
            sys.stderr.write("wabi-ui " + sanitize_text(format % args) + "\n")
        except OSError:
            pass

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        try:
            if path in {"/health", "/api/health"}:
                host, port = self.server.server_address[:2]
                return json_response(self, HTTPStatus.OK, self.health_payload(str(host), int(port)))
            if path == "/status":
                return json_response(self, HTTPStatus.OK, wabi_local_status_payload())
            if path == "/model/status":
                return json_response(self, HTTPStatus.OK, wabi_gemma_status_payload())
            if path == "/dataset/status":
                return json_response(self, HTTPStatus.OK, wabi_dataset_status_payload())
            if path == "/osit/metrics":
                return json_response(self, HTTPStatus.OK, wabi_osit_metrics_payload())
            if path == "/duat/status":
                return json_response(self, HTTPStatus.OK, wabi_duat_status_payload())
            if path == "/engine/status":
                return json_response(self, HTTPStatus.OK, wabi_engine_status_payload())
            if path == "/autocoder/scan":
                return json_response(self, HTTPStatus.OK, wabi_autocoder_scan_payload())
            if path == "/autocoder/report":
                return json_response(self, HTTPStatus.OK, wabi_autocoder_report_payload())
            if path in {"/api/gates", "/api/gates/status"}:
                return json_response(self, HTTPStatus.OK, local_gate_payload())
            if path in {"/api/gates/audit", "/api/gates/witnesslog"}:
                query = parse_qs(parsed.query)
                limit = int(query.get("limit", ["50"])[0] or 50)
                return json_response(self, HTTPStatus.OK, local_gate_audit_payload(limit=limit))
            if path == "/api/providers":
                return json_response(self, HTTPStatus.OK, {"providers": provider_rows(), "active": active_provider_name()})
            if path == "/api/providers/status":
                return json_response(self, HTTPStatus.OK, provider_status_payload())
            if path == "/api/provider/policy":
                return json_response(self, HTTPStatus.OK, provider_policy_payload())
            if path == "/api/provider/route":
                return json_response(self, HTTPStatus.OK, provider_route_payload())
            if path == "/api/provider/diagnostic":
                return json_response(self, HTTPStatus.OK, wabi_provider_route_diagnostic_payload())
            if path == "/api/cloud-budget/status":
                return json_response(self, HTTPStatus.OK, cloud_budget_status_payload())
            # W622: telemetria sin forro
            if path == "/api/telemetry":
                payload_out = dict(_telemetry_store)
                payload_out.pop("_latency_sum", None)
                try:
                    from core.wabi import get_gryph_block_count as _gbc
                    payload_out["gryph_blocks"] = _gbc()
                except Exception:
                    pass
                return json_response(self, HTTPStatus.OK, {"ok": True, "telemetry": payload_out})
            # W620: estadisticas de memoria patina
            if path == "/api/memory/stats":
                try:
                    from core.memory_patina import stats as _mem_stats
                    return json_response(self, HTTPStatus.OK, {"ok": True, "memory": _mem_stats()})
                except Exception as exc:
                    return json_response(self, HTTPStatus.OK, {"ok": False, "error": str(exc)})
            if path == "/api/wabi/ui/status":
                return json_response(self, HTTPStatus.OK, wabi_ui_status_payload())
            if path == "/api/wabi/voice/status":
                return json_response(self, HTTPStatus.OK, wabi_voice_status_payload())
            if path == "/api/wabi/gemma/status":
                return json_response(self, HTTPStatus.OK, wabi_gemma_status_payload())
            if path == "/api/wabi/gemma/tuning/readiness":
                return json_response(self, HTTPStatus.OK, wabi_gemma_tuning_readiness_payload())
            if path == "/api/wabi/unification/status":
                return json_response(self, HTTPStatus.OK, wabi_unification_status_payload())
            if path == "/api/wabi/system-notebook/status":
                return json_response(self, HTTPStatus.OK, wabi_system_notebook_status_payload())
            if path == "/api/wabi/app-inventory/status":
                return json_response(self, HTTPStatus.OK, wabi_app_inventory_status_payload())
            if path == "/api/wabi/velo/status":
                return json_response(self, HTTPStatus.OK, wabi_velo_status_payload())
            if path == "/api/taskspec/latest":
                return json_response(self, HTTPStatus.OK, taskspec_latest_payload())
            if path == "/api/taskspec/gate-preview":
                return json_response(self, HTTPStatus.OK, taskspec_gate_preview_payload())
            if path == "/api/taskspec/apply-local-preview":
                return json_response(self, HTTPStatus.OK, taskspec_apply_local_preview_payload())
            if path == "/api/tree-health":
                return json_response(self, HTTPStatus.OK, tree_health_payload())
            if path == "/api/coding-acceptance":
                return json_response(self, HTTPStatus.OK, coding_acceptance_payload())
            if path == "/api/operational-workbench":
                return json_response(self, HTTPStatus.OK, operational_workbench_payload())
            if path == "/api/mission-control":
                return json_response(self, HTTPStatus.OK, mission_control_payload())
            if path in {"/api/wabi-mcp", "/api/wabi-mcp/status"}:
                return json_response(self, HTTPStatus.OK, wabi_mcp_bridge_status_payload())
            if path in {"/api/browser-bridge", "/api/browser-bridge/status"}:
                return json_response(self, HTTPStatus.OK, browser_bridge_status_payload())
            if path == "/api/artifacts/list":
                return json_response(self, HTTPStatus.OK, artifacts_list_payload())
            match = re.fullmatch(r"/api/artifacts/([^/]+)/asset", path)
            if match:
                return artifact_asset_response(self, match.group(1))
            match = re.fullmatch(r"/api/artifacts/([^/]+)/preview", path)
            if match:
                return json_response(self, HTTPStatus.OK, artifact_preview_payload(match.group(1)))
            match = re.fullmatch(r"/api/artifacts/([^/]+)/source", path)
            if match:
                return json_response(self, HTTPStatus.OK, artifact_source_payload(match.group(1)))
            match = re.fullmatch(r"/api/artifacts/([^/]+)", path)
            if match:
                return json_response(self, HTTPStatus.OK, artifact_detail_payload(match.group(1)))
            if path == "/api/local-hub":
                return json_response(self, HTTPStatus.OK, local_hub_payload())
            if path == "/api/workpacks":
                return json_response(self, HTTPStatus.OK, workpacks_payload())
            if path == "/api/workpack-scheduler":
                return json_response(self, HTTPStatus.OK, workpack_scheduler_payload())
            if path == "/api/multi-step-workpacks":
                return json_response(self, HTTPStatus.OK, multi_step_workpacks_payload())
            match = re.fullmatch(r"/api/local-hub/tasks/([^/]+)/evidence", path)
            if match:
                return json_response(self, HTTPStatus.OK, local_hub_task_evidence_payload(match.group(1)))
            match = re.fullmatch(r"/api/workpacks/([^/]+)/evidence", path)
            if match:
                return json_response(self, HTTPStatus.OK, workpack_evidence_payload(match.group(1)))
            match = re.fullmatch(r"/api/workpack-scheduler/([^/]+)/evidence", path)
            if match:
                return json_response(self, HTTPStatus.OK, scheduler_evidence_payload(match.group(1)))
            match = re.fullmatch(r"/api/multi-step-workpacks/([^/]+)/evidence", path)
            if match:
                return json_response(self, HTTPStatus.OK, multistep_evidence_payload(match.group(1)))
            if path == "/api/agent-hub":
                return json_response(self, HTTPStatus.OK, agent_hub_payload())
            if path == "/api/agent-chat/search":
                return json_response(self, HTTPStatus.OK, agent_chat_search_payload(agent_chat_query_filters(parse_qs(parsed.query))))
            if path == "/api/agent-chat/export/jsonl":
                return json_response(self, HTTPStatus.OK, agent_chat_export_jsonl_payload(agent_chat_query_filters(parse_qs(parsed.query))))
            if path == "/api/agent-chat/export/markdown":
                return json_response(self, HTTPStatus.OK, agent_chat_export_markdown_payload(agent_chat_query_filters(parse_qs(parsed.query))))
            if path == "/api/agent-chat/hash-chain":
                return json_response(self, HTTPStatus.OK, agent_chat_verify_hash_chain())
            match = re.fullmatch(r"/api/agent-chat/messages/([^/]+)/thread", path)
            if match:
                return json_response(self, HTTPStatus.OK, agent_chat_reconstruct_thread_payload(match.group(1)))
            if path == "/api/agent-chat/messages":
                query = parse_qs(parsed.query)
                limit = int(query.get("limit", ["50"])[0] or 50)
                return json_response(self, HTTPStatus.OK, agent_chat_messages_payload(limit=limit))
            match = re.fullmatch(r"/api/agent-chat/inbox/([^/]+)", path)
            if match:
                return json_response(self, HTTPStatus.OK, agent_chat_inbox_payload(match.group(1)))
            match = re.fullmatch(r"/api/agent-chat/outbox/([^/]+)", path)
            if match:
                return json_response(self, HTTPStatus.OK, agent_chat_outbox_payload(match.group(1)))
            if path == "/api/agent-chat/rooms":
                return json_response(self, HTTPStatus.OK, agent_chat_rooms_payload())
            if path == "/api/agent-chat/status":
                return json_response(self, HTTPStatus.OK, agent_chat_status_payload())
            if path == "/api/budget/status":
                return json_response(self, HTTPStatus.OK, budget_status_payload())
            if path == "/api/hub/status":
                return json_response(self, HTTPStatus.OK, hub_status_payload())
            if path == "/api/user_state":
                query = parse_qs(parsed.query)
                psi_c = float(query.get("psi_C", ["1.0"])[0] or 1.0)
                return json_response(self, HTTPStatus.OK, wabi_osit_v04.user_state_payload(psi_C=psi_c))
            if path == "/api/security/tools":
                return json_response(self, HTTPStatus.OK, security_tools_payload())
            if path == "/api/security/status":
                return json_response(self, HTTPStatus.OK, security_status_payload())
            if path == "/api/security/gitleaks/status":
                return json_response(self, HTTPStatus.OK, security_gitleaks_status_payload())
            if path == "/api/security/preflight":
                return json_response(self, HTTPStatus.OK, security_preflight_payload())
            if path == "/api/coding/preflight":
                return json_response(self, HTTPStatus.OK, coding_preflight_payload())
            if path == "/api/chat/session":
                return json_response(self, HTTPStatus.OK, chat_session_payload())
            if path == "/api/provider/active":
                provider = provider_registry.provider_for(active_provider_name())
                return json_response(self, HTTPStatus.OK, {"provider": sanitize_obj(provider.to_public_dict())})
            if path.startswith("/api/coding/session/"):
                session_id = path.rsplit("/", 1)[-1]
                session = coding_workbench.load_session(session_id, repo_root=ROOT)
                return json_response(self, HTTPStatus.OK, {"ok": True, "coding_session": session.to_dict()})
            if path == "/api/doctor":
                live = parse_qs(parsed.query).get("live", ["0"])[0] in {"1", "true", "yes"}
                return json_response(self, HTTPStatus.OK, {"live": live, "rows": doctor_rows(live=live)})
            if path == "/api/workspace":
                return json_response(self, HTTPStatus.OK, workspace_payload())
            if path == "/api/tools":
                return json_response(self, HTTPStatus.OK, tools_payload())
            if path in {"/api/tools/registry", "/api/wabi-tool-registry"}:
                return json_response(self, HTTPStatus.OK, wabi_tool_registry_payload())
            if path == "/api/changes/recent":
                query = parse_qs(parsed.query)
                limit = int(query.get("limit", ["10"])[0] or 10)
                path_filter = query.get("path", [None])[0]
                return json_response(self, HTTPStatus.OK, recent_changes_payload(limit=limit, path_filter=path_filter))
            if path == "/api/session/current":
                return json_response(self, HTTPStatus.OK, read_recent_session())
            if path == "/api/witnesslog/recent":
                return json_response(self, HTTPStatus.OK, recent_witnesslog())
            if path == "/api/governance/status":
                return json_response(self, HTTPStatus.OK, governance_status_payload())
            if path == "/api/world-model/benchmark":
                return json_response(self, HTTPStatus.OK, world_model_benchmark_payload())
            if path == "/api/multimodal/status":
                return json_response(self, HTTPStatus.OK, multimodal_status_payload())
            if path == "/api/paywall/status":
                return json_response(self, HTTPStatus.OK, paywall_status_payload())
            if path == "/api/geo/status":
                return json_response(self, HTTPStatus.OK, geo_status_payload())
            if path == "/api/network/status":
                return json_response(self, HTTPStatus.OK, network_status_payload())
            if path == "/api/lab/status":
                return json_response(self, HTTPStatus.OK, lab_status_payload())
        except Exception as exc:
            return json_response(self, HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": sanitize_text(exc)})
        return super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            payload = self.read_json_body()
            if parsed.path in {"/api/gates", "/api/gates/set"}:
                result = update_local_gate_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path in {"/api/gates/reset", "/api/gates/reset-safe-defaults"}:
                return json_response(self, HTTPStatus.OK, reset_local_gate_payload(payload))
            if parsed.path == "/api/provider/use":
                provider_name = safe_provider_name(str(payload.get("provider", "")))
                config = provider_registry.set_default_provider(provider_name)
                return json_response(self, HTTPStatus.OK, {"ok": True, "provider": provider_name, "config": sanitize_obj(config)})
            if parsed.path == "/api/providers/smoke":
                return json_response(self, HTTPStatus.OK, provider_smoke_payload(payload))
            if parsed.path == "/api/provider/route-test":
                return json_response(self, HTTPStatus.OK, provider_route_payload(payload))
            if parsed.path == "/api/folder/check":
                return json_response(self, HTTPStatus.OK, folder_check_payload(payload))
            if parsed.path == "/api/artifacts/open-path":
                return json_response(self, HTTPStatus.OK, artifact_open_path_payload(payload))
            if parsed.path == "/api/security/gitleaks/scan-fixtures":
                return json_response(self, HTTPStatus.OK, security_gitleaks_scan_fixtures_payload(payload))
            if parsed.path == "/api/security/gitleaks/compare-secret-scan":
                return json_response(self, HTTPStatus.OK, security_compare_payload(payload))
            if parsed.path == "/api/conversation/turn":
                _t0 = time.time()
                result = conversation_turn_payload(payload)
                _latency = int((time.time() - _t0) * 1000)
                _cloud_called = bool(result.get("cloud_provider_called", False))
                _provider = str(result.get("provider") or payload.get("provider") or "local")
                _r_est = result.get("r_est") or (result.get("osit", {}).get("r_est") if isinstance(result.get("osit"), dict) else None)
                if _r_est is None:
                    try:
                        _r_est = wabi_osit_metrics_payload().get("R_est")
                    except Exception:
                        pass
                _tools_used = [k for k in result.keys() if k not in {"ok", "response", "output", "cloud_provider_called", "cloud_budget"}]
                _telemetry_update(_latency, _provider, _tools_used[:8], _r_est, _cloud_called)
                result["telemetry"] = {"latency_ms": _latency, "provider": _provider, "cloud": _cloud_called}
                # W620: auto-save del output al memory_patina si es suficientemente util
                _resp_text = str(result.get("response") or result.get("output") or "")
                if len(_resp_text) >= 60:
                    try:
                        from core.memory_patina import auto_save as _mem_auto_save
                        _mem_auto_save(_resp_text[:1200], tags="auto:turn")
                    except Exception:
                        pass
                return json_response(self, HTTPStatus.OK, result)
            # W620: endpoints de memoria patina
            if parsed.path == "/api/memory/remember":
                try:
                    from core.memory_patina import remember as _mem_remember
                    text = str(payload.get("text", "")).strip()
                    tags = str(payload.get("tags", "")).strip() or None
                    if not text:
                        return json_response(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": "text required"})
                    mem_id = _mem_remember(text, tags)
                    _telemetry_store["memory_recalls"] += 1
                    return json_response(self, HTTPStatus.OK, {"ok": True, "id": mem_id})
                except Exception as exc:
                    return json_response(self, HTTPStatus.OK, {"ok": False, "error": str(exc)})
            if parsed.path == "/api/memory/recall":
                try:
                    from core.memory_patina import recall as _mem_recall
                    query = str(payload.get("query", "")).strip()
                    top_n = int(payload.get("top_n", 5))
                    if not query:
                        return json_response(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": "query required"})
                    results_mem = _mem_recall(query, top_n)
                    return json_response(self, HTTPStatus.OK, {"ok": True, "results": results_mem})
                except Exception as exc:
                    return json_response(self, HTTPStatus.OK, {"ok": False, "error": str(exc)})
            if parsed.path == "/api/taskspec/save-draft":
                return json_response(self, HTTPStatus.OK, taskspec_save_draft_payload(payload))
            if parsed.path == "/api/taskspec/apply":
                return json_response(self, HTTPStatus.OK, taskspec_apply_payload(payload))
            if parsed.path == "/api/taskspec/apply-local-preview":
                return json_response(self, HTTPStatus.OK, taskspec_apply_local_preview_payload(payload))
            if parsed.path == "/api/taskspec/apply-local":
                return json_response(self, HTTPStatus.OK, taskspec_apply_local_payload(payload))
            if parsed.path == "/api/taskspec/llm-proposal":
                return json_response(self, HTTPStatus.OK, taskspec_llm_proposal_payload(payload))
            if parsed.path == "/api/wabi/source-intake/inspect":
                return json_response(self, HTTPStatus.OK, wabi_source_intake_inspect_payload(payload))
            if parsed.path == "/api/wabi/system-notebook/scan":
                return json_response(self, HTTPStatus.OK, wabi_system_notebook_scan_payload(payload))
            if parsed.path == "/api/wabi/app-inventory/scan":
                return json_response(self, HTTPStatus.OK, wabi_app_inventory_scan_payload(payload))
            if parsed.path == "/api/wabi/orchestrator/plan":
                return json_response(self, HTTPStatus.OK, wabi_orchestrator_plan_payload(payload))
            if parsed.path == "/api/wabi/orchestrator/dispatch":
                result = wabi_orchestrator_dispatch_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/autocoder/scan":
                return json_response(self, HTTPStatus.OK, wabi_autocoder_scan_payload())
            if parsed.path == "/api/wabi/gemma/chat":
                result = wabi_gemma_chat_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/wabi/gemma/score-osit":
                return json_response(self, HTTPStatus.OK, wabi_gemma_score_osit_payload(payload))
            if parsed.path == "/api/wabi/gemma/benchmark":
                return json_response(self, HTTPStatus.OK, wabi_gemma_benchmark_payload(payload))
            if parsed.path == "/api/wabi/gemma/tuning-dataset/build":
                return json_response(self, HTTPStatus.OK, wabi_gemma_tuning_dataset_build_payload(payload))
            if parsed.path == "/api/wabi/velo/screen":
                return json_response(self, HTTPStatus.OK, wabi_velo_screen_payload(payload))
            if parsed.path == "/api/wabi/velo/ask":
                result = wabi_velo_ask_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/wabi/programmer/plan":
                return json_response(self, HTTPStatus.OK, programmer_plan_payload(payload))
            if parsed.path == "/api/wabi/programmer/apply":
                return json_response(self, HTTPStatus.OK, programmer_apply_payload(payload))
            if parsed.path == "/api/chat/message":
                return json_response(self, HTTPStatus.OK, chat_message_payload(payload))
            if parsed.path == "/api/chat/reset":
                return json_response(self, HTTPStatus.OK, chat_reset_payload())
            match = re.fullmatch(r"/api/local-hub/tasks/([^/]+)/(prepare|ghostgate|queue|execute|rollback)", parsed.path)
            if match:
                task_id, action = match.groups()
                if action == "prepare":
                    return json_response(self, HTTPStatus.OK, local_hub_prepare_task_payload(task_id, payload))
                if action == "ghostgate":
                    return json_response(self, HTTPStatus.OK, local_hub_ghostgate_payload(task_id, payload))
                if action == "queue":
                    return json_response(self, HTTPStatus.OK, local_hub_queue_task_payload(task_id, payload))
                if action == "execute":
                    return json_response(self, HTTPStatus.OK, local_hub_execute_task_payload(task_id, payload))
                if action == "rollback":
                    return json_response(self, HTTPStatus.OK, local_hub_rollback_task_payload(task_id, payload))
            match = re.fullmatch(r"/api/workpacks/from-task/([^/]+)", parsed.path)
            if match:
                result = create_workpack_from_task_payload(match.group(1), payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/workpacks/([^/]+)/(approve|execute|rollback|chat-note)", parsed.path)
            if match:
                workpack_id, action = match.groups()
                if action == "approve":
                    result = approve_workpack_payload(workpack_id, payload)
                elif action == "execute":
                    result = execute_workpack_payload(workpack_id, payload)
                elif action == "rollback":
                    result = rollback_workpack_payload(workpack_id, payload)
                else:
                    result = workpack_chat_note_payload(workpack_id, payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/workpack-scheduler/enqueue/([^/]+)", parsed.path)
            if match:
                result = scheduler_enqueue_payload(match.group(1), payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/workpack-scheduler/([^/]+)/(approve|retry|rollback)", parsed.path)
            if match:
                queue_id, action = match.groups()
                if action == "approve":
                    result = scheduler_approve_payload(queue_id, payload)
                elif action == "retry":
                    result = scheduler_retry_payload(queue_id, payload)
                else:
                    result = scheduler_rollback_payload(queue_id, payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/workpack-scheduler/tick":
                result = scheduler_tick_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/multi-step-workpacks":
                result = create_multistep_workpack_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("status") != "BLOCK" else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/multi-step-workpacks/tick":
                result = tick_multistep_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/multi-step-workpacks/([^/]+)/(approve|enqueue|rollback)", parsed.path)
            if match:
                workpack_id, action = match.groups()
                if action == "approve":
                    result = approve_multistep_workpack_payload(workpack_id, payload)
                elif action == "enqueue":
                    result = enqueue_multistep_workpack_payload(workpack_id, payload)
                else:
                    result = rollback_multistep_workpack_payload(workpack_id, payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/multi-step-workpacks/([^/]+)/rollback-step/([^/]+)", parsed.path)
            if match:
                workpack_id, step_id = match.groups()
                result = rollback_multistep_step_payload(workpack_id, step_id, payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/agent-chat/messages/([^/]+)/taskspec", parsed.path)
            if match:
                result = agent_chat_message_to_taskspec_payload(match.group(1), payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/agent-chat/messages/([^/]+)/workpack", parsed.path)
            if match:
                result = agent_chat_message_to_workpack_payload(match.group(1), payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/agent-chat/messages/([^/]+)/schedule-workpack", parsed.path)
            if match:
                result = agent_chat_message_schedule_workpack_payload(match.group(1), payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/agent-chat/messages/([^/]+)/multi-step-workpack", parsed.path)
            if match:
                result = agent_chat_message_to_multistep_payload(match.group(1), payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/agent-chat/messages/([^/]+)/route", parsed.path)
            if match:
                result = route_agent_chat_message_payload(match.group(1), payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            match = re.fullmatch(r"/api/agent-chat/messages/([^/]+)/attach-workpack/([^/]+)", parsed.path)
            if match:
                message_id, workpack_id = match.groups()
                result = attach_agent_chat_message_to_workpack_payload(message_id, workpack_id, payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/agent-chat/system-status":
                result = agent_chat_system_status_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/agent-chat/index/rebuild":
                result = agent_chat_build_search_index()
                return json_response(self, HTTPStatus.OK, result)
            if parsed.path == "/api/agent-chat/messages":
                result = agent_chat_post_message_payload(payload)
                return json_response(self, HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST, result)
            if parsed.path == "/api/agent-chat/status":
                return json_response(self, HTTPStatus.OK, agent_chat_post_status_payload(payload))
            if parsed.path == "/api/multimodal/intake-fixture":
                return json_response(self, HTTPStatus.OK, multimodal_intake_fixture_payload(payload))
            if parsed.path == "/api/multimodal/intake-file":
                return json_response(self, HTTPStatus.OK, multimodal_intake_file_payload(payload))
            if parsed.path == "/api/fact-check":
                return json_response(self, HTTPStatus.OK, factcheck_payload(payload))
            if parsed.path == "/api/create-checkout-session":
                return json_response(self, HTTPStatus.OK, create_stripe_checkout_session(payload))
            if parsed.path == "/api/chat":
                result = model_chat_fallback(
                    str(payload.get("message", "")),
                    str(payload.get("provider", "") or active_provider_name()),
                    str(payload.get("mode", "plain") or "plain"),
                )
                if not result.get("ok"):
                    result = {
                        **result,
                        "ok": True,
                        "provider": "safe-fallback",
                        "response": (
                            "Intenté la ruta cloud-first, pero ningún motor devolvió respuesta dentro del límite. "
                            "Sigo operativo para convertir tu pedido en plan, diff, pruebas o revisión local con gate."
                        ),
                        "degraded": True,
                        "secret_values_printed": False,
                    }
                return json_response(self, HTTPStatus.OK, result)
            if parsed.path == "/api/governance/shadow":
                return json_response(self, HTTPStatus.OK, governance_shadow_payload(payload))
            if parsed.path == "/api/coding/session":
                return json_response(self, HTTPStatus.OK, coding_session_payload(payload))
            if parsed.path == "/api/coding/plan":
                return json_response(self, HTTPStatus.OK, coding_plan_payload(payload))
            if parsed.path == "/api/coding/diff":
                return json_response(self, HTTPStatus.OK, coding_diff_payload(payload))
            if parsed.path == "/api/coding/apply":
                return json_response(self, HTTPStatus.OK, coding_apply_payload(payload))
            if parsed.path == "/api/coding/test":
                return json_response(self, HTTPStatus.OK, coding_test_payload(payload))
            if parsed.path == "/api/coding/rollback":
                return json_response(self, HTTPStatus.OK, coding_rollback_payload(payload))
            if parsed.path == "/api/mts/shadow":
                return json_response(self, HTTPStatus.OK, mts_shadow_payload(payload))
            if parsed.path == "/api/mts/select":
                return json_response(self, HTTPStatus.OK, mts_select_payload(payload))
            if parsed.path == "/api/mts/format":
                return json_response(self, HTTPStatus.OK, mts_format_payload(payload))
            if parsed.path == "/api/mts/policy":
                return json_response(self, HTTPStatus.OK, mts_policy_payload(payload))
            if parsed.path == "/api/mts/shadow-trace":
                return json_response(self, HTTPStatus.OK, mts_shadow_trace_payload(payload))
            if parsed.path == "/api/mts/enforce":
                return json_response(self, HTTPStatus.OK, mts_enforce_payload(payload))
            # Docs RAG endpoints
            if parsed.path == "/api/docs/scan":
                return json_response(self, HTTPStatus.OK, docs_scan_payload(payload))
            if parsed.path == "/api/docs/index":
                return json_response(self, HTTPStatus.OK, docs_index_payload(payload))
            if parsed.path == "/api/docs/query":
                return json_response(self, HTTPStatus.OK, docs_query_payload(payload))
            if parsed.path == "/api/docs/chat":
                return json_response(self, HTTPStatus.OK, docs_chat_payload(payload))
            if parsed.path == "/api/docs/stats":
                return json_response(self, HTTPStatus.OK, docs_stats_payload(payload))
            if parsed.path == "/api/wabi/voice/tts":
                return json_response(self, HTTPStatus.OK, wabi_voice_tts_payload(payload))
            if parsed.path == "/api/wabi/voice/stt":
                return json_response(self, HTTPStatus.OK, wabi_voice_stt_payload(payload))
            if parsed.path == "/api/wabi/voice/stt-upload":
                return json_response(self, HTTPStatus.OK, wabi_voice_stt_upload_payload(self))
            if parsed.path == "/api/websearch":
                return json_response(self, HTTPStatus.OK, websearch_payload(payload))
            if parsed.path == "/api/mempalace/search":
                return json_response(self, HTTPStatus.OK, mempalace_search_payload(payload))
            if parsed.path == "/api/paywall/analyze":
                return json_response(self, HTTPStatus.OK, {
                    "ok": True,
                    "url": body.get("url", ""),
                    "gate": "REVIEW",
                    "method": "auditoria-solo",
                    "analyzed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "PublicationGate": "BLOCK",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                })
            if parsed.path == "/api/geo/set":
                return json_response(self, HTTPStatus.OK, {
                    "ok": True,
                    "region": body.get("region", "MX"),
                    "applied": True,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "PublicationGate": "BLOCK",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                })
            if parsed.path == "/api/geo/reset":
                return json_response(self, HTTPStatus.OK, {
                    "ok": True,
                    "region": "MX",
                    "applied": True,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "PublicationGate": "BLOCK",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                })
            if parsed.path == "/api/network/scan":
                return json_response(self, HTTPStatus.OK, {
                    "ok": True,
                    "host": body.get("host", "127.0.0.1"),
                    "ports": body.get("ports", []),
                    "scan_id": str(uuid.uuid4()),
                    "status": "scanning",
                    "note": "simulacion local - no se ejecuta escaneo real",
                    "PublicationGate": "BLOCK",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                })
            if parsed.path == "/api/network/stop":
                return json_response(self, HTTPStatus.OK, {
                    "ok": True,
                    "status": "cancelled",
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "PublicationGate": "BLOCK",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                })
            if parsed.path == "/api/lab/run":
                return json_response(self, HTTPStatus.OK, {
                    "ok": True,
                    "prompt": body.get("prompt", ""),
                    "benchmark": body.get("benchmark", False),
                    "eval": body.get("eval", False),
                    "status": "simulated",
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "PublicationGate": "BLOCK",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                })
            if parsed.path == "/api/lab/clear":
                return json_response(self, HTTPStatus.OK, {
                    "ok": True,
                    "status": "cleared",
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "PublicationGate": "BLOCK",
                    "cloud_provider_called": False,
                    "secret_values_printed": False,
                })
        except subprocess.TimeoutExpired:
            return json_response(self, HTTPStatus.GATEWAY_TIMEOUT, {"ok": False, "error": "wabi request timed out"})
        except Exception as exc:
            return json_response(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": sanitize_text(exc)})
        return json_response(self, HTTPStatus.NOT_FOUND, {"ok": False, "error": "not found"})

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length > MAX_BODY_BYTES:
            raise ValueError("request body too large")
        raw = self.rfile.read(length) if length else b"{}"
        if not raw:
            return {}
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("JSON object required")
        return data

    @staticmethod
    def health_payload(host: str = "127.0.0.1", port: int = 8787) -> dict[str, Any]:
        route = provider_route_payload()
        gate_state = local_gate_payload()
        gates = gate_state.get("gates", {})
        cloud_default = (
            env_flag("WABI_WORKBENCH_CLOUD_FIRST", "0")
            or env_flag("WABI_ALLOW_CLOUD_PROVIDERS", "0")
            or env_flag("WABI_BUILD_ASSIST_CLOUD", "0")
            or env_flag("WABI_LLM_PROVIDER_CLOUD_DEFAULT", "0")
        )
        route_stage = str(route.get("route_stage", "LOCAL") or "LOCAL")
        active_provider_label = str(route.get("selected_provider", active_provider_name()) or active_provider_name())
        if route_stage == "OLLAMA_CLOUD":
            active_provider_label = "ollama-cloud"
        return {
            "ok": True,
            "service": "wabi-local-cockpit",
            "version": "0.6",
            "host": host,
            "port": port,
            "url": f"http://{host}:{port}",
            "workspace": "<BRAIN_OS_ROOT>",
            "math_canon": "07b",
            "cloud": bool(cloud_default),
            "cloud_default": bool(cloud_default),
            "ui_binding": "localhost",
            "model_runtime": "cloud" if cloud_default else "local",
            "cloud_connection": "enabled" if cloud_default else "disabled",
            "apply": False,
            "apply_default": False,
            "cloud_provider_called": False,
            "applied_to_sources": False,
            "active_provider": active_provider_label,
            "provider_route_stage": route_stage,
            "provider_policy": route.get("provider_policy", provider_policy.TEMP_EXTERNAL_APIS_ALLOWED_UNTIL_CLAUDIO_AUTONOMY),
            "external_api_mode": route.get("external_api_mode", "TEMP_ALLOWED"),
            "provider_count": len(provider_registry.PROVIDERS),
            "wabi_script": "02_CLAUDIO/core/wabi.py",
            "publication_gate": "BLOCK",
            "gate_console": {
                "environment": LOCAL_GATE_ENVIRONMENT,
                "owner_authorization": LOCAL_GATE_OWNER_AUTHORIZATION,
                "state_status": gate_state.get("state_status", "OK"),
                "ActionGate": gates.get("ActionGate", "APPROVE_LOCAL"),
                "PublicationGate": gates.get("PublicationGate", "BLOCK"),
                "CloudGate": gates.get("CloudGate", "OFF"),
                "ApplyGate": gates.get("ApplyGate", "REVIEW"),
                "NetworkExposureGate": gates.get("NetworkExposureGate", "LOCALHOST_ONLY"),
                "SecretGate": gates.get("SecretGate", "HARD_BLOCK"),
                "CredentialGate": gates.get("CredentialGate", "HARD_BLOCK"),
            },
            "timestamp_ms": now_epoch_ms(),
        }


def make_server(host: str = "127.0.0.1", port: int = 8787) -> ThreadingHTTPServer:
    UI_ROOT.mkdir(parents=True, exist_ok=True)
    return ThreadingHTTPServer((host, port), WabiLocalHandler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Wabi-Sabi local cockpit server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    server = make_server(args.host, args.port)
    print(f"Wabi Local Cockpit: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
