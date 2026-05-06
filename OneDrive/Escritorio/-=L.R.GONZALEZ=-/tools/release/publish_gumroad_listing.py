from __future__ import annotations

import argparse
import hashlib
import json
import math
import mimetypes
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests

from _common import ROOT, add_common_args, rel, validate_root_arg
from publish_free_dev_github import (
    ACTION_GATE_CLI,
    CLAUDIO_ROOT,
    HOST_GATE,
    PUBLICATION_EVIDENCE_DIR,
    override_can_release,
    run,
    run_json,
    scan_claims,
    scan_path_scrub,
)


API_BASE = "https://api.gumroad.com/v2"
ENV_FILE = CLAUDIO_ROOT / ".env.gumroad"
DEFAULT_LISTING = ROOT / "packages" / "paid" / "medioevo-agent-ops-pack" / "commerce" / "gumroad_listing.json"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_token() -> str:
    load_env_file(ENV_FILE)
    token = os.environ.get("GUMROAD_ACCESS_TOKEN") or os.environ.get("GUMROAD_TOKEN")
    if not token:
        raise RuntimeError("Missing GUMROAD_ACCESS_TOKEN in environment or .env.gumroad")
    return token


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def gumroad_request(method: str, endpoint: str, token: str, **kwargs: Any) -> dict[str, Any]:
    url = f"{API_BASE}{endpoint}"
    response = requests.request(method, url, timeout=180, **kwargs)
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text[:2000]}
    if response.status_code >= 400 or payload.get("success") is False:
        raise RuntimeError(f"Gumroad {method} {endpoint} failed: status={response.status_code} body={payload}")
    return payload


def upload_file_to_gumroad(token: str, file_path: Path) -> str:
    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    presign = gumroad_request(
        "POST",
        "/files/presign",
        token,
        data={
            "access_token": token,
            "filename": file_path.name,
            "file_size": str(file_path.stat().st_size),
            "content_type": mime_type,
        },
    )
    parts = presign.get("parts", [])
    if not parts:
        raise RuntimeError(f"Gumroad presign returned no parts: {presign}")

    total_size = file_path.stat().st_size
    chunk_size = total_size if len(parts) <= 1 else math.ceil(total_size / len(parts))
    etags: list[tuple[str, str]] = []
    with file_path.open("rb") as handle:
        for index, part in enumerate(parts):
            start = index * chunk_size
            current_size = min(chunk_size, max(total_size - start, 0))
            if current_size <= 0:
                raise RuntimeError("Upload failed: empty chunk")
            handle.seek(start)
            chunk = handle.read(current_size)
            if len(chunk) != current_size:
                raise RuntimeError("Upload failed: short chunk read")
            upload_response = requests.put(
                part["presigned_url"],
                data=chunk,
                headers={"Content-Type": mime_type, "Content-Length": str(len(chunk))},
                timeout=900,
            )
            upload_response.raise_for_status()
            etags.append((str(part["part_number"]), upload_response.headers.get("ETag", "")))

    complete_data: list[tuple[str, str]] = [
        ("access_token", token),
        ("upload_id", presign["upload_id"]),
        ("key", presign["key"]),
    ]
    for part_number, etag in etags:
        complete_data.append(("parts[][part_number]", part_number))
        complete_data.append(("parts[][etag]", etag))
    complete = gumroad_request("POST", "/files/complete", token, data=complete_data)
    if not complete.get("file_url"):
        raise RuntimeError(f"Gumroad complete did not return file_url: {complete}")
    return str(complete["file_url"])


def list_products(token: str) -> list[dict[str, Any]]:
    payload = gumroad_request("GET", "/products", token, params={"access_token": token})
    return payload.get("products", [])


def find_product(products: list[dict[str, Any]], listing: dict[str, Any]) -> dict[str, Any] | None:
    wanted_short = str(listing["short_url"]).strip().lower()
    wanted_name = str(listing["name"]).strip().lower()
    for product in products:
        short_url = str(product.get("short_url") or product.get("permalink") or product.get("custom_permalink") or "").lower()
        name = str(product.get("name") or "").lower()
        if short_url.endswith("/" + wanted_short) or short_url == wanted_short:
            return product
        if name == wanted_name:
            return product
    return None


