# Formal Claims Excerpt Comparison - 2026-05-13

Estado: `COMPARACION_CERRADA_SIN_MUTAR_CLAIMS_REGISTER`

## Alcance

Fuentes Formal comparadas:

| Fuente | SHA256 | Nota |
|---|---|---|
| `report.md` | `66A78CFE98D6565365BDC5587075036467F40A695BFFB4FA1E7F4903E6B02A4C` | Formalizacion matematica larga |
| `Auto.txt` | `ABAC8265B8045A30DC16F91EE40BF105BE579AE024F00BF471F2896DB49A6EAD` | Biblia/canon unificado en texto |
| `BIBLIA_MEDIOEVO_Canon_Unificado.pdf` | `4E652E9E816C8A0E5313B4EEFDCDDDDF444DFCF1EDD7FB990A9E6C4A0D35BFF3` | 16 paginas, no cifrado, texto extraible con `pypdf` |
| `OI_P6R_paper_v0_1.md` | `E391DC46087216DBF6193209AEC9315DBE1F7712F4D3F52A9FBCAEA169A106C5` | Borrador OI P6R |
| `paper_observacionismo_inverso.md` | `D48B2F619947A88D82A35DFB17CFDCF29CBA7E82503A3993CFC3DAE9315F06F0` | Paper OI alterno |

Autoridad comparada:

| Canon | SHA256 |
|---|---|
| `MEDIOEVO_OBSERVACIONISMO_MASTER/00_README_MASTER.md` a `22_PROMPTS_OPERATIVOS.md` | carpeta canonica 00-22 |
| `MEDIOEVO_OBSERVACIONISMO_MASTER/16_CLAIMS_REGISTER.md` | `BCAD5C9B9EAD69E7B03E4B1564B1D0A0CDC15ED1D772727339ACCF96A7088DD8` |

## Evidencia De Busqueda

Comandos usados:

- `rg` sobre fuentes Formal y `MEDIOEVO_OBSERVACIONISMO_MASTER` para `R`,
  `Phi_eff`, `J_c`, `EML`, `Markov`, `Shannon`, `Landauer`, `Friston`,
  `Amari`, `Kolmogorov`, `von Foerster`, `Luhmann`, `eta-test`, `handoff
  predictivo`, `CME`.
- `pypdf.PdfReader` sobre `BIBLIA_MEDIOEVO_Canon_Unificado.pdf`: `pages=16`,
  `encrypted=false`, texto extraible en paginas 1-2 con las mismas tesis de
  `Auto.txt`.

## Comparacion Por Delta

