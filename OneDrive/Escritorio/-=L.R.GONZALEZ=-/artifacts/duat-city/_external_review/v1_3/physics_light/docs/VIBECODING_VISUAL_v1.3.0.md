# Vibecoding Visual v1.3.0

**Fingerprint:** DUAT-v1.3.0-VIBECODING-VISUAL

## Frases Soportadas

| Frase | Luz | Física | Paleta | Audio (bridge) |
|-------|-----|--------|--------|----------------|
| "más Vermeer silencioso" | lateral suave, sombras estáticas | polvo casi estático | ocre-azul, 64 colores | low strings drone |
| "más Caravaggio dramático" | alto contraste Q, burst locales | telas que caen con peso | negro-rojo-oro, 128 colores | brass swell, disonancia |
| "más mercado subterráneo" | humo modula luz, neon flicker | multitud colisiones suaves | gris-púrpura-verde | chatter granular, neonHum |
| "jardín bioluminiscente" | Q=11 en plantas, propagación suave | partículas flotan sin inercia | verde-azul-blanco, 96 colores | high strings shimmer, bells |
| "más archivo prohibido" | Q=01 en documentos, luz ausente | estática, polvo suspendido | azul oscuro, 48 colores | archive drone, missing signal |
| "más forge" | Q=11 en hornos, naranja intenso | presión, metal caliente | naranja-gris-negro | forge pulse, brass |

## Parser Determinista

```
Input: frase de vibecoding
→ Tokeniza palabras clave (artista, ambiente, adjetivo)
→ Mapea a parámetros de EngineConfig
→ Aplica a LightFieldFM, PhysicsEngine, IndexedPalette
→ Genera AudioSceneConfig vía bridge
```

No IA externa. No cloud. Parser local.
