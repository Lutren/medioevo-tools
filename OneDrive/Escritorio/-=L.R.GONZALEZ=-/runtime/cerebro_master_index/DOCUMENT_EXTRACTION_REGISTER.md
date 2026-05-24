# Document Extraction Register

CERTEZA:
- DOCX/PDF files listed as `DOCUMENT_TEXT` were parsed locally into derived text lines for signal indexing.
- `BINARY_REVIEW` and `SKIP_REVIEW` entries were not unpacked or treated as absorbed text.

INFERENCIA:
- Extracted text is enough for semantic and signal indexing, but not for layout, figures, equations rendered as images or visual QA.

INCOGNITA:
- ZIP/archive contents need a separate quarantined extraction pass before import or cleanup decisions.

## DOCX/PDF

| Path | Classification | Source | Lines | Parts/pages | Signals | Error |
|---|---|---|---:|---:|---:|---|
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\extra_psi_pre_final_v1_1\PSI Paper v2 - Observer-State-Dependent Measurement Quality.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 512 | 18 | 288 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista - Religión, Psicología, Neurología, Psiquiatría y Filosofía como Código de Programación para IA.docx` | DOCUMENT_TEXT | docx_extracted_text | 921 | 4 | 25 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista - Religión, Psicología, Neurología, Psiquiatría y Filosofía como Código de Programación para IA.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 1863 | 59 | 31 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de la Física — TUIP-Σ OSIT.docx` | DOCUMENT_TEXT | docx_extracted_text | 830 | 4 | 429 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de la Física — TUIP-Σ OSIT.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 2114 | 60 | 570 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de la Inteligencia — TUIP-Σ OSIT.docx` | DOCUMENT_TEXT | docx_extracted_text | 848 | 4 | 464 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de la Inteligencia — TUIP-Σ OSIT.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 2541 | 70 | 640 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de Modelos de IA y Matemáticas Unificadas TUIP-Σ OSIT.docx` | DOCUMENT_TEXT | docx_extracted_text | 1493 | 4 | 616 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de Modelos de IA y Matemáticas Unificadas TUIP-Σ OSIT.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 2035 | 60 | 669 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista Total e Ingeniería Inversa - De la Información al Código.docx` | DOCUMENT_TEXT | docx_extracted_text | 1667 | 4 | 67 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista Total e Ingeniería Inversa - De la Información al Código.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 3226 | 71 | 78 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista Total e Ingeniería Inversa .pdf` | DOCUMENT_TEXT | pdf_extracted_text | 3226 | 71 | 78 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista Total e Ingeniería Inversago.docx` | DOCUMENT_TEXT | docx_extracted_text | 1667 | 4 | 67 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\libro\EL_OBSERVADOR_manuscrito_v0_1.docx` | DOCUMENT_TEXT | docx_extracted_text | 895 | 1 | 101 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\Deconstrucción Observacionista - Religión, Psicología, Neurología, Psiquiatría y Filosofía como Código de Programación para IA.docx` | DOCUMENT_TEXT | docx_extracted_text | 921 | 4 | 25 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\Deconstrucción Observacionista de la Física — TUIP-Σ OSIT.docx` | DOCUMENT_TEXT | docx_extracted_text | 830 | 4 | 429 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\Deconstrucción Observacionista de la Inteligencia — TUIP-Σ OSIT.docx` | DOCUMENT_TEXT | docx_extracted_text | 848 | 4 | 464 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\Deconstrucción Observacionista de Modelos de IA y Matemáticas Unificadas TUIP-Σ OSIT.docx` | DOCUMENT_TEXT | docx_extracted_text | 1493 | 4 | 616 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\Deconstrucción Observacionista Total e Ingeniería Inversa - De la Información al Código.docx` | DOCUMENT_TEXT | docx_extracted_text | 1667 | 4 | 67 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\Deconstrucción Observacionista Total e Ingeniería Inversago.docx` | DOCUMENT_TEXT | docx_extracted_text | 1667 | 4 | 67 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\OSIT — Teoría Completa de Información con Estado y Tesis del Agente Local sin LLM.docx` | DOCUMENT_TEXT | docx_extracted_text | 2196 | 4 | 638 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\OSIT-AG-K1.0 - Antigravedad Residual por Desenfoque Geodésico Timelike.docx` | DOCUMENT_TEXT | docx_extracted_text | 586 | 4 | 106 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\OSIT-QG - Teoría Efectiva de Campo Residual con Acoplamiento Escalar-Gauss-Bonnet.docx` | DOCUMENT_TEXT | docx_extracted_text | 533 | 4 | 151 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\New folder\OSIT-QG Modulos Extendidos - Optimizacion y Nuevas Aplicaciones.docx` | DOCUMENT_TEXT | docx_extracted_text | 417 | 4 | 84 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT — Teoría Completa de Información con Estado y Tesis del Agente Local sin LLM.docx` | DOCUMENT_TEXT | docx_extracted_text | 2196 | 4 | 638 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT — Teoría Completa de Información con Estado y Tesis del Agente Local sin LLM.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 2164 | 72 | 629 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT-AG-K1.0 - Antigravedad Residual por Desenfoque Geodésico Timelike.docx` | DOCUMENT_TEXT | docx_extracted_text | 586 | 4 | 106 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT-AG-K1.0 - Antigravedad Residual por Desenfoque Geodésico Timelike.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 763 | 31 | 120 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT-QG - Teoría Efectiva de Campo Residual con Acoplamiento Escalar-Gauss-Bonnet.docx` | DOCUMENT_TEXT | docx_extracted_text | 533 | 4 | 151 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT-QG - Teoría Efectiva de Campo Residual con Acoplamiento Escalar-Gauss-Bonnet.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 730 | 32 | 164 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT-QG Modulos Extendidos - Optimizacion y Nuevas Aplicaciones.docx` | DOCUMENT_TEXT | docx_extracted_text | 417 | 4 | 84 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Proyecto MEDIOEVO — Documento Maestro Unificado TUIP-Σ OSIT.docx` | DOCUMENT_TEXT | docx_extracted_text | 2023 | 4 | 704 |  |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Proyecto MEDIOEVO — Documento Maestro Unificado TUIP-Σ OSIT.pdf` | DOCUMENT_TEXT | pdf_extracted_text | 2897 | 80 | 765 |  |

