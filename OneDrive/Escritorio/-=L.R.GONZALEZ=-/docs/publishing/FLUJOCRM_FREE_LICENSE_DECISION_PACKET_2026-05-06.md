# FlujoCRM Free License Decision Packet - 2026-05-06

Estado: `MIT_RECORDED / LOCAL_ONLY`

El pedido del operador es dar FlujoCRM gratis en GitHub. El operador definio:
`MIT siempre`. La decision se aplico solo al staging publico.

## Verdad Actual

- Producto activo: `apps\commercial\flujocrm`.
- Staging local: `publish_staging\github\flujocrm-free-review`.
- `package.json` del staging: `license=MIT`, `private=false`.
- Staging Git: commit local `a16c019`, limpio, sin remoto.
- Secret scan staging: `count_reported=0`.
- `npm run check` en staging: passed.
- License readiness: `publication_ready=true`.

## Bloqueadores De Licencia

El verificador local quedo sin bloqueos:

- `publication_ready=true`
- `blockers=[]`

Comando:

```powershell
python tools\release\audit_flujocrm_free_license_readiness.py --write --json
```

Reporte:

- `qa_artifacts\release_validation\flujocrm-free-license-readiness-2026-05-06.json`

## Opciones

| Opcion | Que permite | Riesgo |
|---|---|---|
| MIT | Free/open-source simple, compatible con paid support | Reuso comercial por terceros |
| Apache-2.0 | Similar a MIT con texto de patentes | Mas pesado que MIT |
| AGPL-3.0 | Obliga a compartir cambios en servicios de red | Menor adopcion |
| Source-available/freeware | Gratis en GitHub sin OSI open source | Menor confianza open-source |
| Dual license | Free core + servicios/licencia comercial | Requiere docs legales mas claras |

## Recomendacion Tecnica

Para cumplir "CRM gratis en GitHub" sin romper la separacion comercial, ya se
aplico:

1. Publicar el codigo fuente del staging bajo `MIT`.
2. Mantener Gumroad/Sponsors para soporte, plantillas, instaladores,
   onboarding, automatizaciones y flujos premium.
3. No mover el producto activo `apps\commercial\flujocrm` hasta que el staging
   pase gate completo.
4. Cambiar solo el staging:
   - `package.json`: `private=false`, `license=MIT`.
   - `package-lock.json`: root license consistente.
   - `README.md`: quitar copy propietario.
   - `THIRD_PARTY_NOTICES.md`: describir dependencias sin llamar propietario a
     FlujoCRM.
   - Agregar `LICENSE` con el texto elegido.
5. Re-ejecutar:
   - `npm run check`
   - `python tools\release\scan_secrets.py --path publish_staging\github\flujocrm-free-review --json`
   - `python tools\release\audit_flujocrm_free_license_readiness.py --write --json`
   - path scrub local
   - ActionGate `github-flujocrm-free-release`

## Frontera

No se publico afuera en este ciclo. Este paquete registra la decision MIT y
deja la publicacion externa bloqueada por ActionGate/host.
