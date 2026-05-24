# DUAT Windows App QA v1.4

Fingerprint: DUAT-v1.4-WINAPP-CONVERSION

Status:
- executable: dist/winapp/DUATCity.exe
- wrapper: native_dotnet_edge_app_mode
- preferred wrappers: electron, tauri
- smoke status: PASS
- server URL: http://127.0.0.1:18641/duat-city/?nativeWin=1
- HTTP status: 200
- JS asset status: 200
- root present: true

Boundary:
- publication_allowed=false
- wabi_execution_allowed=false
- cloud_used=false
- mcp_execution=false
- unknown_zip_code_executed=false

Notes:
- Serve-only smoke uses the native launcher static server without launching external cloud services.
- Electron/Tauri were not installed locally; this is the no-new-dependency Windows wrapper path.
