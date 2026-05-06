# Hormiguero Ciudad Viva

Fecha: 2026-04-29

## Estado implementado

`apps/hormiguero_mission_control` es la base operativa para la ciudad viva. La primera pantalla ya no se trata como dashboard generico: representa GEODIA/Hormiguero como una ciudad 2.5D con edificios, rutas, agentes visibles, capas y panel de detalle.

La UI consume el runtime real. Si el backend no responde, la ciudad queda degradada/offline y no inventa metricas.

Endpoints conectados por la pantalla y el smoke test:

- `/api/health`
- `/api/state`
- `/api/buildings`
- `/api/agents`
- `/api/city-registry`
- `/api/observastack/snapshot`
- `/api/governance/status`

## Metafora canonica

GEODIA no es una carpeta ni un panel de administracion. Es una ciudad operativa:

- edificios: departamentos del `city_registry`;
- insectos/agentes: operadores en movimiento entre edificios;
- superficie: estado visible de trabajo;
- subsuelo: memoria, auditoria y rutas internas;
- torres/watchtowers: vigilancia, gobernanza y observacion;
- rutas: conexiones entre departamentos;
- eventos: pulsos de actividad detectados por el runtime.

## Capas de flipbook

La pantalla expone cinco estados narrativos-operativos:

| capa | uso |
|---|---|
| superficie | mapa principal y edificios activos |
| subsuelo | infraestructura, memoria y procesos de soporte |
| torres | observacion, gobierno y control de estado |
| rutas | movimiento entre departamentos |
| eventos | actividad reciente y pulsos de sistema |

## Limites

- No convierte el videojuego ni el TCG en fuente publica.
- No copia lore privado ni manuscritos completos.
- No reemplaza el runtime de Claudio/Gemma que esta en otra linea de trabajo.
- No declara salud completa desde `ok=true`; la pantalla debe distinguir runtime disponible, degradado y offline.

## Pendiente

- QA visual recurrente desktop/mobile despues de cada cambio de UI.
- Mejorar arte de edificios con assets aprobados si se decide publicar esta superficie.
- Mantener los paneles existentes como vistas secundarias y no romper sus endpoints.
