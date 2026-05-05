# Sponsors, APIs and Session Audit - 2026-05-05

Ficha tecnica local para la capa publica. Este documento no contiene valores de
tokens, cookies, claves, IPs ni rutas publicables completas. Es evidencia de
capacidad y frontera operativa, no autorizacion general para publicar.

## Resumen ejecutivo

| superficie | estado | decision |
|---|---|---|
| GitHub profile repo `Lutren/Lutren` | CERTEZA: API disponible y cambios aplicados | KEEP / usar como carril publico principal |
| GitHub Sponsors funding links | CERTEZA: `.github/FUNDING.yml` actualizado | KEEP / verificacion remota hecha |
| GitHub Sponsors tiers/goals | REVIEW: dashboard/UI requerido | no reintentar por API hasta cambiar permisos |
| Website MEDIOEVO | REVIEW: credenciales Cloudflare detectadas; deploy sigue gateado | preparar copy y desplegar solo con release gate |
| Gumroad | REVIEW: tokens/sesion detectados; productos requieren gate individual | no borrar/listar productos sin producto objetivo |
| LinkedIn y redes | REVIEW: historial/sesion posible, sin API segura confirmada | entregar copy paste-ready; live edit solo con validacion visual |
| Google/YouTube | REVIEW: OAuth/sesion detectada | no publicar ni modificar canal sin target y gate |
| Stripe/Shopify/Reddit/Twitter/Discord | REVIEW: claves o variables detectadas | usar solo con runbook especifico y secreto redacted |
| AI APIs | CERTEZA: Anthropic, Gemini y ElevenLabs detectadas por nombre | usar para trabajo local, no para publicar estado |

## Cambios GitHub ejecutados

| item | evidencia | decision |
|---|---|---|
| Profile README | commit `fb60732e5a8a7c564a44d54d363d7915a9ff64b0`, mensaje `Update public profile publication lanes` | publicado en repo publico |
| Funding links | commit `5d760ada6692a4b944f0065b6f95f1748ad6fcbc`, mensaje `Update GitHub Sponsors funding links` | publicado en repo publico |
| Bio/blog | `gh api user` confirma bio local-first y blog `https://medioevo.space` | publicado en perfil |

Contenido remoto verificado de funding:

```yaml
github: [Lutren]
custom:
  - https://medioevo.space/publicacion.html
  - https://medioevo.space/software.html
  - https://lrgonzalez.gumroad.com
```

Limite importante: los tiers/goals de Sponsors no quedaron editados por API en
este pase. La ruta correcta sigue siendo dashboard/UI con evidencia manual,
porque la mutacion de tiers/goals ya estaba bloqueada por permisos en corridas
previas.

## Inventario de credenciales por capacidad

Se verifico presencia de credenciales por nombre y fuente, sin exponer valores.

| canal | fuente detectada | capacidad prudente |
|---|---|---|
| GitHub | entorno `GH_TOKEN` y credencial keyring de `gh` | leer/escribir repos propios, profile README, funding y perfil |
| Cloudflare | variables en `.env` de Claudio | deploy website solo despues de release gate |
| Gumroad | `.env.gumroad`, `gumroad_api.json`, variables de entorno | verificar productos y preparar listings; mutacion producto por producto |
| Stripe | variables de entorno en archivos locales | revisar checkout/configuracion, no crear precios ni payouts sin gate |
| Shopify | variable de acceso local | solo revisar si hay tienda objetivo |
| Google/YouTube | OAuth local y sesiones de navegador | revisar canal/YouTube solo con objetivo explicito |
| Anthropic/Gemini/ElevenLabs/Hugging Face/NVIDIA | variables de entorno y secretos locales | soporte de build/investigacion, sin publicacion externa |
| Discord/Reddit/Twitter | variables de bot/API locales | no publicar ni automatizar social sin copy, target y rollback |

## Chrome / sesiones observadas

Lectura local no destructiva de historial indica uso reciente o posible sesion
en: GitHub, Gumroad, Cloudflare, Stripe, LinkedIn, Instagram, TikTok, Reddit,
YouTube, Google, Gemini, Anthropic, OpenAI y ChatGPT.

Esto no prueba sesion activa. Para cualquier edicion en navegador el protocolo
es:

1. Abrir la superficie objetivo.
2. Confirmar visualmente cuenta y permisos.
3. Aplicar copy public-safe.
4. Guardar evidencia de pantalla o API de verificacion.
5. Registrar resultado en `PORTFOLIO_EXECUTION_LEDGER.md` o doc de canal.

## ActionGate

| accion | gate | razon |
|---|---|---|
| Actualizar `.github/FUNDING.yml` | APPROVE | target exacto, contenido public-safe, sin secretos |
| Actualizar bio/blog GitHub | APPROVE | target exacto, bajo claim, sin rutas privadas |
| Editar Sponsors tiers/goals por API | REVIEW | permiso API insuficiente; usar dashboard |
| Editar LinkedIn/Gumroad/Cloudflare por navegador | REVIEW | requiere validacion visual de cuenta y publish gate |
| Publicar contenido teorico fuerte, medico, fisico o predictivo | BLOCK | claims fuertes requieren revision profesional/evidencia |
| Publicar RPG/TCG/canon privado/datasets/prompts internos | BLOCK | frontera privada |

## Siguiente lote recomendado

1. Verificar en navegador el dashboard de Sponsors y registrar screenshot si la
   sesion esta activa.
2. Actualizar website solo cuando `publicacion.html` pase secret scan y gate de
   deploy.
3. Usar API Gumroad para leer productos y generar diff de copy, no publicar ni
   borrar drafts en lote.
4. LinkedIn queda en copy paste-ready hasta confirmacion visual del perfil
   exacto y sesion autenticada.
