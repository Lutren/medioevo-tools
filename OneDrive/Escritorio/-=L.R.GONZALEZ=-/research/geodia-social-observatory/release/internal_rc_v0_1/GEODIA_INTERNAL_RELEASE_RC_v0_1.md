# GEODIA Internal Release RC v0.1

release_id: GEODIA_INTERNAL_RELEASE_RC_v0.1
timestamp_utc: 2026-05-14T22:17:54Z
publication_gate: BLOCK
action_gate: APPROVE_LOCAL_DOCS_ONLY
public_safe_package_created: false
external_publication: false

## Estado general

GEODIA Harmonization RC v0.1 queda como release candidate interno local. El modulo tiene tres fixtures oficiales capturados o documentados, armonizacion reproducible offline y wrapper QA local. La publicacion externa sigue bloqueada hasta revision humana/legal.

## Objetivo del modulo

GEODIA harmonization crea una capa tecnica para leer fixtures oficiales offline, aplicar un crosswalk de indicadores y emitir registros con clases de comparabilidad. Su objetivo es conservar trazabilidad, polaridad, caveats, hashes y gate de publicacion.

## Que hace

- Ejecuta armonizacion offline desde fixtures congelados.
- Usa crosswalk versionado con `STRONG_PROXY`, `REVIEW` y `NOT_COMPARABLE`.
- Mantiene `publication_gate=BLOCK` en artefactos de salida.
- Genera reportes QA reproducibles.
- Conserva trazabilidad de INEGI ENOE con archivo bruto, manifest y hash.

## Que NO hace

- No genera ranking entre Mexico, Alemania u otros territorios.
- No genera predicciones electorales, sociales o personales.
- No afirma causalidad politica o social.
- No convierte proxies en equivalencias exactas.
- No autoriza publicacion, venta, despliegue ni redistribucion publica.

## Comandos reproducibles

```powershell
python -m pytest

python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty

python research/geodia-social-observatory/scripts/run_harmonization_qa.py --offline --pretty --fixtures research/geodia-social-observatory/fixtures/world_bank_mexico_2018_2023_fixture.json research/geodia-social-observatory/fixtures/eurostat_social_epoch_2018_2023_fixture.json research/geodia-social-observatory/fixtures/inegi_mexico_social_2018_2023_fixture.json
```

## Fixtures incluidos

| Fuente | Fixture | SHA256 | Estado |
| --- | --- | --- | --- |
| World Bank | `research/geodia-social-observatory/fixtures/world_bank_mexico_2018_2023_fixture.json` | `fc05d1c424c04eae43ce1be045455c8feaf56a4241a8e97a6074253edd63b1bc` | official fixture, BLOCK |
| Eurostat | `research/geodia-social-observatory/fixtures/eurostat_social_epoch_2018_2023_fixture.json` | `fef2ce8e3b523a48c0675646705033465bbce788eac8b532c18e0c3461098ad7` | official fixture, BLOCK |
| INEGI ENOE | `research/geodia-social-observatory/fixtures/inegi_mexico_social_2018_2023_fixture.json` | `ce8ab13f7c8b89a7e5ce7fbf1d01a00332ca78f78863fa31af76eb8a0fb7abd4` | official fixture, BLOCK |

INEGI raw XLSX SHA256: `0add6e88da29b8f5eddcafe889f94c353edaab8a9d5ec272565a55c84cae8bd5`

## Source cards

- INEGI: `research/geodia-social-observatory/fixtures/source_intake/inegi/INEGI_SOURCE_CARD.md`
- World Bank: `docs/intake/WORLD_BANK_MEXICO_SOURCE_CARD_2026-05-14.md` si existe en la copia local.
- Eurostat: `docs/intake/EUROSTAT_SOCIAL_EPOCH_SOURCE_CARD_2026-05-14.md`.

## QA summary

- Ultima base recibida: 53 tests passed.
- Wrapper QA default: PASS recibido; se reejecuta en este cierre.
- Wrapper QA three-fixture: PASS recibido; se reejecuta en este cierre.
- Scans recibidos: SecretScan, BoundaryCheck, SourceAttributionScan, LicenseTermsScan, ForbiddenClaimsScan, PrivatePathScan, FixtureFabricationScan y PublicationGateScan PASS.

## Publication gate

`publication_gate=BLOCK` permanece obligatorio. Este RC interno no crea paquete public-safe ni publica artefactos externos.

## License status

`TERMS_DOCUMENTED_HUMAN_REVIEW_REQUIRED`. Los terminos de World Bank, Eurostat e INEGI estan documentados para revision, pero no se declara aprobacion comercial ni redistribucion publica final.

## Limitaciones

- El crosswalk actual es tecnico y conservador, no una equivalencia metodologica completa.
- INEGI desempleo se conserva como `STRONG_PROXY`, no `EXACT`.
- Economia permanece en `REVIEW` cuando la equivalencia fuente/unidad/frecuencia no esta cerrada.
- La robustez con mas fuentes sigue pendiente.

## Proxima accion humana

Revisar `qa_artifacts/release_validation/geodia-human-review-packet-2026-05-14.md` y decidir entre: crear paquete public-safe sanitizado, mantener GEODIA como modulo interno o ampliar a cuarto fixture oficial.
