# Wave FC Client Operating Model

Clasificacion: COMMERCIAL_DRAFT

Estado: documento de producto. No autoriza venta automatica, despliegue cloud ni
acciones externas.

## Tesis

Wave FC es una capa de control documental y operativo reversible para trabajo
con clientes.

No es solo:

- un analista que resume documentos;
- un DBA que consulta tablas;
- un chatbot que responde preguntas;
- un editor que reescribe archivos.

Wave FC controla el ciclo completo:

```text
recibir -> aislar -> observar -> evidenciar -> proponer -> aprobar -> aplicar a copia -> revertir
```

## Producto

Wave FC debe operar como producto local o servidor privado.

| modo | uso | datos | salida |
|---|---|---|---|
| `wave-local` | operador individual | archivos sanitizados locales | reporte, diff/redline, rollback pack |
| `wave-private-server` | equipo o cliente | documentos y datos read-only en red privada | expedientes, aprobaciones, evidencia |
| `wave-client-workspace` | consultor con varios clientes | frontera por cliente/proyecto/caso | control de mezcla y auditoria |

Sin autorizacion explicita, ningun modo usa cloud, publica contenido, llama APIs
externas ni escribe en sistemas del cliente.

## Objetos del Dominio

| objeto | descripcion | regla |
|---|---|---|
| `Client` | persona, empresa o equipo atendido | no se mezcla con otros clientes |
| `Workspace` | frontera local de un cliente o proyecto | tiene politica propia |
| `Case` | expediente operativo concreto | agrupa documentos, datos y decisiones |
| `Document` | archivo original registrado por hash | nunca se edita directo |
| `WorkingCopy` | copia operativa | unica superficie editable |
| `Connector` | fuente read-only, por ejemplo CSV o SQLite | no escribe en MVP |
| `DecisionLog` | registro de evaluaciones y aprobaciones | append-only |
| `EvidenceManifest` | evidencia usada y faltante | separa certeza e incognita |
| `RollbackPack` | paquete para revertir o explicar cambios | obligatorio para aplicar |

## Flujo Operativo

1. Intake

El operador crea un caso y declara objetivo, limites, cliente, nivel de riesgo y
formatos permitidos.

2. Registro

Wave calcula hash del original, crea copia de trabajo y registra metadatos
minimos: fuente, fecha, operador, cliente/proyecto/caso.

3. Observacion

Wave extrae senales del documento y de conectores read-only. No interpreta una
base como verdad absoluta; la trata como evidencia con procedencia.

4. Receptores

Cada propuesta pasa por receptores:

- privacidad;
- evidencia;
- politica;
- estilo;
- contexto de cliente;
- rollback;
- revision humana.

5. Salida

Wave genera reporte con:

```text
CERTEZA
INFERENCIA
INCOGNITA
RIESGO
CAMBIO PROPUESTO
SIGUIENTE ACCION
```

6. Aplicacion

Solo `apply-to-copy` puede modificar contenido, y solo sobre copia. Si falta
diff/redline, evidence manifest o rollback pack, la aplicacion queda bloqueada.

## Capas

| capa | responsabilidad |
|---|---|
| `intake layer` | recibe documentos, objetivo, limites y consentimiento |
| `storage layer` | guarda hashes, copias, decisiones y packs locales |
| `connector layer` | lee CSV/SQLite u otras fuentes sin escribir |
| `receptor layer` | filtra privacidad, evidencia, politica, estilo y rollback |
| `approval layer` | exige revision humana cuando hay impacto alto |
| `export layer` | entrega expediente, redline, manifest y rollback |

## Lo Que Wave Puede Hacer

- Ordenar documentos empresariales por cliente, proyecto y caso.
- Detectar contradicciones, campos faltantes, terminos ambiguos y riesgos de
  proceso.
- Comparar un documento contra politica interna o briefing autorizado.
- Convertir un archivo suelto en expediente con evidencia.
- Proponer redline sobre copia.
- Crear paquetes de rollback y auditoria.
- Preparar decisiones para revision humana.

## Lo Que Wave No Debe Prometer

- No da asesoramiento legal, financiero, fiscal, medico ni terapeutico.
- No garantiza compliance.
- No automatiza aprobaciones de alto impacto.
- No escribe en bases de datos de cliente durante el MVP.
- No publica, compra, envia ni firma sin autorizacion humana explicita.
- No procesa secretos, `.env`, tokens, sesiones, canon privado, RPG ni libros
  completos como demo.

## Recomendaciones de Producto

1. Vender el primer MVP como `Document Control Layer`, no como analista de IA.
2. Mostrar siempre los artefactos: hash, copia, diff/redline, decision log,
   evidence manifest y rollback pack.
3. Usar demo con documentos sanitizados y conectores read-only.
4. Separar planes:
   - Local individual.
   - Servidor privado para equipos.
   - Servicio de implementacion para consultores.
5. Mantener `human review required` en recomendaciones legales, financieras,
   medicas, fiscales, compliance, despidos, pagos, firmas y publicaciones.

## Gate de Preparacion

Wave no debe pasar de draft a venta si no puede demostrar, con artefactos:

- original intacto;
- hash before/after;
- copia de trabajo;
- diff/redline;
- decision log;
- evidence manifest;
- rollback pack;
- bloqueo de secretos;
- bloqueo de escritura en conectores read-only;
- aprobacion humana para acciones de alto impacto.
