<!--
Perfetto. 💪
Ecco un prompt **ottimizzato per GitHub Copilot Codex** (cioè per farlo capire a un’IA integrata in GitHub Codespaces o nel tuo editor GitHub.dev).
È scritto in **inglese tecnico chiaro**, con struttura e commenti che Copilot capisce subito.
Lo puoi incollare come **commento in cima al tuo file `README.md`**, oppure direttamente nella chat Codex per far generare tutto il progetto.

---

## 🧠 Prompt — “Lotto Tracking MVP” for GitHub Codex / Codespaces

````markdown
# 🚀 Build an MVP WebApp: "Lotto Tracking"

You are an AI developer assistant inside GitHub Codespaces.
Your task is to scaffold and implement a **minimal working web app** for a client called **“Lotto Tracking”**.

The goal: automatically update a 20-column Excel file every two days, merging data from  
1️⃣ an external **Tracking API**,  
2️⃣ two **Excel source files**,  
3️⃣ and one **email inbox (IMAP)** used by foreign correspondents.

---

## 🧩 Functional Requirements
- Read shipment data from API, Excel, and IMAP email messages.
- Identify shipments by `ref_code` (AWB/Container/PO).
- Merge records based on rules of priority:
  - `eta`, `status` → API > MAIL > EXCEL  
  - `cost` → EXCEL > API > MAIL  
  - `carrier` → MAIL > API > EXCEL
- Save unified data to a local database.
- Export to `Master.xlsx` (20 columns).
- Schedule auto-refresh every **2 days**.

---

## 🧱 Tech Stack
- **Backend:** Python 3.11 + FastAPI  
- **Database:** SQLite (for MVP)  
- **Scheduler:** APScheduler (interval = 2 days)  
- **Excel IO:** pandas + openpyxl  
- **Email Parser:** imapclient + regex  
- **HTTP Client:** httpx  
- **Frontend:** simple HTML + Vanilla JS (or minimal React)
- **Auth:** single Bearer token from `.env`
- **Packaging:** Dockerfile + docker-compose.yml for local run

---

## 🧮 Data Model (`shipments`)
| Field | Type | Note |
|-------|------|------|
| id | int | primary key |
| supplier | str | vendor name |
| device_type | str | product type |
| ref_code | str | AWB/Container/PO |
| carrier | str | shipping company |
| qty | int | quantity |
| pickup_date | str | |
| ship_date | str | |
| eta | str | estimated arrival |
| final_destination | str | |
| status | str | tracking status |
| last_event | str | |
| last_location | str | |
| last_update | str | |
| order_code | str | PO |
| customer | str | |
| weight | float | |
| volume | float | |
| pieces | int | |
| cost | float | |
| notes | str | |
| last_source | str | “API” / “MAIL” / “EXCEL” |

---

## 🧮 Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/refresh` | Force full update from all sources *(requires Bearer token)* |
| `GET` | `/shipments` | List latest shipments (limit 100, optional filters) |
| `GET` | `/export` | Download current Master.xlsx |
| `POST` | `/excel/upload` | Upload one Excel source file |
| `POST` | `/sources/test` | Quick connectivity check (API / IMAP / files) |

---

## 🧩 Project Structure to Generate
````

lotto_webapp/
├─ backend/
│  ├─ app/
│  │  ├─ main.py              # FastAPI entrypoint + scheduler
│  │  ├─ models.py            # SQLAlchemy Shipment model
│  │  ├─ schemas.py           # Pydantic models
│  │  ├─ tracker_client.py    # Fetch data from tracking API
│  │  ├─ excel_importer.py    # Load Excel source1 + source2
│  │  ├─ email_parser.py      # Read IMAP inbox, extract AWB/container/ETA
│  │  ├─ merger.py            # Apply merge/priority rules
│  │  ├─ exporter.py          # Export to Master.xlsx
│  │  ├─ auth.py              # Simple Bearer-token guard
│  │  ├─ crud.py              # DB operations
│  │  ├─ settings.py          # env-config
│  │  ├─ database.py
│  ├─ requirements.txt
├─ frontend/
│  └─ index.html              # Minimal UI (token, refresh, table, export)
├─ storage/uploads/
├─ storage/exports/
├─ .env.example
├─ Dockerfile
├─ docker-compose.yml
├─ README.md

````

---

## ⚙️ Expected Behaviour
- Running  
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000
````

starts the FastAPI backend.

