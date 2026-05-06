# Hormiguero y RPG: ciudad viva y command center

Fecha: 2026-04-29

## Verdad operativa local

Hormiguero Mission Control ya tiene base real: Flask, `index.html`, endpoints de ciudad y estado, `core/medioevo_registry.py`, `core/medioevo_runtime.py`, ObservaStack y governance. Lo que existe es una primera capa visual; todavia no es una consola viva comparable a un command center moderno.

El RPG/TCG activo vive en `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg` y sigue siendo privado. No debe moverse ni publicarse desde esta linea. El proyecto tiene muchas pantallas y datos (`HubScreen`, `BuildingScreen`, `StoryScreen`, `Battle*`, minijuegos, `characters.ts`, `buildings.ts`, `quest-pool.ts`), pero la lectura rapida muestra corrupcion textual en codigo/documentos (`muyact`, `muyturn`, `[elichicado]`) y `package-lock.json` contiene nombres corruptos de paquetes. Antes de conectar IA/NPCs, el RPG necesita un pase de sanidad/build.

## Lectura de referencias

### Flipbook / FlippingBook

Fuente: https://flippingbook.com/es/blog/news/flippingbook-online-reimagined-publication

Lo importante no es solo el efecto de pasar pagina. Lo importante es que reimaginaron un documento como experiencia: texto seleccionable, pagina enlazable, grosor visible, sombras, encuadernado, logo adaptable, animacion mas suave y optimizacion de carga.

Aplicacion:

- Hormiguero debe tener paginas de estado navegables por tiempo: hoy, ayer, ultimo boot, ultimo incidente, ultimo release.
- Cada snapshot debe ser enlazable y comparable.
- El mapa ciudad debe sentirse tactil: capas, profundidad, sombras sutiles, transiciones y estados historicos.
- El RPG puede usar el flipbook como codex vivo: libro, cartas, misiones y recuerdos no como PDFs, sino como paginas interactivas con anclas al mundo.

### Omnara, Maestro, Tide Commander, AgentMC

Fuentes:

- https://docs.omnara.com/how-it-works
- https://runmaestro.ai/
- https://tidecommander.com/
- https://agentmc.ai/

Patron comun:

- sesiones y workspaces;
- agentes visibles;
- control remoto/mobile;
- playbooks y planes;
- estado persistente por agente;
- historial resumible;
- tareas, boards y calendario;
- comandos en vivo;
- contexto restante;
- infraestructura representada como objetos del mapa.

Aplicacion:

- Hormiguero necesita una pantalla principal tipo ciudad/RTS con edificios, agentes, servidores, bases de datos, colas, jobs y rutas.
- Cada agente debe tener ficha persistente: rol, edificio, objetivo, tarea actual, herramientas permitidas, contexto, riesgo, ultima accion, bloqueo.
- Debe existir una Alcaldia/Boss que no sea decorativa: delega por ownership, contexto y archivo tocado.
- El modo mobile debe permitir supervision, aprobaciones y respuesta a bloqueos, no solo lectura.

### AutoGen Studio, CrewAI, LangSmith Studio, SnapLogic Agent Visualizer

Fuentes:

- https://www.microsoft.com/en-us/research/publication/autogen-studio-a-no-code-developer-tool-for-building-and-debugging-multi-agent-systems/
- https://docs.crewai.com/
- https://docs.langchain.com/langsmith/studio
- https://docs.snaplogic.com/agentcreator/agentvis/agentcreator-agent-visualizer-about.html

Patron comun:

- workflows declarativos;
- grafo visual;
- playground/sesion;
- galeria de componentes;
- vista simple de chat y vista profunda de grafo;
- memoria, threads, asistentes y runs;
- time travel/debug de estado;
- diagrama mas log paso a paso;
- soporte para agentes anidados y tool calls paralelos.

Aplicacion:

- Hormiguero debe tener tres modos sincronizados:
  - Ciudad: vista espacial de GEODIA/Hormiguero.
  - Grafo: nodos, edges, tool calls, dependencias y estado.
  - Bitacora: trace paso a paso, eventos, errores, input/output y decisiones.
- La ciudad no reemplaza al debug. La ciudad es el mapa; el grafo y la bitacora son la verdad operativa.
- El RPG puede consumir el mismo grafo como sistema de quests: cada edge puede convertirse en rumor, ruta, mision, bloqueo o evento del mundo.

### LangSmith, Datadog LLM Observability, AgentPulse

Fuentes:

- https://docs.langchain.com/langsmith/home
- https://docs.datadoghq.com/llm_observability/
- https://www.avepoint.com/products/agentpulse

Patron comun:

- trazas, spans, errores, latencia y costo;
- evaluaciones y datasets;
- monitoreo de calidad;
- seguridad, ownership, inventario y riesgo;
- paneles por agente, workflow y app;
- gobierno de agentes, no solo ejecucion.

Aplicacion:

- Hormiguero necesita ObservaStack visible: traces, costo/tiempo si aplica, errores, retries, evaluaciones, rutas calientes y drift.
- Cada edificio debe mostrar salud, actividad, dueños, tools permitidas, datos tocados y riesgo.
- El RPG puede transformar observabilidad en diegesis: anomalas del mundo, edificios en alarma, facciones bloqueadas, misiones emergentes y consecuencias.

### Pixel Agents, AI Agent Visualizer, command centers ambiguos

Fuentes:

- https://pixelagents.net/
- https://docs.snaplogic.com/agentcreator/agentvis/agentcreator-agent-visualizer-about.html

Varios nombres de la lista son ambiguos o no tienen una fuente oficial clara en esta pasada (`Starlene Command Center`, algunos usos de `Agent Control`, algunos `AI Agent Visualizer`). La leccion util no depende de una marca: agentes visuales sirven si estan conectados a estado real; si solo son avatares decorativos, empeoran la verdad operativa.

Aplicacion:

- Insectos/agentes visibles, si, pero cada insecto debe mapear a un proceso, tarea, trace o NPC real.
- No mostrar vida falsa. Si no hay runtime, mostrar ciudad degradada.
- No llenar la pantalla de telemetria interna incomprensible; mostrar capas con profundidad progresiva.

### Convai, NVIDIA ACE, SIMA 2, Smallville / Generative Agents

Fuentes:

- https://convai.com/
- https://developer.nvidia.com/ace-for-games
- https://deepmind.google/discover/blog/sima-2-an-agent-that-understands-and-acts-in-3d-virtual-worlds/
- https://arxiv.org/abs/2304.03442

Patron comun:

- NPCs conversacionales y embodied agents;
- memoria, planificacion, reflexion y conducta emergente;
- percepcion del entorno;
- acciones dentro de mundos 3D;
- personajes que reaccionan a jugador, lugar, estado y recuerdos;
- Smallville muestra que una simulacion social creible necesita observaciones, memoria, planificacion y reflexion, no solo dialogo.

Aplicacion:

- El RPG no debe empezar por "chat con NPC". Debe empezar por `WorldState + Memory + Schedule + Intent + Action`.
- Cada NPC debe tener:
  - ubicacion;
  - rutina;
  - memoria;
  - relaciones;
  - objetivo;
  - miedo/deseo/bloqueo;
  - ultima observacion;
  - accion siguiente.
- Hormiguero y RPG deben compartir un `city_event_ledger`: lo que hace un agente en Hormiguero puede convertirse en evento narrativo o rumor del RPG; lo que pasa en RPG puede alimentar mapas, lore y pruebas.

## Direccion recomendada

No construir otro dashboard. Construir dos superficies del mismo sistema:

1. Hormiguero: ciudad operativa para controlar agentes, tareas, runtime, documentos, releases y riesgos.
2. RPG: ciudad jugable donde esos mismos principios aparecen como NPCs, edificios, misiones, memoria social y consecuencias.

