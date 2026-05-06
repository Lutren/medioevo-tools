# Gumroad Claudio Software Drafts Recheck - 2026-05-06

Status: `DIRECT_URLS_LIVE / COPY_FIX_READY / NO_GUMROAD_SAVE_EXECUTED`

This closes the local evidence pass for the pending item:

```text
Gumroad Claudio software: pack-empresarial, writer-workbench and claudio-full
exist as drafts/pending store items; do not publish until files/covers/checkout
are verified.
```

## Gate

Latest host gate: `MIXTO / REVIEW` at `2026-05-06T09:46:37Z`.

No Gumroad dashboard/API save, file upload, price change, publish action or
checkout change was executed in this pass.

## Direct URL Findings

| slug | HTTP | product id | price | finding |
|---|---:|---|---:|---|
| `pack-empresarial` | `200` | `czgpdw` | `US$19` | direct page exists with strong capability/security copy |
| `writer-workbench` | `200` | `sdkigo` | `US$97` | direct page exists; package/export/right boundary not verified here |
| `claudio-full` | `200` | `fhkhdo` | `US$197` | direct page exists; bundle promises multiple gated products and future delivery |

Evidence JSON:

```text
qa_artifacts/release_validation/gumroad-claudio-software-drafts-recheck-2026-05-06.json
```

## Current Risk

The URLs are public by direct link even if they are not promoted on the store
profile. The risk is not checkout existence alone; it is buyer-facing copy that
can imply stable delivery, security guarantees or private-runtime access before
the final package gate.

## Safe Replacement Copy

Use this in a Gumroad target window if the products remain visible by direct
link. Do not attach files or publish/promote until product packages pass their
own release gates.

### `pack-empresarial`

Short description:

```text
Founder-access business workflow pack for MEDIOEVO local tools. This page is for guided access and updates while the final customer package is reviewed.
```

Description:

```text
This is not an instant-download stable release yet.

Founder access may include reviewed demos, setup notes, early builds, business workflow templates and implementation support for local-first MEDIOEVO tools.

It does not include private Claudio runtime, private prompts, secrets, account sessions, unreleased books, RPG/TCG material, customer data, guaranteed security, guaranteed uptime, or a finished enterprise CRM bundle.

Use this tier only if you understand it is early access and may require direct support before delivery.
```

Recommended store status: `request access / founder access only`.

### `writer-workbench`

Short description:

```text
Founder-access writing workflow pack for MEDIOEVO. Final export package and editorial boundaries are still under review.
```

Description:

```text
This listing is for reviewed founder access, not a public stable download.

The intended package is a local-first writing workflow with templates, setup notes, export guidance and MEDIOEVO writing support material after editorial and package review.

It does not include unpublished books, private canon vaults, RPG/TCG material, private prompts, account sessions, secrets, guaranteed AI writing quality or unrestricted use of MEDIOEVO lore.

The final customer artifact must pass package, rights, privacy and support checks before broad checkout.
```

Recommended store status: `request access / founder access only`.

### `claudio-full`

Short description:

```text
Founder-access bundle interest page for Claudio/MEDIOEVO local tools. Final stable desktop bundle is not yet a public download.
```

Description:

```text
This is an early-access/support lane, not an immediate stable desktop bundle.

Supporters may receive reviewed demos, setup guidance, public-safe workflows and updates as the local tools are packaged.

It does not include private runtime internals, private prompts, secrets, account access, unpublished books, RPG/TCG material, proprietary calibration, guaranteed autonomy, guaranteed security or final support terms.

Do not treat this as a finished lifetime bundle until the release manifest, installer, legal/support copy, checkout and post-purchase delivery are verified.
```

Recommended store status: `request access / founder access only`.

## Required Before Any Gumroad Save

1. Confirm authenticated target product id in Gumroad.
2. Confirm whether the product is visible, unlisted or profile-listed.
3. Run focused secret and claims scans on replacement copy.
4. Confirm no files are attached unless the package artifact is verified.
5. Save only one target at a time.
6. Verify the public URL after save.
7. Record screenshot or HTTP evidence before claiming live completion.