def product_payload(listing: dict[str, Any], publish: bool, file_url: str | None = None) -> dict[str, str]:
    payload = {
        "name": str(listing["name"]),
        "price": str(listing["price"]),
        "description": str(listing["description"]),
        "short_url": str(listing["short_url"]),
        "custom_permalink": str(listing["short_url"]),
        "content_type": str(listing.get("content_type", "digital")),
        "published": "true" if publish else "false",
        "shown_on_profile": "true" if publish else "false",
        "require_shipping": "false",
        "customizable_price": "false",
    }
    if file_url:
        payload["files[][url]"] = file_url
    return payload


def summarize_product(product: dict[str, Any] | None) -> dict[str, Any] | None:
    if not product:
        return None
    return {
        "id": product.get("id"),
        "name": product.get("name"),
        "published": product.get("published"),
        "price": product.get("price"),
        "short_url": product.get("short_url") or product.get("permalink") or product.get("custom_permalink"),
        "preview_url": product.get("preview_url"),
        "sales_count": product.get("sales_count"),
    }


def summarize_api_result(result: dict[str, Any] | None) -> dict[str, Any] | None:
    if not result:
        return None
    product = result.get("product") if isinstance(result, dict) else None
    return {
        "success": result.get("success") if isinstance(result, dict) else None,
        "product": summarize_product(product) if isinstance(product, dict) else None,
    }


