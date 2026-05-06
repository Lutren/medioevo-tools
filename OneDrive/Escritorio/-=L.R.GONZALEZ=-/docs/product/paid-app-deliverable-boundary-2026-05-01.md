# Paid App Deliverable Boundary

Fecha: 2026-05-01

Decision: `SOURCE_ZIP_INTERNAL_QA_ONLY`.

Los ZIPs bajo `releases\paid-apps` son artefactos locales de auditoria,
empaquetado y secret scan. No son, por defecto, el entregable para clientes.

## Regla Comercial

- Vender instaladores, apps empaquetadas, demos locales guiadas, soporte y
  documentacion de uso.
- No vender ni publicar codigo fuente comercial salvo contrato/tier explicito,
  licencia revisada y paquete separado.
- No incluir secretos, canon privado, RPG, lore no publicado, datos familiares
  ni repos internos en ningun entregable.
- No prometer seguridad garantizada, automatizacion total ni resultados
  medicos/financieros/laborales garantizados.

## FlujoCRM

Recomendacion operativa: `standalone first, bundle later`.

- Standalone: producto simple de entrada para validar demanda, soporte e
  instalacion.
- Pack Empresarial: bundle posterior con Asistente Negocio y plantillas cuando
  haya instaladores probados y legal final.
- El ZIP fuente local de FlujoCRM queda como evidencia interna, no como descarga
  publica.

## Entregables Permitidos Antes De Publicar

| Entregable | Publico | Condicion |
|---|---|---|
| Capturas/demo video | si | sin secretos, sin claims fuertes |
| Instalador `.exe`/`.dmg` | si | QA en maquina limpia, aviso unsigned o firma |
| Guia de instalacion | si | sin rutas privadas ni tokens |
| Source ZIP | no por defecto | solo contrato/licencia/tier revisado |
| Repo privado | no | nunca como beneficio general |

## Siguiente Paso

Generar instalador o ruta de instalacion real por app, probar en maquina limpia
y luego preparar listing public-safe.
