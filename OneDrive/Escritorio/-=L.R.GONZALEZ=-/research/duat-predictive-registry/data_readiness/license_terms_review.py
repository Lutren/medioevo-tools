"""License terms review helpers for DUAT data readiness."""

from __future__ import annotations

from typing import Any


BLOCK_TERMS = ("forbidden", "prohibited", "no internal use", "no reproduction", "not permitted")
PASS_TERMS = ("open", "public domain", "cc-by", "creative commons", "free use with attribution")


def review_license_terms(series: dict[str, Any]) -> dict[str, Any]:
    terms = str(series.get("license_terms") or "UNKNOWN").strip()
    lower = terms.lower()
    if not terms or terms.upper() == "UNKNOWN":
        return {"license_terms_scan": "REVIEW", "reason": "license terms are UNKNOWN"}
    if any(token in lower for token in BLOCK_TERMS):
        return {"license_terms_scan": "BLOCK", "reason": "license terms appear to block internal use or reproduction"}
    if any(token in lower for token in PASS_TERMS) and not series.get("license_review_required", True):
        return {"license_terms_scan": "PASS", "reason": "license terms are documented and review_required=false"}
    return {"license_terms_scan": "REVIEW", "reason": "license terms documented but human/legal review remains required"}
