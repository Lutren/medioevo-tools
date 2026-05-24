# 08 — OBSERVACIONISMO INVERSO (IOE)
**Estado:** R≈0.18 | Método operativo | Gate: PUBLISH_ALLOWED_WITH_SCOPE

---

## Definición

**Ingeniería Observacionista Inversa (IOE):** Extraer la estructura subyacente de un sistema a partir de sus outputs, patrones, límites y residuos. Reconstruir las condiciones, procesos y Sigma que produjeron ese sistema.

Dirección:

```
OE (directa):   Sistema → Variables → Primitivas → Schema
IOE (inversa):  Output deseado → Faltantes → Contratos → Agentes → Pruebas → Handoff
                Estado observado → Condiciones que lo produjeron → Sigma del sistema
```

---

## Tríada operativa

```
OBSERVAR → DECONSTRUIR → RECOMPILAR
```

| Modo | Pregunta | Producto |
|---|---|---|
| DO (Deconstrucción) | ¿Qué hace realmente este sistema? | Primitivas informacionales |
| OE | ¿Qué variable ejecuta? | Schema, métrica, contrato |
| IOE | ¿Qué debe existir para producir este output? | Arquitectura, agente, prompt, protocolo |

---

## IOE aplicada a física

Aplicación: dado un framework físico (Newton, Einstein, QFT), extraer la Sigma del observador que lo produjo.

Pregunta: ¿Cuáles son las dimensiones de Sigma que explican tanto los éxitos como los límites de este framework?

**Newton:**
- V_gain alto → excelente en patrones mecánicos
- AT (tolerancia ambigüedad) bajo → rechazó acción-a-distancia
- Resultado: mecánica válida para objetos macroscópicos, velocidades bajas, sin curvatura

**Einstein:**
- Alta tolerancia geométrica / abstracción espacial
- Bajo switching cost entre representaciones
- Resultado: geometría de spacetime, no mecánica de contacto

**IOE resultado:** Los límites de una teoría física son la huella de la Sigma del observador que la formuló.

---

## IOE aplicada a sistemas de IA

Dado un modelo de lenguaje, extraer:
- Qué sesgos de atención tiene (qué patrones captura automáticamente)
- Cuál es su ventana efectiva de integración (dónde degrada con contexto largo)
- Qué tipos de input aumentan su R funcional (instrucciones contradictorias, larga conversación sin cierre)
- Cuáles son sus "barreras Newton": dominios donde devuelve resultados seguros pero incorrectos

**Producto:** Sigma funcional del modelo → permite predecir en qué contextos fallará y cómo compensarlo.

---

## IOE aplicada a documentos / corpus

Dado un corpus (MEDIOEVO en este caso), extraer:
- Categorías de claims presentes
- Nivel de evidencia por categoría
- Huecos entre claims y evidencia
- Patrones de repetición (señal de R alto en el momento de escritura)
- Tensiones internas (contradicciones como información sobre el estado del autor)

**Este proceso es exactamente lo que el agente CURADOR está ejecutando** sobre el corpus MEDIOEVO.

---

## IOE aplicada a personas / organizaciones

Dado el comportamiento observable de una persona u organización:
1. Mapear input → transformación → output → residuo
2. Inferir qué valores internos, sesgos, traumas o restricciones producen esos outputs
3. Identificar los "barreras Newton" del sistema: dónde está completo y dónde está limitado
4. No confundir "límite de validez" con "error": el sistema puede ser correcto dentro de su Sigma

**Gate:** PUBLISH_ALLOWED_AS_MODEL — heurístico, no diagnóstico clínico ni psicoanálisis.

---

## Plantillas

### Plantilla OE (extracción)
```yaml
sistema: ""
input: []
transformaciones: []
output: []
residuo_R: null
gates: []
evidencia: []
falsadores: []
riesgo: low|medium|high|block
```

### Plantilla IOE (reconstrucción)
```yaml
estado_deseado: ""
faltantes: []
contratos: []
agentes_requeridos: []
herramientas: []
gates: []
validacion: []
handoff: ""
```

---

## Regla de uso

Si una idea no puede pasar por DO/OE/IOE, queda como metáfora o narrativa, no como canon operativo. Esta es la compuerta epistémica del método.

---

## Handoff
`OBSERVACIONISMO_INVERSO_v1.0|IOE-OE-DO-Newton-IA-corpus|2026-05-07`



---

## Corte de curaduría 2026-05-07

CERTEZA:
- Este documento fue compilado desde fuentes locales de `-=PSI=-`, `-=CEREBRO=-` y `PRODUCTOS_MEDIOEVO`.
- Las fuentes originales no fueron movidas, borradas ni reescritas.

INFERENCIA:
- Si una idea aparece en varias fuentes, se conserva aquí como una entrada consolidada y se remite al manifiesto de fuentes para variaciones.

INCÓGNITA:
- PDFs, DOCX, ZIP, TAR.GZ y media quedan trazados por manifiesto; no todos fueron convertidos a texto completo en este pase.

ACCIÓN:
- Usar este archivo como capa maestra de lectura y volver a la fuente solo para auditoría, expansión o verificación puntual.

ARTEFACTO:
- Archivo maestro: `08_OBSERVACIONISMO_INVERSO.md`.
