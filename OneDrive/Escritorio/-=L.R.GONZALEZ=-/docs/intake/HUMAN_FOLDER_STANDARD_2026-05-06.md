# Human Folder Standard - 2026-05-06

## Regla

Las carpetas de entrada no son archivo historico. Son bandejas de trabajo.

Un humano debe poder abrir una carpeta y entenderla en menos de un minuto:

- Raiz limpia.
- Un `README` o `00_LEER_PRIMERO.md`.
- Carpetas por funcion, no por accidente.
- Fuentes archivadas fuera del camino diario.
- Hashes y manifiestos para auditoria, no como unica forma de navegar.

## Estados visibles

| estado | significado humano | accion permitida |
|---|---|---|
| `INBOX` | llego material nuevo | analizar, fichar, absorber |
| `ABSORBIDO` | ya se extrajo lo util | retirar de inbox |
| `ARCHIVO_FRIO` | fuente unica preservada | no editar, consultar por evidencia |
| `BORRADO_SEGURO` | duplicado exacto o basura regenerable | solo con hash y log |
| `REVIEW` | falta decision humana o gate | no mover a publico |
| `BLOQUEADO` | secreto, privado, claim fuerte o riesgo | no publicar ni usar como verdad |

## Contrato de carpeta humana

Cada carpeta operativa debe tener:

- `00_LEER_PRIMERO.md` o `README_*.md`.
- Proposito de la carpeta.
- Que entra.
- Que no entra.
- Donde se archiva lo absorbido.
- Ultima corrida del Curador.
- Conteo de pendientes.

Cada archivo retirado debe tener:

- SHA256.
- Ficha o registro.
- Decision.
- Carril.
- Ruta canonica o archivo frio.
- Falsadores.

## Lobby de Alejandria

Uso: entrada manual de prompts, documentos largos y paquetes de investigacion que deben ser absorbidos.

Raiz visible esperada:

```text
C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria
+-- README_LOBBY_DE_ALEJANDRIA.md
```

Archivo frio humano actual:

```text
runtime\curador_seto\source_archive\lobby_alejandria\2026-05-06
+-- 00_LEER_PRIMERO.md
+-- 01_prompt_master_orquestador
+-- 02_wabi_sabi_osit
+-- 03_osit_qg_research_boundary
+-- 04_matrix_biblioteca
+-- 05_duat_geodia_private_research
+-- 06_duat_readonly_adapter
+-- 07_psi_observacionismo
+-- 08_lenguaje_observacionista
+-- 09_ai_browser_security
+-- 10_mission_control_comms
+-- 11_seguridad_programador_local
+-- 12_publicacion_release
+-- 13_privado_rpg_tcg
```

Regla diaria:

- Todo lo que llega al Lobby se analiza completo.
- Lo util se absorbe a Atlas/canon/runtime.
- La fuente unica se mueve a `ARCHIVO_FRIO`.
- El inbox vuelve a quedar limpio.
- No quedan documentos sueltos sin ficha.

## Criterio de calidad

Una carpeta esta limpia cuando:

- No hay archivos sueltos ambiguos.
- No hay duplicados visibles.
- Cada fuente retirada tiene ficha.
- La raiz no mezcla trabajo activo con archivo.
- Un humano sabe que leer primero.
- Un agente sabe que comando ejecutar despues.