* Opening `http://localhost:8000` shows the small web UI.
* Clicking **“Refresh now”** calls `/refresh` and merges new data.
* Clicking **“Download Excel”** returns the latest `Master.xlsx`.
* The scheduler refreshes automatically every 2 days.

---

## 🧠 Hints for Codex

* Use `pydantic_settings` for `.env` loading.
* Use APScheduler BackgroundScheduler for interval job.
* Parse emails with `imapclient`, regex for AWB (11–14 digits) & container (4 letters + 7 digits).
* Use pandas → DataFrame → to_excel for export.
* Keep everything inside `backend/app`.
* Provide a simple `requirements.txt` listing all dependencies.
* Add `README.md` with basic setup instructions.
* Output working code; don’t just describe it.

---

**Goal:** generate a *working minimal product* that runs entirely inside a GitHub Codespace using `uvicorn`.
Keep it clean, self-contained, and easy to extend later.

````

---

👉 **Come usarlo**
1. Apri GitHub → crea un nuovo repository (es. `lotto_webapp`).  
2. Apri un **Codespace** su quel repo.  
3. Incolla questo prompt come **commento nel README** o direttamente nella chat di Codex.  
4. Aspetta che generi i file, poi lancia:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
````

5. Apri il link del Codespace (`https://…github.dev`) → vedrai la webapp funzionante.

---

Vuoi che ti faccia anche una **versione più “guidata” del prompt** (cioè passo-passo, per far sì che Codex generi i file uno alla volta in sequenza)? Posso scriverla se vuoi costruirla in più step.
-->
# Lotto Tracking MVP

A minimal FastAPI + SQLite solution that consolidates shipment information from API, Excel, and IMAP inputs and exports a two-day refreshed `Master.xlsx` workbook.

## Project Structure

```
backend/
  app/
    main.py           # FastAPI application with scheduler and endpoints
    models.py         # SQLAlchemy ORM models
    schemas.py        # Pydantic models used by the API
    tracker_client.py # Async HTTP client for external tracking API
    excel_importer.py # Excel ingestion helpers (pandas + openpyxl)
    email_parser.py   # IMAP ingestion and AWB/container parsing
    merger.py         # Merge logic honoring business priorities
    exporter.py       # Pandas Excel export pipeline
    auth.py           # Bearer token dependency
    crud.py           # Database helpers
    settings.py       # Environment configuration loader
    database.py       # SQLAlchemy engine/session factory
  requirements.txt
frontend/
  index.html          # Lightweight control panel
storage/
  uploads/            # Drop Excel files here to ingest
  exports/            # Latest Master.xlsx export
Dockerfile
docker-compose.yml
.env.example
README.md
```

## Getting Started

### 1. Local Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env  # set LOTTO_BEARER_TOKEN and optional integrations
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

* Visit `http://localhost:8000` for the interactive docs and minimal UI.
* Use the bearer token configured in `.env` for protected endpoints.

### 2. Docker

```bash
cp .env.example .env
docker compose up --build
```

### 3. Codespaces / GitHub.dev

1. Launch a Codespace.
2. `cp .env.example .env` and populate secrets (API, IMAP, etc.).
3. `pip install -r backend/requirements.txt`.
4. `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

## Core Endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| `POST` | `/refresh` | Merge data from all sources and update the database/export *(Bearer token required)* |
| `GET`  | `/shipments` | List consolidated shipments with optional filters (`ref_code`, `status`, `customer`) |
| `GET`  | `/export` | Download the latest `Master.xlsx` *(Bearer token required)* |
| `POST` | `/excel/upload` | Upload additional Excel data sources *(Bearer token required)* |
| `POST` | `/sources/test` | Check connectivity/configuration for API, IMAP, and Excel sources *(Bearer token required)* |

## Scheduler

APScheduler runs inside the FastAPI process and triggers a refresh job every `REFRESH_INTERVAL_DAYS` (default: 2). Manual calls to `/refresh` reuse the same job logic.

## Data Inputs

* **Tracking API** – Configure `API_BASE_URL` and optional `API_TOKEN` in `.env`.
* **Excel files** – Place static files in `storage/uploads/` or use `/excel/upload`.
* **Email inbox** – Provide `IMAP_HOST`, `IMAP_USERNAME`, `IMAP_PASSWORD`, and optional `IMAP_FOLDER`.

## Frontend

`frontend/index.html` offers a lightweight dashboard for triggering refreshes, downloading exports, and viewing the current dataset in a table.

## Testing the Stack Quickly

Without external integrations the `/refresh` endpoint seeds placeholder data so you can verify the full flow (database + export) immediately.
