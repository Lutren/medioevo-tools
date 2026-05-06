# One Universe Control - MEDIOEVO

Generated UTC: `2026-05-06T03:42:39.835599+00:00`

Principio: un solo universo, varios carriles. Nada queda huerfano; nada entra al canon sin ruta, gate y evidencia.

## Resumen

| metrica | valor |
|---|---:|
| `total_paths` | 100 |
| `by_lane` | `18` grupos |
| `by_decision` | `6` grupos |
| `by_gate` | `2` grupos |
| `by_git_status` | `2` grupos |
| `flag_counts` | `7` grupos |

## Gates

| gate | rutas |
|---|---:|
| `BLOCK` | 4 |
| `REVIEW` | 96 |

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
| `apps` | 4 |
| `archive` | 2 |
| `books` | 1 |
| `control` | 1 |
| `docs` | 1 |
| `github_ci` | 1 |
| `hackathons` | 1 |
| `licenses` | 1 |
| `medioevo_core` | 1 |
| `packages` | 3 |
| `private_game` | 1 |
| `products_staging` | 1 |
| `publish_staging` | 1 |
| `qa_evidence` | 75 |
| `research` | 1 |
| `tools` | 3 |
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
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `DELETED_OR_ARCHIVED.md` |
| ` M` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/ONE_UNIVERSE_CONTROL_2026-05-06.md` |
| ` M` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/one-universe-manifest-2026-05-06.json` |
| `??` | `REVIEW` | `medioevo_core` | `KEEP_AS_CORE_SOURCE_UNTIL_EXTRACTED_TO_ROOT_LANES` | `-=MEDIOEVO=-/` |
| `??` | `BLOCK` | `agent_sessions` | `KEEP_LOCAL_AGENT_SESSION_HISTORY_NOT_MAIN_CANON` | `.claw/` |
| `??` | `REVIEW` | `github_ci` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `.github/` |
| `??` | `REVIEW` | `licenses` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `LICENSES/` |
| `??` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/` |
| `??` | `REVIEW` | `archive` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `_archive/` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/README.md` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/argus-desktop/README.md` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/` |
| `??` | `REVIEW` | `books` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `books/` |
| `??` | `BLOCK` | `private_game` | `KEEP_PRIVATE_BOUNDARY_NOT_PUBLIC_CANON` | `game-private/` |
| `??` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/` |
| `??` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/README.md` |
| `??` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/obsai-core/` |
| `??` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/paid/` |
| `??` | `REVIEW` | `publish_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `publish_staging/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/2026-04-29-hormiguero-city/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/2026-04-29-wave-collapse-name-test.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/2026-05-01-wave-fc-captures/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/asistente_negocio_final_package_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/asistente_negocio_windows_install_2026-05-02-r2/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/asistente_negocio_windows_install_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/duat_audit_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02-r2/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02-r3/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02-r4-final/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_sqlite_install_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_win_unpacked_repro_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/github_sponsors_dashboard_2026-05-01/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/obs_info_kernel_validation_2026-05-03/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/observacionismo_language/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/aggressive-cleanup-publication-gate-2026-05-03.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/argus-archive-generated-artifacts-second-pass-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/argus-archive-generated-artifacts-second-pass-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-empty-dir-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-empty-dir-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-residue-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-residue-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-residue-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-win-unpacked-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-win-unpacked-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-win-unpacked-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/camera-frames-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/camera-frames-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/camera-frames-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/downloads-cleanup-manifest-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/downloads-cleanup-result-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/duat-publication-live-verification-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/external_repos_verification_2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-github-dry-run-duat-genesis-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-github-dry-run.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-github-publish.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-smoke-duat-genesis-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-smoke.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-staging-smoke-duat-genesis-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-staging-smoke.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-staging.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-impact-improvements-2026-05-03.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-public-sanitized-dry-run.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-public-sanitized-publish.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-public-sanitized-staging.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-publication-live-verification-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max5000.csv` |
| `??` | `BLOCK` | `qa_evidence` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `qa_artifacts/release_validation/gumroad-duat-templates.json` |
| `??` | `BLOCK` | `qa_evidence` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `qa_artifacts/release_validation/gumroad-medioevo-agent-ops-pack.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/host-gate-offload-2026-05-01.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/local-cli-security-gate-2026-05-03.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/mini-office-cleanup-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/portfolio-curador-inventory-2026-05-05.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/publication-live-verification-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/pycache-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/pycache-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/pycache-final-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/ruflo-model-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/ruflo-model-duplicate-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/ruflo-model-duplicate-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/store-github-linkedin-verification-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/website-agent-ops-pack-local-check-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/research/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/wave-collapse-landing-1365x768.png` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/wave-collapse-landing-390x844-chrome.png` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/wave-collapse-landing-390x844.png` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/website_agents_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/website_commerce_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/website_duat_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/website_local_audit_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/website_omnis_apps_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/website_software_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `release_manifests/` |
| `??` | `REVIEW` | `archive` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `releases/` |
| `??` | `REVIEW` | `research` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `research/` |
| `??` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/claw-code/` |
| `??` | `REVIEW` | `tools` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `tools/harness/` |
| `??` | `REVIEW` | `tools` | `ARCHIVE_OR_REFERENCE_VENDOR_NOT_MAIN_UNIVERSE` | `tools/vendor/` |
| `??` | `REVIEW` | `website` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `website/` |

## Reglas

- One universe does not mean flattening every folder into one directory.
- A route is canon only when it has lane, purpose, gate, evidence and owner.
- Untracked agent output is production residue until integrated into a lane.
- Generated caches can be deleted by rule; unique sources move only with ficha and migration map.
- Private, secret-like and external-action surfaces never become public canon by accident.
