# World Bank Mexico Social Epoch Source Card - 2026-05-14

Source:

- World Bank Indicators API
- Country: Mexico (`MEX`)
- Period: `2018:2023`
- API documentation: `https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation`
- Terms reference: `https://www.worldbank.org/en/about/legal/terms-and-conditions`

Indicators:

- `SL.UEM.TOTL.ZS`: Unemployment, total (% of total labor force) (modeled ILO estimate)
- `NY.GDP.PCAP.KD.ZG`: GDP per capita growth (annual %)
- `SP.DYN.LE00.IN`: Life expectancy at birth, total (years)

Classification:

- `OFFICIAL_DATA_API_FIXTURE`
- Lane: `DUAT / GEODIA / offline simulation`
- Intake action: `HASHED_OFFLINE_FIXTURE`
- Public boundary: `NO_PUBLIC_CLAIMS_BEYOND_SOURCE_AND_METHOD`
- Runtime boundary: `OFFLINE_ONLY`
- Claim boundary: `INFERENCIA`

Evidence:

- World Bank API metadata returned `lastupdated=2026-04-08`.
- Fixture path:
  `research/geodia-social-observatory/fixtures/world_bank_mexico_2018_2023_fixture.json`
- Fixture SHA256:
  `FC05D1C424C04EAE43CE1BE045455C8FEAF56A4241A8E97A6074253EDD63B1BC`
- Scenario report:
  `qa_artifacts/release_validation/geodia-world-bank-mexico-report-2026-05-14.json`
- Report content SHA256:
  `d49732eecc0fa39807f4a7260d9e167f9f3dba34301f1b745945e55508ef7ef2`
- Retrieval used public API endpoints and no API key.
- API terms require respecting dataset-specific terms, attribution and no
  implied endorsement.

Decision:

- `APPROVE`: local offline fixture, local scenario report and backtest.
- `REVIEW`: publication, commercial redistribution or claims beyond
  reproducible local method.
- `BLOCK`: treating the report as prediction, policy advice, scientific proof
  or World Bank endorsement.

Next Action:

Use this fixture as the first local real-data rehearsal only. Choose the next
dataset after reviewing whether World Bank or Eurostat gives the cleanest
license and attribution path.
