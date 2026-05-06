# One Universe Control - MEDIOEVO

Generated UTC: `2026-05-06T02:47:01.172262+00:00`

Principio: un solo universo, varios carriles. Nada queda huerfano; nada entra al canon sin ruta, gate y evidencia.

## Resumen

| metrica | valor |
|---|---:|
| `total_paths` | 378 |
| `by_lane` | `22` grupos |
| `by_decision` | `7` grupos |
| `by_gate` | `2` grupos |
| `by_git_status` | `2` grupos |
| `flag_counts` | `7` grupos |

## Gates

| gate | rutas |
|---|---:|
| `BLOCK` | 12 |
| `REVIEW` | 366 |

## Carriles Canonicos

| carril | prefijos |
|---|---|
| `control` | `.gitignore, AGENTS.md, README.md, AUDIT_REPO_TREE.md, TREE_PLAN.md, MIGRATION_MAP.md, DELETE_CANDIDATES.md, DELETED_OR_ARCHIVED.md, SOURCE_INTAKE_REGISTER.md` |
| `github_ci` | `.github/` |
| `comms` | `COMMS/` |
| `docs` | `docs/` |
| `runtime_state` | `runtime/` |
| `qa_evidence` | `qa_artifacts/, release_manifests/` |
| `apps` | `apps/` |
| `packages` | `packages/` |
| `books` | `books/` |
| `research` | `research/` |
| `website` | `website/` |
| `tools` | `tools/` |
| `tests` | `tests/` |
| `licenses` | `LICENSES/` |
| `hackathons` | `hackathons/` |
| `publish_staging` | `publish_staging/` |
| `products_staging` | `PRODUCTOS_MEDIOEVO/` |
| `medioevo_core` | `-=MEDIOEVO=-/` |
| `agent_sessions` | `.claw/` |
| `private_game` | `game-private/, -=MEDIOEVO=-/-=LIBROS/metaevo-tcg/, -=MEDIOEVO=-/-=LIBROS/claudio/tcg/` |
| `archive` | `_archive/, releases/` |

## Decisiones Por Carril

| carril | rutas |
|---|---:|
| `agent_sessions` | 1 |
| `apps` | 59 |
| `archive` | 2 |
| `books` | 1 |
| `comms` | 13 |
| `control` | 8 |
| `docs` | 95 |
| `github_ci` | 1 |
| `hackathons` | 1 |
| `licenses` | 1 |
| `medioevo_core` | 1 |
| `packages` | 26 |
| `private_game` | 1 |
| `products_staging` | 1 |
| `publish_staging` | 1 |
| `qa_evidence` | 89 |
| `research` | 1 |
| `root_registers` | 51 |
| `runtime_state` | 3 |
| `tests` | 1 |
| `tools` | 20 |
| `website` | 1 |

## Acciones Siguientes

| orden | accion | gate | decision |
|---:|---|---|---|
| 1 | Root control | `REVIEW` | Mantener AGENTS, Atlas, MIGRATION_MAP, DELETE_CANDIDATES y reportes como sistema nervioso del universo. |
| 2 | Regenerable residue | `APPROVE if path-specific cache rule passes` | Borrar o ignorar solo caches/builds regenerables con reporte; no borrar fuentes unicas. |
| 3 | MEDIOEVO core extraction | `REVIEW` | No mover todo -=MEDIOEVO=- de golpe; extraer a root lanes solo piezas con ficha, hash y destino canonico. |
| 4 | Private boundary | `BLOCK` | Juego, TCG, sesiones, secretos y cuentas quedan bloqueados fuera de open/commercial. |
| 5 | Vendor/imported trees | `REVIEW` | Referenciar, archivar o excluir; no convertirlos en tecnologia principal salvo modulo minimo extraido. |

## Muestra De Rutas

