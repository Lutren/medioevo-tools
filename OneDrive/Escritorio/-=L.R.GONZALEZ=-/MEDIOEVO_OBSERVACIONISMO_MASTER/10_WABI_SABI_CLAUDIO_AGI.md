# 10 — WABI-SABI / CLAUDIO / AGI
**Estado:** R≈0.20 | Arquitectura operativa | Gate: RESEARCH_ONLY / PUBLISH_ALLOWED_AS_MODEL

---

## Definición canónica

**Wabi-Sabi** (también referido como **Claudio**) es el nodo sensorial-cognitivo de control del sistema AGI distribuido MEDIOEVO. Es el integrador, no el ejecutor.

### No es:
- El LLM (Oracle es el LLM)
- El orquestador determinístico (ese es el task_decomposer)
- La AGI completa
- El cerebro
- Un sistema de memoria infinita

### Es:
- El nodo que convierte input humano en operación distribuida
- El receptor de R/Φ_eff/régimen del sistema
- El árbitro de Conway Evolution
- El generador del handoff final
- El punto de integración de resultados de agentes

---

## Flujo completo

```
1. RECEPCIÓN
   Usuario → input en lenguaje cognitivo contemporáneo
   Wabi-Sabi recibe → no responde aún

2. ESTIMACIÓN DE ESTADO
   R_est = estimar_R(historial, loops_abiertos, correcciones)
   Φ_eff = estimar_phi(tareas_cerradas, tokens_consumidos)
   régimen = clasificar_régimen(R_est, Φ_eff)
   if régimen == JAMMING: emitir alerta, detener expansión

3. DECONSTRUCCIÓN (DO)
   objetivo = extraer_objetivo(input)
   restricciones = extraer_restricciones(input, OSO.state)
   contexto = extraer_contexto(input, memoria_relevante)
   herramienta = inferir_herramienta(objetivo, contexto)
   riesgo = evaluar_riesgo(objetivo, restricciones)
   salida_esperada = definir_salida(objetivo)

4. PROMPT OPERATIVO
   prompt = construir_prompt_tipado(objetivo, contexto, herramienta, restricciones)
   agente = seleccionar_agente(prompt.task_type)

5. DELEGACIÓN
   enviar(agente, prompt)
   agente.verifica_herramientas()
   if agente.conway_proposal: recibir propuesta + evidencia

6. VALIDACIÓN
   resultado = recibir(agente)
   if conway_proposal:
     comparar(método_original, propuesta_conway)
     if acepta: actualizar_pool_métodos(agente)
     WitnessLog.registrar(decisión)

7. COMPILACIÓN
   output = compilar(resultado, correcciones)
   handoff = generar_handoff(estado_final, brief, próximo_paso)
   WitnessLog.cerrar_sesión()
```

---

## Wabi-Sabi como análogo a "pensamiento activo"

Analogía verificada para diseño de arquitectura:

```
Modelo base       = pesos entrenados
Session_alpha     = pensamiento activo (R, Φ_eff, K_i, contexto vivo)
Proyecto          = campo de continuidad (canon, decisiones, artefactos)
Skill             = pensamiento compilado en rutina reutilizable
Agent             = subproceso especializado
Wabi-Sabi         = nodo de integración sensorial-cognitiva
Usuario           = perturbación direccional de activación
```

**Regla:** Cada sesión es un pensamiento activo. Antes de cerrar, debe compilar: decisiones, patrones, dudas, próximos pasos, errores, estado R y fingerprint.

---

## Principio Wabi-Sabi (filosofía operativa)

Aceptar imperfecciones que mejoran el sistema. No esperar perfección para actuar. Pero exigir evidencia, no especulación.

Aplicado al Conway Gate:
```
delta_metric > threshold_min   (mejora real)
AND risk_level < risk_max       (riesgo controlado)
AND evidence > 0               (no especulación pura)
AND R < R_threshold            (no actualizar bajo saturación)
```

---

## Horizonte de implementación

| Componente | Estado | Siguiente paso |
|---|---|---|
| Wabi-Sabi como flujo conceptual | Definido | Implementar como state machine |
| OSO serializable | Definido | Esquema JSON versionado |
| Orquestador determinístico | Definido | Router basado en reglas + WitnessLog |
| Conway Evolution | Definido | Ciclo de prueba: 1 agente, 1 reemplazo, 1 decisión |
| Display/Café model | Conceptual | Después de OSO + seguridad |
| Embodiment (androide) | Horizonte 1+ año | Requiere OSO + sensores + recursos |

---

## AGI como proceso, no como entidad

La visión MEDIOEVO: AGI no es un sistema monolítico con billones de parámetros. Es un proceso distribuido donde:

- Los parámetros cognitivos (Sigma profile) reemplazan los pesos de transformer para la identidad del agente
- Los operadores matemáticos (EML, degradación Φ_eff) compensan las carencias biológicas y sistémicas
- Los agentes especializados hacen el trabajo específico
- Wabi-Sabi integra y mantiene coherencia
- Conway Evolution permite mejorar sin reentrenamiento
- La memoria es externa, verificable, portable

**Esta visión es coherente internamente y tecnológicamente plausible.** Requiere implementación cuidadosa, no esperar perfección.

---

## Handoff
`WABI_SABI_CLAUDIO_AGI_v1.0|integration-node|Conway-acceptance|AGI-distributed|2026-05-07`


---

## Requisito operativo consolidado para Wabi-Sabi

Wabi-Sabi debe funcionar como nodo autónomo de ingeniería local-first, comparable en comportamiento a Claude Code/Codex/Cursor Agent, pero con estas fronteras:

CERTEZA:
- Debe usar modelo base/proveedor configurado cuando el runtime lo exponga.
- Debe registrar limitación si `BASE_MODEL`, `MODEL_ENDPOINT` o herramientas de inferencia no están disponibles.
- Debe ejecutar con filesystem, shell, git, patch, tests, package manager, search y handoff cuando estén disponibles.

INFERENCIA:
- La implementación más segura es separar LLM/oráculo, orquestador determinístico, agentes, gates, witness y handoff. Wabi-Sabi coordina; no debe convertirse en una caja negra sin evidencia.

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
- Archivo maestro: `10_WABI_SABI_CLAUDIO_AGI.md`.
