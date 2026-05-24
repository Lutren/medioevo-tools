# DUAT Lite

Local dashboard for reviewing claims through the OSIT Epistemic Engine.

## Run

```powershell
python tools\duat-lite\server.py --host 127.0.0.1 --port 8790
```

Open `http://127.0.0.1:8790/`.

## Gates

- Local only.
- `publication_gate=BLOCK`.
- No cloud/provider call.
- No source apply.
- No dependency install.

## Tests

```powershell
python -B -m pytest tools\duat-lite\tests -q -p no:cacheprovider
```
