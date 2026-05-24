# Public Profile Bilingual Packet - 2026-05-07

Status: `LOCAL_PUBLIC_SAFE_PACKET_READY / EXTERNAL_ACTION_GATED`

Target surfaces:

- GitHub profile: `https://github.com/Lutren`
- GitHub profile README repo: `https://github.com/Lutren/Lutren`
- GitHub Sponsors: `https://github.com/sponsors/Lutren`
- LinkedIn: canonical URL still requires authenticated owner-view confirmation before live edit.

This packet implements the 2026-05-07 profile decision: Spanish-first human
description, English mirror, then technical README material for AI systems and
technical readers.

## Decision

Retain and protect:

- MEDIOEVO books and unreleased editorial canon.
- Private game / RPG / TCG source, lore, mechanics, assets and bridge code.
- Internal OS/runtime layer.
- Internal DUAT / GEODIA layer.
- Raw Observacionismo.
- Raw Observacionismo Inverso.
- Raw MEDIOEVO information theory, formula work, derivations, notebooks and
  proprietary calibration.

Release under MIT when target-specific gates pass:

- Public-safe tools.
- Schemas, validators, CLIs and tests.
- Synthetic fixtures and reproducible examples.
- Public-safe whitepapers and low-claim documentation.
- Agent handoff, release, curation and ActionGate utilities that do not include
  private runtime, secrets, raw research, private canon or RPG/TCG material.

Use tiers for:

- Curated Observacionismo deconstructions.
- Public-safe research briefs.
- Advanced paper previews after review.
- Transfer maps from theory into gates, falsifiers, logs, workflows and
  synthetic demos.
- Support, implementation notes, templates, briefings and priority review.

Important license rule:

MIT code cannot be restricted by tiers after publication. Tiers can control
curation, support, paid packaging and unreleased/private material, not the rights
of already-published MIT code.

## GitHub Bio

Recommended bio:

```text
MEDIOEVO builder. Local-first AI tools, ActionGate, evidence logs, public-safe MIT software, curated Observacionismo research. Sponsor: github.com/sponsors/Lutren
```

Shorter fallback if the UI limit rejects it:

```text
MEDIOEVO builder. Local-first AI tools, ActionGate, evidence logs, MIT software and curated Observacionismo research.
```

## LinkedIn Headline

```text
Creador de MEDIOEVO | Local-first AI systems | ActionGate, evidencia antes de acción y research curado
```

## LinkedIn About - Español

```text
Construyo MEDIOEVO: un ecosistema de herramientas local-first para que agentes de IA trabajen con evidencia, límites y continuidad antes de actuar.

La idea humana es simple: cuando una IA toca código, archivos, cuentas o decisiones reales, no basta con que responda bien. Tiene que dejar evidencia, explicar qué va a hacer, separar lo seguro de lo riesgoso y permitir revisión humana cuando corresponde.

La capa pública de MEDIOEVO libera herramientas MIT y documentación práctica para builders: ActionGate, logs de evidencia, handoffs entre sesiones, fichas técnicas, checklists de publicación, curaduría de datos y demos sintéticas.

La capa de pago ahorra tiempo: plantillas, paquetes listos, soporte, briefings y research curado. Las deconstrucciones observacionistas avanzadas, Observacionismo Inverso y la Teoría de la Información MEDIOEVO se entregan como material revisado para tiers altos, no como dumps crudos.

Lo privado queda protegido: libros no publicados, videojuego/RPG/TCG, runtime interno, OS, DUAT/GEODIA interno, prompts crudos, datasets reales, secretos, calibración propietaria y fórmulas no liberadas.

No vendo claims absolutos. MEDIOEVO no promete seguridad garantizada, predicción social, diagnóstico ni nueva física validada. La promesa pública es más concreta: evidencia antes de acción, límites claros y sistemas que otro humano o agente pueda revisar.

GitHub: https://github.com/Lutren
Sponsors: https://github.com/sponsors/Lutren
MEDIOEVO: https://medioevo.space
```

## LinkedIn About - English

