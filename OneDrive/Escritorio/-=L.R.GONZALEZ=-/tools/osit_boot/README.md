# OSIT boot witness (servicio al inicio de Windows)

Honra el intent "OSIT desde el arranque" de forma **segura y reversible**: en cada inicio de
sesión muestrea señales baratas de salud del sistema, calcula el residuo R y el régimen
canónicos (obsai-core) y registra un veredicto de gate en un witness log encadenado por huella.

- **Fuente de verdad:** `packages/open-dev/obsai-core` (`estimate_residue_from_signals`,
  `estimate_regime`, `evaluate_action`, `stable_fingerprint`). Ver
  `obsai-core/docs/OSIT_CANON_REUSE_CONTRACT_2026-05-29.md`.
- **Read-only:** no cambia ajustes, no toca el BIOS/UEFI, no usa red; solo escribe su log.
- **Calibración:** DEMO_ONLY. Las señales son proxies de stdlib (disco libre, bloat de TEMP).

## Probar sin instalar nada (dry-run)

```powershell
python tools\osit_boot\osit_boot_witness.py --dry-run
python tools\osit_boot\osit_boot_witness.py --dry-run --signal contradiction --signal overload
```

`--dry-run` imprime la entrada y **no** escribe el log. Sin `--dry-run` agrega una línea JSONL a
`%USERPROFILE%\.medioevo\osit_boot\osit_boot_witness.jsonl` (cambia con `--log`).

## Instalar como tarea al inicio de sesión (lo ejecutas tú)

Es un **cambio de sistema**; no requiere admin. Decisión y ejecución tuyas:

```powershell
pwsh -File tools\osit_boot\register_osit_boot_task.ps1          # registrar (logon)
pwsh -File tools\osit_boot\unregister_osit_boot_task.ps1        # revertir
```

La tarea ejecuta `python osit_boot_witness.py` en cada logon (límite 5 min, `-AtLogOn`).
Si `python` no está en el PATH del logon, pásalo explícito:
`register_osit_boot_task.ps1 -Python "C:\ruta\python.exe"`.

## Formato del witness log (JSONL)

Cada línea: `{schema, timestampUtc, host, platform, signals, R, regime, gate, theta,
previousHash, calibration, fingerprint}`. `previousHash` encadena con la `fingerprint` de la
entrada anterior (tamper-evidence ligero). `gate` es el veredicto canónico de
`obsai_core.evaluate_action`.

## Límite de seguridad
No se reflashea el firmware/BIOS físico. La gobernanza "desde el arranque" se logra a nivel de
sesión de usuario (este servicio) y, para la capa firmware real, con el sandbox UEFI/QEMU de
`-= BRAIN_OS =-/osit_firmware` (ver su `build/README.md`).
