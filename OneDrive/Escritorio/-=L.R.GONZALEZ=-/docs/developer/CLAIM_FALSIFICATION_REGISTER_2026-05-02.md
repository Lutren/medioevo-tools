# CLAIM_FALSIFICATION_REGISTER_2026-05-02

Decision aplicada: claims fuertes se prueban o se bajan de nivel.

## Estados

| estado | uso |
|---|---|
| `OBSERVED` | hay archivo, test, output, ruta o evidencia directa |
| `INFERENCE` | interpretacion razonable desde evidencia, marcada como tal |
| `HYPOTHESIS` | idea investigable sin prueba suficiente |
| `UNKNOWN` | no hay informacion suficiente |
| `VERIFIED` | prueba reproducible local o externa paso |
| `FALSIFIED` | prueba concreta contradice la claim |
| `DEMO_ONLY` | funciona en fixtures/sintetico, no en datos reales generalizables |
| `RESEARCH_ONLY` | no es copy comercial ni promesa publica |
| `BLOCK` | no se puede publicar, vender o repetir como claim |

## Registro inicial

| claim | producto/fuente | prueba minima | estado publico |
|---|---|---|---|
| ResidueOS reduce riesgo de acciones de agentes | ResidueOS | dataset sintetico + decisiones `APPROVE/REVIEW/BLOCK` + falsadores | `DEMO_ONLY` hasta dataset real |
| DUAT modela memoria de artefactos y calibracion | DUAT Lab | contrato de simulador + eventos sinteticos + replay deterministico | `DEMO_ONLY` / `RESEARCH_ONLY` |
| NEUROSTATE visualiza estado operativo de agentes | NEUROSTATE UI | UI local con fixtures, privacidad y sin datos medicos | `DEMO_ONLY` |
| NEUROSTATE diagnostica estados cognitivos humanos | fuente externa/raw notes | requeriria revision medica/etica/legal | `BLOCK` |
| GEODIA predice cambios sociales reales | GEODIA Social Observatory | fuentes licenciadas + backtests historicos + falsadores | `BLOCK` para producto; `RESEARCH_ONLY` interno |
| Wave FC ordena documentos sin alterar originales | Wave FC | prueba con documentos sanitizados + hashes antes/despues + rollback | `LOCAL_DEMO_READY` si pasa |
| FlujoCRM aumenta ventas garantizadas | FlujoCRM | requeriria estudio controlado de clientes reales | `BLOCK` |
| FlujoCRM organiza pipeline local sin nube | FlujoCRM | smoke app + DB local + no network dependency para core | `OBSERVED` si smoke pasa |
| Asistente envia WhatsApp automaticamente | Asistente Negocio | la version publica no debe hacerlo | `BLOCK` |
| Asistente prepara borradores aprobados por humano | Asistente Negocio | flujo local con borrador y confirmacion | `ALLOWED_PRODUCT_CLAIM` si QA pasa |
| Claudio OS es un ISO terminado | Claudio OS Blueprint | boot QEMU/ISO firmado/verificado | `BLOCK` hasta evidencia |
| Publicacion Gumroad/website esta hecha | publishing | URL live verificada + GET/API/captura | `BLOCK` hasta evidencia directa |

## Actualizacion DUAT GEODIA OS 2026-05-05

| claim | producto/fuente | prueba minima | estado publico |
|---|---|---|---|
| DUAT GEODIA OS tiene kernel propio local booteable en QEMU | `claudio\os\duat_geodia_kernel`, `runtime\duat_geodia_kernel` | `tools\duat_geodia_kernel_benchmark.py --write --run-qemu --require-qemu` | `VERIFIED_LOCAL`: no es claim publico/comercial |
| DUAT GEODIA OS tiene multistage/protected-mode local con IDT/PIC/timer/UI markers | `runtime\duat_geodia_multistage` | `tools\duat_geodia_multistage_benchmark.py --write --run-qemu --require-qemu` | `VERIFIED_LOCAL`: no es claim publico/comercial |
| DUAT GEODIA OS tiene ISO El Torito local que arranca en QEMU | `runtime\duat_geodia_iso\duat_geodia_os.iso` | `tools\duat_geodia_iso_builder.py --write --run-qemu --require-qemu` | `VERIFIED_LOCAL`: SHA256 `e51a7b89dad1b643a3f96d21334acd191b705feb66311c7f8e5fcf62b0141425`; publicacion sigue `BLOCK` |
| DUAT GEODIA OS esta listo para publicacion externa | release/publicacion | target allowlist + secret scan + path scrub + claims scan + ActionGate | `BLOCK` |
| `Phi_eff(R)`, `epsilon` y `A_eff` prueban ciencia nueva | PSI formal / Brain OS | datos reales, baselines, holdout y revision independiente | `BLOCK`; uso permitido solo como proxy/hipotesis interna |