```text
I build MEDIOEVO: a local-first tooling ecosystem that helps AI agents work with evidence, boundaries and continuity before they act.

The human idea is simple: when an AI agent touches code, files, accounts or real decisions, sounding smart is not enough. It should leave evidence, explain the action, separate safe work from risky work and route sensitive steps to human review.

MEDIOEVO's public layer releases MIT tools and practical documentation for builders: ActionGate, evidence logs, session handoffs, technical fichas, release checklists, data curation workflows and synthetic demos.

The paid layer saves time: templates, packaged workflows, support, briefings and curated research. Advanced Observacionismo deconstructions, inverse Observacionismo and MEDIOEVO information theory are delivered as reviewed high-tier material, not raw dumps.

The private layer stays protected: unpublished books, the game/RPG/TCG, internal runtime, OS, internal DUAT/GEODIA, raw prompts, real datasets, secrets, proprietary calibration and unreleased formulas.

I do not sell absolute claims. MEDIOEVO does not promise guaranteed safety, social prediction, diagnosis or validated new physics. The public promise is narrower and more useful: evidence before action, clear boundaries and systems another human or agent can review.

GitHub: https://github.com/Lutren
Sponsors: https://github.com/sponsors/Lutren
MEDIOEVO: https://medioevo.space
```

## What Each Public Line Does

| line | español: qué hace | english: what it does | problema que resuelve | uso típico | acceso/licencia |
|---|---|---|---|---|---|
| ActionGate / ResidueOS | Clasifica acciones como aprobar, revisar o bloquear antes de ejecutarlas. | Classifies actions as approve, review or block before execution. | Agentes con permisos pueden actuar demasiado rápido. | Preflight para shell, browser, publicación, borrado, deploy o pagos. | MIT/public-safe tooling; soporte/packaging por tier. |
| obsai-core | Da primitivas de evidencia, residuo, claims y continuidad. | Provides evidence, residue, claim and continuity primitives. | La memoria de agente se pierde o no queda auditada. | Base para handoffs, logs, claim gates y fingerprints. | MIT/public-safe. |
| observacionismo-gate | SDK pequeño para gates de evidencia, jamming, costo y revisión. | Small SDK for evidence, jamming, cost and review gates. | Falta una forma simple de bloquear claims o acciones débiles. | Librerías, scripts y pipelines que necesitan un `APPROVE/REVIEW/BLOCK`. | MIT/public-safe. |
| obs-safe-integration-kit | Integra envelopes, evidence store y wrappers dry-run. | Integrates envelopes, evidence store and dry-run wrappers. | Herramientas de agentes necesitan límites antes de tocar sistemas reales. | Adaptadores para flujos de investigación, shell o browser sin ejecución directa. | MIT/public-safe; ejecución externa siempre gated. |
| data-curation-observatory | Convierte carpetas caóticas en fichas, manifiestos y evidencia. | Turns messy folders into fichas, manifests and evidence. | Fuentes mixtas terminan copiadas sin contexto o licencia clara. | Intake de datasets, ZIPs, repos y material descargado. | MIT/public-safe con fixtures sintéticos. |
| agent handoff / release tools | Estandariza continuidad, checklist y prueba antes de publicar. | Standardizes continuity, checklists and proof before release. | Trabajo multiagente se pierde o se publica sin evidencia. | Handoffs, release notes, secret scans y proof artifacts. | MIT/public-safe. |
| DUAT Genesis público | Sandbox sintético de simulación observable. | Public synthetic observable simulation sandbox. | Simulaciones pueden parecer más fuertes de lo que son. | Demos, falsadores, escenarios sintéticos y reportes low-claim. | MIT/public-safe; DUAT interno retenido. |
| Claudio OS Blueprint público | Blueprint/handoff para ideas de OS local-first. | Blueprint/handoff for local-first OS ideas. | La visión OS necesita una capa publicable sin vender runtime interno. | Documentación, perfiles host y políticas de diseño. | MIT/public-safe blueprint; OS interno retenido. |
| Observacionismo curado | Traduce teoría a gates, falsadores, logs y workflows. | Translates theory into gates, falsifiers, logs and workflows. | La teoría cruda puede volverse ruido, claim fuerte o fuga de IP. | Briefings, papers revisados, deconstrucciones y mapas técnicos. | Top-tier curated research; no raw dump. |
| Observacionismo Inverso | Estudia cómo cambia la observación desde el observador/medio. | Studies how observation changes from observer/medium conditions. | Un mismo dato no significa lo mismo bajo distintos estados de observación. | Research briefs, simulaciones sintéticas, falsadores y transfer maps. | Top-tier curated research; raw theory retained. |
| Teoría de la Información MEDIOEVO | Marco propio para evidencia, residuo, información oscura y claims. | Proprietary frame for evidence, residue, dark information and claims. | No todo dato útil es visible, confiable o listo para acción. | Papers revisados, mapas conceptuales y tooling derivado. | Top-tier curated research; formula/raw derivations retained. |

