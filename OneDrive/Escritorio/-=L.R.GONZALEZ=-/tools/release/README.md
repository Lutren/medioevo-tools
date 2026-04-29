# Release Tools

Safe local tooling for audit and release preparation.

All package scripts default to dry-run. Nothing is deleted.

## Commands

```powershell
python tools/release/audit_repo.py
python tools/release/audit_repo.py --include-denied
python tools/release/scan_secrets.py
python tools/release/find_large_files.py --limit 30
python tools/release/find_duplicates.py --limit 30
python tools/release/product_manifest.py
python tools/release/source_intake.py --hash
python tools/release/package_free_dev.py
python tools/release/package_paid_apps.py
python tools/release/generate_release_notes.py
python tools/release/run_tests.py
python tools/release/run_builds.py
```

To create package ZIPs, pass `--execute`. Review dry-run output first.

## Safety

Default denylist excludes:

- private game/TCG paths;
- secrets and env files;
- `.git`, sessions, local tool state;
- vendors and pentest repos;
- `_archive`, `_ARCHIVAR`;
- node_modules, venvs, caches, build outputs.

`source_intake.py` is non-destructive. It inventories the known `Downloads`
ZIPs/docs and external `E:\` roots before any selective absorption work. Use
`--write --hash` only when updating the root intake register.
