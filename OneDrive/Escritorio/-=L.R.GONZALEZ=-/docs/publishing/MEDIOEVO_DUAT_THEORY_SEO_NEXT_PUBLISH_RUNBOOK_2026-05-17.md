# MEDIOEVO DUAT + Teoria - Next Publish Runbook 2026-05-17

## Gate

No ejecutar este runbook si `python tools\host_observacionista.py --no-write` no devuelve `gate=APPROVE`.

Ultimo reintento:

- Fecha UTC: 2026-05-17T00:14:03Z.
- Resultado: `gate=BLOCK`, `status=JAMMING`, `R=0.651`, `Phi_eff=0.378`.
- Razones: `memoria_alta`, `disco_precaucion`, `proceso_dominante_cpu`, `residuo_alto`.
- Reintento aislado posterior: `gate=REVIEW`, `status=CONTAMINADO`; ActionGate target-specific nego push/deploy porque exige host `APPROVE`.
- Autorizacion humana registrada: `autorizo todo , termina con todo`.
- Decisiones target-specific negadas:
  - `medioevo-site-deploy`: `b0ce1f74-77f6-47cb-8d01-50a96ad2a1d0`.
  - `github-medioevo-theory-public-release`: `c5ebd293-fa80-4e89-b19e-58f0fc3995ce`.

## Targets verificados

- GitHub theory package: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\publish_staging\medioevo-theory-public-release`
- Cloudflare site package: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\publish_staging\medioevo-site-deploy-ready-2026-05-16`

## Preflight minimo

Desde `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`:

```powershell
python tools\release\pending_review.py --write --quiet
python tools\release\scan_secrets.py --path publish_staging\medioevo-theory-public-release --json
python tools\release\scan_secrets.py --path publish_staging\medioevo-site-deploy-ready-2026-05-16 --json
```

Desde `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio`:

```powershell
python -m pytest tests\test_duat_lab_visual_smoke.py tests\test_public_theory_release.py -q
python tools\duat_lab_visual_smoke.py
```

## GitHub package

Estado local actual: repo inicializado en `main`, commit `6bdddb9 Publish MEDIOEVO public theory corpus`, sin remoto.

Solo si el gate esta `APPROVE`:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\publish_staging\medioevo-theory-public-release
gh repo create Lutren/medioevo-theory-public-release --public --source . --remote origin --push
```

Si el repo ya existe, sustituir el ultimo comando por:

```powershell
gh repo view Lutren/medioevo-theory-public-release
git branch -M main
git remote add origin https://github.com/Lutren/medioevo-theory-public-release.git
git push -u origin main
```

## Cloudflare Pages

Solo si el gate esta `APPROVE` y el paquete deploy-ready conserva scans limpios:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\publish_staging\medioevo-site-deploy-ready-2026-05-16
npx wrangler pages deploy . --project-name=medioevo-site --branch=main
```

## Smoke publico post-deploy

```powershell
@'
from urllib.request import urlopen
for url in [
    "https://medioevo.space/duat.html",
    "https://medioevo.space/theories.html",
    "https://medioevo.space/observacionismo-osit.html",
    "https://medioevo.space/theory/psi-teoria-completa-v2.html",
    "https://medioevo.space/theory/observacionismo-v27-3.html",
    "https://medioevo.space/theory/frequency-theory.html",
    "https://medioevo.space/theory/brain-os-v34-3.html",
    "https://medioevo.space/theory/psi-ai-framework-v1.html",
    "https://medioevo.space/theory/observacionismo-agent-v3.html",
]:
    with urlopen(url, timeout=20) as r:
        body = r.read(4000).decode("utf-8", "replace")
    print(r.status, url, "DUAT_LOOP_VIVO_v1" in body or "Teoria" in body or "Observacionismo" in body)
'@ | python -
```
