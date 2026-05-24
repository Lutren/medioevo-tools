# R_PHI_JC

R mide residuo acumulado; Phi_eff mide conversion de input en cierre; J_c es el umbral de jamming.

## Escala operativa

| R | Color humano | Lectura |
|---:|---|---|
| 0.00-0.17 | verde | Cierre limpio, bajo residuo. |
| 0.18-0.37 | amarillo | Residuo bajo-medio, revisar pendientes. |
| 0.38-0.61 | naranja | Riesgo de friccion, requiere sintesis y evidencia. |
| 0.62-0.81 | rojo | Alto residuo, priorizar desbloqueo. |
| 0.82-1.00 | rojo/jamming | Jamming: demasiada friccion para continuar sin reducir contexto, bloqueo o incertidumbre. |

Cuando una IA o interfaz soporte color, usar gradiente verde -> amarillo -> naranja -> rojo. Cuando no soporte color, imprimir siempre la etiqueta textual y el valor numerico.
