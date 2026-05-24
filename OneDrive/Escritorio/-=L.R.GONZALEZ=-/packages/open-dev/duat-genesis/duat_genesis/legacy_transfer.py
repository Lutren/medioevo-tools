from __future__ import annotations


LEGACY_TRANSFER_DOCS = (
    "FAMILY_README_START_HERE.md",
    "LEGACY_OPERATOR_GUIDE.md",
    "REVENUE_AND_PUBLICATION_HANDOFF.md",
    "WHAT_IS_SAFE_TO_SHARE.md",
    "WHAT_MUST_STAY_PRIVATE.md",
)


def legacy_transfer_checklist() -> tuple[str, ...]:
    return (
        "List public URLs without credentials.",
        "List paid products without tokens or dashboard secrets.",
        "Explain which folders are private and must not be shared.",
        "Keep books, RPG, TCG, private prompts and raw datasets out of public releases.",
        "Record recovery contacts and account procedures outside public repos.",
    )