| Delta Formal | Ya existe en canon 00-22 / claims | Decision |
|---|---|---|
| `R` como residuo informacional y extension contextual de Shannon | `03_TEORIA_INFORMACION.md` define `H_eff(X|R)=H(X)*Phi_eff(R)` y `16_CLAIMS_REGISTER.md` tiene `I-02 R = residuo acumulado no integrado` | `NO_PATCH_DIRECTO`; se puede anexar como nota formal a `I-02`, no subir a certeza empirica |
| `Phi_eff` cuadratico cerca de `J_c` | `03_TEORIA_INFORMACION.md` usa formula exponencial y alternativa linealizada; `I-03` ya gatea Phi_eff con alcance | `NO_PATCH`; forma cuadratica compite con formulas activas y queda `RESEARCH_ONLY` |
| `EML(x,y)=e^x-ln(y)` | `03_TEORIA_INFORMACION.md`, `02_GLOSARIO_CANONICO.md`, `17_FALSADORES_Y_TESTS.md` y `A-05` ya cubren EML con gate `RESEARCH_ONLY` o hipotesis algebraica con dominio | `NO_PATCH`; hay mismatch de dominio `f(x)` vs `EML(x,y)` |
| `Sigma` con Markov blanket y `J_c(Sigma)` | `02_GLOSARIO_CANONICO.md`, `03_TEORIA_INFORMACION.md`, `07_OBSERVACIONISMO.md` y `18_RIESGOS_CONTRADICCIONES.md` ya separan Sigma, J_c fisico y J_c cognitivo | `PATCH_CANDIDATE`; solo como hipotesis formal si se declara dominio |
| OI como reconstruccion de estructura interna desde outputs, residuos y handoffs | `08_OBSERVACIONISMO_INVERSO.md` ya define IOE como output -> faltantes -> contratos -> agentes -> pruebas -> handoff | `PATCH_CANDIDATE`; el aporte nuevo es el eta-test como falsador operativo |
| Eta-test / handoff predictivo | `08_OBSERVACIONISMO_INVERSO.md` tiene plantillas y handoff, pero no formaliza eta-test | `PATCH_CANDIDATE`; agregar a claims como metodo con scope, no como superioridad empirica |
| OI como cuarta via de inferencia | No aparece asi en claims; el canon ya advierte contra claims totalizantes en `18_RIESGOS_CONTRADICCIONES.md` | `REPHRASE_REQUIRED`; decir "metodo complementario", no reemplazo historico |
| Observacionismo como meta-OS / realidad como interfaz de compresion | `00_README_MASTER.md`, `01_MAPA_GENERAL.md` y `N-02/N-04` ya bloquean universalizacion fuerte | `NO_PATCH`; conservar como narrativa/modelo con alcance |
| CME: una arquitectura se acepta si reduce R sin aumentar riesgo tecnico | Alinea con ActionGate/Wabi-Sabi, pero no existe como claim separado | `PATCH_CANDIDATE_LOW`; heuristica de diseno, no ley universal |

## Patch Pequeno Propuesto, No Aplicado

Si se ejecuta el pendiente P2, el parche minimo a `16_CLAIMS_REGISTER.md`
deberia ser solo aditivo y de bajo reclamo:

| CLAIM_ID sugerido | Claim | Gate | Falsador minimo |
|---|---|---|---|
| `I-10` | Observacionismo Inverso reconstruye estructura interna minima desde outputs, residuos, perturbaciones y handoffs predictivos. | `PUBLISH_ALLOWED_WITH_SCOPE` | Sus reconstrucciones no predicen nuevos residuos/handoffs mejor que baseline bayesiano, abductivo o caja negra |
| `I-11` | Eta-test: una hipotesis interna debe producir handoffs predictivos que sobrevivan perturbaciones no vistas. | `PUBLISH_ALLOWED_WITH_SCOPE` | Tres handoffs no vistos fallan contra prediccion pre-registrada |
| `A-10` | CME es una heuristica de diseno: aceptar arquitectura si reduce R sin aumentar riesgo tecnico real. | `PUBLISH_ALLOWED_AS_MODEL` | Un cambio que reduce R local pero aumenta riesgo tecnico debe ser bloqueado por ActionGate |

No se aplico este patch porque el pendiente P2 exige parche pequeno solo despues
de confirmacion de deltas y sigue clasificado como `external_or_gated` en el
snapshot de pendientes.

## QA Visual

No se identifico un claim que dependa de figura, grafico, formula renderizada o
layout del PDF. El PDF de la Biblia tiene texto extraible (`pypdf`, 16 paginas,
no cifrado) y reproduce las tesis ya presentes en `Auto.txt`. Por tanto, la QA
visual queda `NO_REQUERIDA_EN_ESTE_PASE`; debe reabrirse solo si un claim cita
una figura, PNG o formula cuyo significado dependa del render.

## Decision

- `16_CLAIMS_REGISTER.md` no fue mutado.
- Ningun claim cientifico/fisico fue subido de gate.
- Los deltas validos son metodologicos y de bajo reclamo.
- `Formal P1` de comparacion contra 00-22 y `16_CLAIMS_REGISTER.md` queda
  cerrado con este reporte.

