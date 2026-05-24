# Audio Library Policy v1.2.1

**Fingerprint:** DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC

## Principios

- 70% sonido procedural en tiempo real
- 20% samples pequeños revisados (CC0/CC-BY)
- 10% música orquestal o stems revisados

## Licencias

| Licencia | Estado | Notas |
|----------|--------|-------|
| CC0 | APPROVED | Uso amplio, sin atribución |
| CC-BY | APPROVED* | Requiere atribución en manifest |
| CC-BY-NC | BLOCKED | No uso comercial/public builds |
| UNKNOWN | REVIEW | Requiere revisión manual |

## Reglas

1. CC0 preferred
2. CC-BY allowed solo con attribution manifest
3. CC-BY-NC blocked para commercial/public builds
4. unknown license -> REVIEW
5. NO model training desde downloaded sounds
6. NO sample copiado sin source URL, author, license, SHA256
7. publication_allowed=false by default

## Manifest

Cada sample debe tener:
- id, name, sourceUrl, author
- license (CC0/CC-BY/CC-BY-NC/UNKNOWN)
- sha256 hash
- tags, duration
- attribution (si CC-BY)

## Fuentes Recomendadas

- Freesound.org (CC0, CC-BY)
- OpenGameArt.org (CC0, OGA-BY)
- No Woosh/Sony AI (CC-BY-NC pesos)

## No Descargar

No descargar bibliotecas masivas automáticamente.
Solo 20-50 sonidos revisados, no miles.
