# 📊 ETL El Moro – Integración con PostgreSQL y Metabase

Automatización de extracción, procesamiento y visualización de datos operativos del sistema Zetus (El Moro).

---

## 🚀 Descripción

Este proyecto convierte un sistema web cerrado en una fuente de datos analíticos.

Permite:

- 🔐 Autenticarse automáticamente en Zetus
- 🌐 Consumir endpoints internos
- 🔄 Procesar datos del día
- 💾 Guardarlos en PostgreSQL
- 📊 Visualizarlos en Metabase

---

## 🧠 Arquitectura General

```mermaid
flowchart LR
    A[Sistema Zetus Web] --> B[Playwright Login]
    B --> C[Sesión Guardada]
    C --> D[Requests API]
    D --> E[Procesamiento Pandas]
    E --> F[PostgreSQL]
    F --> G[Metabase]
