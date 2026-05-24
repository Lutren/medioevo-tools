# AI Framework Comparison

Fecha: 2026-05-12

Objetivo: comparar patrones externos actuales y traducirlos a MEDIOEVO MessageBus sin copiar complejidad innecesaria.

## Fuentes primarias verificadas

- Claude Code docs: subagents, skills, hooks, MCP, project memory.
  - https://code.claude.com/docs/en/features-overview
  - https://code.claude.com/docs/en/sub-agents
- OpenAI Agents SDK docs:
  - https://developers.openai.com/api/docs/guides/agents
- Google ADK docs:
  - https://adk.dev/sessions/
  - https://adk.dev/sessions/memory/
  - https://adk.dev/events/
  - https://adk.dev/artifacts/
- Microsoft Agent Framework docs:
  - https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/handoff
  - https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/group-chat
  - https://learn.microsoft.com/en-us/agent-framework/journey/agent-to-agent
- LangGraph docs:
  - https://docs.langchain.com/oss/python/langgraph/durable-execution
- CrewAI docs:
  - https://docs.crewai.com/en/index
- MCP docs:
  - https://modelcontextprotocol.io/docs/develop/build-server
  - https://modelcontextprotocol.io/docs/sdk
- A2A docs:
  - https://a2a-protocol.org/latest/specification/

## Comparacion

| Framework | Que tomamos | Que no tomamos | Traduccion MEDIOEVO |
|---|---|---|---|
| Claude Code | Subagents con herramientas limitadas, skills como conocimiento reusable, hooks para eventos, MCP como conectores y memoria de proyecto | Spawn paralelo automatico sin autorizacion explicita; subagents escribiendo sin ownership | `AgentRecord.capabilities`, canales por rol, `WitnessLog` para hooks, skills como docs de protocolo |
| OpenAI Agents SDK | Handoffs, guardrails/human review, tracing, tools y resultados de estado | Llamadas remotas obligatorias o tracing externo como unico ledger | `handoff_fingerprint`, `Security Review Channel`, `WitnessEvent`, funciones mock locales |
| Google ADK | Sessions, memory, artifacts y event stream con acciones/estado | Memory cloud por defecto o ingestion opaca | `thread_id`, `evidence_refs`, `artifact_refs`, `WitnessLog Stream` |
| Microsoft Agent Framework | Handoff orchestration, Group Chat orchestration, A2A, MCP, checkpointing/HITL | Mesh completo o coordinador pesado en Run 2 | `#handoffs` para handoff directo, `#system_announcements` para group broadcast, ActionGate para HITL |
| LangGraph | Durable execution, persistence, replay/resume, human-in-the-loop | Grafos complejos antes de ledger estable | JSONL/SQLite append-only futuro, `prev_hash`, reanudacion por fingerprint |
| CrewAI | Crews por rol, Flows con estado, guardrails, observability | Autonomia amplia sin evidencia; crews como verdad paralela | Agentes minimos por rol + Task Queue + Operator Console |
| MCP | Resources, tools, prompts, SDKs oficiales | Tools con permisos amplios o logs a stdout en stdio | `resources`: canales/artefactos; `tools`: ack/resolve/create; `prompts`: bulletin/handoff templates |
| A2A | Agent Cards, tasks, messages, artifacts, streaming/push como extension | Descubrimiento remoto publico en Run 2 | Agent Cards locales futuras; `AgentMessage` como base de message/task interop |

## Conclusion

Tomamos:

- Mensajes tipados.
- Handoffs con ownership claro.
- Canales como recursos.
- WitnessLog append-only.
- Guardrails/HITL para acciones de riesgo.
- Artifacts como referencias, no como contenido gigante.
- Export Markdown/JSON local.

No tomamos:

- Backend externo.
- Public discovery.
- Credenciales.
- Red.
- Autonomia amplia sin rollback/evidencia.
- Extraccion de ZIP reconstructivo.
- Publicacion o deploy.

Traduccion a MEDIOEVO:

DUAT Telecom Core debe ser primero un bus vivo local, no una plataforma distribuida publica. La unidad canonica es `AgentMessage`; la unidad de cierre es `WitnessEvent`; la unidad de continuidad es `handoff_fingerprint`. A2A y MCP entran como adaptadores de frontera cuando el ledger local ya sea verificable.
