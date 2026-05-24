# 21 — ACTION GATES

Estado: `POLITICA_OPERATIVA`

## Regla base

Acción permitida solo si:

```text
Phi_eff > 0.60
R < 0.30
evidencia_minima_disponible = true
riesgo_de_sobreafirmacion_controlado = true
siguiente_paso_verificable = true
```

## CERTEZA

- Las fuentes locales definen ActionGate, WitnessLog, Guardian y políticas de hold/allow/ask/block.
- Las acciones irreversibles, publicación, credenciales, pagos, browser externo y borrados masivos requieren revisión o bloqueo.

## INFERENCIA

- La política más segura para Wabi-Sabi/Claudio es un gate determinístico delante de toda acción de filesystem, browser, modelo, publicación o ejecución.

## INCÓGNITA

- Umbrales exactos de R/Phi requieren calibración empírica por tarea.

## ACCIÓN

| Tipo de acción | Gate | Evidencia mínima | Resultado |
|---|---|---|---|
| Leer/inventariar documentación local | APPROVE | ruta local existe | ejecutar y registrar |
| Crear documentación/ficha/manifiesto | APPROVE | destino dentro del workspace | escribir y registrar |
| Ejecutar tests locales seguros | APPROVE_MONITORED | comando específico, sin red | ejecutar y capturar resultado |
| Modificar código no crítico | APPROVE_MONITORED | diff pequeño + test | patch + test |
| Instalar dependencias con red | REVIEW | razón + lockfile | registrar y esperar revisión |
| Publicar, deploy, push, Gumroad, social | REVIEW/BLOCK | autorización explícita + scan + matriz | no ejecutar por defecto |
| Leer/imprimir secretos | BLOCK | ninguna | no ejecutar |
| Borrar/migrar grandes volúmenes | REVIEW/BLOCK | backup + migration log + aprobación | no ejecutar por defecto |
| Browser externo sin manifest | BLOCK | manifest ausente | bloquear |
| Física fuerte sin numérico | BLOCK/NO_PUBLIC | cómputo ausente | reformular como hipótesis |

## ARTEFACTO

Contrato mínimo:

```json
{
  "action": "string",
  "domain": "docs|code|browser|publish|physics|model|filesystem",
  "R": 0.15,
  "Phi_eff": 0.75,
  "evidence": ["path-or-test"],
  "risk": "low|medium|high|critical",
  "reversible": true,
  "external_effect": false,
  "decision": "APPROVE|APPROVE_MONITORED|REVIEW|BLOCK",
  "witness": "path/to/witness.jsonl"
}
```
