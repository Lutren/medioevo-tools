"""World Bank WDI ingest helpers for DUAT source pack v0.8."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen


API_BASE = "https://api.worldbank.org/v2"
RUN_ID = "DUAT_WDI_OFFICIAL_SOURCE_PACK_v0_8"


def build_wdi_url(country_code: str, indicator_code: str, per_page: int = 20000) -> str:
    query = urlencode({"format": "json", "per_page": str(per_page)})
    return f"{API_BASE}/country/{country_code}/indicator/{indicator_code}?{query}"


def fetch_wdi_json(country_code: str, indicator_code: str, timeout: int = 45) -> tuple[str, Any]:
    """Fetch raw WDI JSON with no credentials."""

    url = build_wdi_url(country_code, indicator_code)
    with urlopen(url, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    return url, json.loads(payload)


def write_raw_json(payload: Any, path: str | Path, pretty: bool = True) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return sha256_file(target)


def download_indicator_raw(country_code: str, indicator_code: str, raw_dir: str | Path) -> dict[str, Any]:
    """Download and store a raw World Bank WDI response."""

    accessed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    url, payload = fetch_wdi_json(country_code, indicator_code)
    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected WDI response shape for {indicator_code}")
    if isinstance(payload[0], dict) and payload[0].get("message"):
        raise ValueError(f"WDI API returned message for {indicator_code}")
    raw_path = Path(raw_dir) / f"{country_code}_{indicator_code}_raw.json"
    digest = write_raw_json(payload, raw_path)
    return {
        "country_code": country_code,
        "indicator_code": indicator_code,
        "endpoint": url,
        "accessed_at": accessed_at,
        "raw_file": raw_path.as_posix(),
        "raw_sha256": digest,
        "response_pages": payload[0] if payload and isinstance(payload[0], dict) else None,
    }


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
