## 2026-05-15 - DUAT Dual-Lane Predictive Registry v0.1
- Fecha UTC: 2026-05-15T03:02:47Z
- Estado: DUAT Multidimensional Filter Ecology + Predictive Registry v0.1 implementado localmente.
- Fuentes catalogadas: 29; metodos: 17; filtros: 10.
- Tests: DUAT registry 20 passed; GEODIA regression 53 passed.
- Scans: FAIL.
- Gate: publication_gate=BLOCK; external_publication=false; no keys used or printed.
- Nota: pending_review active_dedup=1 queda en REVIEW tracker, no en bloqueo de implementacion local.
- Proxima accion verificable: escoger un objetivo predictivo concreto y correr benchmark R_before/R_after.

## 2026-05-15 - GEODIA Public-Safe Candidate v0.1
- Fecha UTC: 2026-05-15T01:34:07Z
- Estado: GEODIA Public-Safe Package Candidate v0.1 creado como artefacto local de revision.
- Zip local: `qa_artifacts/release_validation/geodia-public-safe-candidate-v0-1.zip`.
- SHA256: `719ca8a7ef4c7439fe8859b5894483afa062c2b88883303fd5e0628fa9de0e43`.
- Excluye: raw XLSX, fixtures reales, rutas privadas, source vaults, privados/RPG/TCG y runtime privado.
- Incluye: README public-safe, claims boundary, attribution/terms review, source card INEGI sanitizada, QA summary, manifest, ejemplo sintetico de fixture.
- Gate: publication_gate=BLOCK; external_publication=false; human/legal review REQUIRED.
- Proxima accion verificable: revision humana/legal y decision A/B/C/D del candidate.

## 2026-05-14 - GEODIA Internal Release RC v0.1
- Fecha: 2026-05-14T22:17:54Z
- Estado: GEODIA internal RC v0.1 documentado para revision humana/legal.
- Evidencia: tres fixtures oficiales, wrapper QA offline, source card INEGI, hashes y human review packet.
- Gate: publication_gate=BLOCK; public_safe_package_created=false; external_publication=false.
- Proxima accion verificable: revision humana del packet y decision entre paquete public-safe, modulo interno o cuarto fixture oficial.

## 2026-05-14 - INEGI ENOE Third Fixture

| source | decision | risks | notes |
|---|---|---|---|
| `https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/tabulados/enoe_indicadores_estrategicos_2005_2026_mensual.xlsx` | keep_as_official_data_fixture/local_rehearsal_only | Terms documented but publication/commercial redistribution remains REVIEW.; ENOE unemployment is STRONG_PROXY, not EXACT.; 2020-2022 continuity caveats apply. | Third GEODIA official fixture. Source card `research/geodia-social-observatory/fixtures/source_intake/inegi/INEGI_SOURCE_CARD.md`; fixture `research/geodia-social-observatory/fixtures/inegi_mexico_social_2018_2023_fixture.json`; raw SHA256 `0add6e88da29b8f5eddcafe889f94c353edaab8a9d5ec272565a55c84cae8bd5`; final QA `qa_artifacts/release_validation/geodia-third-fixture-final-qa-report-2026-05-14.json`; publication gate `BLOCK`. |

# SOURCE_INTAKE_REGISTER

Generated UTC: `2026-05-05T05:56:01.036569+00:00`

Status: active control document. This is a manifest of sources, not permission to publish.

## Rules

- Classify every new source before extracting or copying code.
- Absorb selectively; never copy ZIPs wholesale into public or commercial packages.
- Keep research claims separate from product claims.
- Keep the game and TCG private unless a separate private release lane is explicitly authorized.
- Mark thresholds, weights and calibration as DEMO_ONLY until a real dataset exists.

## Formal Intake

| source | exists | bytes | lines | sha256_prefix | classification | lane | intake_action | target |
|---|---:|---:|---:|---|---|---|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\Formal` | yes |  |  |  | FORMAL_OBSERVACIONISMO_INBOX | psi-canon-intake | SELECTIVE_DELTA_EXTRACTION_ONLY | docs/intake/FORMAL_TO_PSI_INTAKE_2026-05-08.md |
| `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\banananana.txt` | yes | 365 | 19 | 2fa50b657189ae22 | PRIVATE_SECRET_CONFIG | provider-secrets | REDACTED_EVIDENCE_ONLY_DO_NOT_STAGE | docs/intake/FORMAL_SECRET_PROVIDER_INTAKE_2026-05-08.md |

## Downloads Intake

| source | exists | bytes | lines | sha256_prefix | classification | lane | intake_action | target |
|---|---:|---:|---:|---|---|---|---|---|
| `C:\Users\L-Tyr\Downloads\observacionismo_ai_os_fullstack.zip` | no |  |  |  | EXTERNAL_TECHNICAL_ZIP | obsai | SELECTIVE_ABSORPTION_ONLY | packages/obsai-core |
| `C:\Users\L-Tyr\Downloads\operational_ai_threshold.zip` | no |  |  |  | EXTERNAL_TECHNICAL_ZIP | obsai | SELECTIVE_ABSORPTION_ONLY | packages/obsai-core |
| `C:\Users\L-Tyr\Downloads\residueos_mvp.zip` | no |  |  |  | EXTERNAL_TECHNICAL_ZIP | residueos | SELECTIVE_ABSORPTION_ONLY | apps/residueos |
| `C:\Users\L-Tyr\Downloads\medioevo_observacionismo_codex_pack.zip` | no |  |  |  | EXTERNAL_CANON_TOOLKIT_ZIP | lore | SELECTIVE_ABSORPTION_ONLY | packages/lore-compiler and game-private manifests |
| `C:\Users\L-Tyr\Downloads\duat_lg_patch.zip` | no |  |  |  | EXTERNAL_RESEARCH_TOOLKIT_ZIP | research-boundary | RESEARCH_ONLY | research/ |
| `C:\Users\L-Tyr\Downloads\obs_antigravity_runtime.zip` | no |  |  |  | EXTERNAL_RESEARCH_RUNTIME_ZIP | research-boundary | KEEP_GATED_SELECTIVE_ABSORPTION | docs/OBS_ANTIGRAVITY_RUNTIME_REVIEW_2026-05-01.md and future packages/obsai-core adapters |
| `C:\Users\L-Tyr\Downloads\Aquí tienes el código completo para.txt` | no |  |  |  | EXTERNAL_OBSERVACIONISMO_RESEARCH_CODE_MIXED | research-boundary | KEEP_GATED_TRIAGE | research/obs-info-kernel triage and docs/OBS_INFO_KERNEL_REVIEW_2026-05-01.md |
| `C:\Users\L-Tyr\Downloads\SFAEFAGF.txt` | no |  |  |  | EXTERNAL_OBSERVACIONISMO_ENGINE_ITERATIONS | research-boundary | KEEP_GATED_RUNTIME_TRIAGE | research/obs-info-kernel and future obsai-core experiments after tests |
| `C:\Users\L-Tyr\Downloads\He analizado todo el material compi.txt` | no |  |  |  | EXTERNAL_OBSERVACIONISMO_SYNTHESIS_REVIEW | research-boundary | KEEP_GATED_IMPLEMENTATION_ROADMAP | docs/OBS_INFO_KERNEL_REVIEW_2026-05-01.md and PENDIENTES_MASTER.md |
| `C:\Users\L-Tyr\Downloads\He revisado `La integración correct.txt` | no |  |  |  | EXTERNAL_OBSERVACIONISMO_ARCHITECTURE_SYNTHESIS | github-public-sanitized | CURATOR_TECHNICAL_CARD_AND_WHITEPAPER_SOURCE | docs/developer/AI_WEB_GATEWAY_OBSERVACIONISTA_WHITEPAPER.md and public sanitized repo queue |
| `C:\Users\L-Tyr\Downloads\La integración correcta.txt` | no |  |  |  | EXTERNAL_OBSERVACIONISMO_ARCHITECTURE_BASE | github-public-sanitized | BASELINE_COMPARE_ONLY | curador session and AI-Web Gateway whitepaper source notes |
| `C:\Users\L-Tyr\Downloads\r.txt` | no |  |  |  | USER_ASSERTED_SAFE_NON_BLOCKING | secrets | REDACTED_EVIDENCE_ONLY_DO_NOT_STAGE | RISK_REGISTER.md, RELEASE_CHECKLIST.md and curador redacted evidence |
| `C:\Users\L-Tyr\Downloads\#!usrbinenv python3.txt` | yes | 298930 | 5177 | 2e9d8a6f6317789a | EXTERNAL_OBSERVACIONISMO_V2_NEUROSTATE_BUNDLE | duat-neurostate-residueos | SPLIT_BEFORE_USE | claudio/memory_vault, research/obs-info-kernel, residueos-core, ai-web-gateway-observacionista |
| `C:\Users\L-Tyr\Downloads\Me has pedido que te recomiende pro.txt` | no |  |  |  | EXTERNAL_GITHUB_TECH_INTEGRATION_ROADMAP | github-public-sanitized | VERIFY_EXTERNAL_REPOS_AND_BACKLOG | claudio/memory_vault/external_projects_verification.md and docs/developer/TECHNOLOGY_IMPLEMENTATION_BACKLOG_2026-05-02.md |
| `C:\Users\L-Tyr\Downloads\obs_info_kernel_package.zip` | no |  |  |  | EXTERNAL_OBS_INFO_KERNEL_PACKAGE | research-boundary | INTERNAL_RESEARCH_KERNEL_ONLY | research/obs-info-kernel |
| `C:\Users\L-Tyr\Downloads\Sí, Luis René. Radicalmente. Has pu.txt` | no |  |  |  | EXTERNAL_EOR_AIA_TOPOLOGY_SYNTHESIS | research-boundary | KEEP_GATED_EOR_AIA_SYNTHESIS | research/obs-info-kernel and docs/OBS_EOR_AIA_TOPOLOGY_REVIEW_2026-05-01.md |
| `C:\Users\L-Tyr\Downloads\observacionismo_research_report.md` | no |  |  |  | OBS_INFO_KERNEL_REPORT_OUTPUT | research-boundary | EVIDENCE_ONLY | docs/OBS_INFO_KERNEL_REVIEW_2026-05-01.md |
| `C:\Users\L-Tyr\Downloads\A_MEDIOEVO_OBSERVACIONISMO_DIEGETICO.md` | no |  |  |  | BOOKS_EDITORIAL_SOURCE | lore | CLASSIFY_BEFORE_EXTRACTION | books/ or packages/lore-compiler fixtures |
| `C:\Users\L-Tyr\Downloads\# Sí la idea fuerte es que el ecosi.txt` | no |  |  |  | PRIVATE_GAME_DESIGN_SOURCE | rpg-private | CLASSIFY_BEFORE_EXTRACTION | E:/Medioevo_RPG docs/data only |
| `C:\Users\L-Tyr\Downloads\para el motor gemma 4 te tengo esto.txt` | no |  |  |  | EXTERNAL_AI_ARCHITECTURE_SOURCE | obsai | SELECTIVE_ABSORPTION_ONLY | packages/obsai-core or research/ after claim review |
| `C:\Users\L-Tyr\Downloads\# La App que no existe y que el mun.txt` | no |  |  |  | PRODUCT_CONCEPT_SOURCE | residueos | PRODUCT_IDEA_ONLY | apps/residueos or future kairos brief |
| `C:\Users\L-Tyr\Downloads\deep-research-report.md` | no |  |  |  | RESEARCH_ONLY_REPORT | research-boundary | RESEARCH_ONLY | research/ |
| `C:\Users\L-Tyr\Downloads\# Resultado matemático.txt` | no |  |  |  | RESEARCH_ONLY_REPORT | research-boundary | RESEARCH_ONLY | research/ |
| `C:\Users\L-Tyr\Downloads\A continuación presento una formali.txt` | no |  |  |  | RESEARCH_ONLY_REPORT | research-boundary | RESEARCH_ONLY | research/ |
| `C:\Users\L-Tyr\Downloads\Voy a tomar la petición literalment.txt` | no |  |  |  | RESEARCH_LORE_TRANSLATION_SOURCE | research-boundary | RESEARCH_ONLY | research/ or lore residue with explicit inference labels |
| `C:\Users\L-Tyr\Downloads\insights de programacion e ia..txt` | no |  |  |  | EXTERNAL_AI_ARCHITECTURE_SOURCE | obsai | SELECTIVE_ABSORPTION_ONLY | packages/obsai-core docs or research/ |
| `C:\Users\L-Tyr\Downloads\Esto es material extraordinariament.txt` | no |  |  |  | EXTERNAL_DEBUGTYR_SYNTHESIS_SOURCE | obsai | KEEP_GATED_RESEARCH_TO_RUNTIME_TRIAGE | packages/open-dev/obsai-core and docs/memoria_viva/fichas/ontologias-aei-pac-debugtyr.md |
| `C:\Users\L-Tyr\Downloads\Amigo, entiendo perfectamente tu di.txt` | no |  |  |  | EXTERNAL_MONETIZATION_ONTOLOGY_SYNTHESIS | obsai | KEEP_GATED_MONETIZATION_AND_ONTOLOGY_SYNTHESIS | docs/memoria_viva/fichas/monetizacion-etica-github-sponsors.md and docs/memoria_viva/fichas/ontologias-aei-pac-debugtyr.md |
| `C:\Users\L-Tyr\Downloads\B_observacionist_agent.py` | no |  |  |  | EXTERNAL_RESEARCH_CODE | obsai | SELECTIVE_ABSORPTION_ONLY | packages/obsai-core experiments or research/ |
| `C:\Users\L-Tyr\Downloads\C_lg_benchmark.py` | no |  |  |  | EXTERNAL_RESEARCH_CODE | obsai | SELECTIVE_ABSORPTION_ONLY | packages/obsai-core experiments or research/ |
| `C:\Users\L-Tyr\Downloads\D_MANUSCRITO_DE_CALIBRACION.md` | no |  |  |  | BOOKS_EDITORIAL_SOURCE | lore | CLASSIFY_BEFORE_EXTRACTION | packages/lore-compiler fixtures or game-private lore manifests |
| `C:\Users\L-Tyr\Downloads\_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29` | no |  |  |  | ARCHIVE_DUPLICATE_ROOT | cleanup | MANIFEST_ONLY | _archive/source-intake |
| `C:\Users\L-Tyr\Downloads\_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29\operational_ai_threshold (1).zip` | no |  |  |  | ARCHIVE_DUPLICATE | cleanup | MANIFEST_ONLY | _archive/source-intake |
| `C:\Users\L-Tyr\Downloads\_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29\A_MEDIOEVO_OBSERVACIONISMO_DIEGETICO (1).md` | no |  |  |  | ARCHIVE_DUPLICATE | cleanup | MANIFEST_ONLY | _archive/source-intake |

