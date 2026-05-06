# FlujoCRM Clean Install Checklist 2026-05-01

Status: `CLEAN_MACHINE_QA_READY / CURRENT_USER_QA_PASS / NOT_EXECUTED_ON_CLEAN_VM`

2026-05-06 reconciliation: this is a clean-machine QA script, not a live local
execution queue. Open boxes are preserved as `clean-vm-pending` markers so the
global pending tracker does not count manual VM steps as locally executable
tasks. Current local recheck evidence is in
`docs/product/flujocrm-current-gate-recheck-2026-05-06.md`.

Target artifact:

- `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`
- SHA256: `f7ffa5a513207b15f81778a1e524eff110ff0ea638b893d15e44cd8d88e513c1`
- Signature status: `NotSigned`

2026-05-02 note: this hash supersedes the earlier 2026-05-02 QA installer
after the installed UI fix. Current-user install/launch/uninstall QA passed; a
clean Windows VM/user pass is still pending. See
`docs/product/flujocrm-current-user-install-qa-2026-05-02.md`.

This checklist is for a clean Windows user or VM. Do not mark FlujoCRM ready for
sale until this checklist is executed and evidence is saved.

## Preflight

- [clean-vm-pending] Use a Windows machine or VM without the development repo.
- [clean-vm-pending] Copy only `FlujoCRM-Setup-1.0.0.exe` to the machine.
- [clean-vm-pending] Verify SHA256 before install.
- [clean-vm-pending] Confirm whether Windows SmartScreen or unknown-publisher warning appears.
- [clean-vm-pending] Capture screenshot of any warning shown to users.

## Install

- [clean-vm-pending] Run installer as a normal user first.
- [clean-vm-pending] Confirm install completes without admin-only assumptions.
- [clean-vm-pending] Confirm desktop/start-menu shortcuts if generated.
- [clean-vm-pending] Launch FlujoCRM from the installed app.
- [clean-vm-pending] Confirm the app opens the complete dashboard UI, not the historical
  placeholder page.
- [clean-vm-pending] Record installed version/path.

## App Smoke

- [clean-vm-pending] App window opens.
- [clean-vm-pending] Create a contact.
- [clean-vm-pending] Edit the contact.
- [clean-vm-pending] Create a pipeline item.
- [clean-vm-pending] Create a follow-up task.
- [clean-vm-pending] Close and reopen app.
- [clean-vm-pending] Confirm data persists.
- [clean-vm-pending] Confirm persistence occurs in SQLite:
  `%APPDATA%\FlujoCRM\data\flujocrm.db`.
- [clean-vm-pending] Confirm `stage`, `value` and `last_activity` columns exist after launch.
- [clean-vm-pending] Test CSV import with a tiny synthetic file.
- [clean-vm-pending] Test local backup/export if available in UI.

## Privacy / Support

- [clean-vm-pending] Confirm app does not require login.
- [clean-vm-pending] Confirm no cloud account is required.
- [clean-vm-pending] Confirm support copy points to `medioevo.saga@gmail.com` for pilot/MVP.
- [clean-vm-pending] Confirm no private MEDIOEVO/Claudio/RPG references appear in the app UI.

## Uninstall

- [clean-vm-pending] Uninstall from Windows settings.
- [clean-vm-pending] Confirm app executable is removed.
- [clean-vm-pending] Decide and document whether local user data remains intentionally.

## Evidence To Save

- Install result summary.
- Windows version.
- SHA256 verification result.
- Screenshot of unsigned warning or no warning.
- Screenshot of opened app with synthetic data.
- Notes on any failed step.

## Release Decision

After execution, classify:

- `PASS`: installer can be used for first paid pilot after legal/listing review.
- `REVIEW`: minor issues or warning copy needs adjustment.
- `BLOCK`: install, launch, persistence or privacy issue found.
