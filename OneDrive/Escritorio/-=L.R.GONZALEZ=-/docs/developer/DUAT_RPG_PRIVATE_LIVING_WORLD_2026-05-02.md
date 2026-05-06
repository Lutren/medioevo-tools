# DUAT / RPG Private Living World - 2026-05-02

Estado: `PRIVATE_GAME_BRIDGE_PLAN / NO_PUBLIC_ENGINEERING`.

Este documento aterriza como integrar DUAT al videojuego para hacerlo un entorno
vivo sin mezclarlo con el carril publico. No copia codigo, assets, escenas, lore,
builds ni runtime del RPG.

## Frontera

| carril | decision |
|---|---|
| DUAT Geodia | privado, motor de mundo vivo e hipotesis sociales internas |
| DUAT Genesis | publico, sandbox sintetico sin datos ni motor privado |
| RPG / TCG | privado, propietario, sin publicacion open-source |
| Website / GitHub | solo descripcion low-claim y contratos sanitizados |

## Contrato privado recomendado

```text
LivingWorldEvent
  id
  timestamp
  source: duat_geodia | worldpulse | npc | quest | economy | faction
  scope: private_rpg
  actor_id
  zone_id
  signal
  residue
  phi_eff
  risk
  summary
  evidence_uri_private
```

## Sistemas de juego que pueden usar DUAT

- NPC memory: recuerdos, sesgos, ultima observacion y transferencia de ventana.
- Schedule: rutinas por edificio, hora, faccion y estado del mundo.
- Intent: deseo, miedo, deuda, objetivo y bloqueo.
- Rumors: eventos DUAT convertidos en rumor jugable.
- Quests: `LivingWorldEvent` convertido en mision, carta, dialogo o incidente.
- Factions: tension, confianza, recursos, alianza y conflicto.
- Economy: escasez, exceso, rutas, precios y consecuencias.
- WorldPulse: salud de zonas, anomalias, ritmo de ciudad y eventos emergentes.

## Reglas

- No exponer `LivingWorldEvent` completo fuera del carril privado.
- No incluir prompts, logs, secretos, rutas locales, assets, lore o scripts.
- No publicar puente runtime ni escenas.
- Si se necesita mostrar algo publico, reducir a patron de diseno: "mundo vivo
  con eventos, memoria y consecuencias".

## Primer sprint privado

1. Definir fixture privado con 10 NPCs, 3 zonas y 20 eventos sinteticos.
2. Simular memoria/schedule/intent sin tocar assets finales.
3. Crear validador que bloquee rutas publicas, secretos y lore sensible.
4. Conectar solo a debug interno del RPG.
5. Revisar con frontera privada antes de cualquier demo comercial.
