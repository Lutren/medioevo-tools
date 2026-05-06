# Sensorium / Claudio AI Engineering Extraction 2026-05-03

Status: `LOCAL_RESEARCH_EVIDENCE / SELECTIVE_EXTRACTION_ONLY`

## Opinion Operativa

La idea es valiosa para Claudio, pero no por probar fisica nueva. Su valor real
es de ingenieria: convierte la percepcion de un agente en un contrato medible.

En vez de preguntar solo "que dijo el modelo?", permite preguntar:

- que canal produjo la evidencia;
- que observador la pondero;
- cuanto dependio del canal visual/textual;
- si otros perfiles llegan a la misma etiqueta;
- si la conclusion debe permitirse, degradarse o bloquearse.

Esto encaja directo con ActionGate, witness logs, handoff y DUAT/GEODIA como
laboratorio privado de observadores. No debe entrar como claim publico fuerte.

## Fuente Local Revisada

- ZIP: `C:\Users\L-Tyr\Downloads\sensorium_inversion_lab_pack.zip`
- SHA256 ZIP: `E16A7CB6EA4B884E9CBB55DADE9ACF5C2D8B93AF660F62FF12975572A00E8143`
- Extraccion privada: `C:\Users\L-Tyr\runtime\private_labs\sensorium_inversion_lab_2026-05-03\sensorium_inversion_lab`
- Script: `sensorium_inversion_lab.py`
- SHA256 script: `DF5105E2E46D09C31AA22F6CBB3931EE1C5FF0963A666F247ECADF9FFFA346B2`
- Ficha: `docs/intake/SENSORIUM_INVERSION_LAB_INTAKE_2026-05-03.md`

Nota: el ZIP local contiene Sensorium Inversion Lab base. No contiene
`sensorium_psi_bridge.py` ni comandos SPARC. El archivo legacy encontrado como
`psi_bridge.py` es puente EML/salud de sesion, no puente SPARC.

## Comandos Ejecutados

```powershell
python sensorium_inversion_lab.py explain
python sensorium_inversion_lab.py channels
python sensorium_inversion_lab.py profiles
python -m py_compile sensorium_inversion_lab.py
python sensorium_inversion_lab.py run-demo --out-dir runs\demo_2026-05-03 --n 300 --seed 42
python sensorium_inversion_lab.py observe --input runs\demo_2026-05-03\demo_phenomena.csv --profile human_visual --out runs\demo_2026-05-03\observed_human_fresh.csv --report runs\demo_2026-05-03\human_report_fresh.json --seed 42
python sensorium_inversion_lab.py invert --input runs\demo_2026-05-03\demo_phenomena.csv --out runs\demo_2026-05-03\inversion_report_fresh.json --seed 42
python sensorium_inversion_lab.py veil-test --input runs\demo_2026-05-03\demo_phenomena.csv --out-dir runs\demo_2026-05-03\veil_human_balanced --profile human_visual --profile instrument_balanced --seed 42
python sensorium_inversion_lab.py veil-test --input runs\demo_2026-05-03\demo_phenomena.csv --out-dir runs\demo_2026-05-03\veil_nonvisual --profile dark_observer --profile electric_first --profile magnetic_first --profile phase_observer --seed 42
```

## Resultados

Dataset demo: `300` fenomenos sinteticos.

### Todos Los Perfiles

| metric | value |
|---|---:|
| mean_clarity | 0.6140 |
| median_clarity | 0.6438 |
| mean_visual_dependence | 0.1624 |
| mean_channel_coverage | 0.6406 |
| mean_cross_channel_coherence | 0.4617 |
| mean_label_agreement | 0.2833 |
| invariance_score | 0.5004 |

Recomendacion del propio lab: buscar nuevos invariantes; no colapsar conclusion
todavia por bajo acuerdo entre observadores.

### Perfil Humano Visual

| metric | value |
|---|---:|
| mean_clarity | 0.4484 |
| mean_visual_dependence | 0.5975 |
| mean_coverage | 0.5000 |
| rough_truth_recovery | 0.1267 |

Lectura: el perfil humano visual es dependiente de photon/texto y recupera poco
el truth label sintetico. Es buen proxy para "agente saturado por una modalidad".

### Human Visual + Instrument Balanced

| metric | value |
|---|---:|
| mean_clarity | 0.6336 |
| mean_visual_dependence | 0.3477 |
| mean_channel_coverage | 0.7500 |
| mean_label_agreement | 0.5000 |
| invariance_score | 0.5827 |
| hidden_candidate_fraction | 0.5733 |

Lectura: mejora cobertura y claridad, pero el acuerdo aun es bajo.

### Perfiles No Visuales

| metric | value |
|---|---:|
| mean_clarity | 0.6595 |
| mean_visual_dependence | 0.0000 |
| mean_channel_coverage | 0.6563 |
| mean_label_agreement | 0.3200 |
| invariance_score | 0.5395 |
| hidden_candidate_fraction | 1.0000 |

