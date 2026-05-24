# CRM + Prompts Publication Packet - 2026-05-06

Estado: `LOCAL_PACKET_READY / EXTERNAL_BLOCKED`

Este paquete responde al pedido: actualizar LinkedIn, Gumroad, la pagina,
GitHub, dar el CRM gratis en GitHub y preparar un post sobre la liberacion de
los 3 prompts principales.

No se ejecuto publicacion externa en este ciclo.

## Verdad Operativa

- `pending_review`: `active_dedup=0`, `claudio_open=0`.
- Host gate fresco: `JAMMING/BLOCK`, `R=0.796`, `Phi_eff=0.305`,
  razones `cpu_alta`, `memoria_alta`, `proceso_dominante_cpu`,
  `residuo_alto`.
- ActionGate bloqueo los targets externos aunque el operador autorizo la
  intencion:
  - LinkedIn/post: `fd675953-478b-474d-8b1e-7d897fb3b678`
  - Gumroad: `192694a6-216a-4e49-a8a3-cecef25f0c3e`
  - GitHub FlujoCRM gratis: `a6494d97-b396-4ae7-a81e-3f0559e33e18`
  - Deploy pagina: `674d196c-4627-41a4-9d69-c7d0a7bfd485`
- Recheck ActionGate posterior: host directo marco `CONTAMINADO/REVIEW` a
  `2026-05-06T19:14:45Z`, pero cada ActionGate externo recalculo host como
  `JAMMING/BLOCK`; se mantienen bloqueados:
  - LinkedIn/post: `00c38fc2-393c-465b-9b76-27fb48eace09`
  - Gumroad: `4e666ec1-0ce2-4052-bb48-604e90474ea1`
  - GitHub FlujoCRM gratis: `0fe30efc-48e1-4785-a65a-77a81a935488`
  - Deploy pagina: `43295ef9-bc95-41db-bb44-46a607833ef3`
- GitHub CLI tiene sesion para `Lutren`, pero no se hizo push ni cambio remoto.
- SEO local de `claudio\website`: sin hallazgos mayores.
- FlujoCRM actual esta en `apps\commercial\flujocrm`, `private=true`,
  `license=UNLICENSED` y licencia comercial propietaria. Convertirlo en CRM
  gratis en GitHub requiere decision de licencia y staging limpio.

## Supuesto De Copy

`Los 3 prompts principales` se interpreta como una version publica y
public-safe de los prompts principales del metodo, no como liberacion de los
prompts internos completos, runtimes privados, calibracion propietaria,
secretos, libros privados, RPG/TCG o datos reales.

## LinkedIn Profile

Headline:

```text
Creator of MEDIOEVO | Local-first AI systems | Agent safety gates, release discipline and practical tools
```

About:

```text
I build local-first AI systems for real work: agents that leave evidence,
workflows that pass through gates before risky actions, and tools that make
handoffs, releases and public/private boundaries easier to audit.

MEDIOEVO / Claudio is my portfolio for software, books, local runtime design,
Observacionismo, public-safe AI tooling and commercial products. The open layer
contains small tools, methods, schemas, checklists and public demos. The paid
layer contains finished templates, support, UI wrappers and productized
workflows.

Current public focus:
- Evidence gates for AI agents.
- Release discipline for mixed public/private workspaces.
- Public-safe Observacionismo workflows.
- DUAT Genesis, ResidueOS and local-first tooling.
- FlujoCRM as a local-first CRM release candidate.

I do not publish secrets, private runtimes, internal orchestration, unreleased
books, RPG/TCG material, customer data or unsupported scientific/medical/social
prediction claims.
```

Featured links:

```text
GitHub: https://github.com/Lutren
Software: https://medioevo.space/software.html
Public map: https://medioevo.space/publicacion.html
Store: https://lrgonzalez.gumroad.com
Sponsors: https://github.com/sponsors/Lutren
```

## LinkedIn / Social Post

Version principal:

```text
Solte los 3 prompts principales de MEDIOEVO / Claudio en una version publica y
usable.

La idea no es que un agente haga mas cosas sin control. La idea es lo contrario:
que deje evidencia antes de actuar, que sepa cuando pedir revision y que no
mezcle secretos, trabajo privado o claims sin prueba dentro de una publicacion.

Tambien estoy preparando FlujoCRM como salida gratis en GitHub. Va por la misma
regla: licencia clara, staging limpio, secret scan, QA y frontera publica antes
de empujar nada.

La arquitectura publica queda asi:

1. prompts y metodos para organizar agentes;
2. ActionGate, witness logs y checklists para revisar acciones;
3. herramientas y productos locales que se pueden probar sin depender de una
   nube.

MEDIOEVO no es solo una pagina de libros ni solo un repo. Es una ciudad de
trabajo: canon, software, evidencia, productos y limites privados en el mismo
mapa.

GitHub: https://github.com/Lutren
Software: https://medioevo.space/software.html
Store: https://lrgonzalez.gumroad.com
```

Version corta:

```text
Solte los 3 prompts principales de MEDIOEVO / Claudio en version publica.

Regla central: no hay accion riesgosa sin evidencia, gate y frontera publica.

Tambien estoy preparando FlujoCRM para GitHub como CRM gratis, con licencia y
QA antes del push.

https://github.com/Lutren
https://medioevo.space/software.html
```

