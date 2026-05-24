# GITHUB OBSERVACIONISMO ATLAS 2026-05-16

Estado: `ATLAS_FICHADO_LOCAL`
Gate: `NO_INSTALL_NO_COPY_NO_PUBLICATION`
Scope: producto completo MEDIOEVO/CLAUDIO, con PoC aislada solamente.

## Resumen

Este atlas responde a la busqueda de proyectos/piezas de codigo en GitHub que
pueden servir a MEDIOEVO/CLAUDIO usando Observacionismo y Observacionismo
Inverso.

La conclusion operativa es:

- Si el repo reduce R, aumenta Phi_eff, mejora evidencia o baja riesgo de
  accion, entra como candidato.
- Hay dos carriles separados:
  - `USO_PERSONAL_LOCAL`: pragmatico para Luis/operador, puede usar herramientas
    externas si quedan aisladas y no se redistribuyen.
  - `PRODUCTO_PUBLICABLE`: mucho mas estricto; no acepta licencias ambiguas,
    AGPL embebida, secretos, red sin gate ni claims fuertes.
- Si el repo solo agrega autonomia, proveedores, nube o claims sin cierre, queda
  `IDEA_ONLY`, `REVIEW` o `PERSONAL_ONLY` segun el carril.
- Ningun repo queda adoptado. Ningun codigo externo fue copiado. Ninguna
  dependencia fue instalada.
- Las PoC deben usar fixtures sinteticos, rutas aisladas y salida escaneable.

## Carril Personal Pragmatico

Este carril no piensa primero en vender o publicar. Piensa en lo que te sirve a
ti para trabajar mejor en la PC, siempre que quede fuera de bundles publicos y
no toque secretos/sesiones sin gate.

