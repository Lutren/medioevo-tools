# E Drive Publication Boundary - 2026-05-02

Fuente: inspeccion curador en solo lectura. No se editaron, movieron, borraron ni
crearon archivos en `E:`.

## Clasificacion

| ruta | decision | uso permitido |
|---|---|---|
| `E:\Medioevo_RPG` | CANON privado activo | arquitectura resumida y contratos public-safe; no publicar repo, runtime, escenas, scripts, assets ni datos |
| `E:\Medioevo_RPG\docs\HORMIGUERO_GAME_BRIDGE_CONTRACT_2026-04-29.md` | ficha tecnica resumible | contrato de eventos/esquemas sin codigo ni runtime |
| `E:\Medioevo_RPG\docs\WORLDPULSE_BRIDGE_2026-04-29.md` | ficha tecnica resumible | puente local acotado tipo `WorldPulseBridge` sin estados privados |
| `E:\Medioevo_RPG\docs\OBSERVACIONISMO_EXPERIENCIA_ENCARNADA_2026-04-29.md` | resumen publico minimo | patron de diseno jugable, sin claims cientificos |
| `E:\Medioevo_RPG\docs\private` | NO publicar | protocolo privado, manifiestos, trazas, auditorias RC y distribucion privada |
| `E:\-=Medioevo=-` | archivo editorial/comercial | manifiestos/checksums; no GitHub |
| `E:\-=Medioevo=-\-=Libros` | canon editorial privado/comercial | solo muestras aprobadas, no libros completos |
| `E:\MEDIOEVO` | descartar de publicacion | contiene seguridad, claves, sesiones, tor y backups |
| `E:\MEDIOEVO_ASSETS` | NO GitHub | solo manifiesto y revision de licencia |
| `E:\MEDIOEVO_AUDIO_LIBRARY` y `E:\Suno Downloads` | NO GitHub | requiere revision de licencia/uso |
| `E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate` | duplicado/offload | no usar como fuente canon |
| `E:\Download`, `E:\downloads` | sin hallazgos relevantes | no se hallaron coincidencias utiles a profundidad 2 |

## No Subir

- `E:\Medioevo_RPG\assets`, `builds`, `runtime`, `.godot`, `tools\godot`.
- `E:\Medioevo_RPG\docs\private`.
- `E:\Medioevo_RPG\data\story_bible.json`, `content`, `campaign`,
  `dlcs`, `lore`, `assets`, `audio`.
- Scripts, escenas, prompts generados, manifiestos de assets, hashes, builds y
  cualquier puente runtime del RPG.
- `E:\MEDIOEVO\seguridad`, `E:\MEDIOEVO\sesiones`, `E:\MEDIOEVO\tor`.
- Offloads, ZIPs Gumroad, APKs, modelos/voz, libros completos, portadas,
  radiocinema, TCG y material editorial no aprobado.

## Contratos Publicos Posibles

- `WorldPulseBridge`: puente local de eventos acotados, zonas/lectura viva y
  modificadores de combate, loot o encuentros descritos sin extraer codigo.
- `Hormiguero Game Bridge`: contrato privado de integracion por eventos
  (`threat`, `observation`, `conway`, `light`, `gravity`) y regla explicita de
  no mezclar runtimes.
- Observacionismo gameplay: mecanica diegetica y microeventos, sin claims
  cientificos publicos ni copia de formulas, codigo o datos privados.
- Validadores Godot: mencionar validacion por escenas `Validate*.tscn`, sin
  publicar scripts ni datos.
- DUAT Geodia living world: solo como contrato privado para memoria, rutina,
  facciones, rumores, quests y WorldPulse; no publicar ingenieria.
- DUAT Genesis: carril publico separado con simulacion sintetica y sin material
  de `E:\Medioevo_RPG`.

## Riesgo Principal

La contaminacion de repos MIT/open-source con codigo, assets o lore propietario
del RPG es el riesgo mayor. El segundo riesgo es filtrar secretos o sesiones de
`E:\MEDIOEVO`. El tercero es confundir offloads o archivos editoriales
comerciales con fuente publicable.
