# DUAT License And Comparability Review v0.1

publication_gate: BLOCK

LicenseTermsScan remains REVIEW pending human/legal review.

## Sources And Fixtures

- Fixture: `research/geodia-social-observatory/fixtures/eurostat_social_epoch_2018_2023_fixture.json`
  - Source: eurostat_sdmx
  - URL: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/
  - Geography: DE
  - Period: 2018-2023
  - License status: Eurostat reuse notice applies; attribution required; no endorsement implied; dataset-specific terms require review before publication or commercial redistribution
  - Publication gate: BLOCK
- Fixture: `research/geodia-social-observatory/fixtures/inegi_mexico_social_2018_2023_fixture.json`
  - Source: INEGI
  - URL: https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/tabulados/enoe_indicadores_estrategicos_2005_2026_mensual.xlsx
  - Geography: MEX
  - Period: 2018-2023
  - License status: REVIEW_TERMS_DOCUMENTED
  - Publication gate: BLOCK
- Fixture: `research/geodia-social-observatory/fixtures/world_bank_mexico_2018_2023_fixture.json`
  - Source: world_bank_indicators
  - URL: https://api.worldbank.org/v2/country/MEX/indicator
  - Geography: MEX
  - Period: 2018-2023
  - License status: World Bank data terms apply; attribution and no-endorsement required; review before publication or redistribution
  - Publication gate: BLOCK

## Comparability

### economy.real_growth_rate
- Objective: DUAT_GEODIA_HARMONIZED_INDICATOR_ONE_STEP_FORECAST_v0_1
- Review status: REVIEW_MIXED_OR_WEAK_COMPARABILITY
- world_bank_indicators / NY.GDP.PCAP.KD.ZG / MEX
  - Frequency: annual
  - Years: 2018-2023
  - Units: annual_percent -> annual_percent_growth
  - Transformation: raw percent growth preserved; semantic equivalence held for review
  - Comparability: REVIEW
  - Missing values: none observed in fixture benchmark rows
  - Caveats: GDP per capita growth is not the same semantic unit as aggregate real GDP volume growth.; Use only as economic-growth REVIEW until a stricter harmonization rule exists.
- eurostat_sdmx / tec00115 / DE
  - Frequency: annual
  - Years: 2018-2023
  - Units: CLV_PCH_PRE -> annual_percent_growth
  - Transformation: raw percent growth preserved; semantic equivalence held for review
  - Comparability: REVIEW
  - Missing values: none observed in fixture benchmark rows
  - Caveats: Eurostat value is real GDP volume growth, not per-capita growth.; 2022 and 2023 are provisional in the Eurostat fixture.
### labor_market.unemployment_rate.total
- Objective: DUAT_GEODIA_LABOR_MARKET_UNEMPLOYMENT_ONE_STEP_FORECAST_v0_1
- Review status: REVIEW_STRONG_PROXY_NOT_EXACT
- world_bank_indicators / SL.UEM.TOTL.ZS / MEX
  - Frequency: annual
  - Years: 2018-2023
  - Units: percent -> percent_of_labor_force
  - Transformation: unit_alias_only; raw values preserved; negative polarity can be sign-inverted only for technical scoring
  - Comparability: STRONG_PROXY
  - Missing values: none observed in fixture benchmark rows
  - Caveats: Provider definition and population scope may differ from Eurostat.; This class does not permit ranking Mexico against Germany.
- eurostat_sdmx / une_rt_a / DE
  - Frequency: annual
  - Years: 2018-2023
  - Units: PC_ACT -> percent_of_labor_force
  - Transformation: unit_alias_only; raw values preserved; negative polarity can be sign-inverted only for technical scoring
  - Comparability: STRONG_PROXY
  - Missing values: none observed in fixture benchmark rows
  - Caveats: Eurostat age code is Y15-74 and 2020 has break-in-series status.; This class does not permit ranking Germany against Mexico.
- INEGI / INEGI_ENOE_TASA_DESOCUPACION_ANNUAL_MEAN / MEX
  - Frequency: annual_mean_from_monthly
  - Years: 2018-2023
  - Units: percent_of_economically_active_population -> percent_of_labor_force
  - Transformation: annual arithmetic mean from 12 official monthly ENOE percentage observations per year; raw monthly workbook preserved by SHA256
  - Comparability: STRONG_PROXY
  - Missing values: none observed in fixture benchmark rows
  - Caveats: INEGI ENOE is survey-derived and is not an EXACT semantic match to provider-modelled or Eurostat unemployment definitions.; 2020-2022 carry ENOE/ETOE/ENOE_N continuity caveats from the source workbook.; This class does not permit ranking Mexico, Germany, providers or sources.
### demography.life_expectancy_at_birth.total
- Objective: DUAT_GEODIA_DEMOGRAPHY_LIFE_EXPECTANCY_ONE_STEP_FORECAST_v0_1
- Review status: REVIEW_STRONG_PROXY_NOT_EXACT
- world_bank_indicators / SP.DYN.LE00.IN / MEX
  - Frequency: annual
  - Years: 2018-2023
  - Units: years -> years
  - Transformation: unit_alias_only; raw years preserved
  - Comparability: STRONG_PROXY
  - Missing values: none observed in fixture benchmark rows
  - Caveats: Provider method may differ from Eurostat.; No causal interpretation is allowed.
- eurostat_sdmx / demo_mlexpec / DE
  - Frequency: annual
  - Years: 2018-2023
  - Units: YR -> years
  - Transformation: unit_alias_only; raw years preserved
  - Comparability: STRONG_PROXY
  - Missing values: none observed in fixture benchmark rows
  - Caveats: 2023 has break-in-series status in the Eurostat fixture.; No causal interpretation is allowed.

## What Is Missing For PASS

- Human/legal review of source-specific redistribution terms.
- Approved public-safe attribution text per source.
- Explicit decision that derived fixture redistribution is allowed.
- More historical folds before any stronger public-facing language.
