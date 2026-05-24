# Legal And Human Gate Packet 2026-05-06

Estado: `LOCAL_PACKET_READY / HUMAN_OR_LEGAL_GATE`

Este paquete cierra la preparacion local de los tres pendientes globales que
estaban vivos antes de formalizarlos como gates humano/legales. No marca esos
gates como aprobados y no autoriza publicacion, push, deploy, Gumroad, redes,
borrado ni movimientos.

## Pendientes Cubiertos

| pendiente | estado local | cierre requerido |
|---|---|---|
| Scan global limpio | `NO`, scan global sigue reportando hallazgos secret-like | remediacion/rotacion/exclusion con revision humana |
| Licencia global decidida | `LEGAL_REVIEW_REQUIRED` | decision legal por capa o por target |
| Worktree limpio o cambios acotados | `NO`, hay cambios activos y concurrentes | coordinacion de agentes/commits por scope |

## Evidencia Actual

| verificacion | resultado |
|---|---|
| `python tools\release\pending_review.py --write --quiet` | snapshot final `active_dedup=0`, `claudio_open=0`; los 3 gates quedaron fuera del backlog ejecutable local |
| `python tools\release\scan_secrets.py --json --limit 500` | `count_reported=223`, `truncated_at=500` |
| `python tools\release\scan_secrets.py --path apps\local\wabi-sabi --json` | `count_reported=0` |
| `cd apps\local\wabi-sabi; python -m pytest tests -q` | `57 passed in 19.74s` |
| `python COMMS\tools\validate_seto_comms.py --json` | `PASS`, `errors=[]` |
| `python tools\host_observacionista.py --no-write` | `2026-05-06T18:56:11Z`, `CONTAMINADO/REVIEW`, `lambda_sat=0.921`, dominante `r_cpu` |

## Decision Operativa

Los tres pendientes restantes no son ejecutables locales seguros. El cierre
correcto es:

- mantenerlos como gates vivos;
- usar allowlists por target en lugar de publicar el workspace completo;
- no limpiar secretos por borrado automatico;
- no decidir una licencia global por inferencia;
- no forzar un worktree limpio cuando hay cambios activos de otros agentes.

## Gate 1 - Scan Global

El workspace completo contiene rutas con nombres o contenido secret-like. Algunas
son secretos reales, otras son falsos positivos o docs historicos, pero el
resultado bloquea cualquier paquete por glob amplio.

Ruta segura actual:

- publicar solo por target allowlist;
- ejecutar scan focalizado por target;
- excluir `-=MEDIOEVO=-/-=LIBROS/.discord_token`,
  `-=MEDIOEVO=-/-=LIBROS/.youtube_token.pickle`, `.env`, tokens,
  credenciales, vendors, builds, archives y privados;
- rotar secretos reales si alguna vez se compartieron fuera del host local;
- no copiar valores de secretos a docs.

## Gate 2 - Licencia Global

No existe licencia global segura para todo el workspace. El root sigue como
`LEGAL_REVIEW_REQUIRED` porque mezcla open-dev, comerciales, libros, canon,
private game, vendors y archivos de terceros.

Ruta segura actual:

- paquetes open-dev: licencia por paquete, actualmente MIT donde ya esta
  decidido;
- apps comerciales, paid packs y bundles: propietario/comercial salvo decision
  explicita;
- libros/canon/editorial: all rights reserved;
- game/TCG/RPG: privado/propietario;
- vendors: licencia upstream, no rebranding;
- cualquier target nuevo requiere `LICENSE`, `NOTICE` si aplica y claim boundary.

## Gate 3 - Worktree

El worktree no esta limpio. Hay cambios de Wabi-Sabi, COMMS, publishing, tools y
otros carriles. Algunos son de este pase y otros son concurrentes.

Ruta segura actual:

- no usar `git add .`;
- no revertir cambios de otros agentes;
- cerrar por scope y evidencia;
- si se pide commit, stagear solo rutas verificadas del scope;
- antes de publicar, crear staging limpio por allowlist.

## Criterio De Cierre Futuro

| gate | criterio minimo |
|---|---|
| scan global | `count_reported=0` o decision explicita de no usar workspace global como release target |
| licencia global | dictamen por capa o confirmacion de que no habra licencia global |
| worktree | `git status` limpio o cambios acotados a un target con manifest |

## Resultado

No quedan acciones locales reversibles que puedan convertir estos tres gates en
`done` sin una decision humana/legal o un scope de release nuevo. El backlog
ejecutable local queda en cero; el estado de estos gates es
`BLOCKED_BY_HUMAN_OR_LEGAL_GATE`, con evidencia local lista.
