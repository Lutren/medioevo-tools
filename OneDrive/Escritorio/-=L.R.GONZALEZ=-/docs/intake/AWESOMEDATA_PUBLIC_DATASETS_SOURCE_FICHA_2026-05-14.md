# Awesomedata Awesome Public Datasets Source Ficha - 2026-05-14

Source:

- `https://github.com/awesomedata/awesome-public-datasets`

Classification:

- `PUBLIC_DATASET_CATALOG_INDEX`
- Lane: `DUAT / GEODIA / source discovery`
- Intake action: `CATALOG_INDEX_ONLY`
- Public boundary: `PUBLIC_METADATA_ONLY`
- Runtime boundary: `NO_LIVE_FETCH_NO_RAW_DATA_COPY`
- License boundary: `CATALOG_MIT_DOWNSTREAM_DATASETS_REVIEW_REQUIRED`

Evidence:

- Repository observed as public GitHub repository `awesomedata/awesome-public-datasets`.
- Repository purpose: topic-centric public data-source list.
- Repository license observed: MIT for the catalog repository.
- Repository README states that many listed datasets are free, but some are not.
- Local implementation target:
  - `research/geodia-social-observatory`: allowlisted as `dataset_catalog_index_only`.
  - `packages/open-dev/duat-genesis`: represented as a public `SourceCard`.

Decision:

- `KEEP`: useful discovery index for future DUAT/GEODIA simulation sources.
- `APPROVE`: local metadata registration, source-card creation and policy tests.
- `REVIEW`: selecting any linked dataset for live or offline simulation use.
- `BLOCK`: copying the catalog wholesale into packages, treating linked datasets as license-cleared, or using dataset presence as proof of social/physical claims.

Next Action:

Create one source card per selected dataset with upstream URL, license, retrieval date, payload hash, role, claim boundary and fixture path before using it in DUAT/GEODIA simulations.