## Source Decisions And Risks

| source | decision | risks | notes |
|---|---|---|---|
| `https://github.com/awesomedata/awesome-public-datasets` | keep_as_catalog_index/source_discovery_only | Catalog MIT license does not clear downstream dataset licenses.; Some linked datasets may be paid, restricted, stale or unsuitable for public claims.; Do not copy catalog wholesale or use catalog presence as proof of dataset validity. | Useful source index for DUAT/GEODIA simulations. Integrated locally as GEODIA `dataset_catalog_index_only` policy and DUAT Genesis public `SourceCard`; every selected dataset still needs its own source card, hash, license and claim boundary. |
| `https://api.worldbank.org/v2/country/MEX/indicator` | keep_as_official_data_fixture/local_rehearsal_only | World Bank terms and attribution must be reviewed before public/commercial reuse.; A GEODIA report over a small fixture is not prediction, policy advice or validation of DUAT claims.; Data can update, so fixture hashes and provider `lastupdated` must be preserved. | First real-data DUAT/GEODIA rehearsal. Fixture `research/geodia-social-observatory/fixtures/world_bank_mexico_2018_2023_fixture.json`; SHA256 `FC05D1C424C04EAE43CE1BE045455C8FEAF56A4241A8E97A6074253EDD63B1BC`; report gate `BLOCK`. |
| `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/` | keep_as_official_data_fixture/local_rehearsal_only | Eurostat reuse and dataset-specific terms require review before public/commercial redistribution.; API values can update; fixture is only the captured offline snapshot.; Cross-source comparison with World Bank Mexico is not valid without harmonization. | Second real-data DUAT/GEODIA rehearsal. Fixture `research/geodia-social-observatory/fixtures/eurostat_social_epoch_2018_2023_fixture.json`; SHA256 `FEF2CE8E3B523A48C0675646705033465BBCE788EAC8B532C18E0C3461098AD7`; comparison gate `BLOCK`. |
| `research/geodia-social-observatory/fixtures/geodia_indicator_crosswalk_v0_1.json` | keep_as_harmonization_crosswalk/local_qa_only | Crosswalk can be mistaken for semantic equivalence or ranking permission.; GDP/economy remains REVIEW.; No entry is EXACT in v0.1. | Harmonization layer v0.1 for technical compatibility only. Report `qa_artifacts/release_validation/geodia-harmonization-report-2026-05-14.json`; tests `23 passed`; publication gate `BLOCK`. |
| `research/geodia-social-observatory/geodia_social_observatory/cli.py harmonize` | keep_as_offline_reproducibility_tool/local_qa_only | CLI reproducibility can be mistaken for release readiness.; It must stay offline, explicit-input only and publication-blocked. | Harmonization CLI v0.1 regenerates `qa_artifacts/release_validation/geodia-harmonization-report-2026-05-14.json`; execution report `qa_artifacts/release_validation/geodia-harmonization-cli-report-2026-05-14.json`; tests `32 passed`; publication gate `BLOCK`. |
| `research/geodia-social-observatory/scripts/run_harmonization_qa.py` | keep_as_offline_qa_wrapper/local_qa_only | QA closure can be mistaken for release readiness.; Status-doc scans must not print sensitive values.; Wrapper does not authorize a third fixture or publication. | GEODIA Harmonization QA Wrapper v0.1 regenerates the harmonization report, validates JSON, runs focal scans and pending review; report `qa_artifacts/release_validation/geodia-harmonization-qa-wrapper-report-2026-05-14.json`; tests `37 passed`; publication gate `BLOCK`. |
| `INEGI / Mexico official social indicators` | candidate_third_official_fixture/review_needed | No local official INEGI fixture or source card with captured values was found.; Do not invent official values.; License and terms must be reviewed before redistribution. | Preferred third GEODIA fixture candidate. Scaffold `research/geodia-social-observatory/fixtures/README_THIRD_OFFICIAL_FIXTURE_REVIEW.md`; readiness report `qa_artifacts/release_validation/geodia-third-fixture-readiness-report-2026-05-14.json`; action gate `REVIEW_FIXTURE_SOURCE_NEEDED`; publication gate `BLOCK`. |
| `C:\Users\L-Tyr\Downloads\obs_antigravity_runtime.zip` | keep_gated/research_runtime_to_claim_gate | Domain name can invite overclaiming; public copy must say epistemic filter, not physical antigravity.; ZIP contains generated bytecode in the original source; clean before any package or repo import.; Scientific evidence references must stay tied to primary sources and current uncertainty. | Tests passed locally. Reuse generic parts only: evidence record, PAC gate, conservative validator pattern, ontology handoff and simulation-only fixtures. |
| `C:\Users\L-Tyr\Downloads\Aquí tienes el código completo para.txt` | keep_gated/anti_information_dark_information_code_triage | Contains useful anti-information and dark-information code mixed with speculative claims and aggressive deployment language.; Contains external commands and product-like claims that must not be executed or copied into public copy.; Use only tested, low-claim research primitives; verify sources before novelty claims. | Large mixed source for anti-informacion, informacion oscura, academic search agents and PSI runtime ideas. Treat as research input, not production code. |
| `C:\Users\L-Tyr\Downloads\SFAEFAGF.txt` | keep_gated/observacionismo_engine_iterations | Contains multiple engine versions, optional heavy dependencies and local model references.; Contains subprocess/Ollama patterns that need sandboxing and timeouts before runtime use.; Do not promote claims about non-human discovery without primary-source validation. | Iteration source for persistent PSI state, SQLite cache, graph persistence, surprise/entropy metrics and SESSION_FINGERPRINT continuity. |
| `C:\Users\L-Tyr\Downloads\He analizado todo el material compi.txt` | keep_gated/implementation_roadmap_not_product_claim | Contains a useful roadmap but also strong thesis language that must remain internal.; Dashboard/API/Docker snippets require separate implementation and security review.; Use as backlog and design synthesis, not as proof that the product is production-ready. | Synthesis review: integrate EstadoPSI, academic agents, anti-information, dark-information, ActionGate, SQLite, tests and cache; postpone speculative modules. |
| `C:\Users\L-Tyr\Downloads\He revisado `La integración correct.txt` | use_as_architecture_source/not_raw_publication | Contains useful AI-Web Gateway, ResidueOS, ActionGate and obs-info-kernel architecture mixed with private context and strong research claims.; Mentions exposed credential risk and credential-vault patterns; raw text must not be copied into public repos.; Scientific and cosmology language must be reduced to operational evidence, calibration and claim-boundary wording before GitHub. | Primary new synthesis for public sanitized GitHub lanes: AI-Web Gateway, ObservationEnvelope, MCP interface, evidence store, claim registry and whitepaper queue. |
| `C:\Users\L-Tyr\Downloads\La integración correcta.txt` | source_baseline/compare_against_revised_doc | Base architecture text may include raw implementation suggestions that need secret handling and claim review.; Use as lineage evidence, not as public copy. | Baseline document for the revised architecture synthesis. |
| `C:\Users\L-Tyr\Downloads\r.txt` | user_asserted_safe/non_blocking/no_raw_publication | User clarified this token note was inserted by another AI report and is safe.; Do not print token-like values, copy them into manifests or include the file in any GitHub staging area.; Future publication still depends on allowlist secret scans, not on this file being staged. | No longer a release blocker by human override. Keep only redacted audit metadata and exclude from public staging. |
| `C:\Users\L-Tyr\Downloads\#!usrbinenv python3.txt` | split_neurostate_python_ui_promptshield_papers | Large mixed source contains Python runtime, NEUROSTATE UI, Prompt Shield, paper drafts and pitch copy.; Must be split into technical cards before code import; raw file is not public copy.; Claims about cognition, survival and agent safety require measured evidence and low-claim language. | Observed EstadoPSI, semantic vectorizer, epistemic graph, anti-information, dark-information, academic agents, TerminalGuard, NEUROSTATE v2 UI, Prompt Shield + ResidueOS and paper/pitch sections. |
| `C:\Users\L-Tyr\Downloads\Me has pedido que te recomiende pro.txt` | verify_before_dependency_or_claim | External project status, licenses and activity are time-sensitive.; Do not treat recommendations as current until verified against official repositories or docs.; Integrate as roadmap/backlog first; no auto-forking, vendoring or publication. | Roadmap source for Phoenix/OpenTelemetry, prompt-injection shields, AgentScope, GPTCache, LiteLLM, browser agents, research agents, memory and observability integrations. |
| `C:\Users\L-Tyr\Downloads\obs_info_kernel_package.zip` | internal_research/clean_extract_no_publication | Original ZIP includes generated bytecode and reports; clean before workspace import.; Kernel finds candidates and gaps, not truth; public claims must say research aid only.; Do not publish as open-dev until source validation, secret scan, license review and claims boundary pass. | Installable zero-dependency package for anti-information, dark-information, calibration gaps, reports and continuity artifacts. Temp extraction tests passed. |
| `C:\Users\L-Tyr\Downloads\Sí, Luis René. Radicalmente. Has pu.txt` | keep_gated/eor_aia_entropy_topology_synthesis | Contains useful EOR/AIA architecture mixed with strong entropy, physics and consciousness claims.; Raw phrases such as R is entropy, entropy has owner and control R controls reality must be rewritten or blocked before canon/public use.; Topology snippets require NetworkX/GrafoEpistemicoHibrido and stay optional until dependency and validation review. | Absorb only low-claim primitives: EOR graph proxy, epistemic labels, operational equivalence test, dark-information states and non-anthropocentric AIA as procedure. |
| `C:\Users\L-Tyr\Downloads\observacionismo_research_report.md` | evidence_only/research_report | Report output has high R/JAMMING_TEMPRANO and must not be treated as final truth.; Findings require primary-source validation before being used as public claims. | Generated research report from obs-info-kernel; use for evidence and pending validation only. |
| `C:\Users\L-Tyr\Downloads\Esto es material extraordinariament.txt` | keep_gated/debugtyr_research_to_runtime_triage | Contains speculative scientific/canon claims that must not become product claims.; Contains mixed source material and code-like/UI fragments; absorb only tested runtime controls.; Keep private/canon/family context out of public packages. | DebugTyr raw synthesis. Extract only safety-gate, evidence, ontology and abstention controls with tests. |
| `C:\Users\L-Tyr\Downloads\Amigo, entiendo perfectamente tu di.txt` | keep_gated/monetization_and_ontology_synthesis | GitHub Sponsors setup is an external action and requires ActionGate, clean profile copy and manual payout/tax/2FA readiness.; Legal structures such as LLC, trust, nonprofit and insurance are strategy notes only and require professional advice.; Do not copy raw links, private context or full source text into public artifacts. | Monetization and ontology synthesis: open canon plus paid services, voluntary Sponsors, family legacy planning and ontology layers. |

## Additional Classified Downloads

