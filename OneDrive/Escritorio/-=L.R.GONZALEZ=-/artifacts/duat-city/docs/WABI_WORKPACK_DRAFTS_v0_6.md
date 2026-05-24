# WABI_WORKPACK_DRAFTS v0.6

## Status

Wabi remains design-only.

- `execution_allowed: false`
- `real_apply_allowed: false`
- `sandbox_execution_allowed: false`
- no MCP call
- no localhost call
- no apply path

## Draft Types

- Asset Workpack Draft
- Graphics Upgrade Workpack Draft
- Physics Field Workpack Draft
- RPG Export Workpack Draft

## UI

`WabiPanel` now exposes buttons to generate each draft as JSON download. The buttons only serialize plans; they do not execute commands.

## Test

`src/tests/wabiWorkpackDraft.test.ts`
