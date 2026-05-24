# AGENT LIFE GAME-FEEL v1.3.1

Fingerprint: DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY

## Implementado

Se agrego un grafo interactivo de vida de agentes y mini dashboard en `AgentInspector`.

- `src/agents/agentRelationshipGraph.ts`
- `src/components/AgentLifeDashboardPanel.tsx`
- CSS de grafo y cues en `src/styles.css`

## Datos visibles

- Nodos por agente.
- Enlaces declarados, por proximidad o tarea.
- Necesidad mas baja.
- Tarea actual.
- Memoria reciente.
- `R`, `Phi_eff`, mood y tag de audio.

## Game-feel

Los agentes generan cues de audio si tienen necesidad baja, tarea activa, `R` alto o gate no `APPROVE`. El motor no hace a los NPCs omniscientes: la salida sigue limitada al estado causal local del agente.

## QA

Pruebas:

- `agentLifeDashboard.test.ts`
- `audioGameFeelAdapter.test.ts`

Screenshot:

- `docs/screenshots/v1_3_1/agent_life_relationship_graph.png`
