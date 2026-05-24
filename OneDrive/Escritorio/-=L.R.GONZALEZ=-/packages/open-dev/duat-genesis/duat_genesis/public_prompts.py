from __future__ import annotations


PUBLIC_PROMPTS = {
    "max_token_savings": {
        "title": "Maximum Token Savings Prompt",
        "boundary": "public",
        "license": "CC BY 4.0 or project-selected documentation license",
        "prompt": """Act as a precision compression agent.

Goal:
Reduce token usage while preserving operational meaning, decisions, constraints, evidence and next actions.

Rules:
1. Remove repetition, filler, emotional padding and duplicated context.
2. Preserve names, paths, commands, risks, decisions and unresolved questions.
3. Classify output as KEEP, COMPRESS or DROP.
4. Never remove credentials warnings, safety boundaries, tests, commands, dates or handoff state.
5. Output ESTADO, CERTEZA, INFERENCIA, INCOGNITA, ACCION, ARTEFACTO and HANDOFF.""",
    },
    "full_handoff": {
        "title": "Complete Handoff Prompt",
        "boundary": "public",
        "license": "CC BY 4.0 or project-selected documentation license",
        "prompt": """Act as a continuity handoff generator.

Goal:
Create a compact transfer packet that lets another AI continue the work without reading the entire prior session.

Include project, objective, repo/path, completed work, failures, tests, files changed, decisions, unknowns, risks,
next exact action, commands, protected/private boundaries, fingerprint and timestamp.

Classify every major statement as CERTEZA, INFERENCIA, INCOGNITA or BLOQUEO.""",
    },
}


def get_public_prompt_keys() -> tuple[str, ...]:
    return tuple(PUBLIC_PROMPTS)
