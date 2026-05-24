# Worktree Review Packet - 2026-05-06

Estado: `REVIEW_REQUIRED / SHARED_WORKTREE_ACTIVE`

El workspace esta activo y contiene cambios de multiples carriles. Este paquete
evita convertir el estado sucio en bloqueo operativo falso para targets locales
ya acotados.

## Evidencia

Comando ejecutado:

```powershell
git status --short
```

Resultado resumido:

| metrica | valor |
|---|---:|
| lineas de status | 85 |
| estado | worktree compartido con cambios activos |
| staging amplio | prohibido |

Carriles visibles en el snapshot:

- Wabi-Sabi local app y tests.
- COMMS / agent-city coordination.
- paquetes open-dev.
- docs de ops, publishing, developer, security y legal.
- herramientas de release.
- artefactos `qa_artifacts`.
- nuevos reportes raiz exigidos por `AGENTS.md`.

## Regla De Operacion

- No usar `git add .`.
- No revertir cambios de otros agentes.
- No declarar el workspace global limpio.
- Preparar commits solo por target y con allowlist exacta cuando el operador lo
  pida.
- Mantener `qa_artifacts/release_validation/*` como evidencia de cierre local,
  no como prueba de publicacion global.

## Criterio De Cierre

| objetivo | evidencia requerida |
|---|---|
| commit de target local | lista exacta de archivos, tests del target, secret scan focalizado `0`, `git diff --check` |
| limpieza global | decision humana sobre cambios de otros agentes y ramas/commits separados |
| release publico | worktree de staging limpio o paquete allowlist, sin rutas privadas, sin secretos, licencia resuelta |

## Proxima Accion Segura

Mantener el backlog operativo sin checkboxes globales abiertos. Los tres puntos
globales quedan en `REVIEW_REQUIRED`; el trabajo ejecutable debe continuar por
target validado.
