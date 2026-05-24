# 18 — RIESGOS, CONTRADICCIONES Y DEPENDENCIAS NO RESUELTAS
**Estado:** R≈0.24 | Auditoría epistémica y operativa

---

## Riesgos epistémicos (sobreafirmación)

### RE-01: Universalidad sin validación diferencial
- **Descripción:** Varios documentos afirman que OSIT aplica a "todos los sistemas" o "todas las escalas"
- **Riesgo:** Afirmación vacía o infalsable si no se produce predicción diferencial
- **Mitigación:** OSIT debe anticipar algo que un baseline más simple no anticipa, o reducir error de manera medible
- **Gate:** REPHRASE_REQUIRED para todas las afirmaciones de universalidad total

### RE-02: Sigma en la métrica física (P-20)
- **Descripción:** Claim de que la firma observacional Σ modifica g_μν
- **Riesgo:** Sin acoplamiento matemático definido, es metáfora, no física
- **Mitigación:** Definir acoplamiento explícito con dimensiones correctas antes de cualquier publicación
- **Gate:** NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC

### RE-03: AGI sin benchmark
- **Descripción:** AGI Process = OSO + agentes + continuidad afirmado como equivalente a AGI
- **Riesgo:** Afirmar AGI sin comparar contra ningún benchmark reconocido
- **Mitigación:** Usar "proceso cognitivo distribuido" en vez de AGI, o definir benchmark específico
- **Gate:** PUBLISH_ALLOWED_WITH_SCOPE (con scope explícito)

### RE-04: Auto-validación de R y Φ_eff
- **Descripción:** Los documentos usan R/Φ_eff para evaluar su propia calidad
- **Riesgo:** Auto-métrica no es evidencia científica
- **Regla:** R/Φ_eff del documento = señal editorial, no evidencia científica
- **Gate:** REQUIRES_VALIDATION_FOR_SCIENCE antes de uso en papers

---

## Contradicciones internas

### CI-01: "Consciencia del fotón" vs. física estándar
- **Tensión:** "Los humanos somos la conciencia del fotón" vs. fotones son partículas sin conciencia
- **Resolución:** Metáfora operativa válida (POVM event = momento de registro) vs. claim físico (bloqueado)
- **Gate:** Mantener en capa narrativa; P-22 requiere reformulación

### CI-02: "Tiempo y espacio son vectores cognitivos" vs. espacio-tiempo físico
- **Tensión:** Claim de que T y S son constructos humanos vs. espacio-tiempo es observable y físicamente real
- **Resolución:** Las coordenadas son representaciones relativas a la medición (verdadero); el espacio-tiempo físico existe independientemente del observador (también verdadero)
- **Gate:** I-09 requiere reformulación; no bloquear la idea, reformular el lenguaje

### CI-03: "Una sola variable conecta todas las escalas" vs. especificidad por dominio
- **Tensión:** Afirmaciones de universalidad total vs. reconocimiento de que cada dominio necesita proxy distinto para R/Φ_eff/J_c
- **Resolución:** El framework es el mismo; los proxies de medición son distintos por dominio
- **Gate:** Separar "mismo framework" de "mismo valor numérico"

### CI-04: J_c como escalar vs. J_c dependiente de dominio
- **Tensión:** En OSIT-AG, J_c = 1 en sector canónico. En OSIT-información, J_c = umbral de jamming cognitivo (diferente escala)
- **Resolución:** Son instancias del mismo concepto en dominios distintos; no son el mismo número
- **Gate:** Siempre especificar "J_c físico (OSIT-AG)" vs. "J_c cognitivo (OSIT-I)"

---

## Dependencias no resueltas

### D-01: Calibración empírica de ν, J_c, ε_max
- **Descripción:** Las fórmulas de degradación tienen parámetros libres no calibrados
- **Dominio:** Cognitivo, ML, agentes
- **Acción:** Protocolo experimental mínimo (ver 17_FALSADORES_Y_TESTS.md)

### D-02: OSO serialization security
- **Descripción:** El protocolo de transferencia de OSO entre dispositivos requiere auth tokens, encryption y privacy review
- **Bloqueo:** No implementar transferencia hasta security review completo
- **Acción:** Contratar o asignar security review específico