Lectura: baja dependencia visual, pero no suficiente acuerdo. El `1.0000` de
hidden candidates es una alerta de calibracion, no un descubrimiento.

## Hallazgos De Ingenieria Para IA

1. `ObserverProfile` es el patron mas util.
   Cada agente o herramienta puede declarar pesos de canal, ruido, dropout,
   compresion linguistica y ancho de atencion.

2. `ObservationResult` deberia convertirse en witness log.
   Campos minimos: `observer`, `perceived_label`, `clarity_score`,
   `visual_dependence`, `cross_channel_coherence`, `channel_coverage`,
   `saturation_rate`, `language_loss`, `channel_values`.

3. `invariance_score` sirve como gate epistemico.
   Una accion irreversible o claim fuerte no deberia pasar si el acuerdo entre
   perfiles es bajo, aunque un perfil individual parezca seguro.

4. `visual_dependence` generaliza a `text_dependence`.
   Para Claudio, el equivalente practico no es solo luz; es dependencia de un
   unico canal: texto conversacional, captura de pantalla, log parcial,
   memoria incompleta o una sola fuente.

5. `language_loss` sirve para handoff.
   Si una decision viene de observacion rica pero se reduce a un resumen pobre,
   Claudio debe pedir evidencia o replay antes de ejecutar.

6. `low_bandwidth_human` es un buen modelo de agente cansado.
   Puede alimentar Safe Exec: si baja cobertura, sube compresion y cae claridad,
   degradar a modo lectura/reporte.

7. `instrument_balanced` es el perfil de auditor.
   Debe ser el modo por defecto para revision antes de publicar, borrar, mover,
   ejecutar shell riesgoso o hacer claims.

## Contrato Propuesto Para Claudio

```json
{
  "schema": "sensorium.audit.v1",
  "subject": "claim_or_action_id",
  "channels": {
    "text": 0.0,
    "filesystem": 0.0,
    "test": 0.0,
    "runtime": 0.0,
    "user_instruction": 0.0,
    "external_source": 0.0,
    "memory": 0.0,
    "time": 0.0
  },
  "profiles": ["human_visual", "instrument_balanced", "low_bandwidth_human"],
  "metrics": {
    "clarity_score": 0.0,
    "single_channel_dependence": 0.0,
    "cross_channel_coherence": 0.0,
    "channel_coverage": 0.0,
    "label_agreement": 0.0,
    "language_loss": 0.0,
    "invariance_score": 0.0
  },
  "decision": "ALLOW | REVIEW | BLOCK",
  "witness_log": "path/to/evidence.json"
}
```

Initial gate rule:

- `ALLOW`: low-impact action and `channel_coverage >= 0.6`.
- `REVIEW`: `invariance_score < 0.7`, `label_agreement < 0.55`, or
  `single_channel_dependence > 0.55`.
- `BLOCK`: destructive/external/high-claim action with no independent channel.

## Aplicacion A DUAT / GEODIA

Sensorium no debe entrar como "predice sociedades". Entra como auditor de
observadores para laboratorios sinteticos:

| DUAT/GEODIA channel | Sensorium equivalent | use |
|---|---|---|
| narrativa / rumor | text/photon-like | detectar sobrepeso de relato visible |
| recursos / economia | material channel | balancear contra narrativa |
| espacio / rutas | geometry/gravity-like | medir estructura no textual |
| energia / clima | thermal-like | shocks y coste |
| instituciones | field-like | reglas, permisos, friccion |
| memoria / residuo | temporal_phase | persistencia y demora |
| evidencia externa | instrument_balanced | auditoria antes de claims |

Uso inmediato: agregar `observer_audit` a cada simulacion privada antes de
aceptar una conclusion social. Si `label_agreement` es bajo, GEODIA no colapsa:
genera preguntas, falsadores o nuevos instrumentos.

## Problemas Detectados

- El bridge SPARC descrito en el mensaje no esta dentro del ZIP local.
- No hay tests unitarios en el paquete.
- La inversion marca `hidden_candidate_fraction = 1.0` cuando se usan solo
  perfiles no visuales; eso indica sesgo de reconstruccion.
- Los perfiles y pesos son heuristicas manuales.
- Los datos demo son sinteticos; no son evidencia cientifica real.

## Siguiente Extraccion Recomendada

1. Crear un modulo pequeno `sensorium_audit` en Claudio o `obsai-core`, no copiar
   el paquete entero.
2. Implementar solo el contrato `sensorium.audit.v1`, metricas y tests sinteticos.
3. Agregar un test de regresion para evitar `hidden_candidate_fraction = 1.0`
   como falso positivo.
4. Conectar el contrato con `ActionGate`: delete/publish/push/social requiere
   `instrument_balanced` o evidencia multi-canal.
5. Si aparece el `sensorium_psi_bridge.py` real, registrarlo en intake y correr
   SPARC por separado.