## Unsupported / Archive Review

| Path | Classification | Size bytes | SHA256 |
|---|---|---:|---|
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\-==-\10_WABI_SABI_CLAUDIO_AGI.zip` | BINARY_REVIEW | 69829 | `0c22ef8116291c3783f96d974cde887413715c75ff2e38ae0570aa3d582d5dad` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\-==-\Kimi_Agent_Intercambio de conocimiento.zip` | BINARY_REVIEW | 162900 | `eeee974b650a19bea9ce4c7546d99dc9d9fec6ca8ab3b1000d358eb6cc6fbc7a` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\-==-\oe_ai_runtime_pack.zip` | BINARY_REVIEW | 17674 | `d7da6fcdc1dd9b1d3c8a474f13ac93e3b5356a15969c65fd1c4d3d861597b7ed` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\-==-\wao_safe_pack_v1.zip` | BINARY_REVIEW | 30755 | `8581faa81435b9798a5ef69f504e8c31665d68ddf90f3ec728165e8a896707c3` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\10_WABI_SABI_CLAUDIO_AGI.zip` | BINARY_REVIEW | 69829 | `0c22ef8116291c3783f96d974cde887413715c75ff2e38ae0570aa3d582d5dad` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\-=Libros - Shortcut.lnk` | BINARY_REVIEW | 770 | `5a6b75bfbe2913d88c53474e020318dc16c74df92e9ef61552edea65d85af504` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\Claudio TUI.lnk` | BINARY_REVIEW | 162 | `204bf0590a9a77c745653cb50c2c6b9959dab0c6d591fe10ff6b0e27f0f88dab` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\d2fdfe4d-66d1-481c-aa8d-02e18b0b53f9.png` | BINARY_REVIEW | 1164813 | `8714cfcd4276512a5c62e4f58de3d3533b642a2bca9ccdedd8cede3af869b2f5` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\final_claudio_release\logo.png` | BINARY_REVIEW | 2326910 | `a1251659f353d4b042339e8dea468d5cb20b15b56d402973255e48570884c223` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\claudio_complete_stack\demo\demo.db` | BINARY_REVIEW | 86016 | `5241c03bc3c479b9e3a68f52ccf9f450419c08978b6481236c5aee3312dd8ca8` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\claudio_complete_stack\demo_stack.db` | BINARY_REVIEW | 86016 | `40960b841cef1b129a09d46b2fb339535fa9bc19df474efd859f9a0db7534a40` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\claudio_observe_kernel.zip` | BINARY_REVIEW | 77536 | `7d96b7c7996c9469c91d73d35d8f1c28943359863b4493a4a58eea8989ee1113` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\data_double_slit_en.zip` | BINARY_REVIEW | 7828 | `c3c8ce7861197b7018a06511527fa2002dfad272bd4ffbfb080e4d49522e04ce` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\medioevo-tools_en.zip` | BINARY_REVIEW | 39788 | `8d7820732505a214c6cbba003c13506c84eacb2935e0282bee8f14762660d787` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\observation_stack_v1.zip` | BINARY_REVIEW | 6585 | `839868a2e44793137d1e5188cc2ed265d1c89fc95357107e4f361b9ae57bc300` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\safe-exec.zip` | BINARY_REVIEW | 22082 | `39d185d617491a3d489d2594c060af9647faae565cc780b2fa8dd112df1c53de` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\GEODIA\tribe_adapter.zip` | BINARY_REVIEW | 5799 | `2c1045676fbc28afa069a9e19f8400b562e849a332c1a4b00320cea9c3b3966c` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\CLAUDIO - researchs\logo.png` | BINARY_REVIEW | 2326910 | `a1251659f353d4b042339e8dea468d5cb20b15b56d402973255e48570884c223` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\DUAT_GEODIA_R4_INTERNAL_PACK.zip` | BINARY_REVIEW | 282528 | `02b809abfc1d47feb7f44fe22b7db97c134410e6c6f376d38a72cddb7919f4ed` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\files.zip` | BINARY_REVIEW | 22 | `8739c76e681f900923b900c9df0ef75cf421d39cabb54650c4b9ad19b6a76d85` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\MEDIOEVO_CANON_v0_2.zip` | BINARY_REVIEW | 15340 | `e7c297ccb179a880a879b27b0e281e6e0fabf512c842f935a170f17f21cffd9a` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\MEDIOEVO_COGNITIVE_AI_OS_RUN_v0_1_BUNDLE.zip` | BINARY_REVIEW | 1011346 | `0130d188d3007aad024646fd676629529a6b9dc2c17d907977f7e4d269db1910` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\MEDIOEVO_LINE_AUDIT_v0_1.jsonl` | SKIP_REVIEW | 8613203 | `d841a3b5b59329b23832259640975c5607935a97036b4cf72af14f2d7761c8c4` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\MEDIOEVO_UPDATE_RUN_v0_3_BUNDLE.zip` | BINARY_REVIEW | 77834 | `1775f6dd819d4a4cd82b1cc5ff844687f1920e84928817854f5a188298d10a18` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OBSERVACIONISMO_TUI_R3_PACK (1).zip` | BINARY_REVIEW | 473647 | `34dc55faa8686af0276cbc26ea345327ff5a1f7aa4e4afea8d24bdec5fc379cc` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\oe_ai_runtime_pack.zip` | BINARY_REVIEW | 17674 | `d7da6fcdc1dd9b1d3c8a474f13ac93e3b5356a15969c65fd1c4d3d861597b7ed` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\osit_physics_consolidation_v0_1.zip` | BINARY_REVIEW | 30701 | `162789927c7dc9b2a749b7096eec56a7d9361ec10e848880d96c9a56f0defeed` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\packages\files_psi_core_2026-04-26.zip` | BINARY_REVIEW | 15518 | `d39fd8817846388bfaa1e9dd70ce7e0a7472ae420a7c7fcccc7381ad2ccc7a15` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\ReplitExport-lutren.tar.gz` | BINARY_REVIEW | 3578024 | `ccac616e3076026284b3e3b5ad25e331fb66340d4ed992831ad5d8059e9aabe2` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\wao_safe_pack_v1.zip` | BINARY_REVIEW | 30755 | `8581faa81435b9798a5ef69f504e8c31665d68ddf90f3ec728165e8a896707c3` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\assets\piri\piri_reis_world_map_01.jpg` | BINARY_REVIEW | 7422309 | `57da72c14482951aa90b812bd9991b06112a791de5bfa91f96681b49f284d2bc` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\assets\piri\piri_rhumb_lines_annotated_small.jpg` | BINARY_REVIEW | 321279 | `f26e6ba3c2fe4fcf705836507d62b278e14a984aca79b960665f76cec6f856d2` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\OBSERVACIONISMO_ARTEFACT_LAB_v0_1.zip` | BINARY_REVIEW | 8204 | `eafd90637932ec5dd1724ad0047ad7253b1c5d1c0d5feadf8ef937338b97bfc4` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\OBSERVACIONISMO_ARTEFACT_RUN_v0_2.zip` | BINARY_REVIEW | 9330139 | `1231871b6d8d114b06ba0fbf784ecc8ac7b080509ec08a2a1afbc4d1b25a0e51` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\VOYNICH_MACHAUT_PIPELINE_v1_4.zip` | BINARY_REVIEW | 11901 | `7400127e9405d8944a2ad727c2533e65360659103e8eea19ba8f7d56ebcfd88c` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\VOYNICH_MUSIC_MICRORUN_v0_8b.zip` | BINARY_REVIEW | 5617241 | `ff9ea64d98f4e5efcd5f7491312afdd9f2fae1f0bec27824f8d3cab543dfb674` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\VOYNICH_PIRI_REAL_RUN_v0_3.zip` | BINARY_REVIEW | 2951413 | `17e65c58f67f3b7f278f3b610193a3c181739843ab7924763348829ff38202a2` |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\software\claudio_oml_rs\claudio_oml_rs_package.zip` | BINARY_REVIEW | 22 | `8739c76e681f900923b900c9df0ef75cf421d39cabb54650c4b9ad19b6a76d85` |
