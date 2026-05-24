# BLOCKED_ACTIONS

## 2026-05-07

- Action: run Wabi-Sabi local benchmark.
  Status: BLOCK.
  Evidence: `python tools\host_observacionista.py --no-write` reported
  `JAMMING/BLOCK`, `R=0.775`, `Phi_eff=0.315`, `lambda_sat=1.0`.
  Reason: host pressure and `Phi_eff < 0.60`.
  Boundary: no benchmark, no external action, no process kill.
  Retry condition: host measured standalone outside `REVIEW/BLOCK` with
  `Phi_eff >= 0.60`.
  Resolution: superseded for local benchmark only after host recheck
  `LIMPIO/APPROVE`, `R=0.338`, `Phi_eff=0.637`; `wabi e2e-smoke --json`
  passed and suite reported `64 passed in 4.80s`.

- Action: open new features, benchmarks or external actions during continuation
  2026-05-07T0137Z.
  Status: BLOCK.
  Evidence: root pending `0`, Claudio pending `0`, workpack
  `selected_items=[]`, COMMS `ok=true`; host reported `MIXTO/REVIEW`,
  `R=0.469`, `Phi_eff=0.535`, `lambda_sat=0.806`.
  Reason: `Phi_eff < 0.60` and no selected local items.
  Boundary: no publication, deploy, push, Gumroad, LinkedIn, license changes,
  private game work, destructive cleanup or broad benchmarks.
  Retry condition: isolated host gate outside `REVIEW/BLOCK` with
  `Phi_eff >= 0.60` and a real local candidate from pending/workpack.

- Action: publish bilingual MEDIOEVO GitHub profile README live.
  Status: RESOLVED_AFTER_RECHECK.
  Evidence: staging repo `publish_staging/github-profile-lutren-2026-05-01`
  is locally clean at commit `64a94b2`; secret scan on README returned
  `count_reported=0`; GitHub repo permission check returned `ADMIN`.
  Operator authorization was recorded in
  `qa_artifacts/release_validation/github-profile-readme-bilingual-operator-authorization-2026-05-07.json`.
  ActionGate decisions `c01e3352-bf81-49b8-8180-b9f0d95935f4` and
  `47c3302b-feba-479c-aa6a-aa5a1e5b54d8` both returned `blocked` for
  `public_publish`.
  Reason: host `JAMMING/BLOCK`; direct host checks also reported high pressure
  (`R=0.771`, `Phi_eff=0.316`, then `R=0.769`, `Phi_eff=0.317`).
  Boundary: no `git push`, no GitHub API publish, no LinkedIn/Gumroad/website
  or social action while target ActionGate is blocked.
  Retry condition: re-run `public_publish` target gate after host exits
  `REVIEW/BLOCK`; if allowed, push only commit `64a94b2` and verify the public
  README.
  Resolution: superseded after fresh ActionGate pass
  `2072d678-06f3-4a8c-9331-d0f13b1f1b17`; staging was rebased and published as
  `cc0134b79aa1db4f453a6e5d1de8db8ffdff3cdf`; remote README and GitHub bio
  were verified. LinkedIn remains blocked by `AUTH_UI_REQUIRED`.

- Action: edit LinkedIn profile headline/about live.
  Status: RESOLVED_AFTER_OWNER_VIEW_AUTH.
  Evidence: ActionGate `linkedin-profile-bilingual-2026-05-07` passed with
  decision `f432081b-4743-453c-84b6-db0a800a70c1`, host `LIMPIO/APPROVE`,
  `R=0.339`, `Phi_eff=0.636`. Initially no LinkedIn connector or authenticated
  browser surface was available. Later, after explicit operator authorization,
  the normal Chrome owner-view was used. LinkedIn showed save success for
  headline and About. Evidence:
  `qa_artifacts/release_validation/linkedin-bilingual-live-updated-2026-05-07.json`.
  Boundary: no cookies, browser-profile scraping, credential access or claimed
  signed-out public verification without public-view proof.
  Residual condition: public signed-out profile verification remains pending
  because LinkedIn public probing returned `HEAD=405` and `GET=999`.
