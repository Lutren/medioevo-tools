# Excluded From Public-Safe Candidate

package_id: GEODIA_PUBLIC_SAFE_PACKAGE_CANDIDATE_v0.1
publication_gate: BLOCK

The following are excluded by default:

- INEGI raw XLSX file.
- `fixtures/source_intake/inegi/raw/` contents.
- Real fixture JSON files with official data values.
- Full internal RC folder.
- Internal QA reports with machine-local context beyond this summary.
- Source vaults, raw prompts, private runtime state, source dumps, and historical zip bundles.
- `.env`, credentials, tokens, local settings, session files, or debug dumps.
- Books, manuscripts, RPG, TCG, DUAT private, Wabi-Sabi internals, and Claudio private runtime.

Reason: this candidate is a local public-safe review package, not an external release.
