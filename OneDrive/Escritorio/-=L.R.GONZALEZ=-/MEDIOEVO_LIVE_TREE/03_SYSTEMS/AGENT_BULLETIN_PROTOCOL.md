# Agent Bulletin Protocol

## Proposito

El bulletin es la capa de anuncio y sincronizacion rapida del DUAT Telecom Core. No sustituye handoffs completos ni WitnessLog; reduce R dando a cada agente un resumen actual con evidencia, bloqueo y proxima accion.

## Formato minimo

Un bulletin es un `AgentMessage` con:

- `kind`: `bulletin`
- `channel_id`: `#system_announcements`
- `priority`: `P0` a `P3`
- `summary`: brief humano de una linea o parrafo corto
- `certeza`: hechos verificados
- `inferencia`: supuestos razonables
- `incognita`: faltantes no inventados
- `bloqueo`: stop rules
- `evidence_refs`: rutas o IDs verificables
- `artifact_refs`: rutas de outputs o exports
- `prompt_started_at`: fecha/hora ISO cuando se mando el prompt o inicio la solicitud, si aplica
- `work_delivered_at`: fecha/hora ISO cuando se entrego el trabajo, si aplica

## Ciclo

1. `codex_engineer` o `wabi_sabi_orchestrator` crea bulletin.
2. `sendMessage()` lo publica localmente.
3. Agentes destinatarios hacen `ackMessage()`.
4. Si contiene accion cerrada, se agrega `WitnessEvent`.
5. Si contiene riesgo P0, tambien aparece en `#security_review`.

## Reglas

- No incluir secretos.
- No copiar contenido privado de libros/juego/canon completo.
- No convertir un bulletin en decision irreversible.
- No usarlo para autorizar push/deploy/publicacion.
- Todo P0 debe tener `action_required` y `bloqueo`.
- Si el bulletin funciona como handoff humano, debe abrir con `BRIEF INTELIGENTE` y despues mostrar `DETALLE COMPLETO`.
- El estado R siempre se lee con la misma escala: `0 verde -> 1 rojo/jamming`.

## Traduccion a MEDIOEVO

El bulletin es el tablero central del Hormiguero/GEODIA: breve, accionable, con frontera clara. Su funcion es indicar "donde mirar ahora", no cargar todo el contexto.
