# DUAT / GEODIA Downloads Intake - 2026-05-02

Estado: `INTAKE_VERIFICADO / NO_PUBLICAR / NO_BORRAR_FUENTES`.

Este intake convierte las fuentes nuevas de `Downloads` en evidencia operativa. No
importa texto crudo como canon, no copia codigo bruto al arbol publicable y no
autoriza publicacion externa. Las fichas tecnicas derivadas deben reemplazar la
lectura dispersa, pero las fuentes originales se conservan hasta una pasada
separada de limpieza con respaldo y aprobacion explicita.

## Fuentes verificadas

| fuente | tamano | lineas / miembros | SHA256 | lectura |
|---|---:|---:|---|---|
| `C:\Users\L-Tyr\Downloads\duat_v4_final (1).html` | 50,255 | 1,311 lineas | `1C7DCF9CE872A7FE129DE04E0CC26FDA4F323E4C83D7740B70C2BCB7809215A2` | DUAT v4.2 HTML lab, UI experimental Penrose/Hameroff + Observacionismo |
| `C:\Users\L-Tyr\Downloads\seis.txt` | 64,575 | 1,295 lineas | `6F4E938C279E456820DE2047F1448EA7FEC7FB1C546A2EF3CA0BEC9ED3800CC4` | teoria de fisica sin Newton / MCR / claims falsables |
| `C:\Users\L-Tyr\Downloads\duat_for_integration_v0_1.zip` | 44,936 | 30 miembros | `31973B4C6F3B129E804B0B10F796274D07CC4950097C7909EFA1E3EFE5A9FB55` | FOR kernel, bridges Genesis/GEODIA y local AI |
| `C:\Users\L-Tyr\Downloads\duat_geodia_v0_2.zip` | 70,244 | 34 miembros | `CF30B264305E1B1E42CD119A0F401D7734F841C4D9885D2468BAEC9758994D2E` | DUAT Geodia v0.2, engine, API, UI, falsadores |
| `C:\Users\L-Tyr\Downloads\cinco.txt` | 264,610 | 3,190 lineas | `5442248014702015FBFD90CEC7184C7E4E59838AFA1F38382DC07C2532BECB91` | formalizacion EML, reemplazo F=ma, Landauer, vacios cientificos |
| `C:\Users\L-Tyr\Downloads\el cuarto.txt` | 133,449 | 3,265 lineas | `DE8A88A33FA3315897B9F504A5999C6C9F1C03B4E8BCC6F8D4150301AB77A0F4` | ObservacionistAgent, motor DUAT/GEODIA, falsadores, MCP |
| `C:\Users\L-Tyr\Downloads\y tegnicas, para poder procesar la.txt` | 113,633 | 2,031 lineas | `8E84BF41F51FB97772EF1D675940284A9B6DE4BA67B2078F5CB3E84D0A66825D` | recomendaciones tecnicas para datos, proxies, EML, escalamiento |
| `C:\Users\L-Tyr\Downloads\backup.txt` | 139,310 | 2,303 lineas | `05E05688B537103CD5612558E8C119C8C1E753ADECD108EFA2AFCA9152D8739E` | vacios DUAT, metabolismo, quadtree, UI multiescala, generative connector |
| `C:\Users\L-Tyr\Downloads\¡Claro, amigo! Vamos a extender el.txt` | 65,631 | 1,318 lineas | `AC133AA9544B7E7BCF3605B364E932117D17227E99EB2176F9A2988057FE7CD2` | DUAT MCP Server v1.0, herramientas locales, estado PSI |
| `C:\Users\L-Tyr\Downloads\duat_omnis_v1.py` | 9,327 | 230 lineas | `3C0E0B075635050592B3DA749127B18873354AED4BF5637B1456E30A7533D5D5` | simulador social autonomo DUAT-OMNIS |

## ZIPs

`duat_for_integration_v0_1.zip` contiene `README.md`, `requirements.txt`,
`for_kernel/core.py`, `bridges/genesis_runtime.py`,
`bridges/geodia_for_adapter.py`, `local_ai/intelligence_kernel.py`, demos y
tests. Tambien contiene 12 entradas `__pycache__` o `.pyc`, que no deben copiarse
a ningun paquete publico ni interno versionado.

`duat_geodia_v0_2.zip` contiene `README.md`, `requirements.txt`,
`run_server.py`, el paquete `duat/`, UI en `ui/`, ejemplos y tests. Tambien
contiene 10 entradas `__pycache__` o `.pyc`, que deben excluirse de cualquier
hand-port.

## Evidencia de ejecucion temporal

Los ZIPs se extrajeron solo a temporal:
`C:\Users\L-Tyr\AppData\Local\Temp\medioevo_duat_intake_20260502_160736`.

Resultados:

| paquete | comando | resultado |
|---|---|---|
| `duat_for_integration_v0_1` | `python -m pytest tests -q` | `3 passed in 0.73s` |
| `duat_geodia_v0_2` | `python -m pytest tests -q` | `1 passed in 0.33s` |

Esto prueba que los paquetes son ejecutables en modo local basico. No prueba
validez cientifica, prediccion social, seguridad de publicacion, ni licencia
final.

## Proyectos identificados

| proyecto | certeza | uso propuesto | bloqueo |
|---|---|---|---|
| DUAT Geodia v0.2 | hay ZIP, README, tests y modulos | fuente candidata para `research/geodia-social-observatory` | solo hand-port despues de scan, sin `.pyc`, sin claims predictivos |
| DUAT + FOR v0.1 | hay ZIP, README, tests y bridges | laboratorio de metricas relacionales y adaptadores | claims de fisica quedan `RESEARCH_ONLY/BLOCK` |
| DUAT MCP Server | hay TXT largo con API/herramientas | contrato Claudio local read-only primero | acciones externas pasan por ActionGate |
| DUAT-OMNIS | hay script standalone | fixture/demo de simulacion social | no es modelo validado de humanos |
| DUAT v4.2 HTML Lab | hay app HTML | referencia visual/laboratorio | claims Penrose/Hameroff/neuro quedan bloqueados |
| EML | aparece en fuentes teoricas y codigo | operador experimental para tests sinteticos | no se vende como ley fisica |
| MCR / fisica sin Newton | aparece en `seis.txt` y `cinco.txt` | dossier teorico con falsadores | no entra a copy publico |
| GEODIA colmena / ciudad.matrix | aparece como arquitectura | backlog UI/runtime de ciudad de agentes | sin prediccion garantizada |

## Regla de curaduria

- `CERTEZA`: rutas, hashes, lineas, miembros ZIP y tests temporales.
- `INFERENCIA`: donde puede vivir cada proyecto dentro del workspace.
- `HIPOTESIS`: EML, MCR, FOR, reemplazos de Newton, dinamicas sociales.
- `ESPECULACION`: cosmologia, conciencia, neurofisica o prediccion no probada.
- `BLOQUEADO`: claims publicos fuertes, publicacion externa, MCP con acciones
  destructivas, fuentes reales sin licencia/provenance.