| git | gate | carril | decision | ruta |
|---|---|---|---|---|
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `.gitignore` |
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `AGENTS.md` |
| ` M` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/README.md` |
| ` M` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/handoffs/2026-05-05-claudio-local-agent-seto.md` |
| ` M` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/tools/validate_seto_comms.py` |
| ` M` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/topics/seto-observacionismo-decisions.jsonl` |
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `DELETED_OR_ARCHIVED.md` |
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `MIGRATION_MAP.md` |
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `SOURCE_INTAKE_REGISTER.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/asistente-negocio/README.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/asistente-negocio/electron-builder.json` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/asistente-negocio/electron/main.cjs` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/asistente-negocio/package.json` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/asistente-negocio/scripts/check-public-safe.cjs` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/asistente-negocio/scripts/package-final-release.cjs` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/flujocrm/BUSINESS.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/flujocrm/README.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/flujocrm/index.html` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/flujocrm/installer/BUILD.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/flujocrm/main.js` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/flujocrm/mockup.html` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/flujocrm/package.json` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/CHANGELOG.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/CODE_OF_CONDUCT.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/CONTRIBUTING.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/DEPLOY.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/INICIO_RAPIDO.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/INSTALL_AND_RUN.bat` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/LICENSE` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/PROYECTO_RESUMEN.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/PUBLICAR_AGORA.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/PUBLICAR_EN_GITHUB.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/README.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/SECURITY.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/SECURITY_TESTS_REPORT.md` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/agents/analyst.py` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/agents/copywriter.py` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/agents/creative.py` |
| ` M` | `BLOCK` | `apps` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `apps/commercial/mini-office/gumroad_page.html` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/index.html` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/install_and_run.sh` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/mini_office.py` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/package.json` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/public.css` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/pyproject.toml` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/requirements.txt` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/setup.py` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/tests/test_security.py` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/tools/generate_promo_materials.py` |
| ` M` | `BLOCK` | `apps` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `apps/commercial/mini-office/tools/publicar_gumroad.py` |
| ` M` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/mini-office/tools/publicar_web.py` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/assets.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/claudio-wabisabi.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/curaduria.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/privado-bloqueado.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/productos.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/psi-observacionismo.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/publicacion.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/atlas/seguridad.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/ATLAS_MAIN.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/CURADOR_MASTER_INDEX.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/pending/PENDING_REVIEW_2026-05-05.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/pending/PENDING_REVIEW_LATEST.md` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/gemma-observacionismo-cleanup/README.md` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/gemma-observacionismo-cleanup/pyproject.toml` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/obsai-core/.gitignore` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/obsai-core/README.md` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/obsai-core/obsai_core/__init__.py` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/obsai-core/obsai_core/cli.py` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/obsai-core/obsai_core/gate.py` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/obsai-core/pyproject.toml` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/obsai-core/tests/test_obsai_core.py` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/observacionismo-gate/pyproject.toml` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/residueos/README.md` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/residueos/examples/sample_action.json` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/residueos/pyproject.toml` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/residueos/residueos/gate.py` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/residueos/residueos/store.py` |
| ` M` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/open-dev/residueos/tests/test_residueos.py` |
| ` M` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/pending/pending_review_2026-05-05.json` |
| ` M` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/pending/pending_review_latest.json` |
| ` M` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/curador-automation-downloads-absorb-result-2026-05-05.json` |
| ` M` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/witness_log/curador_seto_witnesslog.jsonl` |
| ` M` | `REVIEW` | `runtime_state` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `runtime/curador_seto/curador_index.sqlite` |
| ` M` | `REVIEW` | `runtime_state` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `runtime/curador_seto/source_intake_export.json` |
| ` M` | `REVIEW` | `tests` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tests/release/test_pending_review_classification.py` |
| ` M` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/release/_common.py` |
| ` M` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/release/audit_repo.py` |
| ` M` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/release/find_duplicates.py` |
| ` M` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/release/pending_review.py` |
| ` M` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/release/run_tests.py` |
| ` M` | `BLOCK` | `tools` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `tools/release/scan_secrets.py` |
| ` M` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/release/source_intake.py` |
| `??` | `REVIEW` | `medioevo_core` | `KEEP_AS_CORE_SOURCE_UNTIL_EXTRACTED_TO_ROOT_LANES` | `-=MEDIOEVO=-/` |
| `??` | `BLOCK` | `agent_sessions` | `KEEP_LOCAL_AGENT_SESSION_HISTORY_NOT_MAIN_CANON` | `.claw/` |
| `??` | `REVIEW` | `github_ci` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `.github/` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `ANALYTICS_PLAN.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `APP_STORE_READINESS.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `ARCHIVE_INDEX.md` |
| `??` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `AUDIT_REPO_TREE.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `BUGS_FOUND.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `BUILD.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `BUSINESS_MODEL.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `BUYMEACOFFEE_PLAN.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `BUYMEACOFFEE_TIERS.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `CHANGELOG.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `CLAIMS_BOUNDARY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `COMMERCIAL_STRATEGY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `COMMIT_PROTOCOL.md` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/agents_state/claudio-local-agent.json` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/agents_state/claudio-local-autonomy.json` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/agents_state/hormiguero-mission-control.json` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/agents_state/publicacion-perfiles-observatorio.json` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/agents_state/wabi-sabi-sentido-comun.json` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/handoffs/2026-05-05-publicacion-perfiles-observatorio.md` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/inbox/publicacion-perfiles-observatorio.jsonl` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/outbox/` |
| `??` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/tests/test_validate_seto_comms.py` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `CONTRIBUTING.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `CUSTOMER_SUPPORT_PLAN.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `DEBUG_REPORT.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `DO_NOT_GIVE_AWAY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `EMAIL_SEQUENCE.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `FINAL_RELEASE_PREP_SUMMARY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `FIX_PLAN.md` |
| `??` | `BLOCK` | `root_registers` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `GUMROAD_CATALOG.md` |
| `??` | `BLOCK` | `root_registers` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `GUMROAD_PRODUCTS.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `INSTALL.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `LANDING_FUNNEL.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `LAUNCH_COPY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `LICENSE` |
| `??` | `REVIEW` | `licenses` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `LICENSES/` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `MANUAL_QA_CHECKLIST.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `MASTER_PLAN_STATUS_2026-05-01.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `MIGRATION_PLAN.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `OPEN_CORE_STRATEGY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `OPEN_SOURCE_STRATEGY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `PORTFOLIO_EXECUTION_LEDGER.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `PRICING.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `PRIVACY_POLICY_DRAFT.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `PRIVATE_GAME_BOUNDARY.md` |
| `??` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `PRODUCT_CATALOG.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `PUBLISHING_PLAN.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `QA_RESULTS.md` |
| `??` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `README.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `REFUND_POLICY_DRAFT.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `RELEASE_CHECKLIST.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `RELEASE_EVIDENCE.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `RELEASE_NOTES_DRAFT_2026-04-30.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `RELEASE_READINESS_MATRIX.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `RELEASE_READINESS_SCORE.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `ROADMAP.md` |
| `??` | `BLOCK` | `root_registers` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `SECRET_SCAN_REPORT.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `SECURITY.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `SECURITY_CHECKLIST.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `SMOKE_TESTS.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `TERMS_DRAFT.md` |
| `??` | `REVIEW` | `root_registers` | `KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX` | `TESTING_DEBUG_BENCHMARKS_FINAL.md` |
| `??` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `TREE_PLAN.md` |

## Reglas

- One universe does not mean flattening every folder into one directory.
- A route is canon only when it has lane, purpose, gate, evidence and owner.
- Untracked agent output is production residue until integrated into a lane.
- Generated caches can be deleted by rule; unique sources move only with ficha and migration map.
- Private, secret-like and external-action surfaces never become public canon by accident.
