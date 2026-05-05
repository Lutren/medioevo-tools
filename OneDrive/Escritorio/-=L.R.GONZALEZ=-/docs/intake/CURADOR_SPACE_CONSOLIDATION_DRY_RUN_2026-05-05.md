# Curador Space Consolidation Dry Run - 2026-05-05

Ficha tecnica del pase global seco para consolidar documentos, programas,
proyectos y residuos. No se ejecutaron borrados ni movimientos en este pase,
porque el gate de host actual devolvio `BLOCK`.

## Estado

| campo | valor |
|---|---|
| Estado PSI | CERTEZA para inventario generado; INFERENCIA para utilidad hasta ficha individual |
| Decision SETO | REVIEW |
| ActionGate host | BLOCK |
| Razon principal | CPU alta, memoria alta, proceso dominante CPU, residuo alto |
| Accion permitida ahora | documentar, clasificar, preparar mapa |
| Accion bloqueada ahora | borrar/mover documentos, publicar, mutar firewall, ejecutar limpieza amplia |

## Artefactos generados

| artefacto | sha256 | lectura |
|---|---|---|
| `qa_artifacts/release_validation/curador-space-dry-run-2026-05-05.json` | `A17A6BC6AFA59C1FDB71A0225D8D0F6D5C7AC2080DF99277A20D414F0BC9FEDA` | inventario seco global |
| `qa_artifacts/release_validation/duplicate-name-dry-run-2026-05-05.json` | `259084B09C5919137A4C185CD454567F36C8AA32FA5C596688F41718DDDD81E8` | duplicados por nombre dentro del workspace principal |
| `qa_artifacts/pending/pending_review_2026-05-05.json` | `F5C5A3BAB30F0373A3E50AB380B7A811F251C8B788294ACDEEF64D7BB5836238` | pendientes actuales |

Dos artefactos de intentos largos quedaron en tamano cero y no se usan como
evidencia: `duplicate-hash-dry-run-2026-05-05.json` y
`curador-audit-2026-05-05-sponsors-cleanup.json`. Son candidatos a limpieza
generada, pero se dejan registrados hasta el siguiente gate.

## Cobertura

Roots incluidos en el dry-run:

- Workspace `-=L.R.GONZALEZ=-`.
- `Downloads`.
- `Desktop`.
- `E:`.

El scan fue acotado y conservador. Los roots se solapan, asi que algunas rutas
aparecen repetidas; el reporte no debe usarse para borrar sin normalizar ruta,
hash y copia canonica.

## Lectura cuantitativa

| categoria | conteo | decision |
|---|---:|---|
| Large files | 47 | REVIEW: priorizar ZIP/EXE/product bundles con hash y destino canonico |
| Archives/installers | 32 | REVIEW: no borrar hasta ficha por producto/version |
| Generated/cache dirs | 120 | REVIEW: muchos son `.git`; no tratarlos como cache eliminable |
| Document name duplicates | 120 grupos | REVIEW: nombre igual no implica duplicado exacto |
| Pending active markdown dedup | 1731 | REVIEW: backlog activo, no limpieza |
| Claudio master open | 83 | REVIEW: pendiente de fase Claudio |

## Hallazgos principales

1. Hay paquetes grandes repetidos de Asistente Negocio entre Desktop archivado,
   Claudio product release y QA final package. Son candidatos fuertes para
   consolidacion, pero requieren SHA256 por archivo, ficha de version y una copia
   canonica elegida antes de borrar.
2. Los grupos `README.md`, `SKILL.md`, `package.json`, `LICENSE` e `index.html`
   aparecen muchas veces. Esto es normal en monorepos, vendors y subproyectos;
   queda bloqueado cualquier borrado por nombre.
3. `.skills/ruflo`, `.skills/hooks-mastery`, vendors, `.git` y bundles de
   producto dominan el ruido. Deben separarse entre vendor canonico, vendor
   duplicado, build regenerable y source privado.
4. Los documentos de auditoria y fichas nuevas siguen siendo evidencia activa
   hasta que exista un indice canonico que los reemplace.
5. El gate de host actual esta en `BLOCK`; cualquier limpieza agresiva ahora
   aumentaria riesgo operacional.

## Reglas de consolidacion

| tipo | decision por defecto | condicion para borrar |
|---|---|---|
| Duplicado exacto con hash igual | CANDIDATE_DELETE | copia canonica verificada + ficha + registro en `DELETED_OR_ARCHIVED.md` |
| Build/cache regenerable | CANDIDATE_DELETE | ruta allowlist + prueba de regenerabilidad + gate APPROVE |
| ZIP/EXE de producto | CANDIDATE_ARCHIVE | version canonica elegida + hashes + destino release/offload |
| Documento repetido por nombre | KEEP/REVIEW | solo borrar si hash igual o reemplazo por ficha firmado |
| Vault bruto con contenido util | REPLACE_BY_FICHA | ficha completa + mapa de migracion + hash |
| RPG/TCG/private/canon completo | BLOCK | nunca a publicacion; mover solo con instruccion privada especifica |
| Secret/session/local state | BLOCK | no publicar, no mover a open lanes |

## Lote siguiente cuando el host gate cambie a APPROVE/REVIEW bajo

1. Hash exacto de los ZIP/EXE de Asistente Negocio que aparecen en mas de una
   ruta.
2. Elegir una sola ruta canonica: `apps/commercial/asistente-negocio/qa_artifacts`
   o `releases/`, segun manifest de producto.
3. Registrar cada duplicado exacto en `DELETE_CANDIDATES.md` con hash, bytes,
   copia canonica y razon.
4. Ejecutar borrado solo de duplicados exactos de build/release ya reemplazados,
   no de fuentes ni documentos.
5. Repetir el mismo metodo para paquetes de Desktop archivado y `Downloads`.

## Decision final de este pase

No borrar ahora. El cierre responsable es dejar el mapa, evidencias y gates
para que el siguiente agente o siguiente loop pueda eliminar solo lo que ya
cumpla hash, ficha, ruta canonica y gate.
