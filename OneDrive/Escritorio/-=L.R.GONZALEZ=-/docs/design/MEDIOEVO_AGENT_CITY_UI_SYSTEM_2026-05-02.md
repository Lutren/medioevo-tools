# MEDIOEVO_AGENT_CITY_UI_SYSTEM_2026-05-02

Decision aplicada: todas las apps vendibles se entienden como agentes especializados dentro de una ciudad MEDIOEVO/GEODIA.

## Principio

La UI no vende "una app suelta". Vende una estacion de trabajo operada por agentes. La tecnologia base puede ser open core; la experiencia integrada, los flujos, la curaduria, el soporte y los instaladores son el producto comercial.

## Shell comun

| region | uso |
|---|---|
| Topbar | marca, estado de sesion, gate, producto activo, link a website/Gumroad |
| Sidebar izquierda | edificios/agentes: Mercado, Mostrador, Oficina, Consola, Archivo, Laboratorio |
| Centro | tarea primaria del producto: CRM, inbox, documentos, dashboard, consola |
| Panel derecho | agente especializado, resumen, evidencia, proximas acciones |
| Footer/ledger | `APPROVE / REVIEW / BLOCK`, hash/reportes, ultimo smoke/test, version |

## Tokens visuales

Usar como base `claudio\website\public.css`, `store-theme.css`, `mission-control`, `Argus` y `Mini Office`.

| token | valor operativo |
|---|---|
| materiales | obsidiana, cobre, bronce, ambar, cyan/turquesa, hueso |
| fondo | oscuro productivo, bandas y superficies sin saturar |
| tipografia | display para marca/hero; sans/mono para herramientas; no texto gigante en paneles densos |
| radio | 8px maximo en cards/controles densos; 4px/8px para tools; evitar card dentro de card |
| iconos | lucide/react-icons donde exista; evitar texto cuando un icono claro funciona |
| estado | verde solo para validado, ambar para review, rojo para block, cyan para evidencia/observacion |

## Mapeo de agentes

| app/producto | edificio | agente UI | promesa permitida |
|---|---|---|---|
| FlujoCRM | Mercado | Agente Mercado | organiza clientes y pipeline local; no promete ventas garantizadas |
| Asistente Negocio | Mostrador | Agente Mostrador | prepara borradores para aprobacion humana; no envia automaticamente |
| Mini Office | Oficina | Agentes de escritorio | ayuda a producir piezas, docs y tareas; no reemplaza revision humana |
| Argus Desktop | Torre de control | Agente Consola | opera Claudio local con evidencia; no publica ni toca secretos sin gate |
| Wave FC | Archivo | Agente Curador Documental | ordena, audita y permite rollback; no altera originales sin accion reversible |
| DUAT Genesis | Laboratorio publico | Agente Laboratorio | simula/calibra con datos sinteticos; no prueba cosmologia/fisica |
| GEODIA OMNIS | Sociometro privado | Agente Sociometro | explora escenarios sociales sinteticos privados; no predice sociedades reales |
| NEUROSTATE UI | Observatorio | Agente Estado | visualiza estado de agentes; no diagnostica personas |
| Website | Plaza publica | Narrador comercial | explica productos, bundles y rutas; no filtra runtime privado |
| RPG | Ciudad privada | Fuente de identidad visual | inspira lenguaje, pero assets/lore no salen del carril privado |

## Reglas de implementacion

- Cada app debe tener un modo "agente": nombre, rol, permisos, inputs, outputs, gate y evidencia visible.
- Todo flujo de accion externa muestra ActionGate antes de ejecutar.
- Las pantallas comerciales deben ser densas y utiles, no landing pages internas.
- La website puede usar heroes visuales, pero las apps deben priorizar operacion repetible.
- No usar assets del RPG/TCG en open-source ni en productos publicos sin aprobacion explicita y ficha de derechos.

## Primeras conversiones

1. FlujoCRM: conservar estructura CRM, cambiar acento SaaS generico a `Agente Mercado`, ledger de evidencia y link a privacidad local.
2. Asistente Negocio: mantener GEODIA visual, reforzar panel de borradores y aprobacion humana.
3. Mini Office: normalizar agentes como edificios de oficina y separar funciones premium.
4. Argus Desktop: declarar como shell principal de ciudad de agentes, con estado de runtime y private-boundary visible.
5. Website: crear indice de "Agentes MEDIOEVO" que conecte open core, demos y productos pagos.
