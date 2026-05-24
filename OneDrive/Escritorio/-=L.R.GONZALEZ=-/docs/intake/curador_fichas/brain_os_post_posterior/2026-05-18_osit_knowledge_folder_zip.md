# Ficha Curador - osit_knowledge_folder_zip

- source_path: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_KNOWLEDGE_FOLDER_v1_0.zip`
- exists: `True`
- hash_kind: `file_sha256`
- sha256: `DE0C9BDF775D2CBD32AA84003F10026B710196D44989E8325888616D54657254`
- file_count: `1`
- byte_count: `17850`
- classification: `OSIT_KNOWLEDGE_FOLDER_ZIP_SOURCE`
- lane: `portfolio`
- intake_action: `ZIP_METADATA_ONLY`
- action_gate: `REVIEW`
- PublicationGate: `BLOCK`
- RuntimeImportGate: `BLOCK`
- RawAdoption: `BLOCK`
- target_destination: `docs/intake; ZIP manifest review only`
- state: `ZIP_CONTAINER_REVIEW`

## Delta

- aporte_unico: Packaged knowledge folder may be useful as a distribution inventory.
- conflicto: ZIP may hide files that need per-file gates.
- claim_boundary: ZIP contents remain unadopted until per-member fichas exist.
- falsificador: Extracting ZIP into runtime/apps/packages falsifies ZIP boundary.

## Decision

`DOCUMENTED_FOR_SELECTIVE_EXTRACTION_ONLY`.

No move, delete, archive, runtime import, publication, deploy, push or raw adoption is authorized by this ficha.