## Intake DUAT / GEODIA 2026-05-02

| claim | producto/fuente | prueba minima | estado publico |
|---|---|---|---|
| DUAT Geodia v0.2 es ejecutable localmente | `duat_geodia_v0_2.zip` | extraer en temporal y correr `python -m pytest tests -q` | `OBSERVED`: `1 passed` en temporal |
| DUAT + FOR v0.1 es ejecutable localmente | `duat_for_integration_v0_1.zip` | extraer en temporal y correr `python -m pytest tests -q` | `OBSERVED`: `3 passed` en temporal |
| DUAT Genesis es sandbox sintetico reproducible | `packages/open-dev/duat-genesis` | `python -m pytest tests -q` + CLI JSON | `OBSERVED`: `3 passed`; `SYNTHETIC_ONLY` |
| DUAT Genesis sirve para estudios reales sin validacion adicional | `packages/open-dev/duat-genesis` | datasets licenciados, protocolo por dominio, holdout y falsadores | `BLOCK`; solo sandbox modificable |
| GEODIA/DUAT predice cambios sociales reales | `duat_geodia_v0_2.zip`, `duat_omnis_v1.py`, textos largos | fuentes reales licenciadas, backtests historicos, holdout y falsadores | `BLOCK` para copy; `RESEARCH_ONLY` interno |
| EML es util como operador numerico experimental | `cinco.txt`, `backup.txt`, ZIPs, `duat_omnis_v1.py` | unit tests de finitud, monotonia, sensibilidad y casos adversos | `HYPOTHESIS` hasta tests dentro del repo |
| EML reemplaza leyes fisicas o explica conciencia/historia | `cinco.txt`, `seis.txt`, DUAT Lab HTML | validacion cientifica externa, predicciones falsables reproducidas | `BLOCK` |
| FOR/MCR corrige o reemplaza a Newton | `seis.txt`, `cinco.txt`, `duat_for_integration_v0_1.zip` | revision formal, predicciones cuantitativas y falsacion independiente | `BLOCK` |
| La "Vibe equation" reemplaza `F=ma` | `cinco.txt` | derivacion formal, experimentos cuantitativos y comparacion contra fisica clasica | `BLOCK` |
| DUAT MCP puede operar Claudio con seguridad autonoma | `¡Claro, amigo! Vamos a extender el.txt` | ActionGate, tools read-only, no shell/red/browser sin aprobacion y tests de permisos | `BLOCK` hasta contrato local |
| DUAT-OMNIS simula sociedades humanas reales | `duat_omnis_v1.py` | calibracion con datasets licenciados y holdout | `BLOCK`; demo sintetico permitido |
| DUAT v4.2 prueba claims Penrose/Hameroff/neuro | `duat_v4_final (1).html` | validacion cientifica/medica externa | `BLOCK` |
| DUAT Geodia puede abrirse como repo publico | decision humana 2026-05-02 | frontera privada, sin ingenieria compartida | `BLOCK`; solo descripcion low-claim |
| Sensorium Inversion Lab audita dependencia de observador en datos sinteticos | `sensorium_inversion_lab_pack.zip` | demo local, `veil_report.json`, metricas de claridad/cobertura/acuerdo | `OBSERVED` como auditor sintetico; `RESEARCH_ONLY` |
| Sensorium demuestra estructuras ocultas reales | `sensorium_inversion_lab_pack.zip` | instrumentos reales calibrados + holdout + falsadores negativos | `BLOCK`; el demo marco `hidden_candidate_fraction=1.0` como alerta de calibracion |
| Sensorium/SPARC bridge package existe localmente | `sensorium_psi_bridge_pack.zip` | ficha + hash + listado ZIP | `OBSERVED` como paquete toy/research; SPARC real sigue `UNKNOWN/BLOCK` hasta corrida local verificada |
| Sensorium/SPARC bridge prueba robustez fisica real | `sensorium_psi_bridge_pack.zip` | corrida SPARC real, proxies declarados, baselines, holdout y revision independiente | `BLOCK`; el paquete toy no basta para claim cientifico |

## Regla para copy publico

No usar palabras como "garantiza", "predice", "diagnostica", "autonomo sin supervision", "cientificamente probado" o "publicado" salvo que la ficha tenga `VERIFIED` y evidencia enlazada.

## Regla para papers

Cada paper debe declarar:

- que datos son sinteticos;
- que claims son hipotesis;
- que pruebas falsarian el metodo;
- que no se esta afirmando diagnostico, prediccion garantizada ni nueva fisica validada.
