# DUAT Extraction For Claudio And Apps - 2026-05-02

Estado: `LOCAL_IMPLEMENTATION_BACKLOG / NO_PUBLIC_GEODIA_ENGINEERING`.

Este documento define que se extrae de DUAT para Claudio, el entorno y las apps
sin mezclar carriles.

## Utilidad extraible

| funcion | destino | estado |
|---|---|---|
| `status` | Claudio local / Argus | read-only, ActionGate si toca runtime |
| `simulate` | DUAT Genesis publico y labs internos | sintetico, reproducible |
| `report` | Claudio, apps, docs de evidencia | JSON con claims `DEMO_ONLY` o `SYNTHETIC_ONLY` |
| `falsify` | claim register, QA, papers | antes de publicar copy o paper |
| `source_registry` | curador de datos | hashes, licencias, provenance |
| `residue/phi_eff` | Observacionismo/PSI-IA | metricas auxiliares, no diagnostico |
| `world_pulse` | RPG/Hormiguero privado | privado, no GitHub |

## Por app

| app | integracion segura |
|---|---|
| Argus Desktop | panel Laboratorio: reportes, falsadores, estado local y private boundary visible |
| FlujoCRM | no integrar DUAT en core; solo evidencia/gate para claims comerciales |
| Asistente Negocio | usar ActionGate y reportes; no automatizar envios |
| Mini Office | templates de reporte/curaduria; no claims 24/7 autonomos |
| Website | mostrar DUAT Genesis como lab publico; describir Geodia solo como investigacion privada |
| Hormiguero | ciudad viva y `CityEvent`; Geodia privado alimenta eventos internos |
| RPG | `LivingWorldEvent`, NPC memory, schedule, intent, rumores y quests privados |

## Bloqueos

- No copiar DUAT Geodia a `packages/open-dev`.
- No publicar MCP DUAT con acciones de escritura/red/browser.
- No vender prediccion social, neurologica, biologica o fisica.
- No mezclar RPG/TCG/canon privado con Genesis.

## Orden de implementacion

1. Usar `packages/open-dev/duat-genesis` para demos publicas y pruebas.
2. Crear adaptador Claudio read-only: `status/report/falsify`.
3. Integrar Argus como panel de laboratorio, no como motor autonomo.
4. Mantener Geodia en privado para Hormiguero/RPG.
5. Publicar solo despues de scan, tests, claims boundary y ActionGate.
