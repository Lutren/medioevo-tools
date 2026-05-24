from __future__ import annotations

import json
import re
import shutil
import textwrap
import zipfile
from hashlib import sha256
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_PORTAFOLIO_HUMANO_IA_2026-05-16")
INTERNAL = ROOT / "INTERNO_COMPLETO"
PUBLIC = ROOT / "PUBLIC_SAFE"

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
for candidate in [Path(r"C:\Windows\Fonts\arial.ttf"), Path(r"C:\Windows\Fonts\calibri.ttf")]:
    if candidate.exists():
        pdfmetrics.registerFont(TTFont("PortfolioRegular", str(candidate)))
        FONT_REGULAR = "PortfolioRegular"
        break
for candidate in [Path(r"C:\Windows\Fonts\arialbd.ttf"), Path(r"C:\Windows\Fonts\calibrib.ttf")]:
    if candidate.exists():
        pdfmetrics.registerFont(TTFont("PortfolioBold", str(candidate)))
        FONT_BOLD = "PortfolioBold"
        break


SOURCES = """Local sources reviewed: BRAIN_OS agent knowledge portfolio, BRAIN_OS MOI/DO/IOI, BRAIN_OS ScienceClaimGate, MEDIOEVO_OBSERVACIONISMO_MASTER information theory, DUAT/GEODIA/Hormiguero, COMMS agents_state, harness_manifest, and public profile SEO/business report 2026-05-16.

External anchors: NIST SI speed of light c = 299,792,458 m/s exact (https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-7-rules-and-style-conventions-expressing-values); CERN Standard Model (https://home.cern/science/physics/standard-model/); OpenStax sensory transduction (https://openstax.org/books/biology-2e/pages/36-1-sensory-processes); NASA/Hubble cosmic history and light travel time (https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/time-travel-observing-cosmic-history/); Feynman Nobel lecture / Wheeler positron idea as speculative historical context, not proof (https://www.nobelprize.org/prizes/physics/1965/feynman/lecture/)."""

COMMON_GATE = """Epistemic gate:
- CERTEZA: artifact, test, source, path, hash, or directly verified state.
- INFERENCIA: useful operational model that still needs calibration.
- INCOGNITA: missing validation, legal review, empirical proof, or owner confirmation.
- BLOQUEO: do not publish credentials, raw vaults, complete unpublished books, RPG/TCG, private runtime, unsupported AGI/physics/consciousness claims, or payment/admin changes without target gate."""

AGENTS = """Observed COMMS agents:
- claims-falsifier-observatorio
- claudio-local-agent
- claudio-local-autonomy
- community-sponsors-observatorio
- curador-seto
- editorial-research-release
- hormiguero-mission-control
- prensa-observatorio
- publicacion-perfiles-observatorio
- publicidad-growth-observatorio
- social-media-observatorio
- wabi-sabi-sentido-comun

Observed harness skills:
- argus-ops
- curador-operativo
- hormiguero-surface
- medioevo-editorial
- medioevo-gumroad
- medioevo-release
- medioevo-seo
- modelo-router"""


def publicize(text: str) -> str:
    replacements = {
        "INTERNO_COMPLETO": "PUBLIC_SAFE",
        "No publicar sin revision.": "Share only after human review.",
        "patrimonio sensible": "non-public material",
        "runtime privado": "non-public runtime",
        "libros completos no aprobados": "unpublished books",
        "RPG/TCG": "private game material",
    }
    out = text
    for old, new in replacements.items():
        out = out.replace(old, new)
    out += "\n\nPublic-safe note: this version is orientation material only. It omits private implementation detail, raw source dumps, non-public manuscripts, private game material, credentials, and unsupported strong claims.\n"
    return out


