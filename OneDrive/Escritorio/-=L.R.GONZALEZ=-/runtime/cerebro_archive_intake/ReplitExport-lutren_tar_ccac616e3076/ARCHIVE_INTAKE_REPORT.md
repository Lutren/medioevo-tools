# Archive Intake Report

CERTEZA:
- Source archive was not moved, deleted or raw-extracted into the workspace.
- Text-like safe members were copied to quarantine text files under this report directory.
- Secret-like paths, `.git`, caches, path traversal, oversized and binary members were blocked from text extraction.

INFERENCIA:
- This is enough for review and routing; it is not an import into production runtime.

INCOGNITA:
- Blocked/binary members still need specialized review if a claim depends on them.

## Archive

- Path: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\ReplitExport-lutren.tar.gz`
- SHA256: `ccac616e3076026284b3e3b5ad25e331fb66340d4ed992831ad5d8059e9aabe2`
- Output: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\cerebro_archive_intake\ReplitExport-lutren_tar_ccac616e3076`

## Counts

- Members: `888`
- Files: `630`
- Text indexed: `215`
- `BINARY_REVIEW`: 13
- `BLOCKED_METADATA_OR_CACHE`: 402
- `DIRECTORY`: 258
- `TEXT_INDEXABLE`: 215

## Top Signals

- `nu`: 395
- `R`: 370
- `OSIT`: 239
- `J_c`: 232
- `WitnessLog`: 227
- `Phi_eff`: 155
- `epsilon`: 152
- `lambda`: 143
- `Sigma`: 125
- `agent_programming`: 111
- `Wabi-Sabi`: 103
- `DUAT`: 71
- `GEODIA`: 49
- `browser`: 40
- `ActionGate`: 34
- `Claudio`: 33
- `Gauss-Bonnet`: 33
- `EML`: 19
- `NEC`: 10
- `QNM`: 6

## Next Action

- Review quarantined text records and select only owned, tested modules for any runtime import.
