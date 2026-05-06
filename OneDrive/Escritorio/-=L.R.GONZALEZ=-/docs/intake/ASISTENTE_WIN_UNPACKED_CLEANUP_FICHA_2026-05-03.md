# Ficha Curador - Asistente win-unpacked cleanup

Fecha: 2026-05-03

Ruta limpiada:

`apps\commercial\asistente-negocio\release\win-unpacked`

## Estado

- classification: `GENERATED_RELEASE_OUTPUT`
- status: `CLEANED_WITH_FINAL_PACKAGE_PRESERVED`
- public_boundary: no publicar desde `release/`; usar paquete final QA/manifest.
- private_boundary: no contiene RPG/TCG; es output comercial generado.
- discard_rule: se puede regenerar con electron-builder; no es fuente.

## Evidencia

Dry-run:

`qa_artifacts\release_validation\asistente-win-unpacked-cleanup-dry-run-2026-05-03.json`

Resultado:

`qa_artifacts\release_validation\asistente-win-unpacked-cleanup-result-2026-05-03.json`

Verificado:

- `git_check_ignore`: `apps/commercial/asistente-negocio/.gitignore:4:release/`
- archivos borrados: `75`
- bytes borrados: `353,080,065`
- ActionGate: `cd4344b5-700e-4cd4-9863-ec5de3b42c98`
- paquete QA preservado:
  `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0\Windows`

## Decision

Borrado como output generado ignorado. Los instaladores finales preservados
mantienen evidencia de distribucion y hashes.