def gate_decision(
    listing: dict[str, Any],
    artifact_path: Path,
    execute: bool,
    product_name: str,
    manifest_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    metadata = {
        "receptor_id": "publish_receptor",
        "product": product_name,
        "listing_name": listing["name"],
        "short_url": listing["short_url"],
        "artifact": rel(artifact_path),
        "sha256": sha256_file(artifact_path),
        "mode": "execute" if execute else "dry_run_plan",
        "lane": "gumroad",
    }
    command = [
        sys.executable,
        str(ACTION_GATE_CLI),
        "gumroad_publish",
        "--target",
        f"gumroad:{listing['short_url']}",
        "--external-authorized",
        "--evidence-ref",
        str(manifest_path),
        "--metadata-json",
        json.dumps(metadata, ensure_ascii=False),
    ]
    if not execute:
        command.insert(3, "--dry-run")
    return run_json(command, CLAUDIO_ROOT)


def create_product(token: str, listing: dict[str, Any], publish: bool, with_file: bool, artifact_path: Path) -> dict[str, Any]:
    file_url = upload_file_to_gumroad(token, artifact_path) if with_file else None
    return gumroad_request("POST", "/products", token, data={"access_token": token, **product_payload(listing, publish, file_url)})


def update_product(token: str, product_id: str, listing: dict[str, Any], publish: bool, with_file: bool, artifact_path: Path) -> dict[str, Any]:
    file_url = upload_file_to_gumroad(token, artifact_path) if with_file else None
    return gumroad_request("PUT", f"/products/{product_id}", token, data={"access_token": token, **product_payload(listing, publish, file_url)})


def enable_product(token: str, product_id: str) -> dict[str, Any]:
    return gumroad_request("PUT", f"/products/{product_id}/enable", token, data={"access_token": token})


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish a single Gumroad listing with evidence gates.")
    add_common_args(parser)
    parser.add_argument("--listing", default=str(DEFAULT_LISTING))
    parser.add_argument("--create-draft", action="store_true")
    parser.add_argument("--with-file", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--owner-override-with-evidence", action="store_true")
    parser.add_argument("--override-operator", default="Luis Rene Gonzalez")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)
    if args.publish and not args.create_draft:
        raise SystemExit("--publish must be paired with --create-draft")

    listing_path = Path(args.listing)
    if not listing_path.is_absolute():
        listing_path = ROOT / listing_path
    listing = json.loads(listing_path.read_text(encoding="utf-8"))
    product_name = str(listing.get("product_name") or Path(str(listing["product_file"])).stem)
    artifact_path = ROOT / str(listing["product_file"])
    source_dir = ROOT / str(listing.get("source_dir") or f"packages/paid/{product_name}")
    manifest_path = ROOT / "release_manifests" / f"{product_name}.json"

    missing = [rel(path) for path in (listing_path, artifact_path, source_dir, manifest_path) if not path.exists()]
    host = run([sys.executable, str(HOST_GATE)], CLAUDIO_ROOT)
    commands: list[dict[str, object]] = []
    if missing:
        data = {"ok": False, "missing": missing, "host_gate_command": host}
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 1

    secret_scan_source = run([sys.executable, str(ROOT / "tools" / "release" / "scan_secrets.py"), "--product", product_name, "--json", "--fail-on-findings"], ROOT)
    secret_scan_artifact = run([sys.executable, str(ROOT / "tools" / "release" / "scan_secrets.py"), "--artifact", rel(artifact_path), "--json", "--fail-on-findings"], ROOT)
    commands.extend([secret_scan_source, secret_scan_artifact])
    path_scrub = scan_path_scrub(source_dir)
    claims_scan = scan_claims(source_dir)
    gate_command, gate_payload = gate_decision(listing, artifact_path, args.create_draft, product_name, manifest_path)
    commands.append(gate_command)
    host_payload = gate_payload.get("action_gate", {}).get("host_gate", {})
    override_applied = False
    override_reason = ""
    if args.owner_override_with_evidence and args.create_draft and not bool(gate_payload.get("ok")):
        override_ok, override_reason = override_can_release(gate_payload.get("action_gate", {}), {"gate": host_payload})
        override_applied = bool(override_ok)

    preflight_ok = (
        secret_scan_source["returncode"] == 0
        and secret_scan_artifact["returncode"] == 0
        and bool(path_scrub.get("ok"))
        and bool(claims_scan.get("ok"))
        and (bool(gate_payload.get("ok")) or override_applied)
    )

    token = None
    products_before = None
    existing_before = None
    api_result = None
    enable_result = None
    verified_after = None
    operation = "dry_run"
    external_error = None
    if preflight_ok and (args.create_draft or args.verify):
        try:
            token = get_token()
            products_before = list_products(token)
            existing_before = find_product(products_before, listing)
            if args.create_draft:
                operation = "update_product" if existing_before else "create_product"
                if existing_before:
                    api_result = update_product(token, str(existing_before["id"]), listing, args.publish, args.with_file, artifact_path)
                else:
                    api_result = create_product(token, listing, args.publish, args.with_file, artifact_path)
            if args.verify or args.create_draft:
                verified_after = find_product(list_products(token), listing)
            if args.publish and verified_after and not bool(verified_after.get("published")):
                enable_result = enable_product(token, str(verified_after["id"]))
                verified_after = find_product(list_products(token), listing)
        except Exception as exc:
            external_error = str(exc)

    data = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "operation": operation,
        "published_requested": bool(args.publish),
        "with_file_requested": bool(args.with_file),
        "owner_override": {
            "requested": args.owner_override_with_evidence,
            "applied": override_applied,
            "operator": args.override_operator if args.owner_override_with_evidence else "",
            "reason": override_reason,
        },
        "listing": {
            "product_name": product_name,
            "name": listing["name"],
            "short_url": listing["short_url"],
            "price": listing["price"],
            "currency": listing.get("currency", "usd"),
        },
        "artifact": {
            "path": rel(artifact_path),
            "size_bytes": artifact_path.stat().st_size,
            "sha256": sha256_file(artifact_path),
        },
        "host_gate_command": host,
        "path_scrub": path_scrub,
        "claims_scan": claims_scan,
        "action_gate": gate_payload.get("action_gate", {}),
        "commands": commands,
        "preflight_ok": preflight_ok,
        "existing_before": summarize_product(existing_before),
        "api_result": summarize_api_result(api_result),
        "enable_result": summarize_api_result(enable_result),
        "verified_after": summarize_product(verified_after),
        "external_error": external_error,
    }
    publish_ok = not args.publish or bool(verified_after and verified_after.get("published"))
    data["ok"] = bool(preflight_ok and not external_error and (not args.create_draft or verified_after) and publish_ok)

    if args.write:
        PUBLICATION_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        target = PUBLICATION_EVIDENCE_DIR / f"gumroad-{listing['short_url']}.json"
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        data["written"] = rel(target)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"gumroad:{listing['short_url']}: {'ok' if data['ok'] else 'blocked'}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
