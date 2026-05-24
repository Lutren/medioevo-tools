# DUPLICATE_AND_OVERLAP_REPORT

## Overlap critico

### DUAT engine vs DUAT physics/light zips

- Motor vivo: `artifacts/duat-city`.
- Fuente candidata: `duat-physics-light-engine-v1.3.0.zip`.
- Estado: overlap tecnico util, pero adopcion cruda BLOCK. Extraer solo ideas o tests con ficha.

### DUAT world sim vs GEODIA social observatory

- `artifacts/duat-city`: mundo visual e interactivo.
- `research/geodia-social-observatory`: simulacion sintetica determinista tipo Smallville.
- Estado: complementariedad real. Deben compartir contratos, no duplicar logica.

### Wabi engine creator vs DUAT simulator

- `wabi_sabi/engine/*`: creador/Forge.
- `artifacts/duat-city`: simulador/visualizador.
- Riesgo: que DUAT absorba el builder Lovable y pierda foco.
- Decision: separar por contrato `ForgeProjectSpec`.

### Light engines dentro de duat-city

- `src/graphics/lightEngine.ts`: light map simple para Canvas.
- `src/light/lightPropagation.ts`: propagacion local mas rica.
- `src/iso3d/vermeerIsoLighting.ts`: direccion artistica Vermeer/iso.
- Riesgo: tres fuentes paralelas de verdad.
- Accion: unificar bajo `LightBudget` y `LightingBackend`.

### Multimodal Wabi vs glomo/cross-modal DUAT

- `wabi_sabi/core/multimodal_intake.py`: captura y metadata.
- `artifacts/duat-city/src/brain/crossModalTransduction.ts`: resumen simple de canales.
- Riesgo: llamar "multimodal" a lo que hoy es metadata y resumen.
- Accion: benchmark GLOMO antes de afirmarlo como mejora.

## Duplicados/legacy detectados

- Gran cantidad de ZIPs bajo `BRAIN_OS\09_ARCHIVE_REVIEW` y `99_INBOX_UNSORTED`.
- `Duat-Fibmob-Lab.zip` contiene `.git` y 32143 entradas: fuente pesada, no integrable sin intake.
- Zips Lovable repetidos: usar solo como fuentes de Forge con ficha.

## Recomendacion

Mantener canon operativo:
- Una verdad de simulacion: `DUAT_SIM_CORE`.
- Una verdad de render web: `DUAT_WEB_RENDERER`.
- Una verdad de creador: `MEDIOEVO_FORGE`.
- Una verdad de control: `WABI_SABI_CONTROL_PLANE`.