## Public README Technical Block

Use this in GitHub profile README after the human description:

```md
## Technical Surface

MEDIOEVO public tooling is built around a few repeatable objects:

- `ObservationEnvelope`: records what was observed, source, uncertainty, risk and evidence.
- `ActionGate`: routes proposed work to `APPROVE`, `REVIEW` or `BLOCK`.
- `EvidenceStore`: keeps traces, manifests, reports and proof artifacts.
- `WitnessLog`: makes agent work replayable across sessions.
- `Fichas`: classify sources before reuse, copying, publishing or deletion.
- `Falsifiers`: define what would downgrade or block a claim.
- `Claims Boundary`: prevents demos from becoming promises of science, safety or prediction.

Public repos use MIT only when they are target-clean: no secrets, no private
runtime, no raw research dumps, no full books, no RPG/TCG, no account state and
no guaranteed-outcome claims.
```

## Recommended GitHub Profile README Order

1. `# MEDIOEVO / Lutren`
2. Español humano.
3. English human mirror.
4. Qué hace / What it does.
5. Problemas que resuelve / Problems solved.
6. Para qué se usa / Use cases.
7. Public work table.
8. Tier ladder.
9. Technical README block.
10. Public/private boundary.
11. Links.

## Social Post - Español

```text
Estoy reorganizando MEDIOEVO alrededor de una frontera más clara:

Gratis y MIT: herramientas fundamentales para agentes con evidencia, ActionGate, logs, fichas, handoffs y demos sintéticas.

Por tiers: plantillas, soporte, briefings y research curado.

Top tier: deconstrucciones observacionistas, Observacionismo Inverso y Teoría de la Información MEDIOEVO en versiones revisadas y public-safe.

Privado: libros no publicados, videojuego/RPG/TCG, OS interno, DUAT interno, prompts, datasets reales, calibración y fórmula cruda.

La idea no es esconder lo útil. Es liberar lo fundamental sin destruir la IP central.

https://github.com/Lutren
https://github.com/sponsors/Lutren
```

## Social Post - English

```text
I am reorganizing MEDIOEVO around a clearer boundary:

Free and MIT: fundamental tools for evidence-gated agents, ActionGate, logs, fichas, handoffs and synthetic demos.

Tiered: templates, support, briefings and curated research.

Top tier: Observacionismo deconstructions, inverse Observacionismo and MEDIOEVO information theory in reviewed public-safe form.

Private: unpublished books, the game/RPG/TCG, internal OS, internal DUAT, prompts, real datasets, calibration and raw formula work.

The point is not to hide what is useful. It is to release the foundations without leaking the core IP.

https://github.com/Lutren
https://github.com/sponsors/Lutren
```

## External Action Gate

GitHub profile README:

- local staging may be edited now;
- live GitHub update requires focused secret scan, diff review, commit/push or API update, and public verification.

LinkedIn:

- paste-ready only until authenticated owner-view confirms canonical profile URL;
- do not post or edit against a guessed URL.

Sponsors:

- high tiers are already published as of 2026-05-06;
- future tier copy updates require dashboard verification.

## Do Not Say

- "guaranteed safe agents";
- "proved consciousness";
- "validated new physics";
- "predicts society";
- "diagnoses";
- "full research access";
- "raw formula included";
- "private runtime included";
- "MIT but only for top tier".

Use:

```text
Evidencia antes de acción. Herramientas MIT public-safe. Research curado por tiers. IP central protegida.
```
