# GODOT_VS_CUSTOM_ENGINE_ANALYSIS

## RUTA A: GODOT-FIRST

Beneficios:
- Buen editor para 2D, 2.5D y 3D.
- Luces, shaders, skeletal 2D, tilemaps y escenas maduras.
- Export web disponible.
- Camaras/cutscenes/cinematic movement mas directo.

Costos/riesgos:
- No se encontro proyecto Godot activo en rutas auditadas.
- Export web puede ser pesado para CPU/RAM baja.
- Riesgo de mezclar sim-core con renderer/editor.
- Integracion con Wabi/cache/cloud/local docs menos natural que web.

Uso recomendado:
- Cliente opcional o laboratorio visual avanzado.
- No nucleo canonico de DUAT hasta que `DUAT_SIM_CORE` sea estable.

## RUTA B: CUSTOM WEB ENGINE

Beneficios:
- Ya existe `artifacts/duat-city`.
- Alineado con target web-first.
- Canvas low tier es barato y portable.
- DOM/React sirve para inspectors/HUD.
- Worker/cache/cloud integration es directa.

Costos/riesgos:
- Hay que madurar renderer propio.
- Aun no hay WebGL/WebGPU principal.
- Sim/render mezclan demasiado con React state.
- Sprite lighting avanzado falta.

Uso recomendado:
- Fallback principal si Godot no justifica peso.

## RUTA C: HIBRIDA

Beneficios:
- Sim-core compartido.
- Web-first ligero como cliente principal.
- Godot puede existir sin secuestrar el nucleo.
- Forge queda separado y puede emitir specs.
- Mejor mantenibilidad para Wabi/DUAT/portal/publicacion.

Costos/riesgos:
- Requiere disciplina de contratos.
- Hay que evitar duplicar render logic entre clientes.

## Decision

Ruta principal: C HIBRIDA.

Ruta fallback: B CUSTOM WEB ENGINE.

Godot queda en REVIEW hasta tener:
- `WorldState` estable.
- Replay ledger.
- Prueba web export en hardware bajo.
- Comparativa real de memoria/FPS contra Canvas/WebGL.