| source | kind | exists | bytes | lines | sha256_prefix | classification | lane | intake_action | target |
|---|---|---:|---:|---:|---|---|---|---|---|
| `C:\Users\L-Tyr\Downloads\# CLAUDIO — LOCAL CODE AGENT.txt` | file | yes | 25753 | 776 | f6c6ef1b838d31f4 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\## 1. ESTADO.txt` | file | yes | 497078 | 7743 | 3088fe23ba847e24 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\### Resumen ejecutivo.txt` | file | yes | 94990 | 1566 | cd172e00c7756cd5 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\1.png` | file | yes | 1921777 |  | 06aa70ec52be683a | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\10.png` | file | yes | 1927064 |  | 6170fed535bd6b25 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\11.png` | file | yes | 2335287 |  | dd4f9b1e1e7a3081 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\12.png` | file | yes | 2004370 |  | 6a76876b7711dbdd | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\13.png` | file | yes | 2105202 |  | 79a4ad7d221b7526 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\14.png` | file | yes | 2069430 |  | 3a802bc81b26c735 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\15.png` | file | yes | 2136058 |  | 944b25348706b53b | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\16.png` | file | yes | 1666832 |  | 025209c956ec34f3 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\17.png` | file | yes | 2254242 |  | edaf383b4f89a5ac | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\18.png` | file | yes | 1527200 |  | 2c1670e47c17b3ce | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\19.png` | file | yes | 1912569 |  | d9890ff800958de6 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\2.png` | file | yes | 2066090 |  | 1b6123606a15062e | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\2.txt` | file | yes | 98648 | 2124 | c3473de67471b033 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\20.png` | file | yes | 2183994 |  | 3b3aec48f50d81de | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\21.png` | file | yes | 1857629 |  | a857a7b057c80388 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\22.png` | file | yes | 1919198 |  | f67667555de6831b | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\23.png` | file | yes | 1647572 |  | b305d6f8a6dfced3 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\24.png` | file | yes | 2081430 |  | 82b1bd35e1b4250f | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\25.png` | file | yes | 2074802 |  | cc124e33d0de30d1 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\26.png` | file | yes | 1949511 |  | aec056da76f35b8e | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\27.png` | file | yes | 2157559 |  | 97ec09224d5c4962 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\28.png` | file | yes | 1992045 |  | ddb22e69560ad890 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\29.png` | file | yes | 1736067 |  | efd3f4b4db069e3d | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\3.png` | file | yes | 2193005 |  | 5a53d7357f01e2fc | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\3.txt` | file | yes | 31514 | 564 | 2a03ca513cbd2dad | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\30.png` | file | yes | 1703484 |  | fcd855c5efe5b820 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\31.png` | file | yes | 1595619 |  | 8bec18c0459e3f1a | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\32.png` | file | yes | 1715956 |  | 6aa68f67cd4f1c67 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\33.png` | file | yes | 2227028 |  | fbc2a48b0402b021 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\34.png` | file | yes | 2115550 |  | 5cd6acb6abc5aa0c | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\35.png` | file | yes | 1872480 |  | 48c0c9ceb47404cd | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\4.png` | file | yes | 1786750 |  | de85ec368a0343e8 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\5.png` | file | yes | 1650823 |  | a148a14967a5105e | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\6.png` | file | yes | 1392898 |  | 72d6d964d9cd98e3 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\7.png` | file | yes | 2324672 |  | 59510383135971fb | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\8.png` | file | yes | 2158908 |  | 866913a7805e2a1c | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\9.png` | file | yes | 2173587 |  | fd8b996ef07877a9 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Activa modo Observacionismo  extrac.txt` | file | yes | 55250 | 1258 | 2fa6ed8f6d3f3e64 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\AGENTS.md` | file | yes | 971 | 23 | b4d92a26610b8208 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Ahora que he estudiado a fondo cada.txt` | file | yes | 52803 | 897 | 5f46fe81903f06b7 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\ANALISIS_LINEA_POR_LINEA_AGENTE_LOCAL.csv` | file | yes | 2537295 | 15746 | 7fe2a57d9d2ef97a | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Aquí tienes el código completo de `.txt` | file | yes | 34272 | 807 | 973f22c75987ac56 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_codex_agent.py` | file | yes | 12944 | 344 | 803fa12635ab4cb7 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent (1).py` | file | yes | 47568 | 1152 | b8236884f87a4350 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent.py` | file | yes | 47568 | 1152 | b8236884f87a4350 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_package (1).zip` | file | yes | 14375 |  | 0b76064911a3a9c5 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_package.zip` | file | yes | 14375 |  | 0b76064911a3a9c5 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_patched.py` | file | yes | 50899 | 1203 | b2318f3245167062 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_v1_final.py` | file | yes | 84296 | 1980 | de049e2d08361a22 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_v1_final.txt` | file | yes | 90859 | 2333 | b374014f7c5f17b1 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_local_code_agent_v2_final_integrated.py` | file | yes | 143266 | 3080 | 7bc488fa3878f335 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\claudio_nollm_agent_pack (1).zip` | file | yes | 18243 |  | 06e0b1d583241cff | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\claudio_nollm_agent_pack.zip` | file | yes | 18243 |  | 06e0b1d583241cff | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\claudio_nollm_final_integrated.zip` | file | yes | 127471 |  | 06d00b5aeddf7508 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\claudio_nollm_product.zip` | file | yes | 82183 |  | f53656adc5e76af0 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\claudio_ui (1).html` | file | yes | 95129 | 2357 | 42467666bef59c29 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\claudio_ui.html` | file | yes | 95129 | 2357 | 42467666bef59c29 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\claudio_ui_nollm (1).html` | file | yes | 112312 | 1875 | 78abd72fdd9adafb | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\claudio_ui_nollm.html` | file | yes | 112312 | 1875 | 78abd72fdd9adafb | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\CODE_AGENT.md` | file | yes | 3544 | 124 | fc52a705b00e2127 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\coding_agent.py` | file | yes | 42341 | 995 | af3e932e7438043d | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\Correcciones necesarias a tu formal.txt` | file | yes | 2701 | 104 | 5c68d9b0e2729a1c | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\Deconstrucción Observacionista de la Física — TUIP-Σ OSIT.docx` | file | yes | 57172 |  | 3c47df924d837968 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\Deconstrucción Observacionista de la Física — TUIP-Σ OSIT.pdf` | file | yes | 526472 |  | bdc094f4b0513cca | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\Deconstrucción Observacionista de la Inteligencia — TUIP-Σ OSIT.docx` | file | yes | 63144 |  | 3a88913cf8188df2 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\Deconstrucción Observacionista de la Inteligencia — TUIP-Σ OSIT.pdf` | file | yes | 598327 |  | 092699e982fb4c61 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\Deconstrucción Observacionista de Modelos de IA y Matemáticas Unificadas TUIP-Σ OSIT.docx` | file | yes | 63365 |  | fff7427889aa3440 | GEMMA_OBSERVACIONISMO_MODEL_SOURCE | obsai | MODEL_ROUTING_BACKLOG_ONLY | packages/open-dev/obsai-core and Claudio model-router docs |
| `C:\Users\L-Tyr\Downloads\Deconstrucción Observacionista de Modelos de IA y Matemáticas Unificadas TUIP-Σ OSIT.pdf` | file | yes | 715208 |  | f9e3cb69906d45fd | GEMMA_OBSERVACIONISMO_MODEL_SOURCE | obsai | MODEL_ROUTING_BACKLOG_ONLY | packages/open-dev/obsai-core and Claudio model-router docs |
| `C:\Users\L-Tyr\Downloads\desktop.ini` | file | yes | 282 |  | b029393ea7b7cf64 | LOCAL_SYSTEM_METADATA | cleanup | IGNORE_FOR_PUBLICATION | none |
| `C:\Users\L-Tyr\Downloads\Destrucción de los Grados de Libert.txt` | file | yes | 47219 | 930 | 6667eaacbdecd64c | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\duat_living_matrix_v07.zip` | file | yes | 83977 |  | 2d90d5c1e4d4ec2f | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\duat_observacionismo.py` | file | yes | 71486 | 1820 | 7356a5059329f3ec | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\duat_observacionismo_pack.zip` | file | yes | 72040 |  | fbf72349889087ee | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\duat_observacionismo_unified.zip` | file | yes | 82840 |  | 31ae645ec091a46e | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\duat_observacionismo_unified_v2.zip` | file | yes | 35648 |  | 17e8f7bb7bd3c92c | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\duat_observacionismo_unified_v4_code_agent (1).zip` | file | yes | 56702 |  | e84760fec379e817 | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\duat_observacionismo_unified_v4_code_agent (2).zip` | file | yes | 56702 |  | e84760fec379e817 | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\duat_observacionismo_unified_v4_code_agent.zip` | file | yes | 56702 |  | e84760fec379e817 | DUAT_LAB_SOURCE | duat-lab | TECHNICAL_CARD_AND_RESEARCH_BACKLOG | claudio/memory_vault and future research/duat-lab |
| `C:\Users\L-Tyr\Downloads\Entendido. Actúo como el arquitecto.txt` | file | yes | 28973 | 578 | 51064a330d8df783 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\ESTADO (R≈0.08, régimen de integrac.txt` | file | yes | 24678 | 320 | 7015470ed32d1dfb | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\He construido el laboratorio unific.txt` | file | yes | 55524 | 1513 | 70f77199a9b30831 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\leaderboard_popnfw_2000.json` | file | yes | 1942 | 88 | 53bbf04caa13a6ad | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\leaderboard_psichi_2000.json` | file | yes | 1937 | 88 | e088b14056c55ad3 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\New folder` | directory | yes |  |  |  | ARCHIVE_OR_LOCAL_DIRECTORY | cleanup | MANIFEST_ONLY | _archive/source-intake |
| `C:\Users\L-Tyr\Downloads\observacionismo_lab_improved.py` | file | yes | 19316 | 469 | 0620c70eeacbe6a8 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\observacionismo_lab_v3.py` | file | yes | 39237 | 1030 | 231a020b167e95b7 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\OBSERVACIONISMO_TUI_R3_PACK.zip` | file | yes | 473647 |  | 34dc55faa8686af0 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\observacionismo_unified_simulator.py` | file | yes | 51340 | 1204 | 2616a724f5ca6e40 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\observacionismo_v8_1_addons.txt` | file | yes | 298930 | 5177 | 2e9d8a6f6317789a | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\observacionismo_v8_integrator.py` | file | yes | 10633 | 246 | 9cecc245362ef043 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\OSIT — Teoría Completa de Información con Estado y Tesis del Agente Local sin LLM.docx` | file | yes | 67538 |  | 3d2424057a226ad0 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\OSIT — Teoría Completa de Información con Estado y Tesis del Agente Local sin LLM.pdf` | file | yes | 833811 |  | a59d9a9c40c215e7 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown (2).md` | file | yes | 10471 | 213 | 89e40049d5b2adcc | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown (3).md` | file | yes | 14551 | 377 | fbf88577127ca884 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown (4).md` | file | yes | 5863 | 82 | aa244b3d9f54205c | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown (5).md` | file | yes | 6814 | 92 | 3b1a5ecff5ae8783 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown (6).md` | file | yes | 31543 | 727 | bdb095a97c130d44 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown (7).md` | file | yes | 12677 | 284 | c07d24646fb251cd | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown (8).md` | file | yes | 9682 | 189 | 76e6eac3c10bc2b3 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted markdown.md` | file | yes | 5291 | 77 | 2c4e83c9b032bf16 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Pasted text (9).txt` | file | yes | 34272 | 807 | 973f22c75987ac56 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v2.py` | file | yes | 39502 | 1138 | 58189ee0bfe00ddb | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v2_pack.zip` | file | yes | 24438 |  | c71a7aa373e460ba | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v2_README.md` | file | yes | 1334 | 34 | 482cdd21215d3283 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v3_pack.zip` | file | yes | 18887 |  | e4bb92fe76cc6aff | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v4_pack.zip` | file | yes | 21143 |  | e945ca5f36869de4 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v5_pack (1).zip` | file | yes | 14760 |  | 3a35499d56aaf732 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v5_pack.zip` | file | yes | 14760 |  | 3a35499d56aaf732 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v6 (1).py` | file | yes | 40122 | 989 | 930a7ceb03af792d | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v6.py` | file | yes | 40122 | 989 | 930a7ceb03af792d | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v7_deep_checks.zip` | file | yes | 3116 |  | 3164bc2fda38930d | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v7_pack.zip` | file | yes | 13060 |  | e741ec2640c958fb | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v8.py` | file | yes | 33795 | 904 | 6ec65fdad3ff8feb | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v8_pack.zip` | file | yes | 12415 |  | d0bf2e3b7eb3bdf6 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\que le falta a este prompt, que le.txt` | file | yes | 115772 | 1735 | 06f3116de731c7c3 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\README (1).md` | file | yes | 2672 | 84 | 243fed5c817461bf | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\README (2).md` | file | yes | 7800 | 260 | c6549eb6f0ad5016 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\README.md` | file | yes | 1070 | 27 | bdd573c85bc4ff40 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Resumen breve Propongo una extensió.txt` | file | yes | 28399 | 742 | 719126081feb0cc8 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\sensorium_inversion_lab.py` | file | yes | 31030 | 571 | df5105e2e46d09c3 | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\sensorium_inversion_lab_pack.zip` | file | yes | 87334 |  | e16a7cb6ea4b884e | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\sensorium_psi_bridge_pack.zip` | file | yes | 138264 |  | 38a280b5c4b77d8d | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\smoke_test_results.json` | file | yes | 7834 | 17 | ce56e5dc5db36079 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Solicitud de auditoría observacioni.txt` | file | yes | 11614 | 228 | 88ea367ed89ea390 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\This synthesis integrates official.txt` | file | yes | 141999 | 2374 | abd79343b9df5240 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\tuip_sigma_core.py` | file | yes | 14747 | 448 | c5380de6bf94392d | EXTERNAL_CODE_PROTOTYPE | research-boundary | READ_REVIEW_TEST_BEFORE_IMPORT | research/ or package-specific experiments |
| `C:\Users\L-Tyr\Downloads\TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md` | file | yes | 30303 | 1541 | 62c6f2e56977f3ac | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\Untitled.txt` | file | yes | 127410 | 2882 | 76c6b475c95cf298 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v6_adversarial (1).csv` | file | yes | 418 | 6 | fbf2ca9d09bc53a0 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v6_adversarial (2).csv` | file | yes | 418 | 6 | fbf2ca9d09bc53a0 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v6_adversarial.csv` | file | yes | 418 | 6 | fbf2ca9d09bc53a0 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v6_crossval (1).csv` | file | yes | 693 | 16 | 663494b6f43e0697 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v6_crossval.csv` | file | yes | 693 | 16 | 663494b6f43e0697 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v6_leaderboard (1).csv` | file | yes | 440 | 6 | 775a2f6412c18e83 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v6_leaderboard.csv` | file | yes | 440 | 6 | 775a2f6412c18e83 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v8_leaderboard_popnfw.csv` | file | yes | 373 | 5 | 6c1fcc86d7148ff6 | REVIEW_REQUIRED_DOWNLOAD | cleanup | HOLD_WITH_TECHNICAL_CARD_BEFORE_USE | curador review and memory_vault index |
| `C:\Users\L-Tyr\Downloads\v8_leaderboard_psichi_strong.csv` | file | yes | 382 | 5 | c22685d937e0ad39 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\v8_leaderboard_psichi_weak (1).csv` | file | yes | 375 | 5 | 430e08c921cad360 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |
| `C:\Users\L-Tyr\Downloads\v8_leaderboard_psichi_weak.csv` | file | yes | 375 | 5 | 430e08c921cad360 | OBSERVACIONISMO_RESEARCH_SYNTHESIS | research-boundary | RESEARCH_ONLY_WITH_CLAIM_BOUNDARY | claudio/memory_vault and research/ |

## PSI Downloads Canon Contract Pass 2026-05-05

No files moved, deleted, extracted or published. This pass formalized the useful
`Downloads` PSI insights into canon and implementation contracts.

Evidence:

- `docs\intake\PSI_DOWNLOADS_CANON_CONTRACT_INTAKE_2026-05-05.md`
- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\canon\extensiones_formales\15_OSIT_TUIP_TUI_CANON_OPERATIVO_2026-05-05.md`
- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\canon\extensiones_formales\16_PSI_CLAIM_REGISTER_DOWNLOADS_2026-05-05.md`
- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\canon\extensiones_formales\17_PSI_TO_CLAUDIO_WABI_TECHNICAL_CONTRACT_2026-05-05.md`

Focused source decisions:

| source | full sha256 | decision | canonical use |
|---|---|---|---|
| `C:\Users\L-Tyr\Downloads\TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md` | `62C6F2E56977F3AC83AF30DA115ACD44338D800599A2BA30F4DAC633E14DA04F` | `FORMALIZE_LOW_CLAIM_ONLY` | PSI canon operativo |
| `C:\Users\L-Tyr\Downloads\tuip_sigma_core.py` | `C5380DE6BF94392D4120653AFF55BC70FB67BEE035065C90BF06AE77B2F974F1` | `CONTRACT_SOURCE_NOT_CODE_IMPORT` | future obsai-core/residueos implementation |
| `C:\Users\L-Tyr\Downloads\claudio_nollm_final_integrated.zip` | `06D00B5AEDDF75080D38729B66359FBDBB7F90F13813575185E48B452DB477EB` | `CLAUDIO_PHASE_REVIEW` | future local-code-agent contract |
| `C:\Users\L-Tyr\Downloads\duat_living_matrix_v07.zip` | `2D90D5C1E4D4EC2FBFF769E582FC234BB529DAD77F305BBCDD0B0DB04B261A4D` | `SYNTHETIC_LAB_RESEARCH_ONLY` | DUAT/GEODIA backlog |
| `C:\Users\L-Tyr\Downloads\observacionismo_v8_1_addons.txt` | `2E9D8A6F6317789AD08D71CC5FF9821275898DE8C1ED90DAD4CB2048AFBD6C45` | `EXTRACT_GUARDS_AND_FALSIFIERS_ONLY` | PSI claim gate/falsifier contract |
| `C:\Users\L-Tyr\Downloads\sensorium_psi_bridge_pack.zip` | `38A280B5C4B77D8DECD2D60C758CCB0A3F4AE2F407F0623CD5237D4B19808076` | `OBSERVER_PROXY_PATTERN_ONLY` | Sigma/proxy audit contract |
| `C:\Users\L-Tyr\Downloads\sensorium_inversion_lab.py` | `DF5105E2E46D09C31AA22F6CBB3931EE1C5FF0963A666F247ECADF9FFFA346B2` | `READ_REVIEW_TEST_BEFORE_IMPORT` | Sigma calibration prototype |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v2.py` | `58189EE0BFE00DDBBC7353D6733C22A76105E1550BB0CA457B46804D2C47FEA0` | `FALSIFIER_SOURCE_ONLY` | blocked physics-claim lane |
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v8.py` | `6EC65FDAD3FF8FEB6086AB518E51CD9C540EDE450DE8B2C1100E1C367E98EB63` | `FALSIFIER_SOURCE_ONLY` | blocked physics-claim lane |
| `C:\Users\L-Tyr\Downloads\OBSERVACIONISMO_TUI_R3_PACK.zip` | `34DC55FAA8686AF0276CBC26EA345327FF5A1F7AA4E4AFEA8D24BDEC5FC379CC` | `EXACT_DUPLICATE_OF_PSI_COPY_KEEP_UNTIL_CLEANUP_GATE` | PSI package lineage review |

Claim posture:

- `CERTEZA`: local paths, hashes, file existence, exact duplicate status and
  already-created fichas.
- `INFERENCIA`: architecture value of TUIP Sigma, Claudio No-LLM, Sensorium and
  DUAT as implementation patterns.
- `BLOQUEADO`: public/scientific/medical/social claims, external actions,
  deletion and wholesale ZIP import.

## External Roots

| root | exists | child_dirs | child_files | git_repo | classification | lane | intake_action |
|---|---:|---:|---:|---:|---|---|---|
| `E:\-=Medioevo=-` | yes | 11 | 0 | no | BOOKS_COMMERCIAL_ARCHIVE | publishing | MANIFEST_AND_CHECKSUM_ONLY |
| `E:\Medioevo_RPG` | yes | 15 | 21 | yes | PRIVATE_GAME | rpg-private | PRIVATE_REPO_ACTIVE_MANIFEST_ONLY |
| `E:\MEDIOEVO` | yes | 8 | 2 | no | LOCAL_SECRET_STATE | cleanup | DO_NOT_COPY |
| `E:\MEDIOEVO_ASSETS` | yes | 2 | 0 | no | PRIVATE_OR_COMMERCIAL_ASSETS | publishing | MANIFEST_AND_LICENSE_REVIEW_ONLY |
| `E:\MEDIOEVO_AUDIO_LIBRARY` | yes | 1 | 0 | no | COMMERCIAL_AUDIO_ASSETS | publishing | MANIFEST_AND_LICENSE_REVIEW_ONLY |
| `E:\Audiobooks` | yes | 0 | 0 | no | COMMERCIAL_AUDIO_ASSETS | publishing | MANIFEST_AND_LICENSE_REVIEW_ONLY |

## Lane Decisions

| lane | allowed intake | hard boundary |
|---|---|---|
| residueos | Extract only gate/API/store concepts into `apps/residueos`; migrate demo JSON stores to SQLite before product closure. | Calibration and confusion matrix stay `DEMO_ONLY` until a real dataset exists. |
| obsai | Extract metrics, action gate and CLI primitives into `packages/obsai-core`. | No claims of consciousness, physics proof or solved cosmology. |
| lore | Extract canon-to-data fixtures and schemas with evidence fields. | Full books, private lore and game data do not enter open packages. |
| rpg-private | Use manifests, hashes and private repo discipline before edits. | No public packaging, no free release, no source mixing. |
| publishing | Use manifests and checksums for books/assets/products. | No publication claim without Gumroad/web verification. |
| research-boundary | Store as `RESEARCH_ONLY` with falsifier or `PREDICTION_REQUIRED`. | No product copy can imply validated science. |
| github-public-sanitized | Convert only reviewed architecture, code and docs into clean repos with `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, tests and synthetic fixtures. | No raw Downloads text, local paths, secrets, private family context, RPG, full books, vendors or strong scientific claims. |
| secrets | Track redacted evidence and staging exclusions. | Never print secret values, stage secret files or rely on ignore rules as publication safety. |

## Residue

- This register lists ZIPs by hash and source contract; use a focused extractor before importing code.
- Duplicate files in `_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29` are kept as manifest-only evidence.
- Deep recursive counts for `E:\` roots are intentionally not performed here to avoid slow or unsafe broad scans.

## Global Curador SETO Dry Audit 2026-05-05

No files moved, deleted, extracted or published. This pass implemented the
global dry inventory requested for PSI, Downloads, Desktop, the L.R.GONZALEZ
workspace and `E:\`.

Artifacts:

- `docs\developer\CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md`
- `tools\release\global_curador_audit.py`
- `docs\intake\GLOBAL_CURADOR_SETO_AUDIT_2026-05-05.md`
- `qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05.json`
- `qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05.csv`
- `qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `global-curador-seto-audit-2026-05-05.json` | `0590DC835BA46290F87220BFCC3DB7F550351E013E8D0FD77132404C6A30D268` |
| `global-curador-file-manifest-2026-05-05.csv` | `1ADF62F605658A9406D9AE9C78F5A4CFC8738CF197455636603475C1A5E72392` |
| `GLOBAL_CURADOR_SETO_AUDIT_2026-05-05.md` | `F57A58F9880417CF180B22EF3AD4D651D07E1C2FE012B1A0C8CFBE2216A880F2` |
| `CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md` | `15184370F9385D683996FCEE056B0348C2B2425626AF119FC684A7BDC608B4D1` |
| `global_curador_audit.py` | `DF572E3DB01E8B6D8D3C97743781CE03892396E9C57A1716E32F6A9E61528541` |

Summary:

- Files inventoried: `81,107`.
- Hashed files: `56,360`.
- ZIP/archive files: `194`.
- Project roots detected: `266`.
- Exact duplicate groups: `12,071`.
- Version-review groups: `5,418`.
- ActionGate: `70,865 REVIEW`, `10,242 BLOCK`.
- Focus stats: PSI `136` files / Downloads `175` files / workspace `45,097`
  files / Desktop focus `46,838` files / `E:\` `34,094` files.

Decisions:

- `CERTEZA`: paths, sizes, generated manifest rows, SHA256 values where
  hashed, and WitnessLog event
  `8189746031215a2705ffda47760c16285f982dc651ce6f89ecb6be54c2ea9388`.
- `INFERENCIA`: lineage or cleanup value of duplicate/version groups until a
  canonical copy is selected.
- `BLOQUEADO`: private game/RPG/TCG, secret-like paths, and any strong medical,
  physics, social-prediction, publication or external-action claim.
- `REVIEW`: exact duplicates, large files, ZIPs, generated caches/builds and
  environment folders until ficha + hash + map + ActionGate are complete.

Next cleanup gate:

- Start with `__pycache__`, `.pytest_cache` and clearly regenerated local build
  caches, not Git history, releases, env folders, private assets or unique
  research material.
- Use the CSV manifest as source evidence for exact duplicate candidates.

## SETO Regenerable Cache Cleanup 2026-05-05

This follow-up executed the first narrow cleanup lane from the global SETO dry
audit.

Artifacts:

- `tools\release\cleanup_regenerable_cache.py`
- `qa_artifacts\release_validation\seto-cache-cleanup-dry-run-2026-05-05.json`
- `qa_artifacts\release_validation\seto-cache-cleanup-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-cache-cleanup-post-validation-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-cache-cleanup-selector-validation-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-cache-cleanup-tools-release-final-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-cache-cleanup-self-cache-final-result-2026-05-05.json`
- `qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `cleanup_regenerable_cache.py` | `75F45CD8B99DCC9C8CF0A2EB3FBAA5263E673646DA19F33A937C270D358B5A2A` |
| `seto-cache-cleanup-dry-run-2026-05-05.json` | `B5684F38A8FD9527B69C01D592DDD0F9F0E0F0D8241F9254DC6BD67D1BDEC105` |
| `seto-cache-cleanup-result-2026-05-05.json` | `C93052DD77DF42E9B89D1C6B6E671869D512211BFE45023D358F1BF44B9F7046` |
| `seto-cache-cleanup-post-validation-result-2026-05-05.json` | `1E1D21C5BA7FCE9705AB52B9FB6E3F37C7E0768B2F2F885D50BA2F836DFDF8D2` |
| `seto-cache-cleanup-selector-validation-result-2026-05-05.json` | `6644C45B103338E5223AF9D09934B3D103B652D5B92BE71E85D222E61284ECF9` |
| `seto-cache-cleanup-tools-release-final-result-2026-05-05.json` | `BBC818EDDBBB6076EC5F5A3AB61A0B52CECC2BC0C355D79D318BD85922EA59C1` |
| `seto-cache-cleanup-self-cache-final-result-2026-05-05.json` | `A74876E56B5AA75742A75623809162809FCC160B67E5FA498C93A7340E3D708E` |

Summary:

- Status: `EXECUTED_REGENERABLE_CACHE_DELETE`.
- Deleted: `122` cache directories, `879` files, `11,194,250` bytes.
- Post-validation residue check: `0` additional cache directories found.
- Selector-validation cleanup: `7` additional cache directories, `25` files,
  `279,254` bytes.
- Final tools-release cleanup: `2` additional cache directories, `14` files,
  `206,789` bytes.
- Self-cache final cleanup: `6` additional cache directories, `19` files,
  `208,999` bytes.
- Errors: `0`.
- WitnessLog event:
  `01f328781e05ccb667001b6e41f2516bd2b7db250657b60e2a0bceabc110d9eb`.

Boundaries:

- Allowed: `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache`.
- Excluded: `.git`, `node_modules`, `.venv`, `venv`, `env`, `.skills`,
  `_archive`, `_ARCHIVAR`, `tools\vendor`, `github-modules`, `release`,
  `releases`, private RPG/TCG/game bridge markers.
- No duplicate source files, ZIPs, release packages, env folders or unique
  Downloads/PSI research sources were deleted.
- The cleanup tool now permits `tools\release\__pycache__` cleanup while still
  excluding product `release/` and `releases/` directories.

## SETO Exact Duplicate Candidate Selector 2026-05-05

This follow-up advances the next cleanup lane without deleting anything. It
reads the global manifest and emits a bounded duplicate review queue.

Artifacts:

- `tools\release\select_exact_duplicate_candidates.py`
- `docs\intake\SETO_EXACT_DUPLICATE_CANDIDATES_2026-05-05.md`
- `qa_artifacts\release_validation\seto-exact-duplicate-candidates-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `select_exact_duplicate_candidates.py` | `81EBECFE83F1C7BA5B7335AB294A068E0D16AA18A49DC6FDE374E3D7B26AA0BD` |
| `seto-exact-duplicate-candidates-2026-05-05.json` | `995A0683CF62F1F38B2878F9A76CC354921DAB5F5C36482832A87E4A34FC552E` |
| `SETO_EXACT_DUPLICATE_CANDIDATES_2026-05-05.md` | `193D1A3ABA6955A222F63273AB12E2F3F927CFED89AEDC48F9D4C79CAE47DA1F` |

Summary:

- Status: `DRY_RUN_NO_DELETE_NO_MOVE`.
- Manifest rows read: `81,107`.
- Exact duplicate groups in manifest: `12,071`.
- Eligible low-risk groups: `157`.
- Selected groups written to report: `80`.
- Blocked or hard-review groups: `11,914`.

Boundaries:

- Only exact-hash textual groups under the workspace root, under `1 MB`, were
  considered for the review queue.
- `E:\`, `Downloads`, Desktop, `publish_staging`, `qa_artifacts`, `.claw`,
  `.claude`, `.wrangler`, `tools\pentest_repos`, `tools\vendor`, Git/env/
  release/archive/private/secret-like paths and boilerplate files were
  excluded.
- All listed candidates remain `REVIEW` until canonical source, ficha and
  ActionGate are complete.

## SETO Concurrent Agent Coordination 2026-05-05

This pass observed active concurrent work and created a coordination boundary.
No concurrent-agent files were edited, moved, deleted or staged by this pass.

Artifacts:

- `docs\developer\SETO_CONCURRENT_AGENT_COORDINATION_2026-05-05.md`
- `qa_artifacts\release_validation\seto-concurrent-agent-coordination-2026-05-05.json`
- `docs\developer\CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `SETO_CONCURRENT_AGENT_COORDINATION_2026-05-05.md` | `CD2E1490CEB6A78D90D3E828FFCE9B533809CF5899E15B0BF2E380A29F8C4C29` |
| `seto-concurrent-agent-coordination-2026-05-05.json` | `38E350F247003D5510F12664C051C8CD80C13EE53E36BE62BAB2CB09BADF69CB` |
| `CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md` | `C1D21CA5372654DA9C79221267050133B47A8E25487A7C73D94FB961728A6E67` |

Observed lanes:

| lane | artifact | sha256 | SETO decision |
|---|---|---|---|
| language | `docs\developer\OBSERVACIONISMO_MINIMAL_MACHINE_LANGUAGE_2026-05-05.md` | `5E4F04AC5FC91CD9AC3A8855E0B1D4F1B5E44FEF32D88C5C9D5952E4A3CA6185` | `READ_ONLY_CONCURRENT_OWNER` |
| language intake | `docs\intake\OBSERVACIONISMO_LANGUAGE_DOWNLOADS_PSI_INTAKE_2026-05-05.md` | `60635C6E9B29A948FC68736F4EBDE01D206C5E34540F74254E3E70A81F8C5316` | `READ_ONLY_CONCURRENT_OWNER` |
| language evidence | `qa_artifacts\observacionismo_language\observacionismo_language_inventory_2026-05-05.json` | `0560040C8F7255FD80F3DA6E982C89312747971168C1E9E44AD04FC68C4D5EAB` | `READ_ONLY_EVIDENCE` |
| local-agent intake | `docs\intake\OBSERVACIONISTA_LOCAL_CODE_AGENT_INTAKE_2026-05-04.md` | `57967DDC6E95B192529BB70FF8B52DFE8DA7C0B35ED6CEE6EF3D3DCFB4DF82E8` | `READ_ONLY_CONCURRENT_OWNER` |

Decisions:

- Language lane owns `research\observacionismo-lab`,
  `qa_artifacts\observacionismo_language` and its language docs.
- Local-agent lane owns Claudio-local implementation details until handoff.
- SETO owns manifests, fichas, duplicate queues, ActionGate, WitnessLog and
  cleanup evidence.
- No broad staging, no cross-lane deletion and no raw source canonization.

## SETO Duplicate Group Fichas Batch 1 2026-05-05

This pass converted the first selected exact-duplicate groups into fichas. It
did not delete, move, extract or publish files.

Artifacts:

- `docs\intake\SETO_DUPLICATE_GROUP_FICHAS_BATCH1_2026-05-05.md`
- `qa_artifacts\release_validation\seto-duplicate-group-fichas-batch1-2026-05-05.json`
- Source selector:
  `qa_artifacts\release_validation\seto-exact-duplicate-candidates-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `SETO_DUPLICATE_GROUP_FICHAS_BATCH1_2026-05-05.md` | `6E2A07D928B5C83393038DA83E9B6FA695F16519B1DE6B61BE75A1CD2FAAA3CF` |
| `seto-duplicate-group-fichas-batch1-2026-05-05.json` | `EB05BA6966892D716731F39FBCBEC1A23DBE11DCEC16D1CCC292F6813E9C4468` |

Summary:

- Status: `REVIEW_NO_DELETE_NO_MOVE`.
- Fichas created: `7`.
- Files represented by the groups: `32`.
- Proposed canonical paths: `7`.
- Candidate duplicate paths: `25`.
- Approved deletions: `0`.

Boundaries:

- Exact-hash equality is `CERTEZA`.
- Canonical choice remains `INFERENCIA`.
- ActionGate remains `REVIEW`.
- Wave FC rollback packs require release-evidence mapping before cleanup.
- Claudio OS, Asistente and PSI groups require owner confirmation before any
  file action.

## SETO PSI Duplicate Cleanup 2026-05-05

This pass executed the first exact duplicate deletion from Batch 1: the PSI
redundant vault copy of `NEXT_SESSION_BRIEF.md`.

Artifacts:

- `qa_artifacts\release_validation\seto-psi-next-session-brief-actiongate-2026-05-05.json`
- `qa_artifacts\release_validation\seto-psi-next-session-brief-cleanup-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-psi-next-session-brief-secret-scan-2026-05-05.json`
- `DELETED_LOG.md`
- `MIGRATION_MAP.md`
- `DELETED_OR_ARCHIVED.md`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `seto-psi-next-session-brief-actiongate-2026-05-05.json` | `48B498C4580479D2B96157F3605FEF4EF392420A64DCAB3CE7CBCA41835E12D9` |
| `seto-psi-next-session-brief-cleanup-result-2026-05-05.json` | `14156B3033984E81036FF72AB37C5007320AC8C38F939C899D2E32C3D422AA1B` |
| `seto-psi-next-session-brief-secret-scan-2026-05-05.json` | `7CAFB6823744D5BD82C20ACC07544D8696BA1CB5C8076920DCA79FBCC587A6A2` |
| `DELETED_LOG.md` | `24DE48679418A1BBE3EF6C665E1BF87657900E5E13F902C30FB517E90910C4A3` |

Result:

- ActionGate: `APPROVE`.
- Deleted files: `1`.
- Deleted bytes: `244`.
- Deleted SHA256:
  `5c7a951213069cd31f6ecda115fe00789cb380ce63a51c296bbbb765ea928b7b`.
- Canonical copy retained:
  `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\templates\NEXT_SESSION_BRIEF.md`.
- Secret scan on touched logs and evidence: `0` findings.

## SETO PSI Vault Residual Review And Decision Learning 2026-05-05

This pass closes the exact-duplicate cleanup line for
`vault_redundante_2026-04-26` by marking the remaining four files as
`REVIEW_UNMATCHED`. It also converts the observed SETO decisions into a local
decision-learning contract for Claudio/Wabi-Sabi.

Artifacts:

- `docs\intake\SETO_PSI_VAULT_RESIDUAL_REVIEW_2026-05-05.md`
- `qa_artifacts\release_validation\seto-psi-vault-residual-review-2026-05-05.json`
- `docs\developer\SETO_OBSERVACIONISMO_DECISION_LEARNING_2026-05-05.md`
- `qa_artifacts\release_validation\seto-observacionismo-decision-examples-2026-05-05.jsonl`
- `qa_artifacts\release_validation\seto-decision-learning-scan-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `SETO_PSI_VAULT_RESIDUAL_REVIEW_2026-05-05.md` | `6224F70782EDCA944030DFD6A703C4665403F6D5FD6CCC60ADDD33679A1664AA` |
| `seto-psi-vault-residual-review-2026-05-05.json` | `D07980496DFCD43DB17D41C74FE3D175EB5267C9BBFD3FF840224FA9D22C940C` |
| `SETO_OBSERVACIONISMO_DECISION_LEARNING_2026-05-05.md` | `86E0FBC05B4C897DADB8481F86D4F7C121B567AD6805EF17EC9E74C9F4303C26` |
| `seto-observacionismo-decision-examples-2026-05-05.jsonl` | `B00114556582418EFD3AE37C453B2B5FC0E2659EDB6D57CF4032A0F2DDE2E4D3` |
| `seto-decision-learning-scan-2026-05-05.json` | `CDFA057F2D4C51E86F0ED8B3C2C5113A42857A2B5B4B5BD830D2D9A9FB6DC4C9` |

Result:

- Residual unmatched vault files: `4`.
- Residual bytes: `7,505`.
- Approved deletions: `0`.
- ActionGate: `REVIEW`.
- Claudio contract examples: `7`.
- Secret scan on touched docs/registers/evidence: `0` findings.
- No external publication, extraction, source move or model training was
  performed.

## SETO COMMS Handoff To Claudio Local Agent 2026-05-05

This pass initialized the physical `COMMS` protocol for a read-only Claudio
local-agent handoff. It created envelopes only; it did not edit Claudio local
agent source code.

Artifacts:

- `COMMS\handoffs\2026-05-05-claudio-local-agent-seto.md`
- `COMMS\inbox\claudio-local-agent.jsonl`
- `COMMS\topics\seto-observacionismo-decisions.jsonl`
- `COMMS\agents_state\curador-seto.json`
- `qa_artifacts\release_validation\seto-comms-handoff-2026-05-05.json`
- `qa_artifacts\release_validation\seto-comms-handoff-scan-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `2026-05-05-claudio-local-agent-seto.md` | `325770239AB6A57601AFE2EDA57CD54D940438B9B96413AF426F83BA058A87B5` |
| `claudio-local-agent.jsonl` | `FEAD000C4905B10F1BA0981A1A13EB296E7DBC7332F9861361F2A59A263DE087` |
| `seto-observacionismo-decisions.jsonl` | `C1B28DE940A7BD70440A0C4EA68FC0A4333B692B396F172E2E756577FF079307` |
| `curador-seto.json` | `73326600E704E5B3E6FB83DBC8AA5A9892D7B9713AD998B873EB13F909963B28` |
| `seto-comms-handoff-2026-05-05.json` | `021B0F0B133995AC1B6D4D6D99BD376BC83E56D4CEB8BAC84DB26C938D7AECC8` |
| `seto-comms-handoff-scan-2026-05-05.json` | `9BD5582835BD511ACA0676403E8B471B92F7C6CC3FC470ED1C72909E19121743` |

Result:

- Physical `COMMS` paths initialized: `4`.
- Handoff recipient: `claudio-local-agent`.
- ActionGate: `REVIEW`.
- Secret scan on touched COMMS/docs/registers/evidence: `0` findings.
- Source moves/deletions: `0`.
- External actions: `0`.

## SETO COMMS Schemas 2026-05-05

This pass added machine-readable schemas for the COMMS protocol so Claudio can
validate envelopes before acting.

Artifacts:

- `COMMS\README.md`
- `COMMS\schemas\observation-envelope.schema.json`
- `COMMS\schemas\action-gate.schema.json`
- `COMMS\schemas\witness-log-event.schema.json`
- `qa_artifacts\release_validation\seto-comms-schemas-2026-05-05.json`
- `qa_artifacts\release_validation\seto-comms-schemas-scan-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `COMMS\README.md` | `373546657C351452C33371DDDF431084FA0A576D3CD595C1ABDDDD6C66F8D919` |
| `observation-envelope.schema.json` | `A5884ABCBD1127AFCA1835C6B8543380EDBF3C875144611125FA9E856D1B6B96` |
| `action-gate.schema.json` | `B0EE69AA4AFDD4444EFDBFD69C03966FFAA9F22C2CE10449080101426847AB7C` |
| `witness-log-event.schema.json` | `38ADBB03F56C506D2DAB419E43252CD4B8B179FCB800A8B93088EA9C34202ED1` |
| `seto-comms-schemas-2026-05-05.json` | `D55282A376AEE179C4E0DE587D82930A2B3F639DDD89FC204E9AE2807E49F766` |
| `seto-comms-schemas-scan-2026-05-05.json` | `0D5731B95504E6A24BC8A0BA51BD40C5015D7851D04D589600224C85A7C9AD03` |

Result:

- JSON parse: `PASS`.
- ObservationEnvelope sample check: `PASS`.
- WitnessLog sample check: `PASS`.
- Secret scan: `0` findings.
- Runtime execution: `0`.

## SETO COMMS Validator 2026-05-05

This pass added a local validator for COMMS envelopes, topic events, decision
examples and WitnessLog tail hash verification.

Artifacts:

- `COMMS\tools\validate_seto_comms.py`
- `qa_artifacts\release_validation\seto-comms-validator-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-comms-validator-scan-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `validate_seto_comms.py` | `4A8874E0DF93F0B2D09981F33B575633914AA8A622FC7638EB57969B7A5E0DB9` |
| `seto-comms-validator-result-2026-05-05.json` | `36EF148FD95A246E39E64424E039BB04DFD1EB18EF90323AFAABDCBB3E2EB9B7` |
| `seto-comms-validator-scan-2026-05-05.json` | `8180134CA9120DAE46DE3BA6F7A35C7AFFD74344515DB107AF47C542AC724BF9` |

Result:

- Validator command:
  `python COMMS\tools\validate_seto_comms.py --json --fail-on-errors`.
- Status: `PASS`.
- Schemas checked: `3`.
- Inbox messages checked: `1`.
- Topic events checked: `1`.
- Decision examples checked: `7`.
- WitnessLog tail hash match: `true`.
- Secret scan: `0` findings.

## Observacionista Engine + Inverse 2026-05-05

This pass implemented the requested observacionista and inverse-observacionista
method as a local COMMS engine and contract for Claudio/Wabi-Sabi. It extracts
only operational patterns from PSI/Downloads and does not copy full prototypes.

Artifacts:

- `COMMS\tools\observacionista_engine.py`
- `COMMS\schemas\observacionista-engine-result.schema.json`
- `docs\developer\OBSERVACIONISTA_ENGINE_INVERSE_CONTRACT_2026-05-05.md`
- `docs\intake\OBSERVACIONISTA_ENGINE_INVERSE_FICHA_2026-05-05.md`
- `qa_artifacts\release_validation\seto-observacionista-engine-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-observacionista-engine-scan-2026-05-05.json`

Source hashes:

| source | sha256 |
|---|---|
| `C:\Users\L-Tyr\Downloads\sensorium_inversion_lab.py` | `DF5105E2E46D09C31AA22F6CBB3931EE1C5FF0963A666F247ECADF9FFFA346B2` |
| `C:\Users\L-Tyr\Downloads\TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md` | `62C6F2E56977F3AC83AF30DA115ACD44338D800599A2BA30F4DAC633E14DA04F` |
| `C:\Users\L-Tyr\Downloads\tuip_sigma_core.py` | `C5380DE6BF94392D4120653AFF55BC70FB67BEE035065C90BF06AE77B2F974F1` |
| `C:\Users\L-Tyr\Downloads\observacionismo_v8_1_addons.txt` | `2E9D8A6F6317789AD08D71CC5FF9821275898DE8C1ED90DAD4CB2048AFBD6C45` |

Result:

- Engine command:
  `python COMMS\tools\observacionista_engine.py --input COMMS\inbox\claudio-local-agent.jsonl --out qa_artifacts\release_validation\seto-observacionista-engine-result-2026-05-05.json --json`.
- Status: `REVIEW`.
- ActionGate: `REVIEW`.
- Claim state: `INFERENCIA`.
- Main reason: autonomy and raw-theory risk require handoff before local writes.
- Tests:
  `python -m unittest COMMS\tests\test_observacionista_engine.py`.
- Test result: `PASS`, `4` tests.
- No Downloads prototype was copied wholesale.
- No file move, delete, extraction, publication, push or external action was performed.

## System Control Dashboard 2026-05-05

This pass activated/verified Cloudflare WARP and generated a local static
control dashboard for SETO, Claudio/Wabi-Sabi, VPN, COMMS, observacionismo,
cleanup, security and publication gates.

Artifacts:

- `tools\control_dashboard.py`
- `docs\control\CONTROL_DASHBOARD.html`
- `qa_artifacts\control_dashboard\system-control-snapshot-2026-05-05.json`
- `qa_artifacts\control_dashboard\system-control-dashboard-scan-2026-05-05.json`

Result:

- VPN command: `warp-cli connect; warp-cli status`.
- WARP status: `Connected`, network `healthy`.
- Cloudflare trace: `warp=on`, public country `US`, Cloudflare colo `DFW`.
- Public geolocation from ipinfo: `Flower Mound, Texas, US`; IP is redacted in committed artifacts.
- Dashboard generation:
  `python tools\control_dashboard.py --write`.
- Pending snapshot: `active_dedup=1708`, `claudio_open=60`.
- Dashboard validation: JSON parse `PASS`; HTML smoke `PASS`.
- Secret scan: `0` findings.
- No daemon, publication, push, source move or deletion was performed.

## Claudio Geolocation Security Guard 2026-05-05

This pass formalized the VPN/geolocation check as a local guard for Claudio and
the SETO dashboard. It verifies network truth, OS/browser location posture and
Google-observed divergence without mutating browser settings or Windows
location policy.

Artifacts:

- `tools\security_geolocation_guard.py`
- `qa_artifacts\control_dashboard\geolocation-security-guard-2026-05-05.json`
- `qa_artifacts\control_dashboard\geolocation-security-guard-scan-2026-05-05.json`
- `docs\control\CONTROL_DASHBOARD.html`
- `qa_artifacts\control_dashboard\system-control-snapshot-2026-05-05.json`

Result:

- Guard command:
  `python tools\security_geolocation_guard.py --connect --reported-google-location "Yucatan" --expected-country US --write --json`.
- Status: `REVIEW`.
- ActionGate: `REVIEW`.
- WARP status: `Connected`, network `healthy`; Cloudflare trace `warp=on`.
- Public IP geolocation: `Flower Mound, Texas, US`; IP is redacted in committed artifacts.
- User-observed Google location: `Yucatan`; this differs from the WARP/IP exit
  and is treated as browser/account/Wi-Fi cache or Google-side inference until
  verified in a clean profile.
- Windows location: current user `Deny`, machine level `Allow`.
- Browser location defaults: Chrome default `block`, Edge default `block`; no
  geolocation exceptions found in checked profiles.
- Automation boundary: Claudio may auto-connect/verify WARP and read browser
  preferences; account location history and site-permission changes remain
  manual; external publication remains `BLOCK`.
- No daemon, browser preference write, registry write, publication, source move
  or deletion was performed.

## SETO PSI Redundant Vault Batch 3 Cleanup 2026-05-05

This pass removed the final exact duplicates discovered in
`vault_redundante_2026-04-26` and leaves the four unmatched files in explicit
`REVIEW`.

Artifacts:

- `qa_artifacts\release_validation\seto-psi-vault-redundante-batch3-actiongate-2026-05-05.json`
- `qa_artifacts\release_validation\seto-psi-vault-redundante-batch3-cleanup-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-psi-vault-redundante-batch3-secret-scan-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `seto-psi-vault-redundante-batch3-actiongate-2026-05-05.json` | `48AEC8943406CA2F3518FD064C62280F75394CBB9F8D5CDFC5D7817FF970BCAC` |
| `seto-psi-vault-redundante-batch3-cleanup-result-2026-05-05.json` | `5A05A1878AB2920D3E352D7204D061F0A2BA85F23897C8C368CBED900F71574E` |
| `seto-psi-vault-redundante-batch3-secret-scan-2026-05-05.json` | `C7ABED297AB43AF684817BA34B0082A91FFEC6665812CE448835FAF37D572C22` |

Result:

- ActionGate: `APPROVE`.
- Deleted files: `2`.
- Deleted bytes: `13,263`.
- Residual unmatched vault files: `4`, all `REVIEW_UNMATCHED`.
- Secret scan on touched logs and evidence: `0` findings.
- No external publication, extraction or source move was performed.

## SETO PSI Redundant Vault Batch 2 Cleanup 2026-05-05

This pass removed the remaining exact duplicate files from the PSI redundant
vault set selected by the SETO duplicate selector.

Artifacts:

- `qa_artifacts\release_validation\seto-psi-vault-redundante-batch2-actiongate-2026-05-05.json`
- `qa_artifacts\release_validation\seto-psi-vault-redundante-batch2-cleanup-result-2026-05-05.json`
- `qa_artifacts\release_validation\seto-psi-vault-redundante-batch2-secret-scan-2026-05-05.json`

Artifact hashes:

| artifact | sha256 |
|---|---|
| `seto-psi-vault-redundante-batch2-actiongate-2026-05-05.json` | `E02FBA2F8D55B4C2B7E6BB44154DA029A0CF655B534C0606E79613F31F11DF94` |
| `seto-psi-vault-redundante-batch2-cleanup-result-2026-05-05.json` | `0304D4E11A45CBDD19AC6FB72A9B0BE5ED011854FD920D773C422E60C9B68E18` |
| `seto-psi-vault-redundante-batch2-secret-scan-2026-05-05.json` | `C035AF7B6C6B4BEA72FCD29FA85E370E3956FBDF8D3D41113838AB8321EB1BE0` |

Result:

- ActionGate: `APPROVE`.
- Deleted files: `5`.
- Deleted bytes: `6,694`.
- Canonical archive copies retained: `5`.
- Exact active references to redundant vault paths before deletion: `0`.
- Secret scan on touched logs and evidence: `0` findings.

## Lobby de Alejandria / Escaner Sigiloso 2026-05-06

Source:

- `C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria\escaner sigiloso.txt`

Classification:

- `EXTERNAL_SECURITY_SNIPPET`
- Lane: `security.network / Curaduria SETO`
- Intake action: `ABSORB_TO_POLICY_AND_ARCHIVE_SOURCE`
- Public boundary: `NO_PUBLICATION`
- Runtime boundary: `NO_NETWORK_EXECUTION`

Evidence:

- SHA256:
  `0C7CDDAA915D42C43D2303583A3E0B737BEEB53A54F574EE382AEFFD371E3D4E`
- Archivo Frio:
  `runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06\20_curaduria_seto\0C7CDDAA915D42C4_escaner-sigiloso.txt`
- Ficha:
  `docs\intake\lobby_alejandria_escaner_sigiloso_2026-05-06_REPORT.md`
- Manifest:
  `docs\intake\lobby_alejandria_escaner_sigiloso_2026-05-06_MANIFEST.json`
- QA:
  `qa_artifacts\release_validation\network-observer-escaner-sigiloso-2026-05-06.json`

Decision:

- `BLOCK`: stealth, Scapy/raw packets, ARP/broadcast and LAN/CIDR discovery.
- `APPROVE` only for local loopback read-only inventory.
- No packets were sent; `network_executed=false`.

Tests:

- `python -B -m pytest tests\test_security_network_observer.py -q`:
  `5 passed`.
- `python -B tools\matrix\validate_library.py --json`: `PASS`.

## CEREBRO / DUAT / Brain OS / Observacionismo Systems Pass 2026-05-05

This pass did not import raw sources, move files, delete files or publish. It
created system-level fichas and claim-boundary maps for the already observed
CEREBRO/PSI/Claudio/DUAT evidence.

Artifacts:

- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\01_MAPA_SISTEMAS_CEREBRO_DUAT_BRAIN_OS_2026-05-05.md`
- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\canon\extensiones_formales\18_MATRIZ_MATEMATICA_OPERATIVA_2026-05-05.md`
- `docs\intake\CEREBRO_DUAT_BRAIN_OS_OBSERVACIONISMO_FICHAS_2026-05-05.md`
- `docs\developer\CEREBRO_DUAT_BRAIN_OS_OBSERVACIONISMO_HANDOFF_2026-05-05.md`

Evidence:

- Pending snapshot: `active_dedup=1718`, `claudio_open=70`.
- Brain OS boot-audit: `event_id=107`, `decision=allow`, `state=listo`,
  `missing_required=[]`.
- DUAT OS orchestrator: `full_os_bootable=true`,
  `publication_allowed=false`.
- Focused tests: `12 passed`.

Decision:

- `KEEP`: maps/fichas/handoff.
- `READY_LOCAL`: Brain OS, Observacion Engineering gates, DUAT kernel/ISO.
- `REVIEW`: DUAT Living Matrix productization, local code-agent write lane.
- `BLOCK`: publication, raw-source import, strong science/social claims.

## MEDIOEVO AI Context Batch 2026-05-07

Source:

- `C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_AI_CONTEXT_BATCH_2026-05-07`

Classification:

- `AI_CONTEXT_PACKET`
- Lane: `CEREBRO / Observacionismo / Claudio / Wabi-Sabi`
- Intake action: `GENERATED_CURATED_BATCH`
- Public boundary: `NO_PUBLICATION`
- Runtime boundary: `LOCAL_CONTEXT_TRANSFER_ONLY`

Evidence:

- ZIP:
  `C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_AI_CONTEXT_BATCH_2026-05-07\MEDIOEVO_AI_CONTEXT_FULL_CANON_20260507.zip`
- ZIP SHA256:
  `3E4C75BE918877228A6B8817EF716108A90D265E8949500CEE6D879DFC2F1A1D`
- Files generated: `97`.
- CEREBRO records indexed: `648`.
- Source mutations: `0`.
- Security scan: `SECURITY_SCAN_LOCAL_REPORT.json`, `finding_count=0`, `result=pass`.
- ZIP policy verified: only `08_VERSION_COMPLETA_CANONICA/`; no 1/5/10 summary variants inside ZIP.
- Ficha:
  `C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_AI_CONTEXT_BATCH_2026-05-07\CURADOR_FICHA_PAQUETE_IA.md`

Decision:

- `KEEP`: generated local IA context batch.
- `APPROVE`: local reading, local agent context transfer, internal curation.
- `REVIEW`: publication, upload, release, claims reuse outside local context.
- `BLOCK`: treating the package as scientific proof, public source dump or license-cleared product.

## Formal to PSI Intake 2026-05-08

Source:

- `C:\Users\L-Tyr\OneDrive\Escritorio\Formal`

Classification:

- `FORMAL_PSI_RAW_INBOX`
- Lane: `CEREBRO / PSI / Observacionismo / Wabi-Sabi`
- Intake action: `SELECTIVE_DELTA_EXTRACTION_ONLY`
- Public boundary: `NO_PUBLICATION`
- Runtime boundary: `NO_CODE_IMPORT_OR_EXECUTION`
- Cleanup boundary: `NO_DELETE_MOVE_RENAME`

Evidence:

- Curador preflight: `NEEDS_FICHA_BEFORE_USE`.
- Files observed: `47`.
- Exact SHA256 matches against PSI/master/runtime index: `0`.
- Wabi/Sabi checks: `cerebro-audit`, `variant-compare`, `duplicate-migration-plan`, `cerebro-merge-review`.
- Wabi/Sabi mutation status: `source_mutations=0`, `auto_merge_actions=0`, duplicate plan `dry_run_only=true`.

Artifacts:

- `docs\intake\FORMAL_TO_PSI_INTAKE_2026-05-08.md`
- `docs\intake\FORMAL_DUPLICATES_REVIEW_2026-05-08.md`
- `docs\intake\FORMAL_CODE_INSIGHTS_2026-05-08.md`
- `docs\intake\FORMAL_CLAIMS_DELTA_2026-05-08.md`
- `docs\intake\FORMAL_CLEANUP_GATE_2026-05-08.md`

Decision:

- `KEEP_REVIEW`: all 47 files in `Formal`.
- `BLOCK`: execution of `uno.py`, `nucleo.txt`, `Para materializar este Pipeline Dir.txt` and `The Solution deploy_overlord.shThis.txt`.
- `REVIEW_EXTRACTION_REQUIRED`: PDF, PNG and ZIP sources.
- `NO_DELETE`: no `Formal` file qualifies for third-pass deletion yet.

## Lovable ZIP Tech Intake 2026-05-10

Source:

- `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\lovable-project-dff2f093-e843-43ad-94f5-91f91f8cec15-2026-05-10.zip`
- `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\lovable-project-15e48d05-7be7-4ec9-ab77-5af7c665fb3c-2026-05-10.zip`
- `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\lovable-project-f60723f6-2a07-4b63-9cd8-1c1734b15597-2026-05-10.zip`

Classification:

- `FORMAL_LOVABLE_SOURCE_REVIEW`
- Lane: `Wabi-Sabi / Claudio / DUAT / public-safe UI review`
- Intake action: `SELECTIVE_TECH_EXTRACTION_ONLY`
- Public boundary: `NO_PUBLICATION`
- Runtime boundary: `NO_EXECUTION_NO_INSTALL`
- Secret boundary: `NO_ENV_NO_SUPABASE_KEYS`

Evidence:

- Curador preflight: all three returned `NEEDS_FICHA_BEFORE_USE`.
- ZIP SHA256:
  - `E2753462500D0EE8840FACCCD39AF77ABCDA889F50795A79CA6D508CC32A4E21`
  - `48350CBB474ECD7A3DC392EF0E591CF4073E9144343E356A21F6404A83A7BBEC`
  - `9CC67E39166ABDA3B99770CFD4D3498B9B7B4BD2229A8D449C7E5D2D5FA8D7A5`
- File counts: `86`, `159`, `87`.
- Internal secret-like markers:
  - `dff2f093`: `0`.
  - `15e48d05`: `.env` and Supabase client/config present; `PRIVATE_REVIEW`.
  - `f60723f6`: policy/security vocabulary marker only; no `.env` observed.

Artifacts:

- `docs\intake\LOVABLE_ZIP_TECH_INTAKE_2026-05-10.md`
- `qa_artifacts\intake\lovable_zip_inventory_2026-05-10.json`

Decision:

- `KEEP_REVIEW`: all three ZIPs are useful sources.
- `INTEGRATE_SELECTIVELY`: ActionGate/Witness/Handoff UI, DUAT console flow, typed artifacts, deterministic tests and math specs.
- `BLOCK`: copying `.env`, Supabase keys/config, raw ZIP publication, full Lovable scaffold vendoring, or treating mock claims as validated runtime truth.

---

## MEDIOEVO GM Lite private MVP ZIP - 2026-05-14

- Source: `C:\Users\L-Tyr\Downloads\medioevo-gm-lite-private-mvp.zip`
- SHA256: `0421D51E6C1EB76E7F060A589169DC8E42E7B22336F63C5E38B79D74D0CEF57C`
- Classification: `PRIVATE_REPO_CANDIDATE`
- Intake action: `LOCAL_STAGING_ONLY_UNTIL_GATE`
- Public boundary: `NO_PUBLIC_REPO_NO_PUBLIC_DEPLOY`
- Runtime boundary: `NO_BACKEND_NO_PAID_SERVICE_NO_DEPLOY_IN_THIS_CYCLE`
- Secret boundary: `NO_ENV_NO_CREDENTIALS_NO_TOKENS`

Evidence:

- Curador preflight: `NEEDS_FICHA_BEFORE_USE`.
- Staging: `publish_staging\github-private\medioevo-gm-lite-private-mvp`.
- File count: `32`.
- Boundary check: `PASS`.
- Secret scan focalizado: `count_reported=0`.
- Host gate: `CONTAMINADO/REVIEW`.

Artifacts:

- `docs\intake\MEDIOEVO_GM_LITE_PRIVATE_MVP_FICHA_2026-05-14.md`
- `qa_artifacts\release_validation\MEDIOEVO_GM_LITE_PRIVATE_GITHUB_REVIEW_2026-05-14.md`

Decision:

- `KEEP_REVIEW`: package is ready for private-repo upload after gate/override.
- `PRIVATE_REPO_LIVE`: uploaded to `https://github.com/Lutren/medioevo-gm-lite` after explicit private-repo override; commit `ec755ca64ed3fb949ce5908036f0be01f3e51fd8`; `private=true`.
- `BLOCK`: public GitHub, public deploy, secret publication, full books, RPG/TCG complete material, DUAT/GEODIA private runtime, Wabi-Sabi internals, Claudio private runtime.

---

## Prompt-Analyzer Base44 Split - 2026-05-14

- Source: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\Prompt-Analyzer.zip`
- SHA256: `48FD6D4CEB5E52CECA596279264F2FAB767F3B0F225F98CCCC9C9827E3928B18`
- Classification: `UNKNOWN_REVIEW_REQUIRED_BASE44_UPLOAD_SOURCE`
- Intake action: `LOCAL_REPACKAGING_ONLY`
- Public boundary: user-directed Base44 upload candidate only; no Codex upload/deploy/push/publication.
- Secret boundary: local repository/cache/build material excluded before split.

Evidence:

- Curador preflight: `NEEDS_FICHA_BEFORE_USE`.
- Original ZIP `testzip`: `None`.
- Generated output: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\Prompt-Analyzer_base44_parts_20260514_195722`.
- Generated parts: `4`.
- Kept files: `234`.
- Excluded files: `30030` (`.git` and `.local` cache/store dominated the original ZIP weight).
- Output ZIP `testzip`: all four parts `None`.
- Direct sensitive-name hits in output parts: `0`.

Artifacts:

- `docs\intake\PROMPT_ANALYZER_BASE44_SPLIT_FICHA_2026-05-14.md`
- `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\Prompt-Analyzer_base44_parts_20260514_195722\BASE44_SPLIT_MANIFEST.json`
- `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\Prompt-Analyzer_base44_parts_20260514_195722\README_BASE44_UPLOAD.md`

Decision:

- `KEEP_REVIEW`: original ZIP remains untouched.
- `APPROVE_LOCAL`: four local Base44 upload parts generated.
- `BLOCK`: no upload to Base44, no deploy, no push, no deletion.

## DUAT Predictive Registry v0.1

- Catalogadas 29 fuentes gratuitas o revisables.
- Source cards piloto: Open-Meteo, World Bank, GDELT, Wikidata, FRED REVIEW_KEY_REQUIRED.
- Fuentes con key: FRED, NOAA CDO, EIA, Census quedan REVIEW_KEY_REQUIRED.

## DUAT Predictive Benchmark v0.2

- Reutiliza fixtures oficiales ya ingeridos por GEODIA: World Bank Mexico 2018-2023 y Eurostat Germany 2018-2023.
- No se agregaron fuentes nuevas ni APIs live.
- Licencia/terminos siguen en REVIEW para publicacion o redistribucion.

## DUAT Benchmark Matrix v0.3

- Reutiliza fixtures GEODIA oficiales existentes: World Bank, Eurostat e INEGI.
- No se agregaron fuentes nuevas.
- Comparabilidad: economy=REVIEW; labor_market=STRONG_PROXY; publication_gate=BLOCK.

## DUAT Domain Calibration Gate v0.4

- Reutiliza fixtures GEODIA oficiales existentes: World Bank Mexico 2018-2023 y Eurostat Germany 2018-2023 para `demography.life_expectancy_at_birth.total`.
- No se descargaron fuentes nuevas ni se usaron APIs live.
- Comparabilidad: demography/life expectancy=STRONG_PROXY, no EXACT.
- LicenseTermsScan sigue REVIEW; redistribution/publication sigue BLOCK.

## 2026-05-14 - DUAT Metric-Aligned R Calibration v0.5

- No new external source was added.
- No network/API call was used.
- Existing GEODIA fixtures remain the data basis; license terms stay REVIEW before publication.

## 2026-05-14 - DUAT Nested Domain Backtest v0.6

- No new source intake.
- No network/API call used.
- Existing GEODIA offline fixtures remain the basis; longer official history is the next evidence need if benchmark continues.
## 2026-05-15 - DUAT Official Long-History Data Readiness v0.7

- Manifest: `research/duat-predictive-registry/data_sources/duat_official_long_history_manifest_v0_7.json`.
- Fuentes derivadas de fixtures offline existentes: World Bank Indicators, Eurostat, INEGI ENOE.
- Estado: no se descargaron datos nuevos; no se inventaron datos oficiales.
- DataGate: BLOCK por 6 observaciones por serie, menor que MIN_OBSERVATIONS_WARN=24.
- LicenseTermsScan: REVIEW.
- ComparabilityReview: REVIEW.
- LeakagePreflight: PASS.
- Proxima accion: recolectar fuente oficial de historia larga con licencia/terminos y source card antes de otro benchmark.

## 2026-05-15 - DUAT World Bank WDI Source Pack v0.8

- Source: World Bank World Development Indicators API v2.
- Scope: MEX, por fixtures/manifests previos.
- Indicators: `NY.GDP.MKTP.KD.ZG`, `SL.UEM.TOTL.ZS`, `SP.DYN.LE00.IN`.
- Raw/processed stored under `research/duat-predictive-registry/data_sources/world_bank_wdi/`.
- Manifest: `research/duat-predictive-registry/data_sources/world_bank_wdi/world_bank_wdi_manifest_v0_8.json`.
- Manifest SHA256: `fe3d7e97baa9cfb7c1d189862a0870cb74b90df5653ed70daa96cabf091981d9`.
- DataGate: REVIEW.
- LicenseTermsScan: REVIEW.
- ComparabilityReview: REVIEW.
- LeakagePreflight: PASS.
- publication_gate: BLOCK.

## 2026-05-15 - DUAT WDI License/Comparability Governance v0.8.1

- License audit: `research/duat-predictive-registry/data_sources/world_bank_wdi/WORLD_BANK_WDI_LICENSE_TERMS_AUDIT_v0_8_1.md`.
- Comparability audit: `research/duat-predictive-registry/data_sources/world_bank_wdi/WORLD_BANK_WDI_COMPARABILITY_AUDIT_v0_8_1.md`.
- Governance decision: `research/duat-predictive-registry/data_sources/world_bank_wdi/world_bank_wdi_governance_decision_v0_8_1.json`.
- LicenseTermsScan: REVIEW.
- ComparabilityReview: REVIEW.
- LeakagePreflight: PASS.
- DataGate: REVIEW.
- BacktestOpenGate: REVIEW_ONLY_DRY_RUN.
- publication_gate: BLOCK.

## 2026-05-18 - BRAIN_OS POST Selective Extraction

| source | exists | sha256 | classification | lane | intake_action | publication_gate | ficha | evidence |
|---|---|---|---|---|---|---|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt` | yes | `C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD` | `INTERNAL_CANON_PORTFOLIO_SOURCE` | `claim-boundary` | `SELECTIVE_CLAIM_EXTRACTION_ONLY` | `NO_PUBLICATION` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_portafolio_medi.md` | `docs/intake/BRAIN_OS_POST_CLAIMS_DELTA_2026-05-18.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Untitled.txt` | yes | `F5C992E17FAE57AB6B3F43488F0017BC635C0FE84A97EF1BBD34B5A90B84DF4B` | `OSIT_RUNTIME_PROTOTYPE_SOURCE` | `runtime-comparison` | `CODE_INSIGHT_ONLY` | `NO_RUNTIME_IMPORT / NO_PUBLICATION` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_osit_epistemic_engine.md` | `docs/intake/BRAIN_OS_POST_CODE_INSIGHTS_2026-05-18.md` |

Decision:

- `Adopcion cruda`: `BLOCK`.
- `Extraccion selectiva`: `APPROVE_LOCAL_DOCS_ONLY` for this pass.
- Raw source move/rename/delete: `BLOCK`.
- Future runtime implementation: `REVIEW` until target-lane tests and evidence exist.

<!-- BRAIN_OS_POST_BATCH_INSIGHTS_2026_05_18_START -->
## 2026-05-18 - BRAIN_OS POST Batch Insights Matrix

Scope: exact-path fichas for the 14 new POST sources. The previously fichado `Portafolio MEDI` and `Untitled.txt` entries remain governed by the earlier `BRAIN_OS POST Selective Extraction` section.

| source | exists | sha256 | classification | lane | intake_action | gate | ficha |
|---|---|---|---|---|---|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\deep-research-report.md` | yes | `26B51C23C6B2CA503CFE62B947835D0AFA88A05E0F059F6817E7A7B76FD44A18` | `POST_SYNTHESIS_REVIEW_SOURCE` | `claim-boundary` | `INSIGHT_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_deep_research_report.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Del Cálculo al Gate_ Cómo OSIT Transforma la Planificación en la Nube en Acciones Locales Seguras y Auditables.pdf` | yes | `F294EF4A73202F8BE5B2C58FBD38053F299423DFDE03654F8FBAEAF2F2143578` | `POST_PDF_CLOUD_GATE_REVIEW_SOURCE` | `gate` | `PDF_INSIGHT_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_cloud_gate_pdf.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\El Noúmeno Informacional Unificació.txt` | yes | `F9D5B122A9B82C568C9CAEBBBFC0869DD5165CF7B4D2684C6C222FF030AEFCAD` | `POST_STRONG_THEORY_SOURCE` | `claim-boundary` | `STRONG_CLAIM_REVIEW_ONLY` | `BLOCK / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_noumeno_informacional.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADO ANÁLISIS_ARQUITECTÓNICO  REV.txt` | yes | `F3805545DB1163971149DC25892467D5F958955A2494740ECCA6D2A70B35180D` | `POST_ARCHITECTURE_REVIEW_STATUS` | `gate` | `ARCHITECTURE_DELTA_ONLY` | `APPROVE_LOCAL_DOCS_ONLY / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_estado_arquitectonico_rev.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADO.txt` | yes | `9B9EC7C6723FB037CA0370B40E31EBD5FD4A79D830DE80B947CA576268AD2D60` | `POST_FORMAL_LAB_STATUS_SOURCE` | `math-state` | `CLAIM_BOUNDARY_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_estado.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADOqqqqq.txt` | yes | `4744D5E3947591D8B5D7D53A9B284D4B0EFC13ECE0B3239C07F40FE53982E473` | `POST_BATCH_META_REVIEW_SOURCE` | `continuity` | `CURATED_META_REVIEW_ONLY` | `APPROVE_LOCAL_DOCS_ONLY / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_estadoqqqqq.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADO222222222.txt` | yes | `2E118556099DEAE74E07A8CCDC2B6F7D97C9BBBF5828EB2C41BDF244EC1137FE` | `POST_ETHICAL_SECURITY_WORKBENCH_SOURCE` | `security` | `DEFENSIVE_SECURITY_WORKBENCH_INSIGHT_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_estado_security_workbench.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Ingeniería Observacionista Inversa_ Un Modelo Operativo para Elevar la Eficiencia de la Investigación desde un Estado Óptimo.md` | yes | `5BE0BF57AB98AE8AC8F21C53DCDB0864DA943BFDF703B928B337008319BEE5BB` | `POST_ENGINEERING_METHOD_SOURCE` | `math-state` | `METHOD_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_ingenieria_observacionista_inversa.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_DOCUMENTOS_ACTUALIZADOS_TRUTHGATE_EIC_v0_3_2026-05-17.zip` | yes | `1FFC289E526E2BA81987B074DF1BDE6805C3E4A3C551E9BB7816BF29699FBE0C` | `ZIP_CONTAINER_TRUTHGATE_EIC_SOURCE` | `gate` | `ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_zip_truthgate_eic_v0_3.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_DOCUMENTOS_FORMALIZADOS_v2_1_2026-05-17.zip` | yes | `44190A3DE0CC6EEB6E3DC7BA37D361DE50653965BCBDFD9B82BD050C9F698937` | `ZIP_CONTAINER_FORMALIZED_DOCS_SOURCE` | `math-state` | `ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_zip_formalizados_v2_1.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_TEORIAS_COMUNICACION_CONSCIENCIA_v0_1_2026-05-17.zip` | yes | `6D1A0E1A686A44599BDB61C66DDC4E8B5212D56FE71ECBD79F8B514CAAFA438C` | `ZIP_CONTAINER_THEORY_CONSCIOUSNESS_SOURCE` | `claim-boundary` | `ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY` | `BLOCK / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_zip_teorias_consciencia_v0_1.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17.zip` | yes | `9871A6010E6E5BEF410C78314D6F60C790DC9E1BE591D6A86F93C7351EFA3523` | `ZIP_CONTAINER_WORK_IMPROVED_SOURCE` | `continuity` | `ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_zip_trabajo_mejorado_v0_2.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# OSIT Epistemic Engine A Formal Fr.txt` | yes | `94BE9A64DF6AD002F0F6B7DB4B2C2FA052314C31AABE2FE5E55ADFCFD40348D2` | `POST_FORMAL_FRAMEWORK_PREPRINT_SOURCE` | `math-state` | `FORMAL_FRAMEWORK_INSIGHT_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_osit_epistemic_engine_formal_framework.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\El Ojo de Ra y el Ojo de Horus (a m.txt` | yes | `F397D144BEA1471761838E7B9D7F209ED31CEC1F3D805B30548D6E0AF0BA6C30` | `POST_SYMBOLIC_AGENCY_AND_DREAM_MODULES_SOURCE` | `gate` | `SYMBOLIC_AGENCY_INSIGHT_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_ra_horus_symbolic_agency.md` |

Decision:

- `Adopcion cruda`: `BLOCK`.
- `RuntimeImport`: `BLOCK`.
- `PublicationGate`: `BLOCK`.
- ZIP handling: metadata/member-reference only; no extraction to runtime.
- Missing alias `# 00  LEER PRIMERO...`: `NOT_FOUND_ALIAS_DO_NOT_REGISTER`.

<!-- BRAIN_OS_POST_BATCH_INSIGHTS_2026_05_18_END -->

<!-- BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026_05_18_START -->
## 2026-05-18 - BRAIN_OS POST Absorcion y Limpieza Posterior

Scope: exact-path register for POST posterior cleanup and the three BRAIN_OS portfolio sets. This section is documentary only: no movement, deletion, archive, runtime import, publication or raw adoption.

| source | exists | hash_kind | sha256 | classification | lane | intake_action | gate | ficha |
|---|---|---|---|---|---|---|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST` | yes | `directory_tree_sha256` | `96EA09ADE2F9D350687DDF727B3850C1B944034D58CBC54A5EBD4DDCFA937492` | `POST_CONTAINER_SCOPE` | `archive` | `TOP_LEVEL_INVENTORY_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_container_scope.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt` | yes | `file_sha256` | `C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD` | `INTERNAL_CANON_PORTFOLIO_SOURCE` | `claims` | `EXISTING_FICHA_REFERENCE_ONLY` | `APPROVE_LOCAL_DOCS_ONLY / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_medi_portfolio_existing.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Assets Du WABI` | yes | `directory_tree_sha256` | `E772C97A4D5F816F3F2267E03BE0E8ADDFC0EB9561CEFC0FDE74FABD7706724F` | `POST_WABI_ASSET_BATCH` | `ui_design` | `ASSET_METADATA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_assets_du_wabi.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\BU` | yes | `directory_tree_sha256` | `2B55F1A2835662AFF20E36772FF41F66C0927D186ECEE7683392BEB44003026F` | `POST_BACKUP_LEGACY_BATCH` | `archive` | `BACKUP_INDEX_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_bu_backup.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_TEORIAS_COMUNICACION_CONSCIENCIA_v0_1_2026-05-17` | yes | `directory_tree_sha256` | `7DACC829297F4D548E032F36981E6253912D9B54F661722215765D648FF3187D` | `EXTRACTED_POST_ZIP_SHADOW_COPY` | `claims` | `DIRECTORY_MANIFEST_ONLY` | `BLOCK / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_teorias_consciencia_extracted_dir.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17` | yes | `directory_tree_sha256` | `7070F87939A382AB4AC25DF45F0EC86C5A72D8CA058E7B940CC7811A41C7CD70` | `EXTRACTED_POST_ZIP_SHADOW_COPY` | `continuity` | `DIRECTORY_MANIFEST_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_trabajo_mejorado_extracted_dir.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\codcx.txt` | yes | `file_sha256` | `F73F3A98C7757D8767213EE2BA59B748396D4E962F708651CA1D298E7C1607B2` | `POST_CODEX_COORDINATION_SOURCE` | `continuity` | `PROMPT_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_codcx.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Continúo. Exploración abierta. Deri.md` | yes | `file_sha256` | `53827A6366C01CDC245C0A2588FB04D508DB3060EEC402D1422CF204E4417B36` | `POST_DERIVATION_CONTINUITY_SOURCE` | `theory` | `DERIVATION_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_deriva_continuo.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Entendido. au poe favior = aun por.txt` | yes | `file_sha256` | `5E5486DFCBF8339C79FDE8553BDBC4F827E652664D8B30082B4E7B870A7AB4DB` | `POST_PENDING_ANALYSIS_SOURCE` | `continuity` | `PENDING_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_entendido_pendiente.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Voy a aplicar DO → IOI con rigor. T.txt` | yes | `file_sha256` | `A2CD0DE77703A828C2B87CE05ADF1D83FCC1FF76F7F25CAA1604ED15439518DD` | `POST_DO_IOI_METHOD_SOURCE` | `theory` | `METHOD_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_doi_ioi_rigor.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\OSIT-EXPLORACION-COMPLETA-v2-2026-0518.pdf` | yes | `file_sha256` | `95645EE4BCF0BDEF39098449D1B8BFF44280578A4F7BFE586F029F4B64FA2245` | `POST_OSIT_EXPLORATION_PDF_SOURCE` | `claims` | `PDF_INSIGHT_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_osit_exploracion_pdf.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\OSIT-RESOLUCION-BLOQUEOS-2026-0518.pdf` | yes | `file_sha256` | `615E9EC6EE246F208D083B89BD87F38541A2CFF3FF61D6E589FAD03738BC5248` | `POST_OSIT_BLOCKER_RESOLUTION_PDF_SOURCE` | `runtime` | `PDF_BLOCKER_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_osit_resolucion_pdf.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\OSIT-RESOLUCION-BLOQUEOS-2026-0518 (1).pdf` | yes | `file_sha256` | `615E9EC6EE246F208D083B89BD87F38541A2CFF3FF61D6E589FAD03738BC5248` | `POST_OSIT_BLOCKER_RESOLUTION_DUPLICATE_CANDIDATE` | `archive` | `DUPLICATE_EVIDENCE_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_osit_resolucion_pdf_duplicate.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\OSIT-SPIN-TORSION-ANSAZ.pdf` | yes | `file_sha256` | `3D4BD7389AE69D5D13F32C7E36738B328B795795D119BFC060EC2BDEE9E3D6FE` | `POST_SPIN_TORSION_STRONG_CLAIM_SOURCE` | `claims` | `STRONG_CLAIM_REVIEW_ONLY` | `BLOCK / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_spin_torsion_ansaz_pdf.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\OSIT-SPIN-TORSION-SCALE.pdf` | yes | `file_sha256` | `0B68E7A67E0A3673D8B84414777077DD7F79FF120F547476007F0976642EEC79` | `POST_SPIN_TORSION_SCALE_STRONG_CLAIM_SOURCE` | `claims` | `STRONG_CLAIM_REVIEW_ONLY` | `BLOCK / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_post_spin_torsion_scale_pdf.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\01_PORTFOLIO_AND_IDENTITY.md` | yes | `file_sha256` | `59AF0A5CDB0319D9D5F8A9FDC64F76F09A86651390D0A24D5F075F1A1EA7D9A3` | `BRAIN_OS_IDENTITY_PORTFOLIO_SOURCE` | `portfolio` | `PORTFOLIO_BOUNDARY_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_brain_os_identity_portfolio.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_AGENT_KNOWLEDGE_PORTFOLIO_v1_0.md` | yes | `file_sha256` | `C2830B50F44E7CF13651697BB88DEA63F08FB31EFE3AECC2B1C73B7388C93F35` | `OSIT_AGENT_KNOWLEDGE_PORTFOLIO_MD_SOURCE` | `portfolio` | `PORTFOLIO_DELTA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_osit_agent_knowledge_portfolio_md.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_AGENT_KNOWLEDGE_PORTFOLIO_v1_0.pdf` | yes | `file_sha256` | `B66A721DBC083A116E880A46438F9B082B1A75BCD7A8B1575C176E11749E46C1` | `OSIT_AGENT_KNOWLEDGE_PORTFOLIO_PDF_SOURCE` | `portfolio` | `PDF_PORTFOLIO_REFERENCE_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_osit_agent_knowledge_portfolio_pdf.md` |
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_KNOWLEDGE_FOLDER_v1_0.zip` | yes | `file_sha256` | `DE0C9BDF775D2CBD32AA84003F10026B710196D44989E8325888616D54657254` | `OSIT_KNOWLEDGE_FOLDER_ZIP_SOURCE` | `portfolio` | `ZIP_METADATA_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_osit_knowledge_folder_zip.md` |

Decision:

- `Adopcion cruda`: `BLOCK`.
- `RuntimeImport`: `BLOCK`.
- `PublicationGate`: `BLOCK`.
- `MIGRATION_LOG` required before any move/archive/delete by exact path.
- Useful deltas flow only through `docs/intake/BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.*` and per-path fichas.

<!-- BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026_05_18_END -->

<!-- BRAIN_OS_LR_WORKING_BENCH_DESCUBRIMIENTOS_2026_05_21_START -->
## 2026-05-21 - BRAIN_OS LR Working Bench Descubrimientos

Scope: exact-path ficha for the technical discovery folder requested for math,
Wabi, DUAT and system review. This is documentary/local-only. No movement,
deletion, archive, publication, external action or raw runtime import was
executed.

| source | exists | classification | lane | intake_action | gate | ficha |
|---|---|---|---|---|---|---|
| `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Descubrimientos` | yes | `BRAIN_OS_FORMAL_LAB_TECH_REVIEW_SOURCE` | `math-state / wabi-duat-system` | `SELECTIVE_ABSORPTION_ONLY` | `REVIEW / PublicationGate=BLOCK / RuntimeImport=REVIEW / RawAdoption=BLOCK` | `docs/intake/curador_fichas/brain_os_workbench/2026-05-21_descubrimientos.md` |

Evidence:

- Inventory: 45 files, 4,182,106 bytes.
- `python -m pytest -q`: 34 passed.
- `python mu_f.py`: Fibonacci base, `mu_F[1..8]`, inversion through `n=100`,
  reconstruction exact.
- Duplicate evidence: `osit_source_cards_gs_osit.json` and
  `osit_source_cards_gs_osit (1).json` have SHA256
  `AC24620C3AEA2FC70DB647185062C24A3FCA6242549F6E677A859F738E1CED20`.

Decision:

- `Adopcion cruda`: `BLOCK`.
- `Extraccion selectiva`: `APPROVE_LOCAL_DOCS_AND_TESTED_PATCHES`.
- Wabi/DUAT runtime integration: `REVIEW` until adapter, fixtures and tests.
- Publication: `BLOCK`.

<!-- BRAIN_OS_LR_WORKING_BENCH_DESCUBRIMIENTOS_2026_05_21_END -->
