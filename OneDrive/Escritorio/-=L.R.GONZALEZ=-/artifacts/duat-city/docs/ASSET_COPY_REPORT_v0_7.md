# ASSET COPY REPORT v0.7

Fingerprint: `DUAT-VISUAL-QA-ASSET-ALLOWLIST-v0.7`
Date: 2026-05-19

Destination:
- `public/reviewed-assets/v0_7/`

Manifest:
- `public/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json`

## Boundary

- Original sources were not moved, deleted, or modified.
- Copied assets remain internal review assets, not public-safe release assets.
- Manifest paths use root tokens such as `ROOT_BRAIN_OS`; no raw private Windows absolute path is exposed in public manifests.

## Hash Evidence

| File | SHA256 |
|---|---|
| `duat-icon-gate.svg` | `DE35C04A3EE2616C444E7EFA1ADCA19FFBFF69978C6473073D7EFBDD50C1CA19` |
| `duat-icon-geo.svg` | `C2DA4BD06A225BD85A9722A4F2C1359D6CDA9001CB9123FD87A0DFB8F48F58F3` |
| `duat-icon-memory.svg` | `42547798891F19B14AE03CF93359524E51C008A127BE9C468BC12A3FBEFC4203` |
| `duat-icon-multi-agent.svg` | `CA5231252B8752DA7B14F885AB1FCF4D08A5C2F1913A34116F5BE25CB29314D7` |
| `duat-icon-witness.svg` | `A6E80B90F5254498732337EF8FC48F704201821EA3D2EB692B42CEB1D8294D09` |
| `duat-icon-handoff.svg` | `D1C703EF2E7F971BE9E6EC9190387A390F62F64849523D6CD1622E1E77A53A2E` |
| `duat-icon-simulate.svg` | `72B38D0A24309D3C7BE1ED1A832EC36C92D6C618A88ABC5691A605966A009E48` |
| `duat-icon-repair.svg` | `93F410D77AE5DEEE8CE5FFB0594CCBEA27B58E3F2992FE2A3BA15233CC3BC046` |

## Integration

The app now loads `REVIEWED_ASSETS_MANIFEST.json` when present and resolves sprites through `src/graphics/spriteResolver.ts`. Missing assets fall back to procedural drawing.
