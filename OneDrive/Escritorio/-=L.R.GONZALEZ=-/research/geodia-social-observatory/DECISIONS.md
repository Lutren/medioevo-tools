# DECISIONS

## 2026-05-22 - Smallville-DUAT Evidence Refresh

- Revalidar y cerrar el carril con la implementacion existente en lugar de
  crear otra simulacion paralela.
- Mantener los artefactos nuevos como QA local sintetica bajo
  `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522`.
- No ejecutar Colab, Kaggle, SimScale, sensores, datos reales ni publicacion.

## 2026-05-17 - DUAT Smallville v0.2

- Decision: conectar SignalSourcePack sintetico local al motor Smallville-DUAT sin red ni datos reales.
- Razon: permite convertir el baseline Smallville en simulacion cientifica auditable con canales ambientales, replay y falsadores.
- Consecuencia: v0.2 queda CPU-only, con 25 agentes fijos, ledgers grandes por trazabilidad y PublicationGate BLOCK.

## 2026-05-17 - Contradicciones MTS

- Decision: una contradiccion fuerte no puede promediarse hasta APPROVE.
- Razon: si `R_contradiction >= 0.50`, el gate minimo debe ser REVIEW aunque la confianza agregada parezca alta.
- Consecuencia: el falsador `contradiction_preservation` bloquea cualquier fusion que oculte contradicciones.

## 2026-05-17 - Remote compute v0.2

- Decision: Colab, Kaggle y SimScale no se ejecutan en este run.
- Razon: el objetivo es cierre local CPU sintetico; remote compute queda en REVIEW separado.
- Consecuencia: v0.3 sugerido es UI panel de evidencia, no compute remoto.

## 2026-05-17 - DUAT Smallville v0.1

- Decision: implementar la simulacion como laboratorio sintetico local-first.
- Razon: permite comenzar simulaciones sin GPU ni nube y mantiene evidencia reproducible.
- Consecuencia: datos reales, cloud runtime y claims predictivos siguen gateados.

## 2026-05-17 - Remote compute

- Decision: `local_cpu=APPROVE_LOCAL`, `colab_notebook=REVIEW`, `kaggle_kernel=REVIEW`, `simscale=REVIEW`.
- Razon: Colab/Kaggle/SimScale requieren runtime externo, cuenta, cuota, posible costo o credenciales.
- Consecuencia: se genera plan y notebook, pero no se ejecuta externo desde Codex.

## 2026-05-17 - Bias claim

- Decision: usar `AUDITABLE_NOT_ABSENT`.
- Razon: ningun simulador serio debe prometer ausencia total de sesgo; debe medirlo, acotarlo y falsarlo.
- Consecuencia: cualquier copy que diga "sin sesgos" debe bajarse a claim auditable.
