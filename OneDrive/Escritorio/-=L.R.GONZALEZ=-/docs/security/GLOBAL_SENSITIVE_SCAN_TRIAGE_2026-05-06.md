# Global Sensitive Scan Triage - 2026-05-06

Estado: `REVIEW_REQUIRED / NO_PUBLICATION`

Este paquete convierte el scan global en cola de triage sin imprimir valores de
secretos. No autoriza borrado, movimiento, publicacion ni rotacion automatica.

## Evidencia

Comando ejecutado:

```powershell
python tools\release\scan_secrets.py --json --limit 500
```

Resultado resumido:

| metrica | valor |
|---|---:|
| `count_reported` | 224 |
| `truncated_at` | 500 |
| `default_workspace_scan` | true |

Resumen por razon:

| razon | count |
|---|---:|
| `secret-like content markers` | 166 |
| `secret-like filename` | 37 |
| `denylist path` | 34 |

Prefijos principales:

| prefijo | count |
|---|---:|
| `-=MEDIOEVO=-/-=LIBROS/claudio` | 126 |
| `-=MEDIOEVO=-/CLAUDIO - researchs/GEODIA` | 26 |
| `runtime/curador_seto/source_archive` | 20 |
| `tools/claw-code/rust` | 12 |
| `-=MEDIOEVO=-/-=LIBROS/-=CEREBRO=-` | 7 |
| `-=MEDIOEVO=-/-=LIBROS/llm-wiki` | 6 |
| `-=MEDIOEVO=-/CLAUDIO - researchs/futuro` | 5 |
| `E:/MEDIOEVO_ASSETS/editorial_web_img` | 2 |
| `E:/MEDIOEVO_ASSETS/Assets` | 2 |

## Lectura Operativa

- El workspace completo no es apto para publicacion directa.
- El hallazgo global no invalida targets locales ya validados por allowlist y
  scan focalizado con `count_reported=0`.
- La publicacion debe seguir siendo por target, con denylist y path scrub.
- Los prefijos bajo `E:/` requieren frontera manual; no se deben copiar,
  publicar ni mover desde este pase.

## Cola De Triage

| cola | criterio de cierre | accion segura ahora |
|---|---|---|
| contenido con marcadores | confirmar placeholder, fixture o secreto real sin imprimir valores | revisar por target antes de release |
| nombre sensible | clasificar falso positivo, ejemplo saneado o archivo real sensible | mantener fuera de release |
| denylist path | confirmar que sigue excluido de artefactos | no publicar por glob amplio |
| rutas externas | confirmar si son referencias, junctions o material externo | no tocar fuera del workspace |

## Gate

ActionGate global: `REVIEW`.

Bloquea:

- publicar el workspace completo;
- generar ZIPs por glob amplio;
- subir carpetas mixtas;
- mover o borrar hallazgos sin plan de migracion;
- imprimir tokens, claves, cookies, `.env` o credenciales.

Permite:

- scans focalizados por target;
- manifests allowlist;
- paquetes locales no publicos;
- documentacion de revision sin valores sensibles.
