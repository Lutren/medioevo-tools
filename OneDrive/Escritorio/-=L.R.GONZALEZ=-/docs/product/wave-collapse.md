# Wave Function Collapse

Clasificacion: COMMERCIAL_DRAFT

Estado: MVP 1 implementado como `Document Collapse` CLI. Local/servidor
privado como direccion de producto. No publicado. No listo para venta
automatica.

## Oferta

Wave Function Collapse, o Wave FC, es un agente reversible para auditoria,
edicion y ordenamiento de documentos empresariales.

Convierte documentos intervenidos por agentes en cambios revisables, auditables
y reversibles, sin tocar el original.

Wave FC no es solo un analista de documentos ni un DBA local. Es una capa de
control documental y operativo: recibe archivos, datos read-only y contexto de
cliente; los convierte en expedientes trazables; propone acciones bajo
receptores; y bloquea cualquier aplicacion que no tenga evidencia, copia,
decision log y rollback.

Metafora publica:

> Wave FC crea una burbuja privada alrededor de tus archivos y datos. Dentro de
> esa ola, cada documento queda conectado, ordenado y auditado.

No se vende como asesoramiento legal, financiero, medico, compliance garantizado
ni productividad garantizada.

## Publico inicial

- Operadores y equipos de operaciones.
- Consultores con documentos de cliente.
- Equipos comerciales que editan propuestas y briefs.
- Founders y builders que necesitan trazabilidad.
- Equipos de producto con specs y handoffs.
- Revisores internos que necesitan redline, evidencia y rollback.
- Personas neurodivergentes que necesitan ordenar documentos, ideas, evidencia,
  proyectos y habilidades sin recibir juicio personal.

## Formatos MVP

- `.docx`
- Markdown
- texto plano
- CSV y SQLite read-only como conectores posteriores de ordenamiento local.

## Posicionamiento operativo

Wave FC vive entre la informacion del cliente y cualquier agente que quiera
actuar sobre ella.

```text
documentos / datos read-only / contexto del cliente
  -> Wave FC control layer
  -> expediente, evidencia, cambio propuesto, aprobacion humana y rollback
```

Su trabajo no es "responder mejor" ni "consultar una base de datos". Su trabajo
es mantener control:

- `intake_control`: registra fuente, objetivo, limites y hash del original.
- `context_control`: conecta documentos, cliente, proyecto, caso y datos
  read-only sin mezclarlos con runtime privado.
- `decision_control`: separa `CERTEZA`, `INFERENCIA`, `INCOGNITA` y `RIESGO`.
- `action_control`: permite solo auditoria, sugerencia o aplicacion sobre copia.
- `rollback_control`: exige diff/redline, evidence manifest y rollback pack.
- `human_control`: marca decisiones legales, financieras, medicas o comerciales
  como revision humana obligatoria.

## Modos

- `audit-only`: audita y reporta sin proponer aplicacion.
- `suggest-edits`: propone cambios con evidencia, sin aplicar.
- `apply-to-copy`: aplica solo sobre copia y genera diff/redline.

## Perfiles

- `enterprise`: documentos empresariales, clientes, casos, borradores,
  recomendaciones revisables y control de riesgo.
- `neurodivergent-workspace`: apoyo cognitivo/laboral para convertir ideas y
  documentos dispersos en mapa de proyectos, habilidades, evidencia y siguiente
  accion. No diagnostica ni reemplaza terapia.

## Salida canonica

```text
original_hash
working_copy_path
diff_or_redline_path
decision_log
evidence_manifest
rollback_pack
report_path
workspace_profile
```

## Receptores documentales

El MVP usa el patron abstracto de transduccion selectiva:

```text
documento -> senales -> receptores documentales -> reporte/diff reversible
```

Receptores iniciales:

- `privacy_receptor`: bloquea secretos, `.env`, tokens, sesiones y rutas privadas.
- `evidence_receptor`: exige evidencia o marca `INCOGNITA`.
- `policy_receptor`: detecta riesgo legal/compliance/negocio sin prometer asesoria.
- `style_receptor`: conserva tono, estructura y terminologia acordada.
- `rollback_receptor`: bloquea aplicacion si falta hash, diff/redline o rollback pack.
- `client_context_receptor`: impide mezclar clientes, proyectos o casos sin
  frontera explicita.
- `human_review_receptor`: detiene recomendaciones medicas, financieras,
  legales, fiscales o de alto impacto hasta aprobacion humana.

Sin receptor activo no hay cambio aplicado, solo auditoria.

El reporte usa:

```text
CERTEZA
INFERENCIA
INCOGNITA
RIESGO
CAMBIO PROPUESTO
SIGUIENTE ACCION
```

## Artefactos actuales

- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\WAVE_COLLAPSE_PRODUCT_SYSTEM_2026-04-29.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\WAVE_COLLAPSE_MVP_SPEC_2026-04-29.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\WAVE_FUNCTION_COLLAPSE_ENTERPRISE_SPEC_2026-04-29.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\WAVE_FC_CLAUDIO_WABI_SABI_ARCHITECTURE_2026-04-29.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\WAVE_NEURODIVERGENT_WORKSPACE_2026-04-29.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\WAVE_FC_PRIVATE_SERVER_2026-04-29.md`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\WAVE_COLLAPSE_DEMO_5_MIN_2026-04-29.md`
- `website\wave-collapse.html`

## Gates

- No editar originales.
- No Gumroad, Ko-fi, Buy Me a Coffee, redes ni publicacion sin ActionGate y
  autorizacion explicita.
- No cloud ni APIs externas en MVP.
- No automatizar recomendaciones medicas, financieras, legales, fiscales o de
  cumplimiento sin revision humana.
- No escribir en bases de datos de cliente en el MVP; solo conectores read-only.
- No Gemma hasta `host_observacionista=APPROVE`.
- No Symphony daemon ni `wide`.
- No rutas privadas, canon, RPG, libros completos, secretos, `.env`, tokens,
  sesiones ni prompts sensibles.

## Modelo cliente/servidor local

Ver `docs/product/wave-fc-client-operating-model.md`.

Resumen:

- `Wave Local`: CLI o app de escritorio para un operador con documentos
  sanitizados.
- `Wave Private Server`: servidor en red privada del cliente, sin cloud por
  defecto, con usuarios, roles, aprobaciones y auditoria.
- `Wave Client Workspace`: frontera por cliente/proyecto/caso para impedir que
  documentos y datos se mezclen.
- `Wave Evidence Pack`: artefacto exportable que explica que cambio se propuso,
  por que, con que evidencia, quien lo aprobo y como revertirlo.

## Siguiente accion

Probar el flujo con un `.md` y un `.docx` sanitizados:

1. confirmar que el original no cambia;
2. confirmar hash before/after;
3. confirmar diff/redline;
4. confirmar decision log y evidence manifest;
5. confirmar rollback pack;
6. confirmar que una persona empresarial puede responder: que cambio, por que,
   donde, quien lo propuso y como revertirlo.
