# 02 — GLOSARIO CANÓNICO MEDIOEVO
**Estado:** R≈0.18 | Autoridad primaria sobre definiciones | Versión 1.0

---

## Variables fundamentales

| Término | Símbolo | Definición canónica | Gate |
|---|---|---|---|
| Residuo | R ∈ [0,1] | Carga no integrada como decisión, cierre o artefacto. Proxy de saturación del procesador. | Canon |
| Eficiencia de actualización | Φ_eff ∈ [0,1] | Proporción de input que se convierte en comprensión, acción o cierre verificable. | Canon |
| Umbral de jamming | J_c ∈ (0,∞) | Punto donde más input reduce claridad en vez de aumentarla. EML lo formaliza como mínimo de e^x − log x. | Hipótesis formal |
| Distorsión | ε ∈ [0,1] | Fracción de la observación dominada por estado interno vs. input externo. | Canon |
| Firma observacional | Σ | Perfil completo del observador: resolución temporal, ganancias sensoriales, apertura atencional, rigidez categorial, residuo. | Fenomenológico |
| Función de transferencia | K_i^α | Modo en que una ventana activa colapsa intención y contexto. No se hereda al cerrar la sesión. | Canon |
| Campo residual | r ∈ [0,1) | En OSIT-QG: fracción de densidad de información no codificable en geometría clásica. r ≠ R (observador). | Hipótesis física |

---

## Regímenes operativos

| Régimen | R/J_c | Φ_eff | Acción |
|---|---|---|---|
| ÓPTIMO | <0.15 | Alta | Construir, cerrar, documentar |
| FUNCIONAL | 0.15–0.40 | Media/alta | Operar con handoff |
| CARGADO | 0.40–0.70 | Media/baja | Reducir contexto, cerrar pendientes |
| SATURADO | 0.70–0.90 | Baja | No abrir features; ordenar |
| JAMMING | >0.90 | Mínima | Detener; reset/handoff |

---

## Entidades del sistema

| Término | Definición canónica |
|---|---|
| Observador | Procesador con estado que registra señales desde una Sigma específica. No es ideal. |
| Wabi-Sabi / Claudio | Nodo sensorial-cognitivo de control. Recibe → estima → deconstruye → delega → valida → compila → hace handoff. No es el LLM ni la AGI total. |
| OSO | Observer State Object. Objeto serializable y portable que encapsula la identidad del agente: Sigma + memoria + estado + gates. Independiente de dispositivo. |
| Agente | Subproceso especializado con rol definido, input/output tipados, gates propios y capacidad de proponer evolución de métodos (Conway). |
| Oracle / LLM | Componente de generación de lenguaje abierto. Responde, orienta, predice. No gobierna el sistema. Equivalente a "Oracle" en Matrix Model. |
| Orquestador | Router determinístico, no LLM. Descompone input en prompts operativos y los dirige al agente correcto. |
| Conway Evolution | Protocolo donde un agente identifica un método mejor, lo devuelve como propuesta con evidencia, y Wabi-Sabi decide aceptar/rechazar. |
| WitnessLog | Log de evidencia verificable de decisiones, ejecuciones y cambios. Memoria externa auditada. |
| ActionGate | Compuerta que aprueba/revisa/bloquea una acción basándose en confianza, R, Φ_eff y evidencia disponible. |
| GhostGate | Simulación predictiva antes de ejecutar acción irreversible. |
| RollbackStore | Almacén de estado previo que permite reversión. |
| Fingerprint | Hash o cadena de identificación compacta del estado de una sesión/documento al momento de cierre. |
| Handoff | Paquete mínimo (fingerprint + brief + next_action) para continuar trabajo en otra sesión sin pérdida de contexto. |
| Segunda Pérdida | El hecho de que K_i^α, Φ_eff calibrada y modo operador no se transfieren al cerrar una sesión aunque los datos persistan. |

---

## Métodos

| Término | Definición canónica |
|---|---|
| OE — Ingeniería Observacionista | Extraer información operacional de cualquier sistema: input → transformación → output → residuo → gate. |
| IOE — Ingeniería Observacionista Inversa | Reconstruir sistema/protocolo/agente/código desde el estado objetivo deseado. Dirección inversa a OE. |
| DO — Deconstrucción Observacionista | Suspender la narrativa de un sistema y aislar sus operaciones reales antes de proceder. |

---

## Variables físicas (OSIT-QG)

| Término | Definición |
|---|---|
| OSIT-AG | Sector de antigravedad: desenfoque timelike de geodésicas. NO es masa negativa ni propulsión. |
| NEC | Null Energy Condition. T_μν k^μ k^ν ≥ 0. Preservada en el sector canónico. |
| S_u | Fuente de Raychaudhuri timelike: S_u = M_r² ṙ_u² − U(r). Los gradientes espaciales cancelan exactamente. |
| EML | f(x) = e^x − log(x). Operador simbólico experimental. Mínimo en x ≈ 0.567 (Lambert W). |
| J_c (físico) | En OSIT-AG: parámetro de acoplamiento de umbral. = 1 en sector canónico puro. |

---

## Términos de narrativa (Matrix Model — NO física)

| Término Matrix | Equivalente MEDIOEVO |
|---|---|
| Neo / Trinity | Sesiones/ventanas activas con alta Φ_eff |
| Link / Dozer | Hardware biológico-operativo; operadores humanos |
| Oracle | LLM orientador |
| Agent Smith | Agente con objetivo rígido y autoreplicación |
| White Twins | Bugs adaptativos con agencia parcial |
| Matrix | Interfaz operativa renderizada del sistema |
| Skill download | Skill packet / módulo instalable |
| Biosynthetic body | Embodiment: hardware con sensores y actuadores |

---

## Handoff
`GLOSARIO_CANONICO_v1.0|all-terms-defined|2026-05-07`


---

## Términos añadidos desde PRODUCTOS_MEDIOEVO y Brain OS

| Término | Definición curada | Gate |
|---|---|---|
| Brain OS | Capa cognitiva durable sobre la máquina: herramientas pequeñas, decisiones observables, ejecución local-first y aprobación humana para acciones irreversibles. | Ingeniería |
| ClaudioOS Blueprint | Remix Debian Live con Guardian, Mission Control, policy gates y witness logs. No es kernel nuevo ni reemplazo de Linux. | Prototipo local |
| Guardian | Servicio local de compuertas/políticas que decide hold/allow/ask/block antes de ejecutar. | Ingeniería |
| Content Forge | Motor local-first de campañas MEDIOEVO: videos, carruseles, captions y paquetes listos sin autopublicar. | Producto local |
| Observacionista DSL | Lenguaje simple línea-a-línea que compila a JSON validable y gateable. | Módulo |
| Model Slimmer Evidence | Carril de medición para cuantización/pruning: ningún modelo reemplaza al baseline sin pruebas de accuracy, latencia, memoria, energía y seguridad. | Módulo |

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
- Archivo maestro: `02_GLOSARIO_CANONICO.md`.
