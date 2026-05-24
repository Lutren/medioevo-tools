# Formal Claims Delta - 2026-05-08

> Math canon update 2026-05-20: `07b_MATEMATICAS_RIGUROSO.md` replaces the
> original document 07. Old EML, R and Phi formulations in this intake remain
> historical observations only and must not be promoted without the 07b forms
> and falsifiers F1-F6.

## Scope

This document records claims or claim-like deltas found in `Formal`. It does not update `16_CLAIMS_REGISTER.md` directly; that requires a later curated merge after excerpt comparison.

## Candidate Claim Deltas

| Source | Claim / delta | Proposed gate | Reason |
|---|---|---|---|
| `report.md` | R as conditional mutual information and contextual extension of Shannon entropy. | `PUBLISH_AS_FORMAL_HYPOTHESIS` | Coherent as formal model, but "CERTEZA" wording is stronger than current validation. |
| `report.md` | Phi_eff quadratic decay around J_c, with analogies to Landau/Ising critical behavior. | `RESEARCH_ONLY` | Useful math metaphor; needs derivation/calibration before strong claim. |
| `report.md` | DEPRECATED historical EML form `EML(x,y)=exp(x)-ln(y)` as compression-expansion operator and renormalization analogy. | `HISTORICAL_ONLY` | Replaced by 07b sigmoidal EML; keep only as provenance. |
| `report.md` | Sigma profile with Markov blanket and J_c(Sigma) capacity function. | `PUBLISH_AS_FORMAL_HYPOTHESIS` | Formalizable but not empirically calibrated. |
| `OI_P6R_paper_v0_1.md` | Observacionismo Inverso reconstructs internal structure from outputs, residues and handoffs. | `PUBLISH_AS_FORMAL_HYPOTHESIS` | Good method candidate; superiority remains unvalidated. |
| `OI_P6R_paper_v0_1.md` | Eta-test: a reconstruction must predict unseen residues/handoffs better than baselines. | `PUBLISH_ALLOWED_WITH_SCOPE` | Useful falsifier framing; needs benchmark suite. |
| `paper_observacionismo_inverso.md` | OI as "fourth way" beyond deduction, induction and abduction. | `REPHRASE_REQUIRED` | Strong epistemic positioning; safer as proposed method, not historical replacement. |
| `Auto.txt` / `BIBLIA_MEDIOEVO_Canon_Unificado.pdf` | Observacionismo as meta-operating system for knowledge and reality as compression interface. | `PUBLISH_ALLOWED_WITH_SCOPE` | Valid as operational/narrative model, not physical totalizing claim. |
| `Auto.txt` | CME principle: systems accept architecture if it reduces R without increasing technical risk. | `PUBLISH_ALLOWED_AS_MODEL` | Useful design heuristic; not universal law. |
| `Completar*`, `P*R`, `PR*` | Prompt compression and EML experiment evidence. | `RESEARCH_ONLY` | Keep dataset/evidence; needs methodology, baselines and reproducibility notes. |
| `nucleo.txt` / `uno.py` | RAM/cache/process priority improves host stability and longevity. | `REPHRASE_REQUIRED` | Host tuning may be useful but claims about electrical residue/longevity are unverified. |
| `Para materializar...` / `The Solution...` | Direct intent-to-shell execution pipeline for Wabi-Sabi. | `BLOCK` for execution, `RESEARCH_ONLY` for design pattern | SafeExecutor and manual review are required before any generated execution. |
| `Untitled.txt` | Prompts for bypassing commercial/legal/security barriers via "matriz epistemica". | `REPHRASE_REQUIRED` / `BLOCK` where bypass intent appears | Keep defensive/conceptual analysis only; avoid bypass framing and proprietary/secret extraction. |
| `banananana.txt` | Not a claim; private provider credential/config source. | `BLOCK_PUBLICATION` | Operational value only: confirms secret-safe cloud adapter need. No scientific, technical-novelty or canon claim should be derived from raw credentials. |

## Comparison With Current Claim Register

Current authority remains `MEDIOEVO_OBSERVACIONISMO_MASTER\16_CLAIMS_REGISTER.md`.

Observed alignment:

- R, Phi_eff, J_c and ActionGate already exist as scoped operational concepts.
- OSIT/fisica strong claims remain gated in current register.
- Browser/automation/security boundaries remain REVIEW/BLOCK.
- Wabi-Sabi remains local coding-agent shell with gates, not unrestricted autonomy.

Observed deltas:

- `Formal` gives a more mathematical information-theory framing for R/Phi_eff/Sigma/EML than the master summary.
- `Formal` contains an OI paper draft that can become a method note if cleaned and compared with existing `08_OBSERVACIONISMO_INVERSO.md`.
- `Formal` contains unsafe execution patterns that should become negative requirements for SafeExecutor, not runtime code.

## Required Merge Step

Before editing `16_CLAIMS_REGISTER.md`, run an excerpt comparison for:

- `report.md` against `03_TEORIA_INFORMACION.md`, `07_OBSERVACIONISMO.md`, `17_FALSADORES_Y_TESTS.md`.
- `OI_P6R_paper_v0_1.md` and `paper_observacionismo_inverso.md` against `08_OBSERVACIONISMO_INVERSO.md`.
- `Auto.txt` and the PDF against `00_README_MASTER.md`, `01_MAPA_GENERAL.md`, `16_CLAIMS_REGISTER.md`, `18_RIESGOS_CONTRADICCIONES.md`.

Update 2026-05-13: excerpt comparison completed in
`docs/intake/FORMAL_CLAIMS_EXCERPT_COMPARISON_2026-05-13.md`. Result: no direct
claim-register mutation; only three low-claim patch candidates (`I-10`, `I-11`,
`A-10`) are proposed for a later gated P2 patch.

## Decision

- No public claim upgraded.
- No physics/science claim marked verified.
- No claim register mutation in this pass.
- Next safe action: produce a small patch to `16_CLAIMS_REGISTER.md` only after excerpt comparison confirms non-duplicative deltas.
