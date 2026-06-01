# ANALISIS: En que trabajar - Opciones y Recomendacion

## Situacion Actual del Workspace (2026-05-31)

### 1. DUAT Genesis
- **Estado:** FUNCIONAL y PUBLICADO (GitHub: Lutren/duat-genesis)
- **Tamano:** 2,126 KB, 43 archivos
- **Que hace:** Sandbox sintetico deterministico para experimentos de simulacion observable
- **Tests:** Pasando (`python -m pytest tests -q`)
- **Stack:** Python puro, zero dependencies, MIT license
- **Gap:** Necesita agentes mas realistas (actualmente son reglas deterministicas)

### 2. Wabi.sabi
- **Estado:** CODEBASE PRIVADO, altamente fragmentado, NO unificado
- **Tamano:** 667 archivos wabi/ en todo el workspace
- **What is it:** Framework de "wellness automation" + calibracion de agentes
- **Stacks encontrados:** Python, TS/JS, Rust (.rs), notebooks Jupyter
- **README privado existente pero no publico
- **Consolidated gap:** NO EXISTE un wabi.sabi unificado; está disperso

### 3. Vibeforge (Motor Grafico)
- **Estado:** IDEAS en README privado + codebase de juego en game-private
- **Tamano real:** README apenas describe el concepto; no hay motor
- **What is it:** Motor grafico + NPC IA automatizados
- **Gap enorme:** Necesitaria implementarse desde cero

---

## Comparativa Rapida

| Criterio | DUAT Genesis | Wabi.sabi | Vibeforge |
|----------|-------------|-----------|-----------|
| Estado actual | ✅ Funcional | 🔶 Fragmentado | ❌ Concepto |
| Impacto inmediato | Medio | ALTO | Bajo |
| Complejidad tecnica | Baja | Media | MUY ALTA |
| Tiempo para ver results | 1-2 semanas | 2-4 semanas | 2-3 meses |
| Tests existentes | ✅ Si | ❌ No | ❌ No |
| Reutilizable en otros proyectos | ✅ Si | ✅ Si | ❓ Potencial |
| Diversión de trabajar | Media | ALTA | MUY ALTA |
| Riesgo de fracaso | Bajo | Medio | ALTO |

---

## Mi Recomendacion: WABI.SABI (consolidacion + testing)

### Por que Wabi.sabi primero:

1. **Es la base faltante.** Todo el workspace menciona wabi.sabi, pero no hay un producto unificado. Esto genera residuo cognitivo y fragmentacion.

2. **Impacto dominante.** Un wabi.sabi funcional se convierte en herramienta propia para debuggear y calibrar agentes (incluyendo duat y futuro vibeforge).

3. **Mas real y cercano.** Te permite ver resultados funcionales en dias, no meses.

4. **Duat se beneficia automaticamente.** Una vez que wabi.sabi tenga un agent runner realista, puede integrarse como backend de duat.

5. **Vibeforge sera factible.** Con wabi.sabi + duat solidos, vibeforge no es 3 meses… es 3-6 semanas adicionales.

---

## Plan de Trabajo Sugerido para Wabi.sabi

### Fase 1: Consolida (Sesion 1-2)
- Crear la estructura inicial del framework
- Identificar y extraer los 10 mejores modulos dispersos
- Crear un test runner unificado

### Fase 2: Calibra (Sesion 3-4)
- Implementar Agent Calibration Engine (el "sabi")
- Integrar con llm local (Ollama) para agent conversation
- Hacer tests de stress

### Fase 3: Aplica a DUAT (Sesion 5-6)
- Reemplazar agentes deterministicos de duat-genesis con agentes wabi.sabi
- Hacer benchmark: duat-classic vs duat-agentic
- Publicar resultados

---

## Alternativa: Si prefieres empezar por DUAT

Podemos hacer un **hybrid approach** durante esta sesion:
- Hacer que duat-genesis pueda correr con agentes LLM reales (no solo reglas)
- Eso nos sirve como **prototipo inmediato** de wabi.sabi agent runner
- Luego extramos el codigo generico a wabi.sabi

**Ventaja:** Ves resultados mas rapido y defines la API real con necesidades concretas.

---

## Alternativa: Si prefieres empezar por Vibeforge

Recomendacion: NO empezar por vibeforge solo.
**Pero:** Podemos crear un **GameBridge desde wabi.sabi hacia Godot/Unity** como POC.
- Levantar un NPC basico con IA en Godot usando wabi.sabi como backend
- 1 escena, 1 NPC, 1 conversacion
- Eso valida la arquitectura y da algo tangible en 1-2 semanas

---

## Mi Propuesta Concreta para HOY

Dado que tienes TODO confirmado y autorizado, propongo:

### Opcion A (Recomendada): 
"Wabi.sabi Core + Agent Calibration"
1. Crear el framework base de wabi.sabi en `packages/open-dev/wabi-sabi/`
2. Implementar `AgentCalibrationEngine` con tests
3. Integrar con duat-genesis como demo
4. Dejar un test suite que corra automaticamente

### Opcion B:
"DUAT Agentic Upgrade"
1. Agregar soporte para agentes LLM en duat-genesis
2. Crear `AgentController` que reemplace reglas con LLM calls
3. Benchmark contra version deterministica
4. Extraer lo generico a wabi.sabi

### Opcion C:
"Vibeforge POC"
1. Crear un Godot project con un NPC IA basico
2. Conectar con wabi.sabi/duat via API local
3. POC de conversacion + decision

---

**¿Cual te gustaria? O si tienes otra idea, me ajusto.**
