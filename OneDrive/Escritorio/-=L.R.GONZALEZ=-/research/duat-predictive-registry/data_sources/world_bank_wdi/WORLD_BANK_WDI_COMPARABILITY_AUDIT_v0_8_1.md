# World Bank WDI Comparability Audit v0.8.1

ComparabilityReview: REVIEW

## economy.real_growth_rate / NY.GDP.MKTP.KD.ZG

- title/name: GDP growth (annual %)
- unit: annual_percent_growth
- frequency: annual
- start_year: 1961
- end_year: 2024
- n_observations: 64
- missing years: []
- duplicate years: []
- source organization: Country official statistics, National Statistical Organizations and/or Central Banks;
National Accounts data files, Organisation for Economic Co-operation and Development (OECD);
Staff estimates, World Bank (WB)
- long definition: Gross domestic product is the total income earned through the production of goods and services in an economic territory during an accounting period. It can be measured in three different ways: using either the expenditure approach, the income approach, or the production approach. This indicator denotes the percentage change over each previous year of the constant price (base year 2015) series in United States dollars.
- aggregation/estimation note: National accounts revision/base-year risk; review before cross-domain comparison.
- modeled/estimate flags: ['external_or_multiple_source_organization', 'national_accounts_revision_risk']
- comparability risk: MED
- required transform before backtest: None in v0.8.1; review notes before any internal backtest.
- ComparabilityReview: REVIEW

## labor_market.unemployment_rate.total / SL.UEM.TOTL.ZS

- title/name: Unemployment, total (% of total labor force) (modeled ILO estimate)
- unit: percent_of_total_labor_force
- frequency: annual
- start_year: 1991
- end_year: 2025
- n_observations: 35
- missing years: []
- duplicate years: []
- source organization: ILO Modelled Estimates database (ILOEST), International Labour Organization (ILO), uri: https://ilostat.ilo.org/data/bulk/, publisher: ILOSTAT, type: external database, date accessed: January 17, 2026
- long definition: Unemployment refers to the share of the labor force that is without work but available for and seeking employment.
- aggregation/estimation note: Modeled estimate detected; keep review before backtest claims.
- modeled/estimate flags: ['modeled_estimate', 'external_or_multiple_source_organization']
- comparability risk: HIGH
- required transform before backtest: None in v0.8.1; review notes before any internal backtest.
- ComparabilityReview: REVIEW

## demography.life_expectancy_at_birth.total / SP.DYN.LE00.IN

- title/name: Life expectancy at birth, total (years)
- unit: years
- frequency: annual
- start_year: 1960
- end_year: 2024
- n_observations: 65
- missing years: []
- duplicate years: []
- source organization: World Population Prospects, United Nations (UN), uri: UN Population Division;
Statistical databases and publications from national statistical offices, National statistical offices, note: Derived from male and female life expectancy at birth from sources such as statistical databases and publications from national statistical offices.;
Demographic Statistics, Eurostat (ESTAT), note: Derived from male and female life expectancy at birth from sources such as Eurostat: Demographic Statistics.
- long definition: Life expectancy at birth indicates the number of years a newborn infant would live if prevailing patterns of mortality at the time of its birth were to stay the same throughout its life.
- aggregation/estimation note: No transform applied; metadata still requires review before benchmark interpretation.
- modeled/estimate flags: ['external_or_multiple_source_organization']
- comparability risk: MED
- required transform before backtest: None in v0.8.1; review notes before any internal backtest.
- ComparabilityReview: REVIEW

publication_gate: BLOCK
No public prediction claim is authorized.