| prioridad | herramienta | decision personal | para que te sirve a ti | limite |
|---:|---|---|---|---|
| 1 | [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | `PERSONAL_POC_NOW` | Revisar rapido carpetas/staging antes de compartir o zippear. | Solo targets focales; no workspace completo por ruido. |
| 2 | [trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) | `PERSONAL_TOOL_REVIEW` | Scanner fuerte para credenciales reales; util cuando sospechas leaks. | AGPL; no bundlear ni meter en producto. Ejecutar solo bajo pedido/foco. |
| 3 | [swarmclawai/swarmvault](https://github.com/swarmclawai/swarmvault) | `PERSONAL_POC_NOW` | Convertir documentos, repos publicos y notas en wiki/memoria local para investigacion propia. | No ingerir libros completos/private game ni secretos. |
| 4 | [agentmemory](https://github.com/jayzeng/agentmemory) | `PERSONAL_POC_SMALL` | Memoria markdown simple para Codex/Claude; puede servir como scratchpad operativo. | Baja madurez; comparar contra memoria actual antes de usar. |
| 5 | [memory-graph](https://github.com/memory-graph/memory-graph) | `PERSONAL_POC_NOW` | Recordar patrones, decisiones, relaciones y errores entre sesiones. | DB por proyecto, no memoria global sin frontera. |
| 6 | [Agent Replay](https://github.com/agentreplay/agentreplay) | `PERSONAL_ONLY_REVIEW` | Desktop local para ver trazas/memoria/evals de agentes. | AGPL; herramienta externa solamente, no producto. |
| 7 | [codex-mem](https://github.com/Just-Boring-Cat/codex-mem) | `PERSONAL_ONLY_REVIEW` | MCP SQLite para memoria de Codex. | AGPL y baja madurez; probar solo en sandbox/perfil separado. |
| 8 | [StackOne defender](https://github.com/StackOneHQ/defender) | `PERSONAL_POC_NOW` | Bloquear prompt injection en outputs de GitHub/docs/web antes de pasarlos al agente. | Solo fixture primero; no asumir seguridad total. |
| 9 | [pipelock](https://github.com/luckyPipewrench/pipelock) | `PERSONAL_POC_REVIEW` | Firewall/recibos para MCP y egress, muy util para acciones reales. | No interceptar sesiones reales hasta PoC seca. |
| 10 | [promptfoo](https://github.com/promptfoo/promptfoo) | `PERSONAL_POC_NOW` | Probar prompts, agents y RAG con red-team local antes de usarlos. | Sin API keys en configs; mock/local primero. |
| 11 | [noWorkflow](https://github.com/gems-uff/noworkflow) | `PERSONAL_POC_NOW` | Registrar provenance de scripts DUAT/GEODIA y experimentos propios. | Ejecutar en temp; no tocar pipelines activos primero. |
| 12 | [Agentify Desktop](https://github.com/agentify-sh/desktop) | `PERSONAL_ONLY_HIGH_RISK` | Controlar sesiones web de ChatGPT/Claude/Gemini desde Codex/Claude. | Muy util pero riesgoso: sesiones logueadas, uploads y browser automation siempre `REVIEW`. |
| 13 | [Thoth](https://github.com/siddsachar/Thoth) | `PERSONAL_IDEA_POC` | Asistente local-first tipo soberania personal con tools/memoria/Ollama. | No reemplazar Claudio; revisar permisos, shell y browser automation. |
| 14 | [Open-Sable](https://github.com/IdeoaLabs/Open-Sable) | `PERSONAL_IDEA_POC` | Ideas de perfiles/agentes locales con memoria y permisos. | Autonomia continua/chat integrations quedan gateadas. |
| 15 | [swarmclaw](https://github.com/swarmclawai/swarmclaw) | `PERSONAL_IDEA_ONLY` | Runtime self-hosted con memoria, MCP y skills; util para comparar. | No migrar Claudio; solo estudiar patrones. |

Lectura practica: para ti, los primeros cierres reales son `gitleaks`,
`swarmvault/memory-graph`, `defender`, `promptfoo` y `noWorkflow`. Lo demas se
puede investigar, pero no debe abrir otra plataforma paralela sin necesidad.

## Metodo

### Observacionismo directo

Para cada repo:

```yaml
sistema: repo GitHub externo
input: README, metadata GitHub, licencia, actividad, permisos requeridos
transformaciones: que operacion ejecuta realmente
output: pieza util para MEDIOEVO/CLAUDIO
residuo_R: complejidad, licencia, secretos, red, vendor lock-in, claims
gates: ActionGate, SecretScan, LicenseReview, BoundaryCheck, ClaimGate
evidencia: URL + metadata consultada 2026-05-16
falsadores: condiciones que lo bloquean
riesgo: low|medium|high|block
```

### Observacionismo inverso

Output deseado:

```yaml
estado_deseado: producto completo local-first con memoria, evidencia,
  ActionGate, sandbox, UI de trazas, seguridad de tool calls, PoC y release
  public-safe por allowlist
faltantes:
  - memoria durable verificable
  - trazas y WitnessLog consultables
  - defensa contra prompt injection indirecta
  - egress/tool firewall con recibos
  - sandbox local/aislado para PoC
  - provenance reproducible para scripts DUAT/GEODIA
  - licencia/secret scan mas fuerte para intake
contratos:
  - no instalar sin ficha
  - no copiar codigo externo a producto
  - no publicar ni empujar
  - no tocar RPG/TCG/canon privado
validacion:
  - PoC aislada
  - scans
  - reporte con decision
handoff: este atlas
```

## Decisiones Rapidas

| decision | significado |
|---|---|
| `CANDIDATE_POC` | Vale una prueba aislada con fixtures sinteticos. |
| `CANDIDATE_POC_WSL` | Vale solo si corre en WSL/Linux o sandbox separado. |
| `PERSONAL_ONLY` | Puede usarse como herramienta local externa para Luis, pero no entra a producto ni release. |
| `PERSONAL_TOOL_REVIEW` | Util para uso propio, pero requiere foco/gate por permisos o licencia. |
| `IDEA_ONLY` | Leer patrones, no instalar ni bundlear. |
| `REVIEW_LICENSE` | Licencia GitHub `NOASSERTION` o ambigua; no usar hasta revisar. |
| `BLOCK_FOR_BUNDLE` | No entra a productos/release propios por licencia o blast radius. |
| `BLOCK_RUNTIME` | No se usa como runtime activo por riesgo de autonomia/acciones. |

## Top P0 Para PoC Aislada

Estos son los candidatos con mejor relacion utilidad/riesgo para el siguiente
ciclo. Ordenados por cierre local verificable.

| prioridad | repo | decision | pieza util | PoC aislada |
|---:|---|---|---|---|
| 1 | [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | `CANDIDATE_POC` | Secret scan externo sobre staging/release, complementario a `tools/release/scan_secrets.py`. | Correr contra carpeta fixture con falso secreto sintetico y contra un paquete public-safe pequeno. |
| 2 | [StackOneHQ/defender](https://github.com/StackOneHQ/defender) | `CANDIDATE_POC` | Defensa contra prompt injection escondida en resultados de herramientas MCP/Docs/GitHub. | Fixture TS con tool result malicioso y salida `allowed=false`; sin red. |
| 3 | [open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification) + [opentelemetry-python](https://github.com/open-telemetry/opentelemetry-python) | `CANDIDATE_POC` | Contrato estandar para traducir `ObservationEnvelope`/WitnessLog a spans locales. | Exportador local JSON/console de 3 eventos sinteticos; sin backend externo. |
| 4 | [gems-uff/noworkflow](https://github.com/gems-uff/noworkflow) | `CANDIDATE_POC` | Provenance de scripts Python para DUAT/GEODIA sin reescribir experimentos. | Ejecutar sobre script toy en temp y verificar grafo/provenance exportado. |
| 5 | [swarmclawai/swarmvault](https://github.com/swarmclawai/swarmvault) | `CANDIDATE_POC` | Wiki/memoria local-first, raw/wiki/state, encaja con Biblioteca de Alejandria y Curador. | Ingesta de 3 markdown sinteticos fuera del repo; verificar que no modifica fuentes. |
| 6 | [memory-graph/memory-graph](https://github.com/memory-graph/memory-graph) | `CANDIDATE_POC` | Memoria MCP graph/SQLite para agentes, mas simple que Neo4j. | Guardar 5 memorias sinteticas y recuperar relacion; DB en temp. |
| 7 | [evilmartians/agent-prism](https://github.com/evilmartians/agent-prism) | `CANDIDATE_POC` | Componentes React para visualizar trazas de agentes; util para Argus/telecom. | Render fixture de spans JSON, sin conectar runtime real. |
| 8 | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | `CANDIDATE_POC` | Red-team/evals para prompts, RAG y agentes. | Suite local con 3 prompts public-safe y proveedor mock/local, sin claves. |
| 9 | [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) | `CANDIDATE_POC` | Scanner para skills/MCP/package hallucination/prompt injection. | Modo audit sobre skill fixture; `auto-fix` bloqueado. |
| 10 | [anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime) | `CANDIDATE_POC_WSL` | Restricciones filesystem/network para procesos de agente. | Solo WSL/Linux/macOS; probar deny network + read-only temp. |

## Atlas Fichado

### Memoria, Knowledge Graph, Curador

| repo | metadata 2026-05-16 | DO/OE/IOE fit | decision | falsador |
|---|---|---|---|---|
| [swarmclawai/swarmvault](https://github.com/swarmclawai/swarmvault) | MIT, activo, TS, 454 stars, pushed 2026-05-11 | IOE fuerte: raw/wiki/state se parece a canon curado + memoria durable. | `CANDIDATE_POC` | Si modifica fuentes raw, exige nube o mezcla secretos en wiki: `BLOCK`. |
| [doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service) | Apache-2.0, activo, Python, 1851 stars, pushed 2026-05-16 | Memoria compartida REST/MCP; util para COMMS si queda local. | `CANDIDATE_POC` | Si requiere OAuth/remote para el valor basico o expone memoria fuera de localhost: `REVIEW`. |
| [memory-graph/memory-graph](https://github.com/memory-graph/memory-graph) | MIT, activo, Python, 201 stars, pushed 2026-02-12 | Graph MCP pequeno para patrones/decisiones; encaja con memoria de agentes. | `CANDIDATE_POC` | Si la DB no es portable o no se puede aislar por proyecto: `IDEA_ONLY`. |
| [rendro/sediment](https://github.com/rendro/sediment) | MIT, activo, Rust, 32 stars, pushed 2026-03-30 | Memoria local MCP-native con embeddings locales; posible alternativa pequena. | `CANDIDATE_POC` | Si descarga modelos o escribe fuera de temp sin control: `REVIEW`. |
| [jayzeng/agentmemory](https://github.com/jayzeng/agentmemory) | MIT, activo, TS, 2 stars, pushed 2026-04-06 | Encaje directo con Codex/Claude memory; baja madurez. | `IDEA_ONLY_OR_POC_SMALL` | Si no aporta mas que la memoria actual de Codex: descartar. |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | Apache-2.0, activo, Python, 203 stars, pushed 2026-05-16 | Graph memory robusta; puede servir a BRAIN_OS v3. | `IDEA_ONLY` | Neo4j/FastAPI/Next stack sube R y operaciones; no usar en P0 local. |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | Apache-2.0, activo, Python, 55k stars, pushed 2026-05-16 | Universal memory layer; alto valor conceptual. | `IDEA_ONLY` | Si requiere servicios externos o almacenes cloud para valor real: no integrar. |
| [Just-Boring-Cat/codex-mem](https://github.com/Just-Boring-Cat/codex-mem) | AGPL-3.0, activo, TS, 3 stars, pushed 2026-05-14 | Codex memory SQLite, idea cercana al objetivo. | `BLOCK_FOR_BUNDLE` | AGPL bloquea bundle comercial/open-dev propio; solo referencia. |

### Observabilidad, WitnessLog, UI de Trazas

| repo | metadata 2026-05-16 | DO/OE/IOE fit | decision | falsador |
|---|---|---|---|---|
| [open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification) | Apache-2.0, activo, 4238 stars, pushed 2026-05-15 | Estandar para no inventar formato de trazas. | `CANDIDATE_POC` | Si obliga backend externo: usar solo schema/local export. |
| [open-telemetry/opentelemetry-python](https://github.com/open-telemetry/opentelemetry-python) | Apache-2.0, activo, Python, 2446 stars, pushed 2026-05-15 | Instrumentacion Python para `ObservationEnvelope`/WitnessLog. | `CANDIDATE_POC` | Si la instrumentacion contamina runtime Claudio: wrapper externo. |
| [future-agi/traceAI](https://github.com/future-agi/traceAI) | Apache-2.0, activo, Python, 181 stars, pushed 2026-05-15 | AI tracing sobre OpenTelemetry; util como comparador. | `CANDIDATE_POC` | Si depende de vendor/backends remotos: `IDEA_ONLY`. |
| [traceloop/openllmetry](https://github.com/traceloop/openllmetry) | Apache-2.0, activo, Python, 7115 stars, pushed 2026-05-14 | Observabilidad LLM madura; posible inspiracion. | `IDEA_ONLY_OR_POC` | Mucho peso/transitivos; PoC solo si se limita a export local. |
| [evilmartians/agent-prism](https://github.com/evilmartians/agent-prism) | MIT, activo, TS, 343 stars, pushed 2026-04-14 | UI React para traza jerarquica; encaja con `/telecom` y Argus. | `CANDIDATE_POC` | Si exige cambiar el stack UI activo: no integrar, solo adapter. |
| [Rxflex/agenttrace](https://github.com/Rxflex/agenttrace) | MIT, activo, Python, 6 stars, pushed 2026-05-07 | Debugger local-first minimal para agentes. | `IDEA_ONLY_OR_POC_SMALL` | Baja madurez; si no hay tests/docs suficientes, queda idea. |
| [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | `NOASSERTION`, activo, Python, 9705 stars, pushed 2026-05-16 | Observability/evals robusto. | `REVIEW_LICENSE` | Licencia no resuelta por GitHub API; no usar hasta revisar manualmente. |
| [agentreplay/agentreplay](https://github.com/agentreplay/agentreplay) | AGPL-3.0, activo, Rust, 9 stars, pushed 2026-03-21 | Idea muy alineada: local-first desktop evals/memory/traces. | `BLOCK_FOR_BUNDLE` | AGPL; solo lectura de patrones o herramienta externa separada. |

### Seguridad, SecretScan, Prompt Injection, MCP Firewall

| repo | metadata 2026-05-16 | DO/OE/IOE fit | decision | falsador |
|---|---|---|---|---|
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | MIT, activo, Go, 27k stars, pushed 2026-05-13 | Mejorar gate de secretos, especialmente historial/staging. | `CANDIDATE_POC` | Si genera falsos positivos inmanejables sin baseline: usar solo target focal. |
| [StackOneHQ/defender](https://github.com/StackOneHQ/defender) | Apache-2.0, activo, TS, 97 stars, pushed 2026-05-14 | Defensa tool-result injection para MCP/GitHub/docs/email. | `CANDIDATE_POC` | Si el modelo ONNX no es auditable o mete latencia/riesgo: `IDEA_ONLY`. |
| [luckyPipewrench/pipelock](https://github.com/luckyPipewrench/pipelock) | Apache-2.0, activo, Go, 588 stars, pushed 2026-05-16 | Firewall MCP/egress con recibos firmados; muy alineado a ActionGate. | `CANDIDATE_POC` | Si requiere interceptar red real o credenciales: PoC fixture solamente. |
| [protectai/llm-guard](https://github.com/protectai/llm-guard) | MIT, activo, Python, 2956 stars, pushed 2025-12-15 | Sanitizers/scanners para LLM IO. | `CANDIDATE_POC` | Si requiere modelos pesados o baja precision: `IDEA_ONLY`. |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | MIT, activo, TS, 21k stars, pushed 2026-05-16 | Red-team/evals para prompts/agentes; util para public-safe claims. | `CANDIDATE_POC` | Si necesita claves proveedor o cloud para pruebas: usar mock/local o bloquear. |
| [Giskard-AI/giskard-oss](https://github.com/Giskard-AI/giskard-oss) | Apache-2.0, activo, Python, 5352 stars, pushed 2026-05-16 | Testing LLM/agent: hallucination, prompt injection, leakage. | `CANDIDATE_POC` | Si dependencia es pesada para local P0: `IDEA_ONLY`. |
| [sinewaveai/agent-security-scanner-mcp](https://github.com/sinewaveai/agent-security-scanner-mcp) | MIT, activo, JS, 101 stars, pushed 2026-05-12 | Seguridad para skills/MCP/package hallucination. | `CANDIDATE_POC` | `auto-fix` bloqueado; solo audit. |
| [trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) | AGPL-3.0, activo, Go, 26k stars, pushed 2026-05-15 | Secret scanning fuerte. | `BLOCK_FOR_BUNDLE` | AGPL bloquea bundle; puede usarse solo como herramienta externa separada si se aprueba. |
| [oktsec/oktsec](https://github.com/oktsec/oktsec) | Apache-2.0, activo, Go, 11 stars, pushed 2026-05-13 | Firma/inspeccion/log para agent-to-agent; alinea con COMMS. | `IDEA_ONLY_OR_POC` | Madurez baja; no usar en hot path sin pruebas. |

### Sandboxes y Ejecucion Controlada

| repo | metadata 2026-05-16 | DO/OE/IOE fit | decision | falsador |
|---|---|---|---|---|
| [anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime) | Apache-2.0, activo, TS, 4064 stars, pushed 2026-05-13 | Sandbox OS-level sin container; ideal para ActionGate local si host compatible. | `CANDIDATE_POC_WSL` | No es Windows nativo; si exige bypass de controles host: `BLOCK`. |
| [sandbox0-ai/sandbox0](https://github.com/sandbox0-ai/sandbox0) | Apache-2.0, activo, Go, 34 stars, pushed 2026-05-16 | Sandboxes persistentes con network policy. | `CANDIDATE_POC` | Cloud/API keys bloqueados; self-host o fixture local solamente. |
| [agent-sandbox/agent-sandbox](https://github.com/agent-sandbox/agent-sandbox) | Apache-2.0, activo, Go, 123 stars, pushed 2026-05-14 | Sandbox E2B-compatible para agentes. | `IDEA_ONLY_OR_POC` | Kubernetes/E2B/infra pesada sube R; no P0. |
| [synth-laboratories/Horizons](https://github.com/synth-laboratories/Horizons) | `NOASSERTION`, activo, Rust, 77 stars, pushed 2026-04-20 | Agents propose actions + approval gates + append-only log. | `REVIEW_LICENSE` | Licencia no resuelta; no integrar. |

### Provenance, Licencias, Benchmarks y Research Ops

| repo | metadata 2026-05-16 | DO/OE/IOE fit | decision | falsador |
|---|---|---|---|---|
| [gems-uff/noworkflow](https://github.com/gems-uff/noworkflow) | MIT, activo, Python/Jupyter, 124 stars, pushed 2026-05-01 | Provenance de scripts sin workflow manager; encaja con DUAT/GEODIA. | `CANDIDATE_POC` | Si no corre en Windows o ensucia scripts: usar temp/WSL. |
| [provena/provena](https://github.com/provena/provena) | `NOASSERTION`, activo, Python, 7 stars, pushed 2026-05-13 | Provenance para modelado/simulacion; idea de schema. | `REVIEW_LICENSE` | Stack microservicios/nube o licencia ambigua: no adoptar. |
| [fossology/fossology](https://github.com/fossology/fossology) | GPL-2.0, activo, 986 stars, pushed 2026-05-14 | Compliance licencias. | `IDEA_ONLY_STANDALONE` | GPL y stack pesado; no bundle, solo referencia/herramienta externa. |
| [aboutcode-org/scancode-toolkit](https://github.com/aboutcode-org/scancode-toolkit) | `NOASSERTION`, activo, Python, 2530 stars, pushed 2026-05-15 | License/copyright/dependency scan. | `REVIEW_LICENSE` | GitHub API no resolvio licencia; revisar antes de uso. |
| [aiming-lab/ClawArena](https://github.com/aiming-lab/ClawArena) | MIT, activo, Python, 47 stars, pushed 2026-05-15 | Benchmark multi-sesion para agentes; util como patron de tests. | `IDEA_ONLY` | No instalar suites enormes; extraer ideas de escenarios. |
| [claw-bench/claw-bench](https://github.com/claw-bench/claw-bench) | Apache-2.0, activo, Python, 168 stars, pushed 2026-04-08 | Benchmark/verificadores para agentes. | `IDEA_ONLY` | No enviar resultados externos ni usar leaderboard. |
| [InternLM/WildClawBench](https://github.com/InternLM/WildClawBench) | MIT, activo, Python, 371 stars, pushed 2026-05-15 | Eval end-to-end realista; privacidad/leak tests interesantes. | `IDEA_ONLY` | No ejecutar tareas con dependencias/red sin gate. |
| [sourcegraph/CodeScaleBench](https://github.com/sourcegraph/CodeScaleBench) | Apache-2.0, activo, 21 stars, pushed 2026-04-04, 2.5GB | Benchmark contexto externo/codigo grande. | `IDEA_ONLY` | Tamano enorme; no clonar en PC real. |
| [Vexp-ai/vexp-swe-bench](https://github.com/Vexp-ai/vexp-swe-bench) | MIT, activo, 8 stars, pushed 2026-05-02 | Comparativa costo/resolucion coding agents. | `IDEA_ONLY` | Requiere licencia/servicio para valor completo; no ejecutar. |

### Runtimes de Agentes, Browser y Gateways

| repo | metadata 2026-05-16 | DO/OE/IOE fit | decision | falsador |
|---|---|---|---|---|
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | Apache-2.0, activo, Python, 25k stars, pushed 2026-05-15 | Patrones de agentes observables/confiables. | `CANDIDATE_POC_AFTER_SECURITY_REVIEW` | Si implica reemplazar Claudio runtime: `IDEA_ONLY`. |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | MIT, activo, Python/.NET, 10k stars, pushed 2026-05-15 | Orquestacion y workflows multi-agent; referencia industrial. | `IDEA_ONLY_OR_POC` | Azure/Foundry/cloud no entra al core local-first. |
| [swarmclawai/swarmclaw](https://github.com/swarmclawai/swarmclaw) | MIT, activo, TS, 486 stars, pushed 2026-05-15 | Runtime self-hosted con memoria/MCP/skills. | `IDEA_ONLY` | Reemplazar Claudio por otro runtime sube R; solo patrones. |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | MIT, activo, Python, 94k stars, pushed 2026-05-15 | Browser automation para agentes. | `CANDIDATE_POC_AFTER_SECURITY_REVIEW` | Browser actions siempre `REVIEW`; no credenciales ni sesiones privadas. |
| [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) | Apache-2.0, activo, Python, 27k stars, pushed 2026-04-16 | Research agent; util para metodologia de reportes. | `IDEA_ONLY` | Autonomous web research con red/proveedores queda gated. |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | `NOASSERTION`, activo, Python, 73k stars, pushed 2026-05-16 | Coding agent runtime grande. | `REVIEW_LICENSE_IDEA_ONLY` | No vendorizar ni ejecutar como runtime alterno sin aislamiento. |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | `NOASSERTION`, activo, Python, 47k stars, pushed 2026-05-16 | Gateway/proxy multi-provider. | `REVIEW_LICENSE_IDEA_ONLY` | Proveedores/API keys/secret handling: no integrar sin gate propio. |

## PoC Aisladas Propuestas

### POC-01 SecretScan externo

Objetivo: comparar scanner local con Gitleaks sin exponer secretos.

```powershell
# Preparar carpeta temporal con archivo fixture sintetico.
# Ejecutar gitleaks solo sobre esa carpeta y luego sobre un staging public-safe pequeno.
# No usar workspace completo.
```

Criterio:

- PASS si detecta secreto sintetico y no reporta secretos en staging limpio.
- REVIEW si produce ruido no triageable.

### POC-02 ToolResult Injection Guard

Objetivo: evaluar `defender` contra payloads indirectos antes de pasar outputs a
un LLM.

Criterio:

- PASS si bloquea payloads tipo "ignore previous instructions" en campos `body`,
  `description`, `message`.
- BLOCK si requiere enviar contenido a un servicio externo.

### POC-03 ObservationEnvelope a OpenTelemetry

Objetivo: convertir eventos existentes (`ActionGate`, `WitnessLog`,
`ObservationEnvelope`) a spans locales.

Criterio:

- PASS si genera JSON/console spans sin red y sin backend.
- REVIEW si necesita Jaeger/Grafana/servicio para funcionar.

### POC-04 Provenance Python con noWorkflow

Objetivo: capturar provenance de un script toy parecido a DUAT sin modificar el
script fuente.

Criterio:

- PASS si produce artefacto provenance exportable y reproducible.
- REVIEW si no funciona en Windows o requiere cambios invasivos.

### POC-05 Memoria local comparativa

Objetivo: comparar SwarmVault, MemoryGraph y Sediment con 5 documentos
sinteticos, no con corpus privado.

Criterio:

- PASS si indexa, recupera y no modifica fuentes.
- REVIEW si requiere modelos, servicios o escribe fuera de carpeta temporal.

## Linea Roja

No adoptar ni copiar directamente:

- AGPL en productos: `agentreplay`, `codex-mem`, `trufflehog`.
- Licencia `NOASSERTION` hasta revision manual: `Phoenix`, `LiteLLM`,
  `OpenHands`, `Horizons`, `Provena`, `ScanCode`.
- Runtimes completos que compitan con Claudio sin contrato de interfaz.
- Browser automation sobre sesiones privadas.
- Cualquier pieza que requiera API keys o nube para la PoC basica.
- Cualquier pieza que toque RPG/TCG, libros completos, runtime privado o
  secrets/sesiones locales.

## Proxima Accion Verificable

`POC-01 SecretScan externo / Gitleaks` ya fue ejecutada como PoC aislada con
fixtures sinteticos.

La siguiente accion verificable es una de estas dos:

- Reabrir `POC-01` solo si existe un binario local/portable aprobado de
  Gitleaks, sin instalacion global ni clone.
- Ejecutar `POC-02 ToolResult Injection Guard` con `StackOneHQ/defender` sobre
  fixtures sinteticos, sin red ni integracion de producto.

## POC-01 Gitleaks Local Synthetic Scan

Fecha: 2026-05-16

Ruta PoC:
`qa_artifacts/security_poc/POC-01_GITLEAKS_LOCAL_SYNTHETIC_SCAN_2026-05-16/`

Estado: `PASS_WITH_GITLEAKS_SKIPPED`

Resultado:

- `gitleaks` no esta en PATH.
- No se encontro binario portable bajo `tools/` ni `qa_artifacts/`.
- No se instalo globalmente.
- No se clono repo externo.
- No se copio codigo externo.
- No se escaneo material privado amplio.
- Se crearon 5 fixtures sinteticos marcados como no reales.
- `tools/release/scan_secrets.py` corrio solo contra la carpeta de fixtures y
  reporto 1 finding de nivel ruta por `denylist path`.
- El scanner minimo auxiliar encontro 7 patrones sinteticos con valores
  redactados.

Decision:

- `USO_PERSONAL_LOCAL`: `REVIEW_LOCAL_TOOL`. Gitleaks sigue siendo buen
  candidato pragmatico, pero falta binario local aprobado.
- `PRODUCTO_PUBLICABLE`: `REVIEW`. No hay inclusion en producto, bundle,
  release ni workflow publico.

Artefactos:

- `reports/gitleaks_report.json`
- `reports/medioevo_scan_secrets_report.json`
- `reports/medioevo_secret_scan_minimal.json`
- `reports/POC-01_GITLEAKS_COMPARISON_REPORT.md`
- `reports/POC-01_GITLEAKS_COMPARISON_REPORT.json`
- `reports/QA_SUMMARY.json`
- `reports/HASHES_SHA256.csv`

## Fuentes Consultadas

- GitHub REST API `https://api.github.com/repos/{owner}/{repo}` consultado el
  2026-05-16 para metadata de repos.
- Busqueda web/GitHub sobre memoria local, MCP, observabilidad, sandboxes,
  prompt injection, provenance, compliance y benchmarks de agentes.
- Canon local: `MEDIOEVO_OBSERVACIONISMO_MASTER/07_OBSERVACIONISMO.md`,
  `08_OBSERVACIONISMO_INVERSO.md`, `17_FALSADORES_Y_TESTS.md`.
- Gate local: `docs/developer/DEPENDENCY_ADOPTION_GATE_2026-05-02.md`.

## POC-01 Gitleaks Portable Local Rerun

- Fecha: 2026-05-16
- PoC: $poc
- Binario: $(@{available=True; binary_path=C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\tools\security\gitleaks\gitleaks.exe; binary_sha256=17157e2ee8b76fc8b1d8bee607a250e34b8a8023c8bc81822d4b5ee4d78fcb7c; install_mode=PORTABLE_LOCAL; ok=True; product_publication=REVIEW_OR_BLOCK; publication_gate=BLOCK; secret_values_printed=False; status=ADOPT_LOCAL_TOOL; version=8.30.1}.binary_path)
- Version: 8.30.1
- Checksum: MATCHED_OFFICIAL_RELEASE_ASSET_SHA256
- Resultado: Gitleaks findings 0 sobre fixtures sinteticos; MEDIOEVO minimal findings 7.
- USO_PERSONAL_LOCAL: ADOPT_LOCAL_TOOL como herramienta externa local.
- PRODUCTO_PUBLICABLE: REVIEW_OR_BLOCK, no bundle, no distribucion.
- PublicationGate: BLOCK.


## WABI/Claudio Final Stabilization v0.6

- Fecha: 2026-05-16T17:15:16-06:00
- Gitleaks: APPROVE_LOCAL_TOOL para USO_PERSONAL_LOCAL.
- Producto publicable: REVIEW_OR_BLOCK; no bundle, no publicacion, no distribucion.
- Security parity: Gitleaks 23 / MEDIOEVO 23 / missed_by_gitleaks [].
- PublicationGate: BLOCK.