DOCS: list[dict[str, str]] = [
    {
        "id": "01",
        "title": "Portafolio Maestro Frontera y Gaps",
        "body": f"""# 01 - Portafolio Maestro, Frontera y Gaps

## Proposito
Este documento organiza MEDIOEVO / OSIT / Claudio / DUAT como portafolio humano y para IA. No es un volcado total del archivo; es un mapa curado para explicar que existe, que esta listo, que falta y que se debe proteger.

## Tesis del portafolio
MEDIOEVO no es solo teoria ni solo producto. Es un sistema de investigacion, ejecucion y publicacion con tres niveles: canon conceptual, runtime operativo y superficie publica/comercial.

## Las 10 piezas canonicas del paquete
1. Portafolio maestro, frontera y gaps.
2. Sistema de investigacion MOI / DO / IOI.
3. Teoria de informacion digital.
4. Teoria de informacion fisica / causal rendering.
5. DUAT: descripcion y funciones.
6. Agentes, personalidades y correcciones.
7. Skills, herramientas y sistemas.
8. Matematicas cientificas OSIT / DUAT.
9. Biologia, IA y transduccion.
10. Business / SEO / GitHub / LinkedIn / Gumroad.

## Que falta para que sea un portafolio completo
- Demo publico de DUAT separado de DUAT privado.
- Screenshots y media final para GitHub, LinkedIn, website y Gumroad.
- Revision legal/comercial de licencias y precios.
- README bilingue definitivo por producto.
- Agent packet public-safe para cada rol clave.
- Matriz de publicacion que conecte producto, claim, evidence y gate.
- Website deploy solo tras scan limpio del target.
- LinkedIn confirmado desde vista autenticada del propietario.

## Estado publico al 2026-05-16
GitHub profile fue actualizado y verificado con commit 10f103834e1d72895ce73fb1511fe1ebf715d954. Website staging fue endurecido localmente pero no desplegado por findings de revision. Gumroad quedo vivo sin cambios. LinkedIn requiere confirmacion autenticada.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "02",
        "title": "Sistema de Investigacion MOI DO IOI",
        "body": f"""# 02 - Sistema de Investigacion MOI / DO / IOI

## Definicion
MOI es el sistema de investigacion de MEDIOEVO para convertir intuicion, archivos, conversaciones, codigo y evidencia en artefactos verificables. Opera con dos movimientos: DO e IOI.

## DO: Deconstruccion Observacionista
DO separa cada entrada en claim, fuente, estado epistemico, riesgo, falsador y ruta. Evita que una intuicion se convierta en dogma o copy publico sin frontera.

## IOI: Ingenieria Observacionista Inversa
IOI reconstruye desde el resultado deseado. Si el objetivo es una teoria, genera ecuaciones, falsadores y source cards. Si es producto, genera README, tests, manifests y gates. Si es continuidad, genera SessionFingerprint, NextSessionBrief y WitnessLog.

## Loop operativo
```text
Entrada -> DO -> source card -> IOI -> artefacto -> QA -> handoff
```

## Variables
```text
R = residuo acumulado
Phi_eff = eficiencia de actualizacion
J_c = umbral de jamming
ActionGate = APPROVE / REVIEW / BLOCK
ScienceClaimGate = public-safe / formal-lab / blocked-as-fact
PublicationGate = BLOCK salvo evidencia y autorizacion target-specific
```

## Resultado esperado
Un agente que usa MOI no produce volumen por reflejo. Cierra loops: clasifica, verifica, crea artefacto, ejecuta QA y deja proxima accion medible.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "03",
        "title": "Teoria de Informacion Digital",
        "body": f"""# 03 - Teoria de Informacion Digital

## Tesis
La informacion digital no es solo bits almacenados. En MEDIOEVO se mide por capacidad de registro, recuperacion, accion y continuidad. Un dato que existe pero no puede ser usado por el agente opera como informacion oscura.

## Modelo base
```text
H_eff(X | R) = H(X) * Phi_eff(R)
```
`H(X)` es informacion disponible; `R` es residuo acumulado; `Phi_eff` es eficiencia de actualizacion; `H_eff` es informacion utilizable.

## Diferencia con Shannon
Shannon mide informacion transmisible por canal. OSIT pregunta que informacion puede integrar un receptor con estado, memoria, ruido, contradicciones, herramientas y latencia.

## Residuo digital
```text
R_next = R_prev + noise + contradiction + open_loops - verified_closure
```
Un repositorio con muchos archivos puede subir informacion disponible pero bajar informacion util si no hay indices, manifests, tests o handoff.

## Stack de informacion util
Archivo -> source card -> claim register -> schema -> test -> handoff -> producto.

## Falsadores
Si agregar contexto mejora siempre, el modelo de R pierde valor. Si un brief no permite reconstruir decisiones, no preserva informacion util. Si un agente no distingue fuente, inferencia y bloqueo, el sistema no esta controlando informacion.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "04",
        "title": "Teoria de Informacion Fisica Causal Rendering",
        "body": f"""# 04 - Teoria de Informacion Fisica / OSIT Causal Rendering

## Status
Formal-lab / operational extension. No prueba fisica, no prueba de conciencia, no claim de AGI y no identidad literal foton-electron.

## Frase canonica
La velocidad de la luz puede interpretarse operacionalmente como limite de actualizacion causal de un observador, no solo como velocidad de vision humana.

## Ecuacion principal
```text
RenderedReality(O, e) = Decode(
  InformationInsidePastCausalCone(O, e),
  ObserverState(O),
  InterfaceStack(O),
  ChannelLimits,
  Noise,
  CalibrationContract
)
```

## Extension de InterfaceState
```text
O_i(t) = D_i(X(t - tau_i), S_i(t), K_i, B_i, N_i)
H_eff_i(X,t) = H_in(X,t) * Phi_eff_i(S_i, R_i, tau_i, K_i, B_i)
CausalRender_i(e) = D_i(C_i(e), S_i, K_i, B_i, N_i)
```

## Submodelos
Transduction Ladder: senales fisicas distintas pueden compararse como senales transducidas a codigos internos, sin decir que son la misma fisica.

Finite-Space / Infinite-State: el universo observable de un agente es limitado por horizonte causal, resolucion e interfaz.

Electromagnetic Dual-Aspect: electron como persistencia cargada/localizada; foton como propagacion libre/evento detectable del campo electromagnetico.

Gravity-Light Compression: agujero negro como cierre causal extremo; no foton = agujero negro.

## Bloqueos
No afirmar como hecho: foton = electron, foton = agujero negro, un solo foton literal, gravedad convierte electrones en fotones, conciencia probada en luz, OSIT prueba fisica universal.

## Anclas
NIST fija c exacta; CERN separa electrones y fotones en el Modelo Estandar; OpenStax documenta transduccion sensorial; NASA explica luz distante como estados pasados; Feynman/Wheeler es antecedente especulativo, no prueba.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "05",
        "title": "DUAT Descripcion y Funciones",
        "body": f"""# 05 - DUAT: Descripcion y Funciones

## Definicion
DUAT es una superficie de operacion cognitiva: display/orquestador para trabajos de IA con muchos agentes, memoria, evidencia, geografia conceptual, gates, handoff y simulacion. En GEODIA/Hormiguero, DUAT es la ciudad visible donde humanos y agentes ven estado, rutas y acciones.

## Funciones principales
- Orquestar agentes y departamentos.
- Mostrar estado de tareas, memoria, witness logs y gates.
- Separar APPROVE, REVIEW y BLOCK antes de acciones externas.
- Convertir sesiones largas en brief, fingerprint, report y manifest.
- Conectar producto, investigacion y runtime sin mezclar capas privadas/publicas.

## Componentes logicos
```text
Input humano/IA -> ActionGate -> TaskManager -> AgentPool -> WitnessLog -> Handoff -> Public/Private Router
```

## Paneles esperados
Mission Control, Agents, Claims/Falsifiers, Tools, Products, Boundary, Reports.

## Reglas de DUAT
La v1 publica debe ser read-only o synthetic-only. No autopublica, no ejecuta pagos/deploys/redes sin gate, no presenta claims cientificos fuertes como validacion y no incluye datos reales privados ni runtime interno.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "06",
        "title": "Agentes Personalidades y Correcciones",
        "body": f"""# 06 - Agentes, Personalidades y Correcciones

## Inventario actual
{AGENTS}

## Problema a corregir
Los agentes tienen ownership y gates, pero la personalidad debe ser una capa separada. Si personalidad modifica permisos, el agente puede actuar teatralmente y perder rigor.

## Esquema recomendado
```json
{{
  "agent_id": "...",
  "role": "...",
  "persona_style": {{
    "anchor": "figura historica o mitologica",
    "virtue": "criterio principal",
    "voice": "tono operativo",
    "shadow_risk": "exceso que debe evitar",
    "must_not_override": ["ActionGate", "ScienceClaimGate", "ownership", "boundary"]
  }}
}}
```

## Asignacion propuesta
- curador-seto -> Thoth/Hermes escriba: archivo, fichas, trazabilidad.
- claudio-local-agent -> Daedalus: constructor local, puentes, herramientas.
- claudio-local-autonomy -> Athena: prudencia estrategica.
- hormiguero-mission-control -> Janus: entradas/salidas, pasado/futuro.
- wabi-sabi-sentido-comun -> Seneca: sobriedad y reduccion de ruido.
- claims-falsifier-observatorio -> Karl Popper/Socrates: falsadores y preguntas.
- publicacion-perfiles-observatorio -> Hermes/Mercury: mensajeria publica.
- publicidad-growth-observatorio -> Benjamin Franklin: impresor/growth pragmatico.
- prensa-observatorio -> Ida B. Wells: evidencia publica rigurosa.
- social-media-observatorio -> Scheherazade: narrativa serial sin revelar de mas.
- community-sponsors-observatorio -> Maecenas: patronazgo y comunidad.
- editorial-research-release -> Hypatia: estudio, edicion y publicacion cuidada.

## Politica
Personalidad no concede permisos. Todo agente conserva ActionGate, ScienceClaimGate, ownership y boundary.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "07",
        "title": "Skills Herramientas y Sistemas",
        "body": f"""# 07 - Skills, Herramientas y Sistemas

## Inventario observado
{AGENTS}

## Herramientas de control
ActionGate, ScienceClaimGate, SecretScan/BoundaryScan, WitnessLog, SessionFingerprint, NextSessionBrief, ClaimRegister/Falsifiers y source cards.

## Sistemas
- BRAIN_OS: canon y operacion viva; extraer solo public-safe.
- Claudio: runtime local y agentes; publicable parcialmente.
- Wabi-Sabi: CLI/agente local; sin credenciales/proveedores privados.
- CEREBRO: protocolos y canon; publicar solo con gates.
- DUAT: display/orquestacion; demo synthetic/read-only.
- GEODIA: ciudad/simulacion/datos; public-safe con datos sinteticos.
- COMMS: bus de agentes; no publicar streams privados.
- GitHub/Gumroad/Website/LinkedIn: superficies publicas con gates.

## Que falta
Catalogo unico con estado por herramienta, tests por skill, owner por sistema, version public-safe por herramienta y matriz de permisos para red/pagos/publicacion.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "08",
        "title": "Matematicas Cientificas OSIT DUAT",
        "body": f"""# 08 - Documento Cientifico de Matematicas OSIT / DUAT

## Informacion utilizable
```text
H_eff(X | R) = H(X) * Phi_eff(R)
```

## Degradacion por residuo
```text
Phi_eff(R, J_c) = exp(-nu * R / (J_c - R))  para R < J_c
Phi_eff = 0                                 para R >= J_c
Phi_eff = Phi_0 * (1 - R/J_c)^nu            version lineal inicial
```

## Residuo dinamico
```text
R_next = clamp(R_prev + noise + contradiction + open_loops - verified_closure, 0, 1)
```

## Vector R
```text
R_vector = [R_context, R_io, R_claims, R_tools, R_memory, R_publication]
R_total = w dot R_vector
```

## EML / costo de carga
```text
f(x) = exp(x) - log(x), x > 0
f'(x) = exp(x) - 1/x
minimo cuando x * exp(x) = 1, x = W(1) aprox 0.567143
```

## Causal Render
```text
CausalRender_i(e) = D_i(C_i(e), S_i, K_i, B_i, N_i)
```

## DUAT task score
```text
TaskPriority = Impact * Urgency * EvidenceReadiness / (Risk + Residue + HandoffCost)
```

## Gate decision
APPROVE si es local, reversible, testeable y dentro de ownership. REVIEW si toca red, pagos, legal, publicacion, credenciales, datos reales o arquitectura grande. BLOCK si destruye, exfiltra, publica privado o afirma claims prohibidos.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "09",
        "title": "Biologia IA y Transduccion",
        "body": f"""# 09 - Documento Cientifico: Biologia, IA y Transduccion

## Tesis
La vida y la cognicion no acceden a una realidad directa; operan con transductores. Celulas, sentidos, instrumentos y herramientas de IA convierten diferencias fisicas en codigos internos accionables.

## Escalera de transduccion
```text
estimulo fisico -> receptor/transductor -> senal interna -> integracion -> accion/memoria
```

## Ejemplos
- Radiacion EM -> retina/opsinas -> codigo visual.
- Vibracion/presion -> coclea -> audicion.
- Deformacion -> mecanorreceptores -> tacto.
- Aceleracion/inercia -> vestibular -> orientacion.
- Archivos/logs/comandos -> herramientas Wabi/Codex -> estado operativo.

## IA como interfaz transductora
Un agente de IA no ve el mundo directamente. Ve texto, archivos, rutas, logs, screenshots, APIs y tool outputs. Su realidad operativa es lo que puede decodificar, retener y actuar bajo gates.

## Cuidado biologico/medico
Diferencias sensoriales o de integracion pueden inspirar modelos de input/integracion distintos. No hacer diagnosticos, no prometer tratamiento, no convertir analogias en claims medicos.

## BioDigital / MIMI
```text
O_i(t) = D_i(X(t - tau_i), S_i(t), K_i, B_i, N_i)
```
La lectura correcta es interfaz con latencia, memoria, ruido, calibracion y ancho de banda.

## Falsadores
Si el modelo no mejora clasificacion de claims biologicos, no aporta. Si promueve intencionalidad bacteriana, falla boundary. Si confunde transduccion con equivalencia fisica literal, falla ScienceClaimGate.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
    {
        "id": "10",
        "title": "Business SEO GitHub LinkedIn Gumroad",
        "body": f"""# 10 - Business / SEO / GitHub / LinkedIn / Gumroad

## Objetivo
Convertir el portafolio tecnico-teorico en una superficie comprensible para colaboradores, clientes, sponsors y agentes de IA sin regalar patrimonio sensible.

## GitHub
Perfil actualizado y verificado. El README ahora apunta a software, store, Sponsors y boundary. Commit: 10f103834e1d72895ce73fb1511fe1ebf715d954.

## Website
Vivo publicamente. Staging endurecido localmente, pero no desplegado. Cambios locales: home/sitemap dejan de empujar ruta privada, checkout directo deshabilitado hacia Gumroad, ruta sensible noindex/nofollow. Faltan 4 findings de scan antes de deploy.

## Gumroad
Profile y productos publicos verificados en lectura. No se cambio copy/precio/media en este run. Recomendacion: mantener Gumroad como checkout seguro hasta revisar pagos directos del website.

## LinkedIn
No editar hasta confirmar desde sesion autenticada. La lectura publica devuelve 999; no hay evidencia suficiente para aplicar cambios.

## SEO pragmatico
Ruta clara homepage -> GitHub -> Gumroad -> Sponsors. Metadata y JSON-LD consistentes. Sitemap sin rutas privadas. Copy por problema/solucion. Evitar claims fuertes de AGI, prediccion, medicina, seguridad total o fisica demostrada.

## Copy recomendado
MEDIOEVO builds local-first AI tools and research workflows for complex projects: evidence gates, handoffs, agent coordination, source cards and public-safe product templates.

{COMMON_GATE}

## Fuentes
{SOURCES}""",
    },
]


def pdf_safe_line(line: str) -> str:
    return line.replace("`", "").replace("\t", "    ")


def write_pdf(pdf_path: Path, title: str, text: str) -> None:
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    margin = 54
    y = height - margin
    footer = f"MEDIOEVO Portfolio - {pdf_path.stem}"

    def new_page() -> None:
        nonlocal y
        c.setFont(FONT_REGULAR, 8)
        c.drawString(margin, 28, footer[:120])
        c.showPage()
        y = height - margin

    c.setTitle(title)
    for raw_line in text.splitlines():
        line = pdf_safe_line(raw_line.rstrip())
        if not line:
            y -= 12
            if y < margin:
                new_page()
            continue
        is_h1 = line.startswith("# ")
        is_h = line.startswith("##") or is_h1
        font = FONT_BOLD if is_h else FONT_REGULAR
        size = 15 if is_h1 else 12 if is_h else 9.5
        clean = re.sub(r"^#+\s*", "", line)
        max_chars = 62 if is_h else 88
        for chunk in textwrap.wrap(clean, width=max_chars, replace_whitespace=False) or [""]:
            c.setFont(font, size)
            c.drawString(margin, y, chunk[:170])
            y -= 16 if is_h else 12
            if y < margin:
                new_page()
    c.setFont(FONT_REGULAR, 8)
    c.drawString(margin, 28, footer[:120])
    c.save()


def header(title: str, variant: str) -> str:
    gate = "BLOCK_INTERNAL_REVIEW" if variant == "INTERNO_COMPLETO" else "PUBLIC_SAFE_REVIEW"
    return f"---\ntitle: {title}\nvariant: {variant}\ndate_utc: 2026-05-16\nstatus: portfolio_artifact\npublication_gate: {gate}\n---\n\n"


def safe_stem(doc_id: str, title: str) -> str:
    value = f"{doc_id}_{title.upper().replace(' ', '_').replace('/', '_')}"
    return re.sub(r"[^A-Z0-9_\-]", "", value)


def materialize(folder: Path, variant: str) -> dict[str, object]:
    md_dir = folder / "MARKDOWN"
    pdf_dir = folder / "PDF"
    md_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "schema": "medioevo.portfolio_package.v1",
        "variant": variant,
        "date_utc": "2026-05-16",
        "canonical_document_count": len(DOCS),
        "pdfs_are_renditions": True,
        "publication_gate": "BLOCK_INTERNAL_REVIEW" if variant == "INTERNO_COMPLETO" else "PUBLIC_SAFE_REVIEW",
        "documents": [],
    }
    combined: list[str] = []
    for doc in DOCS:
        body = doc["body"] if variant == "INTERNO_COMPLETO" else publicize(doc["body"])
        text = header(doc["title"], variant) + body + "\n"
        stem = safe_stem(doc["id"], doc["title"])
        md_path = md_dir / f"{stem}.md"
        pdf_path = pdf_dir / f"{stem}.pdf"
        md_path.write_text(text, encoding="utf-8", newline="\n")
        write_pdf(pdf_path, doc["title"], text)
        combined.append(text)
        manifest["documents"].append(
            {"id": doc["id"], "title": doc["title"], "markdown": str(md_path.relative_to(folder)), "pdf": str(pdf_path.relative_to(folder))}
        )
    combined_text = "\n\n---\n\n".join(combined)
    combined_md = folder / f"MEDIOEVO_PORTAFOLIO_{variant}_COMBINADO.md"
    combined_pdf = folder / f"MEDIOEVO_PORTAFOLIO_{variant}_COMBINADO.pdf"
    combined_md.write_text(combined_text, encoding="utf-8", newline="\n")
    write_pdf(combined_pdf, f"MEDIOEVO Portfolio {variant}", combined_text)
    manifest["combined_markdown"] = combined_md.name
    manifest["combined_pdf"] = combined_pdf.name
    (folder / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    return manifest


def zip_folder(folder: Path, target: Path) -> None:
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(path.relative_to(ROOT)))


def main() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    INTERNAL.mkdir(parents=True)
    PUBLIC.mkdir(parents=True)

    materialize(INTERNAL, "INTERNO_COMPLETO")
    materialize(PUBLIC, "PUBLIC_SAFE")

    readme = """# MEDIOEVO Portafolio Humano / IA - 2026-05-16

Contiene dos variantes:
- INTERNO_COMPLETO: paquete operativo para trabajo local humano/IA. No publicar sin revision.
- PUBLIC_SAFE: paquete reducido para compartir despues de revision humana.

Cada variante contiene 10 documentos canonicos en Markdown y PDF, mas un PDF combinado que incluye todo el contenido.

Gate: no incluye credenciales, raw vaults, libros completos no aprobados, RPG/TCG, runtime privado ni deploy externo.

Zips incluidos:
- MEDIOEVO_PORTAFOLIO_INTERNO_COMPLETO_2026-05-16.zip
- MEDIOEVO_PORTAFOLIO_PUBLIC_SAFE_2026-05-16.zip
"""
    (ROOT / "LEEME_PRIMERO.md").write_text(readme, encoding="utf-8", newline="\n")

    zip_folder(INTERNAL, ROOT / "MEDIOEVO_PORTAFOLIO_INTERNO_COMPLETO_2026-05-16.zip")
    zip_folder(PUBLIC, ROOT / "MEDIOEVO_PORTAFOLIO_PUBLIC_SAFE_2026-05-16.zip")

    hashes = {}
    for path in sorted(ROOT.rglob("*")):
        if path.is_file():
            hashes[str(path.relative_to(ROOT))] = sha256(path.read_bytes()).hexdigest()
    (ROOT / "SHA256SUMS.json").write_text(json.dumps(hashes, indent=2), encoding="utf-8", newline="\n")

    print(json.dumps({
        "root": str(ROOT),
        "canonical_documents_per_variant": len(DOCS),
        "internal_file_count": sum(1 for p in INTERNAL.rglob("*") if p.is_file()),
        "public_file_count": sum(1 for p in PUBLIC.rglob("*") if p.is_file()),
        "zip_count": 2,
        "hash_manifest": "SHA256SUMS.json",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
