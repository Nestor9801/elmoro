# 🍩 Elmoro ETL Pipeline

> Pipeline ETL para extracción automatizada de datos desde **EOS Zetus (Elmoro)** hacia **PostgreSQL**, utilizando autenticación vía navegador y consumo de endpoints privados.

---

## 🚀 Overview

Este proyecto permite:

* 🔐 Autenticarse automáticamente en la plataforma Elmoro
* 📡 Consumir endpoints internos protegidos
* 🔄 Transformar datos dinámicos
* 💾 Persistir información en PostgreSQL
* 🧾 Controlar ejecuciones con checkpoints

---

## 🏗️ Arquitectura

```mermaid
flowchart TD
    A[Playwright Login] --> B[Cookies / Session]
    B --> C[Requests API]
    C --> D[Transformación]
    D --> E[PostgreSQL]
    E --> F[Checkpoint]
```

---

## 📁 Estructura del Proyecto

```bash
.
├── main.py                  # Entry point
├── etl.py                   # Gestión de sesión
├── auth_playwright.py       # Login automatizado
├── api_requests.py          # Consumo API
├── fetch_with_playwright.py # Alternativa HTTP via Playwright
│
├── endpoints.py             # Configuración de endpoints
├── param_builders.py        # Generación de payloads
├── date_ranges.py           # Manejo de fechas
│
├── db.py                    # Persistencia (PostgreSQL)
├── preview.py               # Debug / validación de datos
│
├── config.py                # Configuración (⚠️ sensible)
└── playwright_state.json    # Sesión (⚠️ sensible)
```

---

## 🔐 Autenticación

El sistema usa **Playwright** para simular login real y obtener cookies de sesión.

* Detecta dinámicamente inputs de login
* Soporta múltiples layouts de formulario
* Guarda sesión reutilizable

📌 Resultado:

```json
playwright_state.json
```

---

## 🍪 Gestión de sesión

El flujo es resiliente:

1. Intenta usar cookies existentes
2. Si fallan → relogin automático
3. Reconstruye sesión `requests`

✔ Transparente para el usuario

---

## 📡 Consumo de datos

Se utilizan requests autenticados:

* Headers tipo navegador
* Cookies persistentes
* Autenticación básica adicional

📌 Soporta múltiples formatos de respuesta (`MSG`):

* Lista
* Diccionario por sucursal

---

## 🧠 Generación de payloads

Los parámetros se construyen dinámicamente:

* Multi-sucursal
* Rangos de fechas
* Filtros por tipo

Ejemplo:

```python
build_tabla_cuentas_payload_for_day(fecha)
```

---

## 📅 Manejo de fechas

Modos soportados:

| Modo       | Descripción         |
| ---------- | ------------------- |
| `daily`    | Día anterior        |
| `weekly`   | Últimos 7 días      |
| `biweekly` | Últimos 15 días     |
| `monthly`  | Mes actual          |
| `custom`   | Rango manual        |
| `catalogs` | Catálogos completos |

---

## 🔄 Pipeline ETL

### 1. Extract

* Requests autenticados
* Iteración por fechas

### 2. Transform

* Limpieza de valores inválidos
* Normalización de columnas

### 3. Load

* Inserción en PostgreSQL
* Upsert automático
* Refresh de catálogos

---

## 💾 Persistencia

Soporta múltiples estrategias:

| Modo              | Descripción         |
| ----------------- | ------------------- |
| `append_upsert`   | Inserta o actualiza |
| `catalog_refresh` | Borra y recarga     |
| `insert`          | Inserción simple    |

---

## 🧾 Control de ejecución (Checkpoint)

Se registra cada ejecución:

* `RUNNING`
* `SUCCESS`
* `FAILED`

✔ Evita reprocesos
✔ Permite auditoría
✔ Mejora confiabilidad

---

## 📊 Endpoints

### 🔹 Transaccionales

* Consumos

### 🔹 Catálogos

* Categorías
* Artículos
* Unidades de medida

---

## ▶️ Ejecución

### 🔹 Básico

```bash
python main.py --mode daily
```

### 🔹 Custom

```bash
python main.py \
  --mode custom \
  --fecha-inicio 2024/01/01 \
  --fecha-fin 2024/01/31
```

### 🔹 Catálogos

```bash
python main.py --mode catalogs
```

---

## 🧪 Debug y validación

Herramientas incluidas:

* Preview de DataFrame
* Tipos de datos
* Nulos
* Estructura

---

## ⚙️ Configuración

Archivo:

```
config.py
```

Incluye:

* URLs
* Credenciales API
* Configuración DB

---

## ⚠️ Seguridad

**NO subir al repositorio:**

* `config.py`
* `playwright_state.json`
* Credenciales
* Cookies

✔ Usa `.gitignore` correctamente

---

## 🧩 Flujo completo

```text
Login → Cookies → Session → API → Transform → DB → Checkpoint
```

---

## 📈 Roadmap

* [ ] Variables de entorno (`.env`)
* [ ] Logging estructurado
* [ ] Docker
* [ ] Tests automáticos
* [ ] Orquestación (Airflow / Prefect)

---

## 🧑‍💻 Autor

**Néstor Zavaleta**
Data / Automation

---

## ⭐ Notas

Este proyecto combina:

* Web scraping autenticado
* Reverse engineering de endpoints
* ETL incremental

Diseñado para escenarios donde no existe API pública oficial.

---
