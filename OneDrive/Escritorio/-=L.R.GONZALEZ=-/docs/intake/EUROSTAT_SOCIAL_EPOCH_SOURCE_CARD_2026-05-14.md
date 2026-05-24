# EUROSTAT_SOCIAL_EPOCH_SOURCE_CARD_2026-05-14

## ID

`eurostat_social_epoch_de_2018_2023`

## Nombre

Eurostat Social Epoch Fixture - Germany 2018-2023.

## Origen Oficial

Eurostat Statistics API, agency `ESTAT`.

## URL Oficial

- API introduction:
  `https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction`
- Statistics API base:
  `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/`
- Copyright and reuse notice:
  `https://ec.europa.eu/eurostat/help/copyright-notice`

## Fecha De Captura

`2026-05-14T16:05:00Z`

## Licencia / Terminos

Eurostat states that its website data can generally be reused, with exceptions
or dataset-specific notices. Reuse must preserve attribution and must not imply
European Commission or Eurostat endorsement. This card does not resolve legal
review for commercial redistribution.

## Tipo De Dataset

Official public statistical API snapshot, normalized into a local offline
fixture for GEODIA Social Observatory.

## Indicadores Elegidos

| id | label | unit | polarity | caveat |
|---|---|---|---|---|
| `une_rt_a` | Unemployment by sex and age - annual data | `PC_ACT` | negative | 2020 has `b` break-in-series status. |
| `tec00115` | Real GDP growth rate - volume | `CLV_PCH_PRE` | positive | 2022 and 2023 are provisional. |
| `demo_mlexpec` | Life expectancy by age and sex | `YR` | positive | 2023 has `b` break-in-series status. |

## CERTEZA

- The source is official Eurostat.
- API responses were public and required no credential.
- The local fixture is offline and hashable.
- Dataset labels, update timestamps and status flags were preserved in the
  fixture caveats.

## INFERENCIA

- The three selected indicators are compatible with the current GEODIA fixture
  schema.
- The fixture can rehearse a multi-source social epoch pipeline next to the
  World Bank Mexico fixture.
- Any scenario interpretation from the fixture is methodological rehearsal, not
  prediction.

## INCOGNITA

- Dataset-specific reuse restrictions still require review before public or
  commercial redistribution.
- Eurostat values can update because the API serves latest data, not historical
  API versions.
- Cross-country comparison with World Bank Mexico is not semantically valid
  without a separate harmonization design.

## BLOQUEO

- `publication_gate=BLOCK`.
- No public release, deploy, push, Gumroad, social posting or DNS action.
- No use as policy advice, forecast, electoral inference, personal inference or
  scientific proof.

## Claims

- Allowed: "official Eurostat data was captured into a small offline fixture for
  local GEODIA schema and pipeline QA."
- Blocked: "GEODIA predicts German social outcomes" or "Eurostat validates DUAT."

## Falsifiers

- Missing year in 2018-2023 range -> fixture FAIL.
- Missing publication gate or non-`BLOCK` gate -> fixture FAIL.
- Any source outside Eurostat API -> fixture FAIL.
- Any substantive report conclusion outside `INFERENCIA` -> REVIEW/BLOCK.
- Any API key, secret or private path in exportable metadata -> BLOCK.

## Destination

- Fixture:
  `research/geodia-social-observatory/fixtures/eurostat_social_epoch_2018_2023_fixture.json`
- Report:
  `qa_artifacts/release_validation/geodia-eurostat-report-2026-05-14.json`
- Comparison:
  `qa_artifacts/release_validation/geodia-multisource-comparison-2026-05-14.json`

## Trace

- Source card created by local agent in MEDIOEVO/CLAUDIO workspace.
- Captured from public Eurostat Statistics API endpoints.
- No credentials, private files, RPG/TCG material or publication actions used.

## publication_gate

`BLOCK`
