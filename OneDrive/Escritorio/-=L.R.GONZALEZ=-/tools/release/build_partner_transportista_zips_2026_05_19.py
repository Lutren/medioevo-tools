from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
import zipfile
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "releases" / "partner_transportista_wabi_duat_2026-05-19"
TECH_DIR = OUT_ROOT / "MEDIOEVO_WABI_DUAT_SOCIEDAD_TECNICA_2026-05-19"
CLIENT_DIR = OUT_ROOT / "MEDIOEVO_WABI_DUAT_CLIENTES_CURADO_2026-05-19"
DATE = "2026-05-19"

TECH_ZIP_NAME = "MEDIOEVO_WABI_DUAT_SOCIEDAD_TECNICA_2026-05-19.zip"
CLIENT_ZIP_NAME = "MEDIOEVO_WABI_DUAT_CLIENTES_CURADO_2026-05-19.zip"

REPORTLAB_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    REPORTLAB_AVAILABLE = True
except Exception:
    canvas = None
    letter = None
    pdfmetrics = None
    TTFont = None


BASE_EXCLUSIONS = [
    "No credentials, tokens, .env files, payment configs or account data.",
    "No raw canon vaults, full unpublished books, RPG/TCG/game material or private runtime dumps.",
    "No provider API keys, local URL secrets, browser/session state or private prompts.",
    "No claims of guaranteed prediction, AGI equivalence, medical diagnosis or definitive AI detection.",
    "No broad workspace copy; every file is generated from this allowlisted builder.",
]

COMMON_GATE = """## Gate de lectura

CERTEZA:
- Este paquete fue generado desde una allowlist local nueva; no es copia cruda del workspace.
- Los documentos separan teoria, arquitectura, herramienta escolar, propuesta transportista y limites.

INFERENCIA:
- Las formulas y gates son modelos operativos utiles para diseno y pilotos; requieren calibracion por dominio.
- La herramienta escolar produce indicadores de revision, no una sentencia definitiva sobre autoria.

INCOGNITA:
- Costos, integraciones con mapas/ERP/telematica y obligaciones legales dependen del cliente final.
- Cualquier dato real de rutas, choferes, alumnos o empresas requiere consentimiento, contrato y politica de retencion.

BLOQUEO:
- No usar estos materiales para publicar secretos, vigilar sin consentimiento, afirmar predicciones garantizadas o automatizar sanciones.
"""


@dataclass(frozen=True)
class FileSpec:
    relative_path: str
    content: str


