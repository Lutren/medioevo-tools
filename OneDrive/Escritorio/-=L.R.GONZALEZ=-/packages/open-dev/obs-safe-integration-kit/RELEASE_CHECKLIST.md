# Release Checklist

Status: required before any public push or package upload.

- [x] `python -m pytest -q` passes from this package root.
- [x] Python files compile with `python -m py_compile`.
- [x] CLI/import smoke passes without writing secrets or external state.
- [x] `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, `SECURITY.md` and `LICENSE` are present.
- [x] Secret scan reports `count_reported=0`.
- [x] Path scrub finds no local machine paths, private game paths or account/service names.
- [x] Claims scan reviewed; prohibited categories appear only as negative boundary language.
- [x] No caches, build outputs, virtualenvs, vendor folders or raw intake/source files are included.
- [x] Destination repo/package name is selected: `Lutren/obs-safe-integration-kit`.
- [x] ActionGate and host gate approved the 2026-05-03 external publication action; repo rechecked public on 2026-05-06 with `gh repo view Lutren/obs-safe-integration-kit`.

Current state: published public repo verified at `https://github.com/Lutren/obs-safe-integration-kit`. Any future external change still needs a fresh gate.
