# Lobby De Alejandria - Ultimos Documentos 2026-05-06

Estado: `ABSORCION_LOCAL_EJECUTADA / RED_STEALTH_BLOCK`

## Ruta De Entrada

```text
C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria
```

## Destino Operativo

Lo que se pone en el Lobby se ficha en `docs\intake` y, si se absorbe, la
fuente original sale del Lobby hacia:

```text
runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06
```

El README queda en el Lobby como contrato operativo.

## Ultimos 3 Documentos Detectados

| orden | documento | estado | destino |
|---:|---|---|---|
| 1 | `escaner sigiloso.txt` | `ABSORBIDO_ARCHIVO_FRIO` | `runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06\20_curaduria_seto\0C7CDDAA915D42C4_escaner-sigiloso.txt` |
| 2 | `ESTADO.txt` | `ABSORBIDO_ARCHIVO_FRIO` | `runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06\03_osit_qg_research_boundary\369DCD91A9BB70DC_estado.txt` |
| 3 | `Bloque para agregar a tu prompt act.txt` | `ABSORBIDO_ARCHIVO_FRIO` | `runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06\02_wabi_sabi_osit\1CD663AEED468CAA_bloque-para-agregar-a-tu-prompt-act.txt` |

## Ejecucion Del Nuevo Documento

- Curador preflight: `NEEDS_FICHA_BEFORE_USE`.
- Absorcion: `docs\intake\lobby_alejandria_escaner_sigiloso_2026-05-06_REPORT.md`.
- Manifest: `docs\intake\lobby_alejandria_escaner_sigiloso_2026-05-06_MANIFEST.json`.
- Retiro seguro: `1` fuente archivada, `1` README conservado.
- SHA256 fuente: `0C7CDDAA915D42C43D2303583A3E0B737BEEB53A54F574EE382AEFFD371E3D4E`.
- QA: `qa_artifacts\release_validation\network-observer-escaner-sigiloso-2026-05-06.json`.

## Aplicacion Segura Al Sistema

El fragmento propone Scapy, ARP/broadcast, LAN/CIDR y lenguaje de sigilo. No se
ejecuto como scanner. Se aplico como politica defensiva ya integrada:

- `docs\security\NETWORK_OBSERVER_POLICY_2026-05-06.md`.
- `tools\security_network_observer.py`.
- `library\modules\network_observer_defensive.json`.

Decision del clasificador:

- `decision=BLOCK`.
- `network_executed=false`.
- `risk_flags=stealth_or_evasion_intent, raw_packet_or_arp_discovery, lan_or_cidr_target, unsupported_network_mode`.
- `fingerprint=NETWORK_OBSERVER_B4C8853A771BC286`.

## Verificacion

```powershell
python -B -m pytest tests\test_security_network_observer.py -q
python -B tools\matrix\validate_library.py --json
```

Resultados:

- `5 passed in 0.31s`.
- Matrix library validator: `PASS`, `errors=[]`, `warnings=[]`.
- Scan focal de este resumen: `count_reported=0`.
- Scan del QA artifact: `count_reported=1` por `denylist path`; no se
  imprimieron valores ni se detecto secreto en el contenido del resumen.