# 2026-05-14 - DESPERTAR Gumroad / medioevo.space external publication blocked by host gate

- Requested action: publish `MEDIOEVO: Despertar Preview` to Gumroad and deploy updated shop to `medioevo.space`.
- Local prep completed: anti-AI review PASS, Gumroad ZIP/listing prepared, medioevo-site staging updated, local smoke PASS.
- Block reason: `python tools\host_observacionista.py --no-write` returned `JAMMING/BLOCK`.
- Evidence: R `0.635`, Phi_eff `0.388`, memory `87.2%`, disk `95.4%`, reasons `memoria_alta`, `disco_alto`, `residuo_alto`.
- Not executed: Gumroad API calls, file upload, product publish/update, Cloudflare deploy, git push.
- Report: `docs\publishing\DESPERTAR_GUMROAD_MEDIOEVO_SPACE_PUBLICATION_REPORT_2026-05-14.md`

## 2026-05-14 continuation - medioevo.space real source prepared, deploy still blocked

- Requested action: continue publication after operator said `adelante`.
- Local prep completed: real live-source repo identified as `publish_staging\medioevo-duat-public-release`; DESPERTAR store route, product content, books catalog, sitemap and llms boundary added; `src\content\despertarStore.test.ts` added.
- QA evidence: `npm test` => 5 files / 32 tests passed; `npm run build` PASS; `npm audit --audit-level=moderate` => 0 vulnerabilities; focused `src` and `public` secret scans => `count_reported=0`.
- Live finding: `https://medioevo.space/sitemap.xml` currently returns app HTML fallback, not XML `urlset`; `/despertar-preview` is not live yet.
- Block reason: final `python tools\host_observacionista.py --no-write` returned `JAMMING/BLOCK`.
- Evidence after stopping local preview: R `0.438`, Phi_eff `0.520`, memory `85.2%`, disk `95.5%`, reasons `memoria_alta`, `disco_alto`.
- Not executed: Gumroad API calls, Gumroad upload/edit/publish, Cloudflare/Wrangler deploy, git push, DNS changes.
- Report: `publish_staging\medioevo-duat-public-release\qa\DESPERTAR_STORE_STAGING_REPORT_2026-05-14.md`

## 2026-05-14 continuation - DESPERTAR target gates tested, execution still blocked

- Requested action: continue toward Gumroad and `medioevo.space` publication.
- Local prep completed: `medioevo-despertar-preview` added to `tools\release\_common.py`; `release_manifests\medioevo-despertar-preview.json` generated with `blocked_count=0`; product and release ZIP secret scans returned `count_reported=0`.
- Public package path scrub: PASS after replacing the absolute local ZIP path in `QA\ZIP_QA.json` with `releases/books/MEDIOEVO_DESPERTAR_PREVIEW_20260513_232758.zip`.
- Gumroad dry-run ActionGate: PASS for `gumroad:dmqgzi`.
- Gumroad real publish ActionGate: BLOCK, decision `6f2ab2e7-8b8d-4607-aa21-e0d0196b55be`, reason `host bloqueado por observacionismo: JAMMING/BLOCK`; owner override rejected because `host not overrideable: JAMMING/BLOCK`.
- Website deploy dry-run ActionGate: PASS for `cloudflare-pages:medioevo-site`.
- Website deploy real ActionGate: BLOCK, decision `8bc78e64-33e8-471b-9760-b1ba1cffcdc4`, reason `host bloqueado por observacionismo: JAMMING/BLOCK`.
- Latest blocking host evidence in target gates: R `0.698`, Phi_eff `0.353`, memory `89.8%`, disk `95.5%`, reasons `memoria_alta`, `disco_alto`, `residuo_alto`.
- Not executed: Gumroad API/token access, file upload, product publish/update, Wrangler deploy, git push, DNS changes.
