# ⚠️ MIGRACIÓN EN PROGRESO - BRAIN_OS ABSORCIÓN 2026-05-31

**ESTADO: INICIALIZANDO FASE 1**

**Agente responsable:** Codex (Claude)
**Fecha inicio:** 2026-05-31
**Scope:** Migrar todo lo funcional de la ra a BRAIN_OS

---

## 🎯 OBJETIVO

BRAIN_OS absorve todos los sistemas, ideas y tecnologás que le enriquecen:
- **DUAT Genesis** (motor de simulación funcional) → 03_DUAT/
- **Wabi.sabi legacy** (extracto del motor modular) → 04_WABI_SABI/phoenix/
- **Apps comerciales** (Argus, flujocrm, etc.) → 04_APPS/
- **Runtime de Claudio** (núcleo IA) → 02_CLAUDIO/
- **Docs y teoría** → 01_CEREBRO/

---

## 📋 MAPEO ORIGEN → DESTINO

| Origen (Raíz) | Destino (BRAIN_OS) | Estado | Notas |
|---------------|---------------------------|--------|-------|
| `packages/open-dev/duat-genesis/` | `BRAIN_OS/03_DUAT/duat-genesis/` | ⏳ Pendiente | Tests OK, listo para migrar |
| `_archive/legacy/wabi-sabi-legacy-2026-05-31/` | `BRAIN_OS/04_WABI_SABI/phoenix/` | ⏳ Pendiente | Extraer motor modular |
| `apps/commercial/` | `BRAIN_OS/04_APPS/` | ⏳ Pendiente | Fusionar con existente |
| `runtime/` | `BRAIN_OS/02_CLAUDIO/` | ⏳ Pendiente | Revisar estructura |
| `docs/` | `BRAIN_OS/01_CEREBRO/docs/` | ⏳ Pendiente | Estructurar por dominio |
| `tools/` | `BRAIN_OS/02_CLAUDIO/tools/` | ⏳ Pendiente | Herramientas de desarrollo |

---

## 🚨 REGLAS PARA OTROS AGENTES

1. **NO BLOQUEAR** la raíz del proyecto por ahora (solo leer).
2. Si necesitas modificar algo en la raíz, **DOCUMENTARLO** en este archivo.
3. **TODAS** las nuevas features van a BRAIN_OS, no a la raíz.
4. Si ves algo en la raíz que no está mapeado aquí, **añadirlo** a este archivo.

---

## 🔄 ESTADO ACTUAL

- ✅ Fase 0: Auditora iniciada - Se encontraron:
  - `packages/open-dev/duat-genesis/` (FUNCIONAL, 16/16 tests pasan)
  - `_archive/legacy/wabi-sabi-legacy-2026-05-31/` (ARCHIVADO, 300+ archivos, 10,000KB+)
  - `apps/commercial/` (argus-desktop, asistente-negocio, flujocrm, mini-office)
  - `runtime/` (2.3GB, infraestructura de Claudio)
- ✅ Fase 1: Preparación del mapa de migración (EN PROGRESO)
- ⏳ Fase 2: Copia física de código funcional
- ⏳ Fase 3: Verificación de tests y referencias
- ⏳ Fase 4: Señalización completa

---

## 📝 NOTAS DE LA SESIÓN

**2026-05-31 14:30:** Inicio de planificación. Identificados 32 directorios en raíz.

---

**Última actualización:** 2026-05-31
**Próximo paso:** Iniciar copia física de packages/open-dev/duat-genesis/