def clean_text(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def markdown_header(title: str, variant: str, gate: str) -> str:
    return clean_text(
        f"""
        ---
        title: {title}
        variant: {variant}
        date: {DATE}
        package: MEDIOEVO_WABI_DUAT_PARTNER_TRANSPORTISTA
        publication_gate: {gate}
        ---
        """
    )


def technical_docs() -> list[FileSpec]:
    variant = "SOCIEDAD_TECNICA"
    gate = "REVIEW_PARTNER_ONLY_NO_PUBLICATION"
    return [
        FileSpec(
            "docs/00_LEEME_PRIMERO.md",
            markdown_header("LEEME PRIMERO - Sociedad tecnica", variant, gate)
            + clean_text(
                f"""
                # LEEME PRIMERO

                Este ZIP esta pensado para una sociedad tecnica o potencial socio que quiere evaluar MEDIOEVO, Wabi-Sabi, DUAT y el caso transportista. Es mas profundo que la version de cliente, pero sigue siendo un paquete curado: explica el modelo, las matematicas operativas, gates, funciones y planes sin incluir secretos, credenciales, libros completos, runtime privado ni rutas sensibles.

                ## Que contiene

                - Teoria de informacion OSIT aplicada a IA y biologia digital.
                - Motor epistemologico: MOI, DO, IOI, R, Phi_eff, J_c, EML y gates.
                - Wabi-Sabi como capa local de coordinacion, propuesta, escritura controlada, rollback y WitnessLog.
                - DUAT como tablero/cerebro operativo para datos, rutas, clima, evidencia y simulaciones.
                - Herramienta escolar MOI para revisar trabajos de alumnos con enfoque de integridad, no castigo automatico.
                - Propuesta de sistema transportista con choferes, biblioteca/audiolibros, mapas, clima, rutas y analitica DUAT.
                - Schemas sinteticos y ejemplos locales.

                ## Como usarlo

                1. Leer `docs/01_TEORIA_INFORMACION_BIOLOGIA_DIGITAL.md`.
                2. Leer `docs/02_MOTOR_EPISTEMOLOGICO_GATES_WABI_SABI.md`.
                3. Revisar el caso transportista en `docs/05_TRANSPORTISTA_ARQUITECTURA_DUAT.md`.
                4. Probar la herramienta escolar:

                ```powershell
                cd tools\\moi_school_checker
                python moi_school_checker.py --input examples\\trabajo_alumno_demo.txt --out report.json --markdown-out report.md
                ```

                ## Frontera

                {chr(10).join("- " + item for item in BASE_EXCLUSIONS)}

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/01_TEORIA_INFORMACION_BIOLOGIA_DIGITAL.md",
            markdown_header("Teoria de informacion y biologia digital", variant, gate)
            + clean_text(
                """
                # Teoria de informacion y biologia digital

                ## Tesis

                Shannon mide informacion transmisible por un canal. MEDIOEVO/OSIT pregunta cuanta informacion puede registrar, integrar, actuar y preservar un receptor con estado. La diferencia central es:

                ```text
                Informacion disponible != informacion utilizable
                ```

                El receptor importa. Un humano, un chofer, una empresa, una IA o un sensor no observan desde cero; observan desde un estado.

                ## Variables nucleares

                ```text
                H_eff(X | R) = H(X) * Phi_eff(R)
                ```

                - `H(X)`: informacion disponible en la fuente.
                - `R`: residuo acumulado, contradiccion, loops abiertos, ruido, fatiga o carga no integrada.
                - `Phi_eff`: eficiencia de actualizacion; cuanta informacion se vuelve accion util.
                - `J_c`: umbral de jamming; despues de este punto mas input puede empeorar el sistema.
                - `H_eff`: informacion realmente utilizable.

                Formula de degradacion para laboratorio:

                ```text
                Phi_eff(R, J_c) = exp(-nu * R / (J_c - R))  para R < J_c
                Phi_eff = 0                                 para R >= J_c
                ```

                Version inicial mas simple:

                ```text
                Phi_eff = Phi_0 * (1 - R/J_c)^nu
                ```

                ## Residuo

                ```text
                R_next = clamp(R_prev + ruido + contradiccion + loops_abiertos - cierres_verificados, 0, 1)
                ```

                En una cadena transportista, R puede venir de rutas contradictorias, falta de mantenimiento, clima no integrado, chofer cansado, instrucciones dispersas, app pesada, reportes sin cierre o datos sin trazabilidad.

                ## EML como costo de carga

                ```text
                f(x) = exp(x) - log(x), x > 0
                f'(x) = exp(x) - 1/x
                minimo cuando x * exp(x) = 1
                ```

                Lectura operativa: poca informacion es costosa, saturacion tambien. El valor no esta en meter todo, sino en la carga correcta para el objetivo y el estado del receptor.

                ## Biologia digital

                La biologia observa mediante transductores:

                ```text
                estimulo fisico -> receptor -> senal interna -> integracion -> memoria/accion
                ```

                Un sistema digital opera igual:

                ```text
                ruta/clima/sensor/texto -> adapter -> evento normalizado -> DUAT -> decision/gate
                ```

                Formula de interfaz:

                ```text
                O_i(t) = D_i(X(t - tau_i), S_i(t), K_i, B_i, N_i)
                ```

                - `D_i`: decodificador/interfaz del observador.
                - `tau_i`: latencia.
                - `S_i`: estado actual.
                - `K_i`: conocimiento/calibracion.
                - `B_i`: sesgo o constraint.
                - `N_i`: ruido.

                ## Por que el motor epistemologico es avanzado

                El motor no solo genera respuestas. Clasifica el estado epistemico de cada afirmacion, obliga a source cards, gates, falsadores, evidencia y handoff. En vez de "mas IA", produce un circuito verificable:

                ```text
                entrada -> claim -> fuente -> gate -> accion -> evidencia -> handoff
                ```

                ## Limite de claims

                Estas matematicas son modelos formales y operativos. No se presentan como fisica demostrada universal ni como prediccion garantizada. En piloto real se calibran con datos, falsadores y revision legal.

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/02_MOTOR_EPISTEMOLOGICO_GATES_WABI_SABI.md",
            markdown_header("Motor epistemologico, gates y Wabi-Sabi", variant, gate)
            + clean_text(
                """
                # Motor epistemologico, gates y Wabi-Sabi

                ## MOI

                MOI es el Metodo/Motor de Observacion e Integridad. Convierte intuicion, archivos, conversaciones, logs y datos en artefactos verificables. Su foco es cerrar ciclos, no producir volumen.

                ## DO e IOI

                DO: Deconstruccion Observacionista.

                ```text
                entrada -> objetivo -> restricciones -> fuente -> claim -> riesgo -> evidencia requerida
                ```

                IOI: Ingenieria Observacionista Inversa.

                ```text
                resultado deseado -> condiciones de verdad -> tests -> gates -> artefacto -> handoff
                ```

                ## Gates

                | Gate | Funcion |
                |---|---|
                | ActionGate | Decide APPROVE / REVIEW / BLOCK antes de acciones. |
                | GhostGate | Simula o dry-run antes de escribir, publicar o ejecutar. |
                | ScienceClaimGate | Evita elevar hipotesis a verdad cientifica sin evidencia. |
                | PublicationGate | Mantiene publicaciones, deploys, redes y Gumroad bloqueados hasta gate target-specific. |
                | PrivacyGate | Bloquea secretos, datos personales, rutas privadas y vigilancia no consentida. |
                | ForecastGate | Evita vender simulaciones como prediccion garantizada. |
                | SchoolIntegrityGate | Evita sancionar a alumnos solo por heuristicas de IA. |

                ## Funcion de Wabi-Sabi

                Wabi-Sabi es una capa local de coordinacion. No es el LLM y no reemplaza al humano. Recibe una intencion, estima R/Phi_eff/regimen, deconstruye la tarea, elige agente/herramienta, genera plan, aplica gates, produce evidencia y deja handoff.

                Flujo:

                ```text
                operador -> Wabi-Sabi local -> ActionGate
                         -> TaskSpec/PatchPlan/Workpack
                         -> SafeExecutor / herramienta local
                         -> tests / rollback / WitnessLog
                         -> handoff
                ```

                ## Funciones que debe exponer

                - Chat y plan local.
                - Estado de proveedores sin imprimir secretos.
                - Worktree/status solo lectura.
                - PatchPlan antes de escribir.
                - Apply con rollback y tests.
                - Run-safe-tests.
                - Multimodal metadata-only.
                - Cloud providers solo como propuesta, no como autoridad de ejecucion.
                - WitnessLog hash-chain.
                - DecisionLog y NextSessionBrief.
                - Claim contracts para mantener claims en su carril.

                ## Por que es defendible para socios

                Un socio no recibe una "caja magica". Recibe un sistema con reglas de evidencia, gates, logs, rollback, fronteras de privacidad y arquitectura por capas. Eso permite pilotos auditables.

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/03_FUNCIONES_WABI_SABI_DUAT.md",
            markdown_header("Funciones Wabi-Sabi y DUAT", variant, gate)
            + clean_text(
                """
                # Funciones Wabi-Sabi y DUAT

                ## Wabi-Sabi: capa operativa

                Wabi-Sabi traduce intenciones humanas a tareas verificables. Sus funciones se agrupan en:

                - Entender objetivo y restricciones.
                - Separar tareas locales, tareas de revision y acciones bloqueadas.
                - Preparar prompts o workpacks para agentes.
                - Validar propuestas externas antes de integrarlas.
                - Ejecutar solo acciones locales, reversibles y testeables.
                - Registrar DecisionLog, WitnessLog, rollback y handoff.

                ## DUAT: tablero/cerebro operativo

                DUAT muestra el estado del sistema: tareas, agentes, claims, rutas, clima, eventos, riesgos, logs y evidencia. En el caso transportista, DUAT se vuelve una sala de control:

                ```text
                Chofer/app/sensores -> eventos normalizados -> DUAT
                                      -> gates -> recomendaciones -> evidencia
                ```

                ## Interfaces esperadas

                - Mission Control: estado de flota, alertas, rutas, clima, seguridad.
                - Driver Companion: biblioteca/audiolibros, instrucciones, pausas, mapas, voz.
                - Fleet Ops: asignacion, tiempos, mantenimiento, incidentes.
                - Evidence Desk: logs, consentimientos, auditoria, reportes.
                - Analytics DUAT: R por ruta, clima, carga, retrasos, fatiga y cierre operativo.

                ## Modos de trabajo

                | Modo | Uso |
                |---|---|
                | Read-only | Observar rutas, eventos y datos sin actuar. |
                | Assistive | Recomendar pausas, rutas o contenido de audio. |
                | Controlled apply | Enviar tareas internas con autorizacion humana. |
                | Review required | Cambios de politicas, datos personales, integraciones externas. |
                | Block | Sanciones automaticas, vigilancia oculta, sharing de secretos. |

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/04_MOI_HERRAMIENTA_ESCOLAR.md",
            markdown_header("MOI herramienta escolar", variant, gate)
            + clean_text(
                """
                # MOI herramienta escolar de integridad

                ## Proposito

                La herramienta `moi_school_checker.py` ayuda a revisar trabajos escolares para detectar senales de falta de proceso, baja trazabilidad, citacion pobre, estilo inconsistente o posible asistencia de IA no declarada.

                ## Regla etica

                No existe un detector perfecto de IA. El resultado del script es una recomendacion de revision, no una prueba para castigar alumnos. El uso correcto es pedir bitacora, borradores, defensa oral, fuentes y proceso.

                ## Que mide

                - Conteo de palabras y oraciones.
                - Diversidad lexica.
                - Longitud promedio de oraciones.
                - Frases genericas de estilo IA o conclusion automatica.
                - Indicadores de proceso: "borrador", "revise", "fuente", "entrevista".
                - Citaciones o referencias.
                - Repeticion de n-gramas.
                - Comparacion opcional contra textos base del mismo alumno.

                ## Salidas

                - `OK`: hay evidencia suficiente de proceso o bajo riesgo.
                - `REVIEW`: pedir evidencia adicional.
                - `HIGH_REVIEW`: requiere revision humana cuidadosa.

                ## Uso

                ```powershell
                cd tools\\moi_school_checker
                python moi_school_checker.py --input examples\\trabajo_alumno_demo.txt --out report.json --markdown-out report.md
                python moi_school_checker.py --input nuevo_trabajo.txt --baseline baselines\\alumno_01 --markdown-out reporte.md
                ```

                ## Integracion con escuela

                1. Al inicio del curso, pedir muestra de escritura presencial.
                2. En cada tarea, pedir mini bitacora de proceso.
                3. Usar MOI como filtro de apoyo.
                4. Si hay `REVIEW`, pedir borradores/fuentes o defensa corta.
                5. Registrar decision con criterio humano.

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/05_TRANSPORTISTA_ARQUITECTURA_DUAT.md",
            markdown_header("Arquitectura transportista DUAT", variant, gate)
            + clean_text(
                """
                # Sistema transportista con DUAT

                ## Objetivo

                Crear un sistema para una cadena transportista que ayude al chofer, a operaciones y a direccion sin convertirlo en vigilancia oculta. La meta es seguridad, continuidad, eficiencia, aprendizaje y evidencia.

                ## Modulos

                ### 1. Driver Companion

                App movil o dispositivo vehicular con:

                - Mapas y ruta.
                - Clima en ruta.
                - Alertas de descanso.
                - Biblioteca de audiolibros/cursos.
                - Lectura por voz de documentos autorizados.
                - Checklists de salida/llegada.
                - Reporte simple de incidente.
                - Modo manos libres.

                ### 2. Biblioteca de audio

                La biblioteca no debe distraer. Debe priorizar:

                - Audiolibros aprobados.
                - Manuales de seguridad.
                - Cursos cortos por tramo.
                - Noticias o clima solo si no saturan.
                - Pausas automaticas durante maniobras o alertas.

                ### 3. Fleet Mission Control

                Panel para operaciones:

                - Unidades activas.
                - Ruta prevista vs ruta real.
                - Clima/incidentes.
                - Estado de descanso.
                - Checklists.
                - Alertas por gate, no por castigo automatico.

                ### 4. DUAT Analytics

                DUAT integra rutas, clima, tiempos, incidentes y eventos operativos para crear:

                - R por ruta: friccion acumulada.
                - Phi_eff por proceso: si los datos reducen problemas.
                - Patrones de retraso.
                - Zonas de riesgo.
                - Puntos de fatiga.
                - Mejora de planificacion.
                - Evidencia para mantenimiento y capacitacion.

                ## Flujo de datos

                ```text
                GPS/mapa -> RouteEvent
                clima -> WeatherSignal
                app chofer -> DriverCheckin
                vehiculo -> VehicleSignal
                operaciones -> DispatchDecision
                todo -> DUAT Event Store -> Gates -> Reportes
                ```

                ## Acciones permitidas iniciales

                - Recomendar pausa.
                - Recomendar ruta alterna a confirmar.
                - Alertar clima severo.
                - Pausar audio por maniobra/alerta.
                - Pedir confirmacion simple.
                - Generar reporte posterior.

                ## Acciones bloqueadas

                - Sancion automatica a chofer.
                - Monitoreo oculto.
                - Compartir ubicacion fuera del contrato.
                - Grabar audio del chofer sin consentimiento.
                - Usar datos para profiling laboral sin reglas claras.

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/06_DATOS_RUTAS_CLIMA_DUAT_ANALYTICS.md",
            markdown_header("Datos de rutas, clima y DUAT analytics", variant, gate)
            + clean_text(
                """
                # Datos de rutas, clima y DUAT analytics

                ## Datos recolectables

                | Dominio | Ejemplos | Gate |
                |---|---|---|
                | Ruta | origen, destino, ETA, desvios, paradas | APPROVE con contrato |
                | Clima | lluvia, viento, temperatura, visibilidad | APPROVE si fuente licenciada |
                | Trafico/mapa | congestion, cierres, incidentes | REVIEW segun proveedor |
                | Chofer | check-in, descanso, confirmaciones | REVIEW por privacidad laboral |
                | Vehiculo | odometro, combustible, sensores, fallas | APPROVE/REVIEW |
                | Audio biblioteca | contenido reproducido, duracion, pausa | REVIEW; no vigilancia personal |
                | Incidentes | retrasos, riesgo, soporte | APPROVE con minimizacion |

                ## Que hacer con la informacion

                - Optimizar rutas por riesgo, no solo por distancia.
                - Detectar tramos con fatiga operativa.
                - Cruzar clima con retrasos y siniestros.
                - Mejorar ventanas de entrega.
                - Priorizar mantenimiento por evidencia.
                - Crear entrenamiento por patrones reales.
                - Reducir R operativo: menos llamadas dispersas, menos decisiones sin evidencia.
                - Alimentar simulaciones DUAT con datos agregados y anonimizados.

                ## Integracion DUAT

                DUAT no debe ingerir datos sin ficha. Cada fuente necesita:

                ```text
                source_id
                owner
                license/contract
                collection_method
                personal_data_class
                retention_days
                allowed_uses
                forbidden_uses
                hash/provenance
                gate
                ```

                ## ForecastGate

                Se puede estimar riesgo de retraso o friccion, pero no prometer prediccion garantizada. Las recomendaciones deben incluir incertidumbre y falsadores:

                - Si clima empeora pero retraso no sube, ajustar pesos.
                - Si una ruta se marca riesgosa sin incidentes, revisar sesgo.
                - Si el modelo penaliza siempre al mismo chofer, revisar variables laborales y contexto.

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/07_IMPLEMENTACION_ROADMAP_COSTOS_RIESGOS.md",
            markdown_header("Roadmap de implementacion", variant, gate)
            + clean_text(
                """
                # Roadmap de implementacion

                ## Fase 0 - Diagnostico y contrato

                - Definir objetivos del piloto.
                - Revisar privacidad laboral y consentimiento.
                - Elegir fuente de mapas/clima.
                - Crear matriz de datos permitidos.
                - Definir KPIs: seguridad, puntualidad, fatiga operativa, cierre de incidencias.

                ## Fase 1 - MVP local

                - App demo de chofer con check-in, biblioteca y reporte.
                - Panel DUAT read-only.
                - Ingestion de rutas/clima sintetico o dataset aprobado.
                - Reportes diarios.
                - Sin decisiones automaticas.

                ## Fase 2 - Piloto controlado

                - Integracion con 3-10 unidades.
                - Mapa real y clima real.
                - Consentimiento firmado.
                - Retencion limitada.
                - Analitica de R por ruta.
                - Recomendaciones humanas, no sanciones.

                ## Fase 3 - Escalamiento

                - Integracion con ERP/TMS.
                - APIs de mantenimiento.
                - Biblioteca de entrenamiento.
                - Modelos calibrados por ruta.
                - DUAT simulador para planeacion.

                ## Costos que faltan por cotizar

                - Proveedor de mapas.
                - Proveedor de clima/trafico.
                - Dispositivos o uso de smartphones.
                - Hosting o servidor local.
                - Integracion TMS/ERP.
                - Soporte, privacidad y legal.

                ## Riesgos

                - Rechazo laboral si se comunica como vigilancia.
                - Datos incompletos que generen falsas conclusiones.
                - Dependencia de proveedores de mapas.
                - Responsabilidad si el sistema distrae al chofer.
                - Sobreclaim predictivo.

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/08_PRIVACIDAD_LEGAL_CLAIMS_BOUNDARY.md",
            markdown_header("Privacidad, legal y claims boundary", variant, gate)
            + clean_text(
                """
                # Privacidad, legal y claims boundary

                ## Frase operativa

                El sistema acompana y documenta; no castiga automaticamente.

                ## Datos de choferes

                Todo dato personal requiere:

                - Finalidad clara.
                - Consentimiento o base legal aplicable.
                - Minimizacion.
                - Retencion limitada.
                - Acceso por roles.
                - Bitacora de consulta.
                - Proceso de correccion.
                - Prohibicion de usos no informados.

                ## Seguridad al manejar

                La biblioteca de audio debe tener:

                - Modo manos libres.
                - Pausa automatica en alerta.
                - No lectura visual obligatoria.
                - No notificaciones largas en maniobras.
                - Politica de contenido seguro.

                ## Claims bloqueados

                - "Predice accidentes".
                - "Elimina fatiga".
                - "Detecta IA con certeza".
                - "Vigila choferes sin que se den cuenta".
                - "Prueba AGI".
                - "Resuelve la fisica".

                ## Claims permitidos con alcance

                - "Ayuda a organizar evidencia operativa".
                - "Reduce friccion por datos dispersos".
                - "Puede sugerir revisiones humanas".
                - "Usa gates para separar acciones locales, revisiones y bloqueos".
                - "Puede correr pilotos con datos sinteticos o autorizados".

                {COMMON_GATE}
                """
            ),
        ),
    ]


def client_docs() -> list[FileSpec]:
    variant = "CLIENTES_CURADO"
    gate = "CLIENT_PRESENTATION_REVIEW"
    return [
        FileSpec(
            "docs/00_LEEME_PRIMERO.md",
            markdown_header("LEEME PRIMERO - Cliente curado", variant, gate)
            + clean_text(
                f"""
                # LEEME PRIMERO

                Este ZIP es para presentacion a clientes. Mantiene la misma estructura general que el paquete tecnico, pero omite formulas sensibles, detalles internos, rutas de implementacion, lenguaje de laboratorio y material clave.

                ## Que explica

                - Que problema resuelve el sistema.
                - Como puede ayudar a una cadena transportista.
                - Que hace Wabi-Sabi/DUAT en terminos de operacion.
                - Como funcionaria la biblioteca de audio para choferes.
                - Como se usarian rutas, clima y eventos para mejorar decisiones.
                - Como se maneja privacidad y limite de claims.
                - Incluye una demo escolar MOI de integridad como herramienta de ejemplo.

                ## Frontera

                {chr(10).join("- " + item for item in BASE_EXCLUSIONS)}

                {COMMON_GATE}
                """
            ),
        ),
        FileSpec(
            "docs/01_VISION_EJECUTIVA.md",
            markdown_header("Vision ejecutiva", variant, gate)
            + clean_text(
                """
                # Vision ejecutiva

                MEDIOEVO propone una capa de operacion inteligente para empresas con procesos complejos. En vez de depender de una IA que responde sin control, el sistema organiza datos, tareas, evidencia y decisiones mediante tableros, reglas y gates.

                Para una cadena transportista, el resultado buscado es:

                - Mejor visibilidad de rutas.
                - Menos friccion operativa.
                - Apoyo seguro al chofer.
                - Reportes con evidencia.
                - Aprendizaje por rutas, clima e incidencias.
                - Integracion futura con sistemas de despacho, mantenimiento y capacitacion.

                La propuesta no es vigilancia oculta. Es un sistema de acompanamiento, registro y mejora continua.
                """
            ),
        ),
        FileSpec(
            "docs/02_WABI_DUAT_EN_TERMINOS_CLIENTE.md",
            markdown_header("Wabi-Sabi y DUAT para cliente", variant, gate)
            + clean_text(
                """
                # Wabi-Sabi y DUAT para cliente

                ## Wabi-Sabi

                Wabi-Sabi es la capa que convierte peticiones y eventos en tareas ordenadas. Ayuda a decidir que se puede hacer localmente, que requiere revision y que no debe hacerse.

                ## DUAT

                DUAT es el tablero operativo. Muestra rutas, choferes, unidades, clima, incidentes, reportes y acciones pendientes. Su valor esta en convertir datos dispersos en decisiones revisables.

                ## Ejemplo simple

                ```text
                Clima fuerte + retraso + chofer sin pausa reciente
                -> alerta de revision
                -> recomendacion de pausa/ruta alternativa
                -> registro de decision
                -> reporte para operaciones
                ```

                El sistema no sanciona solo. Presenta evidencia y recomendaciones para decision humana.
                """
            ),
        ),
        FileSpec(
            "docs/03_HERRAMIENTA_ESCOLAR_MOI_DEMO.md",
            markdown_header("Herramienta escolar MOI demo", variant, gate)
            + clean_text(
                """
                # Herramienta escolar MOI demo

                La herramienta escolar incluida revisa textos de alumnos y genera una recomendacion de integridad academica. No acusa ni confirma uso de IA; ayuda a decidir si conviene pedir borradores, fuentes o una explicacion oral.

                ## Uso

                ```powershell
                cd tools\\moi_school_checker
                python moi_school_checker.py --input examples\\trabajo_alumno_demo.txt --markdown-out report.md
                ```

                ## Resultado

                - OK: no hay senales fuertes.
                - REVIEW: pedir evidencia adicional.
                - HIGH_REVIEW: revisar con cuidado antes de calificar.

                La decision final debe ser humana.
                """
            ),
        ),
        FileSpec(
            "docs/04_TRANSPORTISTA_PROPUESTA_CLIENTE.md",
            markdown_header("Propuesta transportista", variant, gate)
            + clean_text(
                """
                # Propuesta transportista

                ## Componentes

                - App o pantalla para chofer.
                - Biblioteca de audiolibros y capacitacion en audio.
                - Mapas, clima y alertas de ruta.
                - Checklists de salida y llegada.
                - Reporte simple de incidencias.
                - Panel para operaciones.
                - Reportes diarios y semanales.

                ## Beneficios esperados

                - Menos llamadas y mensajes desordenados.
                - Mejor seguimiento de entregas.
                - Mas seguridad por alertas y pausas.
                - Capacitacion continua en ruta sin distraer.
                - Evidencia para mejorar rutas y mantenimiento.
                - Informacion para tomar decisiones con menos improvisacion.
                """
            ),
        ),
        FileSpec(
            "docs/05_DATOS_Y_VALOR_OPERATIVO.md",
            markdown_header("Datos y valor operativo", variant, gate)
            + clean_text(
                """
                # Datos y valor operativo

                El sistema puede integrar datos autorizados de ruta, clima, tiempos, paradas, incidentes, mantenimiento y uso de biblioteca de audio.

                Con esos datos se pueden generar:

                - Rutas con mas friccion.
                - Tramos donde conviene pausar.
                - Riesgos por clima.
                - Causas frecuentes de retraso.
                - Capacitacion recomendada por tipo de ruta.
                - Reportes para direccion.
                - Simulaciones para planear mejor.

                Los datos personales deben minimizarse y usarse solo para fines acordados.
                """
            ),
        ),
        FileSpec(
            "docs/06_ROADMAP_PILOTO.md",
            markdown_header("Roadmap piloto", variant, gate)
            + clean_text(
                """
                # Roadmap piloto

                ## Paso 1: Diagnostico

                Revisar rutas, sistemas actuales, reglas internas, necesidades de choferes y datos disponibles.

                ## Paso 2: Demo

                Crear una demo con rutas y clima de prueba, biblioteca de audio y panel simple.

                ## Paso 3: Piloto

                Probar con pocas unidades y consentimiento claro. Medir seguridad, puntualidad, facilidad de uso y calidad de reportes.

                ## Paso 4: Integracion

                Conectar con mapas, clima, despacho, mantenimiento o ERP si el piloto demuestra valor.

                ## Paso 5: Escalamiento

                Expandir por rutas o regiones, manteniendo privacidad, soporte y revision humana.
                """
            ),
        ),
        FileSpec(
            "docs/07_PRIVACIDAD_Y_LIMITES.md",
            markdown_header("Privacidad y limites", variant, gate)
            + clean_text(
                """
                # Privacidad y limites

                ## Principios

                - Informar claramente que datos se usan.
                - Pedir consentimiento cuando aplique.
                - Usar datos minimos.
                - No grabar audio o video sin autorizacion.
                - No castigar automaticamente.
                - Permitir revision humana.
                - Mantener historial de decisiones.

                ## Mensaje recomendado

                El sistema acompana a choferes y operaciones para mejorar seguridad, capacitacion y planeacion. No es una herramienta de vigilancia oculta.

                ## Claims que no deben usarse

                - Detecta IA con certeza.
                - Predice accidentes.
                - Elimina errores humanos.
                - Reemplaza al supervisor.
                - Vigila sin consentimiento.
                """
            ),
        ),
    ]


TOOL_CODE = r'''#!/usr/bin/env python3
"""MOI School Checker: local academic-integrity review helper.

This tool does not detect AI with certainty. It produces review indicators
for teachers: process evidence, citation signals, generic phrasing, repetition
and optional baseline-style distance.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


GENERIC_PATTERNS = [
    r"\bin conclusion\b",
    r"\bin summary\b",
    r"\boverall\b",
    r"\bdelve\b",
    r"\btapestry\b",
    r"\bit is important to note\b",
    r"\bas an ai\b",
    r"\bcomo inteligencia artificial\b",
    r"\ben conclusion\b",
    r"\ben resumen\b",
    r"\bes importante destacar\b",
    r"\bcabe resaltar\b",
]

PROCESS_PATTERNS = [
    r"\bborrador\b",
    r"\brevise\b",
    r"\bcorregi\b",
    r"\bfuente\b",
    r"\bentrevista\b",
    r"\bobserv[eé]\b",
    r"\bmi proceso\b",
    r"\baprendi\b",
    r"\bdraft\b",
    r"\brevised\b",
    r"\bsource\b",
    r"\binterview\b",
]

CITATION_PATTERNS = [
    r"\([^)]*\d{4}[^)]*\)",
    r"\[[0-9]+\]",
    r"https?://",
    r"\bBibliografia\b",
    r"\bReferences\b",
    r"\bObras citadas\b",
]


@dataclass
class Metrics:
    word_count: int
    sentence_count: int
    avg_sentence_words: float
    lexical_diversity: float
    repeated_trigram_ratio: float
    generic_phrase_hits: int
    process_evidence_hits: int
    citation_hits: int
    baseline_distance: float | None


@dataclass
class Report:
    schema: str
    verdict: str
    score: int
    metrics: Metrics
    reasons: list[str]
    recommended_actions: list[str]
    disclaimer: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9']+", text.lower())


def sentences(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"[.!?]+", text) if p.strip()]
    return parts or [text.strip()] if text.strip() else []


def count_patterns(text: str, patterns: list[str]) -> int:
    total = 0
    for pattern in patterns:
        total += len(re.findall(pattern, text, flags=re.IGNORECASE))
    return total


def repeated_trigram_ratio(tokens: list[str]) -> float:
    if len(tokens) < 6:
        return 0.0
    trigrams = list(zip(tokens, tokens[1:], tokens[2:]))
    counts = Counter(trigrams)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    return repeated / max(1, len(trigrams))


def vector_for(text: str) -> list[float]:
    toks = words(text)
    sents = sentences(text)
    word_count = max(1, len(toks))
    return [
        len(toks) / 1000.0,
        sum(len(words(s)) for s in sents) / max(1, len(sents)) / 30.0,
        len(set(toks)) / word_count,
        repeated_trigram_ratio(toks) * 10.0,
        count_patterns(text, GENERIC_PATTERNS) / 5.0,
        count_patterns(text, PROCESS_PATTERNS) / 5.0,
        count_patterns(text, CITATION_PATTERNS) / 5.0,
    ]


def euclidean(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def baseline_distance(text: str, baseline_dir: Path | None) -> float | None:
    if not baseline_dir:
        return None
    paths = [p for p in baseline_dir.glob("**/*") if p.is_file() and p.suffix.lower() in {".txt", ".md"}]
    if not paths:
        return None
    base_vectors = [vector_for(read_text(path)) for path in paths]
    candidate = vector_for(text)
    distances = [euclidean(candidate, base) for base in base_vectors]
    return min(distances) if distances else None


def analyze(text: str, baseline_dir: Path | None = None) -> Report:
    toks = words(text)
    sents = sentences(text)
    wc = len(toks)
    sc = len(sents)
    avg_sentence = sum(len(words(sentence)) for sentence in sents) / max(1, sc)
    lexical = len(set(toks)) / max(1, wc)
    repeated = repeated_trigram_ratio(toks)
    generic = count_patterns(text, GENERIC_PATTERNS)
    process = count_patterns(text, PROCESS_PATTERNS)
    citations = count_patterns(text, CITATION_PATTERNS)
    distance = baseline_distance(text, baseline_dir)

    score = 0
    reasons: list[str] = []

    if wc < 250:
        score += 12
        reasons.append("Texto corto: conviene pedir contexto o borrador.")
    if avg_sentence > 28:
        score += 12
        reasons.append("Oraciones largas en promedio; revisar claridad y voz propia.")
    if lexical < 0.34 and wc > 400:
        score += 10
        reasons.append("Diversidad lexica baja para la longitud del texto.")
    if repeated > 0.035:
        score += 10
        reasons.append("Repeticion de trigrama elevada.")
    if generic >= 3:
        score += 15
        reasons.append("Varias frases genericas detectadas.")
    if process == 0:
        score += 15
        reasons.append("No hay senales de proceso o trazabilidad.")
    if citations == 0 and wc > 350:
        score += 12
        reasons.append("No se detectaron citas o referencias en un texto largo.")
    if distance is not None and distance > 1.25:
        score += 18
        reasons.append("Distancia alta contra textos base del alumno.")

    score = max(0, min(100, score))
    if score >= 55:
        verdict = "HIGH_REVIEW"
    elif score >= 28:
        verdict = "REVIEW"
    else:
        verdict = "OK"

    if not reasons:
        reasons.append("No se detectaron senales fuertes; conservar revision humana normal.")

    recommended = [
        "Solicitar bitacora de proceso o borradores si el veredicto no es OK.",
        "Pedir al alumno explicar oralmente dos decisiones del trabajo.",
        "Revisar fuentes y citas; no sancionar solo por esta salida.",
    ]
    if baseline_dir is None:
        recommended.append("Para mejor contexto, ejecutar con --baseline usando textos previos del mismo alumno.")

    metrics = Metrics(
        word_count=wc,
        sentence_count=sc,
        avg_sentence_words=round(avg_sentence, 3),
        lexical_diversity=round(lexical, 4),
        repeated_trigram_ratio=round(repeated, 4),
        generic_phrase_hits=generic,
        process_evidence_hits=process,
        citation_hits=citations,
        baseline_distance=round(distance, 4) if distance is not None else None,
    )
    return Report(
        schema="medioevo.moi_school_integrity_report.v0_1",
        verdict=verdict,
        score=score,
        metrics=metrics,
        reasons=reasons,
        recommended_actions=recommended,
        disclaimer="Heuristic review aid only. It is not proof of AI use or academic misconduct.",
    )


def markdown(report: Report, source: Path) -> str:
    metrics = report.metrics
    lines = [
        "# MOI School Checker Report",
        "",
        f"- Source: `{source}`",
        f"- Verdict: `{report.verdict}`",
        f"- Score: `{report.score}`",
        f"- Disclaimer: {report.disclaimer}",
        "",
        "## Metrics",
        "",
    ]
    for key, value in asdict(metrics).items():
        lines.append(f"- {key}: {value}")
    lines += ["", "## Reasons", ""]
    lines += [f"- {reason}" for reason in report.reasons]
    lines += ["", "## Recommended Actions", ""]
    lines += [f"- {action}" for action in report.recommended_actions]
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="MOI academic-integrity review helper.")
    parser.add_argument("--input", required=True, help="Path to .txt or .md student work.")
    parser.add_argument("--baseline", help="Optional folder with prior .txt/.md texts from the same student.")
    parser.add_argument("--out", help="Write JSON report to this path.")
    parser.add_argument("--markdown-out", help="Write Markdown report to this path.")
    args = parser.parse_args()

    input_path = Path(args.input)
    baseline = Path(args.baseline) if args.baseline else None
    report = analyze(read_text(input_path), baseline)
    data = asdict(report)

    if args.out:
        Path(args.out).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.markdown_out:
        Path(args.markdown_out).write_text(markdown(report, input_path), encoding="utf-8")
    if not args.out and not args.markdown_out:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


TOOL_README = clean_text(
    """
    # MOI School Checker

    Herramienta local, sin red y sin dependencias externas para apoyar revision de integridad academica.

    ## Importante

    No detecta IA con certeza. Entrega indicadores para que un docente pida evidencia de proceso, fuentes o una defensa breve.

    ## Uso rapido

    ```powershell
    python moi_school_checker.py --input examples\\trabajo_alumno_demo.txt --out report.json --markdown-out report.md
    ```

    ## Uso con baseline

    ```powershell
    python moi_school_checker.py --input trabajo.txt --baseline baselines\\alumno_01 --markdown-out report.md
    ```

    ## Veredictos

    - `OK`: revision normal.
    - `REVIEW`: pedir evidencia adicional.
    - `HIGH_REVIEW`: revision humana cuidadosa; no sancion automatica.
    """
)


DEMO_STUDENT_TEXT = clean_text(
    """
    Mi proceso para este trabajo empezo con una lectura del tema en clase y despues hice un borrador a mano.
    Revise mis notas sobre transporte, clima y seguridad. Tambien compare dos fuentes del manual escolar.
    La idea principal es que la tecnologia puede ayudar, pero no debe reemplazar el criterio humano.
    En el primer borrador confundi vigilancia con acompanamiento. Despues corregi esa parte porque un sistema justo
    debe explicar que datos usa y para que los usa. En conclusion, la herramienta sirve mejor cuando deja evidencia
    y cuando el profesor puede revisar el proceso, no solo el resultado final.

    Bibliografia:
    - Apuntes de clase, semana 3.
    - Manual de seguridad vial entregado por la escuela.
    """
)


BASELINE_TEXT = clean_text(
    """
    En mi ensayo anterior explique que me cuesta organizar las ideas si empiezo por la conclusion.
    Primero hago una lista, luego escribo un borrador y al final reviso si la fuente realmente dice lo que puse.
    Me gusta usar ejemplos de clase porque asi puedo defender el trabajo cuando el profesor pregunta.
    """
)


SCHEMAS: list[FileSpec] = [
    FileSpec(
        "schemas/moi_integrity_report.schema.json",
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "medioevo.moi_integrity_report.v0_1",
                "title": "MOI Integrity Report",
                "type": "object",
                "required": ["schema", "verdict", "score", "metrics", "reasons", "recommended_actions", "disclaimer"],
                "properties": {
                    "schema": {"const": "medioevo.moi_school_integrity_report.v0_1"},
                    "verdict": {"enum": ["OK", "REVIEW", "HIGH_REVIEW"]},
                    "score": {"type": "integer", "minimum": 0, "maximum": 100},
                    "metrics": {"type": "object"},
                    "reasons": {"type": "array", "items": {"type": "string"}},
                    "recommended_actions": {"type": "array", "items": {"type": "string"}},
                    "disclaimer": {"type": "string"},
                },
            },
            indent=2,
        )
        + "\n",
    ),
    FileSpec(
        "schemas/transport_driver_event.schema.json",
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "medioevo.transport_driver_event.v0_1",
                "title": "Transport Driver Event",
                "type": "object",
                "required": ["event_id", "timestamp_utc", "vehicle_id", "driver_pseudonym", "event_type", "gate"],
                "properties": {
                    "event_id": {"type": "string"},
                    "timestamp_utc": {"type": "string", "format": "date-time"},
                    "vehicle_id": {"type": "string"},
                    "driver_pseudonym": {"type": "string"},
                    "event_type": {
                        "enum": ["checkin", "route_update", "rest_prompt", "incident_report", "audio_pause", "delivery_event"]
                    },
                    "route_id": {"type": "string"},
                    "notes": {"type": "string"},
                    "personal_data_class": {"enum": ["none", "pseudonymous", "personal_review_required"]},
                    "gate": {"enum": ["APPROVE_LOCAL", "REVIEW_PRIVACY", "BLOCK"]},
                },
            },
            indent=2,
        )
        + "\n",
    ),
    FileSpec(
        "schemas/route_weather_signal.schema.json",
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "medioevo.route_weather_signal.v0_1",
                "title": "Route Weather Signal",
                "type": "object",
                "required": ["signal_id", "timestamp_utc", "route_id", "source", "condition", "risk_level"],
                "properties": {
                    "signal_id": {"type": "string"},
                    "timestamp_utc": {"type": "string", "format": "date-time"},
                    "route_id": {"type": "string"},
                    "source": {"type": "string"},
                    "condition": {"type": "string"},
                    "temperature_c": {"type": "number"},
                    "wind_kph": {"type": "number"},
                    "visibility_km": {"type": "number"},
                    "risk_level": {"enum": ["low", "medium", "high", "review"]},
                    "allowed_use": {"type": "string"},
                    "gate": {"enum": ["APPROVE_LOCAL", "REVIEW_SOURCE_LICENSE", "BLOCK"]},
                },
            },
            indent=2,
        )
        + "\n",
    ),
]


EXAMPLE_TRANSPORT_EVENT = json.dumps(
    {
        "event_id": "evt_demo_001",
        "timestamp_utc": "2026-05-19T15:00:00Z",
        "vehicle_id": "unit_demo_07",
        "driver_pseudonym": "driver_hash_demo",
        "event_type": "rest_prompt",
        "route_id": "route_mx_demo_01",
        "notes": "Demo event: rest prompt after long route segment and weather review.",
        "personal_data_class": "pseudonymous",
        "gate": "REVIEW_PRIVACY",
    },
    indent=2,
) + "\n"


EXAMPLE_WEATHER_SIGNAL = json.dumps(
    {
        "signal_id": "wx_demo_001",
        "timestamp_utc": "2026-05-19T15:05:00Z",
        "route_id": "route_mx_demo_01",
        "source": "synthetic_demo",
        "condition": "heavy_rain_possible",
        "temperature_c": 18.5,
        "wind_kph": 42,
        "visibility_km": 3.2,
        "risk_level": "review",
        "allowed_use": "pilot planning only; not a real forecast",
        "gate": "APPROVE_LOCAL",
    },
    indent=2,
) + "\n"


def pdf_font_names() -> tuple[str, str]:
    if not REPORTLAB_AVAILABLE:
        return "Helvetica", "Helvetica-Bold"
    regular = "Helvetica"
    bold = "Helvetica-Bold"
    font_candidates = [
        (Path(r"C:\Windows\Fonts\arial.ttf"), "PartnerRegular"),
        (Path(r"C:\Windows\Fonts\calibri.ttf"), "PartnerRegular"),
    ]
    bold_candidates = [
        (Path(r"C:\Windows\Fonts\arialbd.ttf"), "PartnerBold"),
        (Path(r"C:\Windows\Fonts\calibrib.ttf"), "PartnerBold"),
    ]
    for path, name in font_candidates:
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))
            regular = name
            break
    for path, name in bold_candidates:
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))
            bold = name
            break
    return regular, bold


def write_pdf(md_path: Path, pdf_path: Path, regular: str, bold: str) -> None:
    if not REPORTLAB_AVAILABLE:
        return
    text = md_path.read_text(encoding="utf-8")
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    margin = 54
    y = height - margin
    footer = pdf_path.stem

    def new_page() -> None:
        nonlocal y
        c.setFont(regular, 8)
        c.drawString(margin, 28, footer[:120])
        c.showPage()
        y = height - margin

    c.setTitle(md_path.stem)
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            y -= 9
            if y < margin:
                new_page()
            continue
        is_heading = line.startswith("#")
        line = re.sub(r"^#+\s*", "", line)
        line = line.replace("`", "")
        font = bold if is_heading else regular
        size = 14 if is_heading else 9
        width_chars = 72 if is_heading else 92
        for chunk in textwrap.wrap(line, width=width_chars, replace_whitespace=False) or [""]:
            c.setFont(font, size)
            c.drawString(margin, y, chunk[:170])
            y -= 15 if is_heading else 11
            if y < margin:
                new_page()
    c.setFont(regular, 8)
    c.drawString(margin, 28, footer[:120])
    c.save()


def write_files(package_dir: Path, docs: list[FileSpec], variant: str) -> list[str]:
    files = docs + SCHEMAS + [
        FileSpec("tools/moi_school_checker/moi_school_checker.py", TOOL_CODE),
        FileSpec("tools/moi_school_checker/README.md", TOOL_README),
        FileSpec("tools/moi_school_checker/examples/trabajo_alumno_demo.txt", DEMO_STUDENT_TEXT),
        FileSpec("tools/moi_school_checker/baselines/alumno_01/texto_prev_01.txt", BASELINE_TEXT),
        FileSpec("examples/transport_driver_event.demo.json", EXAMPLE_TRANSPORT_EVENT),
        FileSpec("examples/route_weather_signal.demo.json", EXAMPLE_WEATHER_SIGNAL),
        FileSpec(
            "manifests/PRIVATE_EXCLUSIONS.md",
            clean_text(
                "# PRIVATE EXCLUSIONS\n\n"
                + "\n".join(f"- {item}" for item in BASE_EXCLUSIONS)
                + "\n"
            ),
        ),
        FileSpec(
            "manifests/CLAIMS_AND_GATES.md",
            clean_text(
                """
                # Claims and gates

                ## Allowed with scope

                - Local-first operational architecture.
                - Evidence gates for actions and publications.
                - MOI school checker as review helper, not definitive detector.
                - Transport pilot with authorized data and human review.
                - DUAT analytics as decision support, not guaranteed prediction.

                ## Blocked

                - Secrets or credentials.
                - Full private canon, books, RPG/TCG or runtime internals.
                - Automatic sanctions for drivers or students.
                - Hidden surveillance.
                - Guaranteed AI detection, guaranteed route prediction or AGI proof.
                """
            ),
        ),
    ]
    written: list[str] = []
    for spec in files:
        path = package_dir / spec.relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(spec.content, encoding="utf-8", newline="\n")
        written.append(spec.relative_path)

    regular, bold = pdf_font_names()
    pdf_count = 0
    for md_path in sorted((package_dir / "docs").glob("*.md")):
        pdf_path = package_dir / "pdf" / (md_path.stem + ".pdf")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        write_pdf(md_path, pdf_path, regular, bold)
        if pdf_path.exists():
            written.append(str(pdf_path.relative_to(package_dir)).replace("\\", "/"))
            pdf_count += 1

    manifest = {
        "schema": "medioevo.partner_transportista_package.v0_1",
        "variant": variant,
        "date": DATE,
        "file_count_without_manifest": len(written),
        "pdf_generated": bool(pdf_count),
        "pdf_count": pdf_count,
        "publication_gate": "REVIEW_PARTNER_ONLY_NO_PUBLICATION"
        if variant == "SOCIEDAD_TECNICA"
        else "CLIENT_PRESENTATION_REVIEW",
        "allowlist_note": "All files are generated by tools/release/build_partner_transportista_zips_2026_05_19.py.",
        "private_exclusions": BASE_EXCLUSIONS,
        "files": sorted(written),
    }
    manifest_path = package_dir / "manifests" / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    written.append("manifests/MANIFEST.json")
    return sorted(written)


def hash_files(package_dir: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(package_dir.rglob("*")):
        if path.is_file():
            rel = str(path.relative_to(package_dir)).replace("\\", "/")
            hashes[rel] = sha256(path.read_bytes()).hexdigest()
    (package_dir / "manifests" / "SHA256SUMS.json").write_text(
        json.dumps(hashes, indent=2), encoding="utf-8", newline="\n"
    )
    return hashes


def zip_package(package_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_dir.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(path.relative_to(package_dir)).replace("\\", "/"))


def test_zip(zip_path: Path) -> str | None:
    with zipfile.ZipFile(zip_path, "r") as zf:
        return zf.testzip()


def run_tool_smoke(package_dir: Path) -> dict[str, Any]:
    tool_dir = package_dir / "tools" / "moi_school_checker"
    report_json = tool_dir / "report_smoke.json"
    report_md = tool_dir / "report_smoke.md"
    command = [
        sys.executable,
        "moi_school_checker.py",
        "--input",
        "examples/trabajo_alumno_demo.txt",
        "--baseline",
        "baselines/alumno_01",
        "--out",
        "report_smoke.json",
        "--markdown-out",
        "report_smoke.md",
    ]
    completed = subprocess.run(command, cwd=tool_dir, text=True, capture_output=True, timeout=30)
    data: dict[str, Any] | None = None
    if report_json.exists():
        data = json.loads(report_json.read_text(encoding="utf-8"))
    return {
        "command": "python moi_school_checker.py --input examples/trabajo_alumno_demo.txt --baseline baselines/alumno_01 --out report_smoke.json --markdown-out report_smoke.md",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "report_exists": report_json.exists() and report_md.exists(),
        "verdict": data.get("verdict") if data else None,
        "score": data.get("score") if data else None,
    }


SECRET_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"api[_-]?key\s*[:=]",
        r"secret\s*[:=]",
        r"token\s*[:=]",
        r"password\s*[:=]",
        r"bearer\s+[A-Za-z0-9_\-.]+",
        r"sk-[A-Za-z0-9]{20,}",
        r"ghp_[A-Za-z0-9]{20,}",
        r"xox[baprs]-[A-Za-z0-9-]{20,}",
    ]
]


def focal_secret_scan(path: Path) -> dict[str, Any]:
    findings: list[str] = []
    for file_path in sorted(path.rglob("*")):
        if not file_path.is_file() or file_path.suffix.lower() in {".pdf", ".zip"}:
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(str(file_path.relative_to(path)).replace("\\", "/"))
                break
    return {"count_reported": len(findings), "findings": findings}


def path_boundary_scan(path: Path) -> dict[str, Any]:
    blocked_terms = [
        ".env",
        ".git/",
        ".git\\",
        "metaevo-tcg",
        "/tcg/",
        "\\tcg\\",
        "runtime/game_bridge",
        "runtime\\game_bridge",
        "gumroad_api",
        "stripe",
        "discord_token",
        "youtube_token",
        "claudio_secrets",
    ]
    findings: list[str] = []
    for file_path in sorted(path.rglob("*")):
        rel = str(file_path.relative_to(path)).replace("\\", "/").lower()
        if any(term.lower() in rel for term in blocked_terms):
            findings.append(rel)
    return {"count_reported": len(findings), "findings": findings}


def build() -> dict[str, Any]:
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)
    TECH_DIR.mkdir(parents=True)
    CLIENT_DIR.mkdir(parents=True)

    tech_files = write_files(TECH_DIR, technical_docs(), "SOCIEDAD_TECNICA")
    client_files = write_files(CLIENT_DIR, client_docs(), "CLIENTES_CURADO")

    tech_smoke = run_tool_smoke(TECH_DIR)
    client_smoke = run_tool_smoke(CLIENT_DIR)
    (TECH_DIR / "manifests" / "TOOL_SMOKE.json").write_text(
        json.dumps(tech_smoke, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    (CLIENT_DIR / "manifests" / "TOOL_SMOKE.json").write_text(
        json.dumps(client_smoke, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )

    tech_hashes = hash_files(TECH_DIR)
    client_hashes = hash_files(CLIENT_DIR)

    tech_zip = OUT_ROOT / TECH_ZIP_NAME
    client_zip = OUT_ROOT / CLIENT_ZIP_NAME
    zip_package(TECH_DIR, tech_zip)
    zip_package(CLIENT_DIR, client_zip)

    evidence = {
        "schema": "medioevo.partner_transportista_build_evidence.v0_1",
        "date": DATE,
        "output_root": str(OUT_ROOT),
        "packages": {
            "sociedad_tecnica": {
                "folder": str(TECH_DIR),
                "zip": str(tech_zip),
                "zip_sha256": sha256(tech_zip.read_bytes()).hexdigest(),
                "zip_testzip": test_zip(tech_zip),
                "file_count": len(tech_hashes),
                "tool_smoke": tech_smoke,
                "secret_scan": focal_secret_scan(TECH_DIR),
                "path_boundary_scan": path_boundary_scan(TECH_DIR),
            },
            "clientes_curado": {
                "folder": str(CLIENT_DIR),
                "zip": str(client_zip),
                "zip_sha256": sha256(client_zip.read_bytes()).hexdigest(),
                "zip_testzip": test_zip(client_zip),
                "file_count": len(client_hashes),
                "tool_smoke": client_smoke,
                "secret_scan": focal_secret_scan(CLIENT_DIR),
                "path_boundary_scan": path_boundary_scan(CLIENT_DIR),
            },
        },
    }
    evidence_path = OUT_ROOT / "BUILD_EVIDENCE.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    readme = clean_text(
        f"""
        # MEDIOEVO Wabi-DUAT partner transportista packages

        Fecha: {DATE}

        ## ZIPs

        - `{TECH_ZIP_NAME}`: paquete tecnico para sociedad / socio.
        - `{CLIENT_ZIP_NAME}`: paquete curado para clientes.

        ## Evidencia

        Ver `BUILD_EVIDENCE.json` para SHA256, testzip, smoke test de herramienta escolar, secret scan focal y boundary scan.

        ## Frontera

        No son paquetes de publicacion externa automatica. Requieren revision humana antes de enviar.
        """
    )
    (OUT_ROOT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Build partner/client transportista ZIP packages.")
    parser.add_argument("--json", action="store_true", help="Print build evidence JSON.")
    args = parser.parse_args()
    evidence = build()
    if args.json:
        print(json.dumps(evidence, ensure_ascii=False, indent=2))
    else:
        print(f"Built packages in {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