## Gumroad Update

Store tagline:

```text
MEDIOEVO digital products for local-first AI workflows, agent operations,
writing systems, DUAT templates and practical release discipline.
```

Store announcement:

```text
The public MEDIOEVO layer is expanding: three main prompt workflows are now
being prepared as public-safe operating material, and FlujoCRM is moving toward
a free GitHub release after license and QA gates.

Paid Gumroad products remain focused on time-saving artifacts: templates,
checklists, support notes, product workflows and commercial wrappers. They do
not include private prompts, internal runtime, unreleased books, RPG/TCG
material, customer data or unsupported claims.
```

FlujoCRM Gumroad note:

```text
FlujoCRM is not a paid Gumroad checkout in this packet. The current direction is
GitHub/free after license review, clean staging, scans and QA. Gumroad can later
offer support, setup help, templates or premium workflows around the free CRM.
```

## Website Copy

Target pages after gate: `software.html` and `publicacion.html`.

Suggested section:

```html
<section>
  <p class="eyebrow">New public lane</p>
  <h2>Three prompts, one gate, one free CRM path</h2>
  <p>
    MEDIOEVO / Claudio is releasing public-safe prompt workflows for agent
    orchestration, evidence-first action gates and publication handoffs. The
    boundary stays explicit: no secrets, no private runtime, no RPG/TCG assets
    and no unsupported claims.
  </p>
  <p>
    FlujoCRM is being prepared for a free GitHub release after license review,
    clean staging, secret scan and QA. The paid layer remains support,
    templates, installers and productized workflows.
  </p>
  <a href="https://github.com/Lutren">GitHub</a>
  <a href="https://lrgonzalez.gumroad.com">Gumroad</a>
</section>
```

Do not deploy this copy until ActionGate/host gate allows `medioevo-site-deploy`.

## GitHub: FlujoCRM Gratis

Owner intent recorded: make FlujoCRM free on GitHub.

Current blocker: the app is still proprietary and private in the local product
metadata.

Local staging completed after the initial packet:

- `publish_staging\github\flujocrm-free-review`
- local commit `dbead56 Initial FlujoCRM free GitHub review staging`
- 20 staged source/review files committed in the local staging repo
- secret scan `count_reported=0`
- main/preload/renderer smoke checks passed
- publication remains blocked by host/ActionGate and license decision

Evidence report:

- `docs\publishing\FLUJOCRM_FREE_GITHUB_STAGING_2026-05-06.md`
- `qa_artifacts\release_validation\flujocrm-free-github-review-staging-2026-05-06.json`
- `docs\publishing\WEBSITE_CRM_PROMPTS_DROPIN_2026-05-06.md`
- `docs\publishing\FLUJOCRM_FREE_LICENSE_DECISION_PACKET_2026-05-06.md`
- `qa_artifacts\release_validation\flujocrm-free-license-readiness-2026-05-06.json`
- `docs\publishing\FLUJOCRM_GITHUB_REPO_PACKET_2026-05-06.md`

License readiness recheck:

- `publication_ready=false`
- blockers:
  - `package_license_not_free`
  - `package_lock_root_license_not_free`
  - `package_private_true`
  - `proprietary_markers_present`

Required safe path:

1. Decide release license: MIT, Apache-2.0, AGPL, freeware/source-available or
   another explicit license.
2. Create a clean GitHub staging folder or repo from allowlist only.
3. Exclude `dist`, `node_modules`, local runtime data, `.env`, credentials,
   private assets, Gumroad/Stripe data, logs and build artifacts.
4. Update `package.json` only in staging after license decision.
5. Replace or remove `COMMERCIAL_LICENSE.md` only after legal/owner license
   decision is recorded.
6. Run:
   - `npm run check`
   - `npm audit --audit-level=high`
   - `python tools\release\scan_secrets.py --product flujocrm --json`
   - path scrub and claims scan on staging
7. Push only when target ActionGate and host gate allow it.

Proposed public repo copy after gate:

```text
FlujoCRM is a local-first CRM for freelancers, small teams and operators who
want contacts, pipeline stages and follow-up notes without a hosted SaaS
account. This free GitHub release focuses on source transparency and local
use. Support, setup help, templates and polished installers may remain paid.
```

## Do Not Publish

- Private prompts or raw master prompt internals.
- Full Claudio runtime orchestration.
- Secrets, tokens, account state or local configs.
- Unreleased books, canon vaults or editorial private material.
- RPG/TCG assets, lore, mechanics or bridge code.
- FlujoCRM installer/source as public until license, staging, QA and ActionGate
  pass.

## Next Gate

Re-run when host pressure is lower:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio
python tools\host_observacionista.py --no-write
python tools\action_gate_cli.py public_publish --target github-flujocrm-free-release --external-authorized --evidence-ref <fresh-host-report>
python tools\action_gate_cli.py public_publish --target medioevo-site-deploy --external-authorized --evidence-ref <fresh-host-report>
python tools\action_gate_cli.py public_publish --target linkedin-profile-post --external-authorized --evidence-ref <fresh-host-report>
python tools\action_gate_cli.py public_publish --target gumroad-products-update --external-authorized --evidence-ref <fresh-host-report>
```
