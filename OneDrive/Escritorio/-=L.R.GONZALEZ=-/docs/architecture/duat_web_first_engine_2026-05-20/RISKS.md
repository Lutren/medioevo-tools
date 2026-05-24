# RISKS

- R-001: `quaternaryAdapter` y `witnesslog` tienen estado global; replay completo no esta cerrado.
- R-002: Godot-first puede aumentar peso web y duplicar logica antes de estabilizar sim-core.
- R-003: Zips con `.git`/vendor/builds pueden contaminar el arbol si se adoptan crudos.
- R-004: Cloud enrichment puede romper local-first si no pasa por cache, hash y ProviderGate.
- R-005: Sprites iluminados sin normales/height maps pueden verse planos con camaras dramaticas.
- R-006: React state loop limita agent_count si no se mueve sim/render hot path a worker/external store.

