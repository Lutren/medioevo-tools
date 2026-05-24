# Research Local Validation Sweep 2026-05-06

Estado: `INTERNAL_RESEARCH_LOCAL_OK / NO_PUBLICATION`.

Este barrido cierra evidencia local para `research/geodia-social-observatory`.
No habilita venta, prediccion publica, publicacion externa, deploy, push ni uso
de datos externos. El producto queda como investigacion interna.

## Gate

- Root pending review: `active_dedup=0`, `claudio_open=0`.
- Claudio pending review: `active_dedup=0`, `claudio_open=0`.
- Claudio workpack: `selected_items=[]`, COMMS `ok=true`,
  `action_gate=BLOCK` para carriles externos.
- Host aislado final, sin comandos Python paralelos:
  `2026-05-06T22:41:17Z`, `LIMPIO/APPROVE`, `R=0.387`,
  `Phi_eff=0.597`, `lambda_sat=0.805`, dominante `r_io`.

Nota operativa: no ejecutar `host_observacionista.py` en paralelo con otros
comandos Python. La muestra paralela puede observar esos procesos hermanos como
`proceso_dominante_cpu` y degradar el gate de forma no representativa.

## Target

- Producto: `geodia-social-observatory`.
- Clasificacion: `INTERNAL_RESEARCH`.
- Lane: `internal-research`.
- Fuente: `research/geodia-social-observatory`.
- Nota de manifest: MVP privado/local para simulacion de epocas sociales; sin
  publicacion ni claims predictivos.

## Evidencia

Comandos:

```powershell
Get-ChildItem -Force research
rg --files research\geodia-social-observatory
python tools\release\product_manifest.py --product geodia-social-observatory --hash
python tools\release\scan_secrets.py --product geodia-social-observatory --json
python -m pytest tests -q
python tools\host_observacionista.py --no-write
```

Resultados:

- Manifest: `file_count=21`, `blocked_count=0`, `excluded_count=20`,
  `total_bytes=91526`.
- Secret scan focal: `count_reported=0`.
- Tests locales: `15 passed in 0.34s`.
- Validacion de cierre: JSON parse OK, `SESSION_FINGERPRINT.json` parse OK,
  `git diff --check` focal sin errores.
- Scan del reporte: `count_reported=0`.
- Scan del QA artifact: `count_reported=1` por `denylist path`, sin secreto de
  contenido detectado.
- No se tocaron rutas privadas de videojuego ni TCG.
- No se hizo red, push, deploy, Gumroad, LinkedIn ni publicacion.

## Decision

GEODIA queda validado como paquete local de investigacion interna. Puede usarse
para demos locales y evolucion de laboratorio con evidencia, pero no para claims
publicos ni distribucion externa sin un ActionGate target-specific y revision de
lenguaje, datos, licencia y publicacion.

## Proxima accion verificable

Validar `research/obs-info-kernel` con el mismo patron focal: inventario,
secret scan por ruta, tests locales si existen y reporte separado.
