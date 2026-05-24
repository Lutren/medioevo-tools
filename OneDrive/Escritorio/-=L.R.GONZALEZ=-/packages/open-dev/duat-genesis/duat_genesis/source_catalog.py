from __future__ import annotations

from .source_card_schema import SourceCard


PUBLIC_SOURCE_CARDS: tuple[SourceCard, ...] = (
    SourceCard(
        id="awesomedata_public_datasets",
        title="Awesomedata Awesome Public Datasets",
        source_type="catalog_index",
        boundary="public",
        claims=(
            "Catalog index for discovering candidate public datasets.",
            "Linked datasets require separate license, provenance and claim review.",
        ),
        evidence=(
            "https://github.com/awesomedata/awesome-public-datasets",
            "Repository license: MIT for the catalog.",
        ),
        risks=(
            "Linked datasets may have different terms, stale links or non-public restrictions.",
            "Using catalog presence as proof of dataset validity would overclaim the source.",
        ),
        next_action="Use as discovery index only; create one source card per selected dataset before simulation use.",
    ),
    SourceCard(
        id="world_bank_indicators",
        title="World Bank Indicators API",
        source_type="official_data_api",
        boundary="public",
        claims=("Candidate source for public indicator snapshots.",),
        evidence=("https://api.worldbank.org/",),
        risks=("Review current World Bank data terms before publication or redistribution.",),
        next_action="Create hashed offline fixture before any DUAT simulation claim.",
    ),
    SourceCard(
        id="imf_data",
        title="IMF Data APIs",
        source_type="official_data_api",
        boundary="public",
        claims=("Candidate source for macroeconomic indicator snapshots.",),
        evidence=("https://data.imf.org/",),
        risks=("Review IMF dataset/API terms before publication or redistribution.",),
        next_action="Create hashed offline fixture before any DUAT simulation claim.",
    ),
    SourceCard(
        id="oecd_api",
        title="OECD API",
        source_type="official_data_api",
        boundary="public",
        claims=("Candidate source for social and economic indicator snapshots.",),
        evidence=("https://sdmx.oecd.org/",),
        risks=("Review OECD reuse and attribution terms for the exact dataset.",),
        next_action="Create hashed offline fixture before any DUAT simulation claim.",
    ),
    SourceCard(
        id="eurostat_sdmx",
        title="Eurostat SDMX API",
        source_type="official_data_api",
        boundary="public",
        claims=("Candidate source for European statistical snapshots.",),
        evidence=("https://ec.europa.eu/eurostat/api/",),
        risks=("Review Eurostat reuse and attribution rules for the exact dataset.",),
        next_action="Create hashed offline fixture before any DUAT simulation claim.",
    ),
    SourceCard(
        id="owid_grapher",
        title="Our World in Data Grapher API",
        source_type="data_api",
        boundary="public",
        claims=("Candidate source for public grapher datasets.",),
        evidence=("https://ourworldindata.org/grapher/",),
        risks=("OWID can aggregate third-party datasets; original provider terms must be reviewed.",),
        next_action="Record the original provider and license before any DUAT simulation claim.",
    ),
    SourceCard(
        id="gdelt_doc_2",
        title="GDELT DOC 2.0",
        source_type="media_signal_api",
        boundary="public",
        claims=("Candidate source for media-narrative signals only.",),
        evidence=("https://api.gdeltproject.org/api/v2/doc/doc",),
        risks=("Media coverage is not raw social fact and needs corroboration.",),
        next_action="Use only as INFERENCIA narrative signal with corroborating sources.",
    ),
    SourceCard(
        id="fred_api",
        title="FRED API",
        source_type="official_data_api",
        boundary="unknown_review",
        claims=("Candidate source for economic time series after API-key handling review.",),
        evidence=("https://api.stlouisfed.org/",),
        risks=("Live use requires API key handling and no-endorsement notice.",),
        next_action="Keep in REVIEW until key storage, attribution and fixture hashing are defined.",
    ),
)


def get_public_source_cards() -> tuple[SourceCard, ...]:
    return PUBLIC_SOURCE_CARDS
