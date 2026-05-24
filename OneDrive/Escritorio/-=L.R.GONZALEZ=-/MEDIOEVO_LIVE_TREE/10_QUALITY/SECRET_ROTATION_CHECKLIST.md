# SECRET_ROTATION_CHECKLIST

Usar solo si se confirma que un hallazgo corresponde a secreto real.

1. Identificar proveedor sin imprimir el valor.
2. Revocar o rotar credencial desde el panel del proveedor.
3. Confirmar que el archivo queda fuera de Git, ZIPs y paquetes.
4. Reemplazar por ejemplo seguro si el proyecto necesita plantilla.
5. Reejecutar `tools/secret_scan.py`.
6. Registrar evidencia en `07_TRACE/WITNESSLOG.jsonl`.

No borrar archivos fuente en esta corrida.
