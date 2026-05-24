# DUAT Dual-Lane Cognitive Filter v0.1

publication_gate: BLOCK

## Objetivo

Separar informacion limpia, residuo estructurado y ruido real antes de alimentar
agentes o prediccion DUAT.

```text
Input = S_clean + R_structured + R_noise
Output_Final = alpha * CleanResult + beta * UserAdaptedResult + gamma * StructuredResidueNotes
```

## Lanes

- `CleanResult`: version completa, operativa y lista para agentes.
- `UserAdaptedResult`: version adaptada al patron cognitivo del usuario.
- `StructuredResidueNotes`: residuo util, no tratado como hecho factual.

## Pesos

- Tareas tecnicas/criticas: `alpha >= 0.70`, `beta <= 0.25`, `gamma <= 0.10`.
- Tareas creativas/explicativas: `alpha >= 0.40`, `beta <= 0.50`, `gamma <= 0.15`.
- `R_sensitive` domina siempre y puede bloquear el output.
