# MEDIOEVO Local Queue Closeout - 2026-05-15

## Estado

- R estimado: 0.18 -> 0.07
- Phi_eff estimado: 0.78 -> 0.94
- Regimen: FUNCIONAL_LOCAL_REVIEW
- Autonomia usada: LEVEL 4.5
- ActionGate local: APPROVE_LOCAL_DOCS_AND_TESTS / REVIEW_EXTERNAL
- PublicationGate: BLOCK_PUBLICATION
- DataGate: REVIEW
- BacktestGate: REVIEW_ONLY_DRY_RUN

## Workstreams cerrados

1. R/Phi runtime: episodio real local sanitizado agregado; calibracion PASS con 10/10 episodios.
2. DUAT/WDI v0.9: dry-run interno generado como `DUAT_WDI_BACKTEST_DRY_RUN_v0_9`; queda REVIEW_INTERNAL_ONLY.
3. Publishing metadata sprint: Deriva, Fragmentos y Calibracion tienen metadata draft revisable; no hay upload ni public page change.
4. MTS v0.4: pre-registro creado y bloqueado antes de fixtures; fixtures sinteticos/evaluacion local ejecutados despues del lock.
5. Live docs: brief, handoff, gates, pendientes, test report y fingerprint actualizados.

## Gates

- SecretScan: PASS en runtime, DUAT y docs publishing; MTS minimum targeted scan sin matches.
- BoundaryCheck: PASS focal; MTS forbidden true-state scan sin matches.
- ClaimsScan: PASS focal; no forbidden assertions en artefactos nuevos.
- SchemaValidation: PASS JSON load para publishing, DUAT, R/Phi y MTS.
- PublicationGate: BLOCK; no publicacion ejecutada.
- ReconstructionTest: PASS por presencia de brief, fingerprint, gates, comandos y artefactos.

## Hashes principales

- Publishing control board JSON: `307790273072dddedc20f09c4b3716871708dd9ebf69b08ebab9c4f269328bfc`
- Publishing metadata sprint JSON: `81f7df4cdd915ed03b9a893fa2fcf2ca8fb3f2be370b07d70c4037c3651c2fdb`
- DUAT/WDI v0.9 JSON: `e5fbbf3ffd993a95e4b66b243a3a0af5501d1205d3845c25df6d13b1700d2503`
- R/Phi budget latest JSON: `e602282b5ba87f1b41e55ce3489a8b5d2e378042310baadceb13ebd0fcb33caa`
- R/Phi calibration latest JSON: `8417e73c171fdcdf0e4e52fe7a12084809c73d14ad88cb9a9108c9a5fb672b62`
- MTS v0.4 lock JSON: `38da31cb8a877492fc922b7fb33b57dbc31d4ee517a925b395442a66839a6e75`
- MTS v0.4 fixture manifest JSON: `acae733f7d40184bd56f16658e2873deea4bcfa1babe28f3bc33fca645951615`
- MTS v0.4 results JSON: `11c189f9b931d0096cbc4d8cf936a2b0de6822db4701e937f28f86786e7f1801`
- MTS v0.4 leakage audit JSON: `979fc8ca813f2efb1bedee900dc721b4c6348d1234099a114edf3b70c48983be`
- MTS ledger entry hash: `fb2a8c1c4c7e5e2676f8dc25b6ba2d308b5465a74d450db2830ea471f1de6c68`

## Bloqueos

- Publicacion, upload, deploy, git push, Gumroad, KDP, redes y ZIP publico.
- Claims predictivos/cientificos fuertes fuera de soporte local.
- WDI externo hasta revision legal/comparabilidad.
- MTS con sensores reales, datos personales, cambios de modelo/labels o recalibracion de holdout.

## Proxima accion

Revision local del paquete de metadata para tres libros candidatos y definicion de assets/export, manteniendo PublicationGate en BLOCK.
