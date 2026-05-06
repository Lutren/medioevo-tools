# DEPENDENCY_ADOPTION_GATE_2026-05-02

Decision aplicada: `Ficha antes de instalar`.

Ninguna dependencia externa nueva se instala, copia, vende o bundlea por defecto. Primero se registra, se revisa y se prueba aislada.

## Ficha obligatoria

| campo | requisito |
|---|---|
| name/repo | nombre, URL, version/tag o commit si aplica |
| license | SPDX o `NOASSERTION`; si es AGPL/copyleft fuerte, bloquear bundling comercial hasta revision |
| status | activo, archived, disabled, pushed_at, issues, maintainer risk |
| value | que aporta al producto y que problema real resuelve |
| adoption mode | `IDEA_ONLY`, `DEV_DEP`, `OPTIONAL_INTEGRATION`, `RUNTIME_DEP`, `DO_NOT_USE` |
| security | permisos, red, filesystem, browser, ejecucion de codigo, secretos |
| claim risk | que claims podria inducir y como se limita |
| isolated test | comando y artefacto de prueba sin tocar producto |
| decision | `CANDIDATE`, `REVIEW`, `BLOCK`, `ADOPTED_WITH_EVIDENCE` |

## Snapshot actual revisado

Fuente local: `qa_artifacts\release_validation\external_repos_verification_2026-05-02.json` y `claudio\memory_vault\external_projects_verification.md`.

| dependencia/proyecto | licencia snapshot | estado | decision |
|---|---|---|---|
| OpenTelemetry Python/spec | Apache-2.0 | activo | `CANDIDATE` para observabilidad, preferir interfaces estandar |
| AgentScope | Apache-2.0 | activo | `CANDIDATE_AFTER_SECURITY_REVIEW` para patrones de agentes observables |
| GPTCache | MIT | activo | `CANDIDATE` como idea/cache opcional, no meter datos privados sin threat model |
| SWE-agent | MIT | activo | `IDEA_ONLY` para patrones de tareas; no runtime autonomo sin ActionGate |
| browser-use | MIT | activo | `CANDIDATE_AFTER_SECURITY_REVIEW`; browser actions siempre gated |
| VisualWebArena | MIT | activo | `IDEA_ONLY` para evaluaciones visuales/sinteticas |
| mem0 | Apache-2.0 | activo | `CANDIDATE` para memoria, solo con privacidad/local review |
| Rebuff | Apache-2.0 | archived | `BLOCK_FOR_RUNTIME`, puede inspirar tests historicos |
| Skyvern | AGPL-3.0 | activo | `BLOCK_FOR_COMMERCIAL_BUNDLE`; solo revisar como referencia externa |
| Phoenix | NOASSERTION | activo | `REVIEW_LICENSE` antes de cualquier uso |
| LiteLLM | NOASSERTION | activo | `REVIEW_LICENSE`; usar interfaz propia por ahora |
| OpenHands | NOASSERTION | activo | `IDEA_ONLY`; no vendor ni runtime |
| AI Scientist / v2 | NOASSERTION | activo | `RESEARCH_ONLY`; no claims cientificos ni publicacion dependiente |
| BrowserGym | NOASSERTION | activo | `IDEA_ONLY`; validar licencia antes de tests publicos |

## Flujo de adopcion

1. Registrar ficha.
2. Revisar licencia y permisos.
3. Crear prueba aislada fuera del producto.
4. Ejecutar secret/path/claim scan sobre cualquier output.
5. Decidir `IDEA_ONLY`, `OPTIONAL_INTEGRATION` o `BLOCK`.
6. Solo si pasa, abrir tarea de integracion por producto.

## Regla comercial

Si una dependencia impone copyleft fuerte, licencia incierta o runtime con permisos amplios, no entra al wrapper comercial. Puede quedar como idea, comparador o referencia de paper.
