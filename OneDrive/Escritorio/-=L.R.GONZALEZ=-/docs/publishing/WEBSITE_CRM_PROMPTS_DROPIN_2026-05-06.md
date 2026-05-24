# Website CRM/Prompts Drop-in - 2026-05-06

Estado: `READY_LOCAL_DROPIN / DO_NOT_DEPLOY`

Este archivo deja listo el cambio de pagina pedido para el paquete CRM/prompts
sin tocar el HTML vivo. La fuente canonical del sitio es
`-=MEDIOEVO=-\-=LIBROS\claudio\website`, pero ese worktree tiene cambios
activos de otros agentes y el host gate sigue bloqueando publicacion externa.

## ActionGate

- Target: `medioevo-site-deploy`
- Estado vigente: `BLOCK`
- Motivo: host `JAMMING/BLOCK`, recursos altos y worktree compartido sucio.
- Accion permitida en este ciclo: documentar drop-in, no aplicar ni desplegar.

## Insertion Targets

Aplicar solo cuando el host y el target gate permitan cambios:

- `-=MEDIOEVO=-\-=LIBROS\claudio\website\software.html`
  - Insercion sugerida: despues del hero, antes de la primera
    `section class="section-head"` que introduce los problemas objetivo.
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\publicacion.html`
  - Insercion sugerida: despues del `section class="lane-grid"` o antes de
    `section class="section-head"` de repos publicos.

## Software Page Section

```html
<section class="boundary" aria-labelledby="crm-prompts-release">
  <p class="eyebrow">Public lane ready</p>
  <h2 id="crm-prompts-release">Three public prompts and a free CRM path</h2>
  <p>
    MEDIOEVO / Claudio is preparing three public-safe prompt workflows for
    agent orchestration, evidence-first action gates and publication handoffs.
    The boundary stays explicit: no secrets, no private runtime, no RPG/TCG
    assets and no unsupported claims.
  </p>
  <p>
    FlujoCRM is staged locally for a future free GitHub release after license
    review, clean staging, secret scan and QA. The paid layer remains support,
    templates, installers and productized workflows around the free source.
  </p>
  <div class="cta-row">
    <a class="btn primary" href="https://github.com/Lutren" target="_blank" rel="noopener">GitHub</a>
    <a class="btn" href="https://lrgonzalez.gumroad.com" target="_blank" rel="noopener">Gumroad</a>
    <a class="btn" href="/publicacion.html">Open/private boundary</a>
  </div>
</section>
```

## Publicacion Page Card

```html
<article class="card">
  <h3>FlujoCRM free GitHub lane</h3>
  <p>
    FlujoCRM has a local review-only GitHub staging repo ready. Publication is
    still gated until the release license is decided and ActionGate allows the
    external push.
  </p>
  <div class="tag-row">
    <span class="tag open">GitHub pending</span>
    <span class="tag open">secret scan clean</span>
    <span class="tag paid">support/services later</span>
  </div>
</article>
```

## Publicacion Page Boundary Line

```html
<li>
  FlujoCRM can move to a free GitHub lane only from the clean staging repo, not
  from the commercial working tree, and only after a license decision.
</li>
```

## Validation Required After Applying

```powershell
python C:\Users\L-Tyr\.agents\skills\seo-growth-medioevo\scripts\seo_audit_medioevo.py --site-root C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website
python tools\release\scan_secrets.py --path -=MEDIOEVO=-\-=LIBROS\claudio\website\software.html --json
python tools\release\scan_secrets.py --path -=MEDIOEVO=-\-=LIBROS\claudio\website\publicacion.html --json
git -C -=MEDIOEVO=-\-=LIBROS\claudio\website diff --check -- software.html publicacion.html
```

Do not deploy until `medioevo-site-deploy` passes target-specific ActionGate and
the live URL is verified after deployment.