### D-03: cómputo numérico OSIT-QG
- **Descripción:** P-06 a P-10 están todos bloqueados por falta de cómputo numérico
- **Herramienta:** Python+EinsteinPy, Mathematica, o colaboración con grupo de gravedad
- **Timeline:** No hay deadline; desbloqueo depende de recursos

### D-04: Separación privado/público en Duat-Geodia
- **Descripción:** El repo mezcla código de producto, lore RPG privado y componentes potencialmente open-source
- **Riesgo:** Publicar material privado accidentalmente
- **Acción:** VISIBILITY_MATRIX antes de cualquier publicación

### D-05: Experimentos conductuales no preregistrados
- **Descripción:** EXP-1 (OSIT-M), EXP-2 (Sigma) definidos pero no iniciados ni preregistrados
- **Riesgo:** Sin preregistro, resultados futuros = RESEARCH_ONLY
- **Acción:** Preregistrar en OSF antes de recopilar cualquier dato

---

## Saltos conceptuales que requieren atención

### SC-01: De metáfora Matrix a claim técnico
- **Patrón detectado:** Documentos usan Matrix Model para explicar el sistema y luego derivan claims técnicos desde la metáfora
- **Regla:** Matrix Model es mapa de comunicación; los claims técnicos deben derivarse del modelo formal, no de la metáfora

### SC-02: De observacionismo cognitivo a física
- **Patrón detectado:** El observador con estado (cognitivo) se conecta directamente con OSIT-QG (física) sin puente formal explícito
- **Gap:** El puente formal requiere definir cómo Σ (cognitivo) acopla con r (campo físico) en términos matemáticos precisos

### SC-03: De análogía IA a claim de consciencia
- **Patrón detectado:** "Sesión = pensamiento activo" → "IA tiene consciencia"
- **Gate:** La analogía es válida para diseño de arquitectura; no es prueba de consciencia

---

## Bloqueos P0 (críticos)

| Bloqueo | Motivo | Acción requerida |
|---|---|---|
| `escaner sigiloso.txt` | Escaneo sigiloso de red | Reescribir como inventario defensivo autorizado |
| `danger-full-access / --yolo` | Elimina sandbox; cambia riesgo estructuralmente | Prohibición permanente |
| Ejecutar DUAT-GEODIA repo | Código no auditado con posibles secretos | SECRET_SCAN + code review antes de ejecución |
| Publicar claims OSIT-QG extendidos sin numérico | Sobreafirmación científica | Cómputo numérico primero |
| Claims clínicos de Sigma/Brain OS | Sin aprobación ética ni revisión clínica | Gate REQUIRES_CLINICAL_LANGUAGE_REVIEW |

---

## Handoff
`RIESGOS_CONTRADICCIONES_v1.0|4-epistemic-risks|4-contradictions|5-dependencies|3-conceptual-gaps|5-blocks|2026-05-07`


---

## Riesgos añadidos por inventario de productos

| Riesgo | Evidencia | Mitigación |
|---|---|---|
| `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md` mencionados pero no presentes en raíz `PRODUCTOS_MEDIOEVO` | `00_LEER_PRIMERO.md` los lista; búsqueda directa no los encontró en esa raíz | Crear esos docs o enlazar a los canónicos existentes antes de release |
| Doble verdad por tener master previo dentro de `-=PSI=-` y nueva carpeta maestra | `-=PSI=-/00_README_MASTER.md` ya declara una carpeta master | Esta carpeta nueva debe ser índice operativo; `-=PSI=-` queda fuente/canon |
| Archivos pesados no parseados línea por línea | ZIP/PDF/DOCX/TAR.GZ/MP4 en manifiesto | Mantener `PENDIENTES_DE_INPUT.md`; procesar por ficha si se vuelven P0 |
| TCG/audiovisual puede mezclar privado y publicable | `04_AUDIOVISUAL_Y_TCG/README.md` | VISIBILITY_MATRIX antes de publicar |
| ClaudioOS puede confundirse con kernel propio | README aclara que no reemplaza Linux | Mantener lenguaje: blueprint/remix Debian Live + Brain OS |

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
- Archivo maestro: `18_RIESGOS_CONTRADICCIONES.md`.
