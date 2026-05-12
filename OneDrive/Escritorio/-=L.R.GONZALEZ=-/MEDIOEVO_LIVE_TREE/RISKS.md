# RISKS

- Secret scan con hallazgos: bloquea publicacion, push y deploy.
- ZIPs grandes no extraidos pueden contener `.git`, secretos, rutas locales o material privado.
- Clasificacion automatica puede producir falsos positivos; no borrar desde heuristica.
- E: fue escaneado de forma limitada; no representa cobertura completa del disco.
- Run 2 usa `localStorage` y hash mock: suficiente para UI/local demo, insuficiente para ledger verificable real.
- Seed de UI y seed runtime deben consolidarse en un canon JSONL/SQLite para evitar divergencia futura.
# Run 3 - riesgos MessageBus

- `localStorage` es manipulable: hash-chain detecta alteraciones al validar, pero no impide escritura local manual.
- Fallback `fnv1a-NOT_CRYPTOGRAPHIC` no sirve como seguridad; solo como compatibilidad local si Web Crypto no existe.
- `service.ts` conserva algunas mutaciones legacy para la UI; el ledger append-only ya existe, pero falta migrar transiciones a eventos derivados.
- MCP write tools quedan bloqueadas hasta ActionGate, evidencia y ledger durable.
- Canon ZIP sigue sin validacion de contenido; solo se verifico SHA256/listado central sin extraccion.

# Run 4 - riesgos Durable JSONL

- El log JSONL es durable, pero no anti-manipulacion fisica; la defensa es verificacion hash-chain, no control de acceso.
- El log principal contiene una muestra inicial; aun no es espejo completo de `localStorage`.
- Los scripts Node-only deben mantenerse fuera de imports React para no romper Vite/browser.
- MCP Run 5 debe ser read-only; cualquier write tool queda bloqueada por ActionGate.
