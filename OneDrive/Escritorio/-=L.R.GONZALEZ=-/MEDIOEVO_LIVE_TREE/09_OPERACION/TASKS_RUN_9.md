# TASKS RUN 9

Fecha: 2026-05-12

## Objetivo recomendado

Run 9: Sandbox receipt review gate and hardened execution controls.

La meta es revisar y verificar receipts del sandbox antes de ampliar cualquier capacidad de ejecucion.

## Reglas

- Produccion sigue bloqueada.
- MessageBus principal no debe mutar.
- No deploy.
- No push.
- No DNS.
- No publicacion.
- No delete.
- No move.
- No rename.
- No comandos shell arbitrarios.
- No credenciales.
- No tokens reales.
- No Supabase/backend externo.
- No extraer ZIP canon.

## Tareas

1. Crear verifier de execution receipts.
2. Validar receipt hash y campos de seguridad.
3. Reproducir sandbox runs desde receipts.
4. Verificar que rollback solo apunta a sandbox.
5. Crear review gate manual local para receipts.
6. Crear reporte de diferencias entre dry-run, execution receipt y rollback.
7. Mantener `publish_release`, `delete_or_move`, deploy, DNS y publicacion bloqueados.
8. Agregar tests de no mutacion del MessageBus principal.
9. Agregar tests de path escape y produccion denied.
10. Actualizar `/telecom` con receipt review gate.
11. Crear handoff Run 10.

## Criterios de exito

- Receipt verifier existe.
- Receipt replay pasa.
- Rollback verification pasa.
- Main MessageBus SHA256 no cambia.
- Sandbox runtime no se commitea.
- Tests pasan.
- Build pasa.
- Audit prod queda en 0.
- /telecom responde HTTP 200.

## Stop conditions

- Cualquier intento de escribir fuera de sandbox.
- Cualquier intento de mutar MessageBus principal.
- Cualquier deploy/push/DNS/publicacion.
- Cualquier delete/move/rename.
- Cualquier token real o secreto.
