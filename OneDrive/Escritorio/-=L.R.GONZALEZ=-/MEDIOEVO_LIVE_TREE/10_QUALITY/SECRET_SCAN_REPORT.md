# SECRET_SCAN_REPORT

Fecha: 2026-05-12T01:21:26

Metodo: escaneo no destructivo por nombres sensibles y patrones de contenido. Este reporte no imprime valores completos; las coincidencias se reemplazan por `REDACTED_*`.

## Resultado ejecutivo

- Archivos candidatos escaneados: `2601`
- Hallazgos reportados: `475`
- BLOQUEO_PUBLICACION: `TRUE`
- BLOQUEO_PUSH: `TRUE`
- BLOQUEO_DEPLOY: `TRUE`

## Conteo por tipo

- content: 164
- content_skipped: 3
- path_name: 306
- zip_name: 2

## Conteo por razon

- assignment_secret: 158
- bearer_token: 2
- env_file: 6
- file_too_large_for_content_scan: 3
- github_like_token: 2
- local_settings: 1
- openai_like_key: 2
- payment_or_provider: 277
- secret_name: 22
- secret_name inside ZIP name: 2

## Hallazgos enmascarados

| Root | Ruta | Tipo | Razon | Linea | Redaccion |
|---|---|---|---:|---:|---|
| `ROOT_BRAIN_OS` | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_CANON_MINIMO_PARA_IAS_v1_0.md` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_BRAIN_OS` | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_CANON_MINIMO_PARA_IAS_v1_0.pdf` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_BRAIN_OS` | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_v12_2_1_CARPETA_MAESTRA_RECONSTRUCTIVA.zip` | `zip_name` | `secret_name inside ZIP name` | `0` | `REDACTED_ZIP_ENTRY_NAME` |
| `ROOT_BRAIN_OS` | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\Prompt-Execute-Master.zip` | `zip_name` | `secret_name inside ZIP name` | `0` | `REDACTED_ZIP_ENTRY_NAME` |
| `ROOT_BRAIN_OS` | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Qwen_01.png` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_BRAIN_OS` | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\Qwen_02.png` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\SECRET_SCAN_REPORT.md` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.claudeignore` | `path_name` | `local_settings` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.discord_client_id` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.discord_token` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.discord_token` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.youtube_token.pickle` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.youtube_token.pickle` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio_local.py` | `content` | `assignment_secret` | `540` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio_local.py` | `content` | `assignment_secret` | `544` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\create_playlist_videos.py` | `content` | `assignment_secret` | `12` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\create_youtube_albums.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\discord_bot.log` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\discord_bot.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\discord_bot.py` | `content` | `assignment_secret` | `176` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\gumroad_api_fix.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\gumroad_audit.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\gumroad_debug.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\gumroad_fix_v3.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\gumroad_upload_all.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\gumroad_upload_files.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\send_email_philippe.py` | `content` | `assignment_secret` | `177` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\upload_youtube.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\upload_youtube_albums.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\upload_youtube_audiobooks.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\upload_youtube_playwright.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\youtube_album_uploads.json` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\youtube_metadata.json` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\youtube_uploads.json` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\youtube_upload_all.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_gumroad_debug.json` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\ANALISIS1txt.txt` | `content` | `assignment_secret` | `713` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Arquitectura de la Persistencia Sis.txt` | `content` | `assignment_secret` | `395` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Arquitectura de la Persistencia Sis.txt` | `content` | `assignment_secret` | `398` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Arquitectura de la Persistencia Sis.txt` | `content` | `assignment_secret` | `399` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Arquitectura de la Persistencia Sis.txt` | `content` | `assignment_secret` | `400` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Arquitectura de la Persistencia Sis.txt` | `content` | `assignment_secret` | `407` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `212` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `498` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `501` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `502` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `503` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `506` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `507` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `508` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `509` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `512` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `513` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `514` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `517` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `518` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `519` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `520` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `521` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `530` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `538` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\BRAIN OS.txt` | `content` | `assignment_secret` | `541` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\consegui mucha informacion util.txt` | `content` | `assignment_secret` | `2470` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\consegui mucha informacion util.txt` | `content` | `assignment_secret` | `2473` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\consegui mucha informacion util.txt` | `content` | `assignment_secret` | `2572` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\consegui mucha informacion util.txt` | `content` | `assignment_secret` | `2575` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\consegui mucha informacion util.txt` | `content` | `assignment_secret` | `2709` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\from pathlib import Path.txt` | `content` | `assignment_secret` | `302` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\from pathlib import Path.txt` | `content` | `assignment_secret` | `307` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\from pathlib import Path.txt` | `content` | `assignment_secret` | `350` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\from pathlib import Path.txt` | `content` | `assignment_secret` | `360` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\from pathlib import Path.txt` | `content` | `assignment_secret` | `398` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\from pathlib import Path.txt` | `content` | `assignment_secret` | `402` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\LCP.txt` | `content` | `assignment_secret` | `5` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\LCP.txt` | `content` | `assignment_secret` | `103` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\LCP.txt` | `content` | `assignment_secret` | `104` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\LCP.txt` | `content` | `assignment_secret` | `106` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\para revisar 2.txt` | `content` | `assignment_secret` | `2467` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\para revisar 2.txt` | `content` | `assignment_secret` | `2483` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\para revisar 2.txt` | `content` | `assignment_secret` | `2554` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\por revisar 1.txt` | `content` | `assignment_secret` | `797` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\por revisar 1.txt` | `content` | `assignment_secret` | `978` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\por revisar 1.txt` | `content` | `assignment_secret` | `1013` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Sí, es absolutamente posible y, de.txt` | `content` | `assignment_secret` | `1606` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Sí, es absolutamente posible y, de.txt` | `content` | `assignment_secret` | `1708` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Untitled.txt` | `content` | `assignment_secret` | `157` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Untitled.txt` | `content` | `assignment_secret` | `161` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Untitled.txt` | `content` | `assignment_secret` | `167` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\Untitled.txt` | `content` | `assignment_secret` | `257` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\-==-\Sí, es absolutamente posible y, de.txt` | `content` | `assignment_secret` | `1606` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\-==-\Sí, es absolutamente posible y, de.txt` | `content` | `assignment_secret` | `1708` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `assignment_secret` | `10` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `bearer_token` | `39` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `assignment_secret` | `74` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `assignment_secret` | `107` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `assignment_secret` | `136` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `bearer_token` | `173` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `assignment_secret` | `203` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\banananana.txt` | `content` | `assignment_secret` | `229` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Entendido. Aquí tienes el paquete c.txt` | `content` | `assignment_secret` | `1965` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Entendido. Aquí tienes el paquete c.txt` | `content` | `assignment_secret` | `1997` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\ESTADO.txt` | `content` | `assignment_secret` | `151` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\ESTADO.txt` | `content` | `assignment_secret` | `152` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\ESTADO.txt` | `content` | `assignment_secret` | `153` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\ESTADO.txt` | `content` | `assignment_secret` | `156` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\ESTADO.txt` | `content` | `assignment_secret` | `157` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\ESTADO.txt` | `content` | `assignment_secret` | `158` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Lei los 19 archivos del roadmap y t.txt` | `content` | `assignment_secret` | `30` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Lei los 19 archivos del roadmap y t.txt` | `content` | `assignment_secret` | `31` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Lei los 19 archivos del roadmap y t.txt` | `content` | `assignment_secret` | `32` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Lei los 19 archivos del roadmap y t.txt` | `content` | `assignment_secret` | `35` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Lei los 19 archivos del roadmap y t.txt` | `content` | `assignment_secret` | `36` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Lei los 19 archivos del roadmap y t.txt` | `content` | `assignment_secret` | `37` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\medioevo_sensory_ai.py` | `content` | `assignment_secret` | `511` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\NOMBRE02.txt` | `content` | `assignment_secret` | `3247` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\NOMBRE02.txt` | `content` | `assignment_secret` | `3695` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Perfect — incluyo también un `env.e.txt` | `content` | `assignment_secret` | `1368` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Sí, es absolutamente posible y, de.txt` | `content` | `assignment_secret` | `1606` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\Sí, es absolutamente posible y, de.txt` | `content` | `assignment_secret` | `1708` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\The Solution deploy_overlord.shThis.txt` | `content` | `assignment_secret` | `87` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\vs vertex 2.txt` | `content` | `assignment_secret` | `301` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\bu\ython.txt` | `content` | `assignment_secret` | `3373` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\extra_psi_pre_final_v1_1\OTROS INSIGHTS DE OBSERVACIONISMO.txt` | `content` | `assignment_secret` | `387` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\extra_psi_pre_final_v1_1\OTROS INSIGHTS DE OBSERVACIONISMO.txt` | `content` | `assignment_secret` | `390` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\extra_psi_pre_final_v1_1\OTROS INSIGHTS DE OBSERVACIONISMO.txt` | `content` | `assignment_secret` | `413` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\extra_psi_pre_final_v1_1\OTROS INSIGHTS DE OBSERVACIONISMO.txt` | `content` | `assignment_secret` | `416` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\extra_psi_pre_final_v1_1\OTROS INSIGHTS DE OBSERVACIONISMO.txt` | `content` | `assignment_secret` | `425` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\extra_psi_pre_final_v1_1\OTROS INSIGHTS DE OBSERVACIONISMO.txt` | `content` | `assignment_secret` | `436` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\extra_psi_pre_final_v1_1\OTROS INSIGHTS DE OBSERVACIONISMO.txt` | `content` | `assignment_secret` | `439` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\futuro\security\secrets_scan.py` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\GEODIA\_github_staging\safe-exec\safe-exec\examples\example_openai.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\archive\_MANIFIESTOS\ORDEN_MINIMO_CANON.md` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.env` | `path_name` | `env_file` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.env` | `content` | `assignment_secret` | `23` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.env.example` | `path_name` | `env_file` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.env.gumroad` | `path_name` | `env_file` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.env.gumroad` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.env.mova.example` | `path_name` | `env_file` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_secrets.json` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_secrets.json` | `content` | `openai_like_key` | `5` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_secrets.json` | `content` | `github_like_token` | `7` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_tv_token.json` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\generate_gumroad_covers.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\gumroad_api.json` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\gumroad_products.json` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\gumroad_verificar.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\gumroad_verificar.py` | `content` | `assignment_secret` | `68` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\publish_gumroad_6plus1.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\setup_gumroad.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\update_gumroad_listings.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\WORKFLOW.symphony.md` | `content` | `assignment_secret` | `4` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\youtube_descriptions.json` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.agents\skills\claudio-gumroad\SKILL.md` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\api\integration_3t.py` | `content` | `assignment_secret` | `93` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\api\integration_3t.py` | `content` | `assignment_secret` | `134` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\api\integration_3t.py` | `content` | `assignment_secret` | `155` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\llms.txt` | `content` | `assignment_secret` | `27` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\medioevo-auth.js` | `content` | `assignment_secret` | `647` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\medioevo-auth.js` | `content` | `assignment_secret` | `708` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\medioevo-auth.js` | `content` | `assignment_secret` | `734` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\medioevo.bundle.js` | `content` | `assignment_secret` | `1896` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\medioevo.bundle.js` | `content` | `assignment_secret` | `1957` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\medioevo.bundle.js` | `content` | `assignment_secret` | `1983` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\medioevo.bundle.js` | `content` | `assignment_secret` | `32304` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\public.js` | `content` | `assignment_secret` | `315` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\stripe-store.js` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\functions\api\gumroad\webhook.js` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\img\maps\map_plano_astral_archivo_onirico_secreto.jpg` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\img\maps\map_plano_astral_archivo_onirico_secreto.webp` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\editorial_web\website-assets\public.js` | `content` | `assignment_secret` | `260` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\animacion\cycles.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\animacion\easing.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\animacion\pose.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\animacion\timing.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\animacion\__init__.py` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\core\style_tokens.py` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\core\style_tokens.py` | `content` | `assignment_secret` | `127` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\arte\core\style_tokens.py` | `content` | `assignment_secret` | `153` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\autopilot\.env` | `path_name` | `env_file` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\autopilot\.env.example` | `path_name` | `env_file` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\autopilot\CONFIGURACION_COMPLETADA_20260411.md` | `content` | `assignment_secret` | `19` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\beta\discord_message.txt` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\bomberos\runbooks\secret_leak.md` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\brain_os\beta\DISCORD_MESSAGE.md` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\Claudio_Accesos_Directos\12_Gumroad_Check.bat` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_os\wizard\steps.py` | `content` | `assignment_secret` | `148` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_os\wizard\steps.py` | `content` | `assignment_secret` | `160` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\docs\MEDIOEVO_AI_CONTEXT_GATEWAY.md` | `content` | `assignment_secret` | `22` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\lab_offensive\data\wordlists\default_passwords.txt` | `path_name` | `secret_name` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\scripts\fetch_medioevo_ai_context.py` | `content` | `assignment_secret` | `31` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\ads_trackers_audit.py` | `content` | `assignment_secret` | `106` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\ads_trackers_audit.py` | `content` | `assignment_secret` | `162` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\ads_trackers_audit.py` | `content` | `assignment_secret` | `248` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\ads_trackers_audit.py` | `content` | `assignment_secret` | `261` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\controller.py` | `content` | `assignment_secret` | `202` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\controller.py` | `content` | `assignment_secret` | `203` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\controller.py` | `content` | `assignment_secret` | `404` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\codex\src\local_ollama_desktop\controller.py` | `content` | `assignment_secret` | `405` | `REDACTED_MATCH` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\commercial\GUMROAD_PRODUCTS_READY.md` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |
| `ROOT_WORKSPACE` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\commercial\gumroad_upload_ready.md` | `path_name` | `payment_or_provider` | `0` | `REDACTED_PATH_VALUE` |

## Bloqueo

Si `Hallazgos reportados > 0`, no publicar, no hacer push y no desplegar desde las rutas escaneadas. Revisar por allowlist de target, no por glob amplio.
