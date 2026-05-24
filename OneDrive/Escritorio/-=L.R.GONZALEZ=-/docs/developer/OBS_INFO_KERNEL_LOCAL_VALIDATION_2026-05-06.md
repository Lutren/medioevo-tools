# obs-info-kernel Local Validation 2026-05-06

Estado: `INTERNAL_RESEARCH_LOCAL_OK / DO_NOT_PUBLISH`.

Este barrido cierra evidencia local para `research/obs-info-kernel`. No cambia
su frontera: sigue como laboratorio interno, sin release open-source, sin claims
cientificos publicos y sin publicacion externa.

## Target

- Ruta: `research/obs-info-kernel`.
- Declaracion de README: `INTERNAL_RESEARCH / DO_NOT_PUBLISH`.
- Paquete: `obs-info-kernel`.
- Version: `0.1.0`.
- Dependencias declaradas: ninguna.
- CLI local declarada: `obs-info = obs_info_kernel.cli:main`.

## Evidencia

Comandos:

```powershell
rg --files research\obs-info-kernel
Get-ChildItem -Force research\obs-info-kernel
python tools\release\scan_secrets.py --path research\obs-info-kernel --json
python -m pytest tests -q
Get-ChildItem -Recurse -File research\obs-info-kernel
Get-Content research\obs-info-kernel\pyproject.toml
Get-Content -TotalCount 60 research\obs-info-kernel\README.md
```

Resultados:

- Inventario sin caches: `file_count=26`, `total_bytes=104803`.
- Secret scan por ruta: `count_reported=0`.
- Tests locales: `22 passed in 0.21s`.
- `pyproject.toml` declara `dependencies=[]`.
- README marca explicitamente `INTERNAL_RESEARCH / DO_NOT_PUBLISH`.
- No se ejecuto red, instalacion de dependencias, push, deploy, social,
  Gumroad ni publicacion.

## Decision

`obs-info-kernel` queda validado como kernel local de investigacion. Puede
seguir como herramienta interna para pruebas y continuidad, pero no debe
convertirse en copy publico ni paquete distribuible sin revision de fuentes,
licencia, claims y ActionGate target-specific.

## Proxima accion verificable

Validar `research/observacionismo-lab` con inventario, scan focal y tests o
smoke local si existen.