La unidad comun debe ser:

```txt
CityEvent
  id
  timestamp
  layer: runtime | agent | doc | build | qa | story | rpg
  actor_id
  building_id
  target_id
  action
  status
  risk
  summary
  evidence_uri
```

## Hormiguero: pantallas que faltan

- `Ciudad`: mapa principal 2.5D/RTS con edificios, agentes, rutas y alertas.
- `Grafo`: workflow real de agentes, tool calls, dependencias y estados.
- `Bitacora`: timeline filtrable de eventos y traces.
- `Agentes`: roster con ficha persistente, permisos, contexto y tarea actual.
- `Edificios`: departamentos, owner, salud, archivos, endpoints, tareas, riesgos.
- `Playbooks`: flujos reproducibles para boot, QA, release, editorial, RPG, web.
- `ObservaStack`: traces, evaluaciones, fallos, costo/latencia cuando exista, drift.
- `Flipbook`: snapshots navegables del sistema por fecha/hito.
- `Mobile Control`: aprobaciones, bloqueos, estado critico y mensajes de agentes.

## RPG: sistemas que faltan

- Sanidad de fuente/build antes de cualquier IA.
- Mapa de ciudad coherente con GEODIA/Hormiguero, no menu de pantallas aisladas.
- NPC scheduler inspirado en Smallville: rutina, memoria, reflexion, relacion y evento.
- Quest graph desde `CityEvent`: cada evento puede abrir rumor, combate, carta, edificio, puzzle o investigacion.
- Codex flipbook: historia y canon como objeto jugable.
- Puente privado con Hormiguero: importar solo eventos public-safe o internos aprobados; nunca filtrar secretos, prompts, logs sensibles ni private game assets.
- Observabilidad de juego: eventos de combate, progreso, economia, bugs y balance como trazas.
- DUAT Geodia privado como motor de mundo vivo: memoria de NPC, schedule,
  intent, facciones, rumores, economia y WorldPulse. DUAT Genesis queda fuera de
  este puente y se usa solo como sandbox publico sintetico.

## Primer roadmap ejecutable

### Sprint 1: verdad de estado

- Crear `city_event_ledger` en Hormiguero.
- Normalizar payloads `/api/state`, `/api/buildings`, `/api/agents`, `/api/city-registry`.
- Agregar endpoint `/api/city/events`.
- Agregar fixture/test con 20 eventos sinteticos.

### Sprint 2: command center real

- Dividir UI en tabs: Ciudad, Grafo, Bitacora, Agentes, Edificios, Flipbook.
- Implementar filtros por capa, edificio, agente, severidad y fecha.
- Cada visual debe venir de datos reales o mostrar estado offline/degradado.

### Sprint 3: RPG bridge privado

- Reparar corrupcion textual/build del RPG.
- Crear contrato privado `rpg_city_bridge_v1.json`.
- Exportar desde Hormiguero solo eventos safe/test.
- En RPG, convertir eventos en rumors/quests sin tocar public release lanes.

### Sprint 4: NPC social simulation

- Crear modelo `NPCMemory`, `NPCSchedule`, `NPCRelation`, `NPCIntent`.
- Simular 10 NPCs en 3 edificios.
- Mostrar memoria/reflexion en debug interno, no como texto tecnico al jugador.

### Sprint 5: visual polish

- Pasar de dashboard a ciudad con profundidad: capa superficie, subsuelo, torres, rutas, eventos, interiores.
- Mantener legibilidad profesional: no saturar, no telemetria incomprensible en primer plano.
- QA visual desktop/mobile con screenshots y checks de no solape.

## Decision de producto

El Hormiguero debe ser el "sistema nervioso" y el RPG la "proyeccion jugable". Si ambos comparten eventos, edificios, agentes y memoria, el ecosistema deja de ser una coleccion de pantallas y empieza a comportarse como ciudad viva.
