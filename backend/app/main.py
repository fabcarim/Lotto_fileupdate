from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from . import crud
from .auth import require_token
from .database import Base, SessionLocal, engine, get_db
from .email_parser import fetch_shipments_from_email
from .excel_importer import load_excel_sources
from .exporter import export_shipments
from .merger import merge_shipments
from .schemas import RefreshResponse, Shipment, ShipmentCreate
from .settings import settings
from .tracker_client import fetch_shipments_from_api, build_placeholder_api_payload

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = AsyncIOScheduler()
Base.metadata.create_all(bind=engine)
_lock = asyncio.Lock()


async def refresh_shipments() -> RefreshResponse:
    async with _lock:
        api_shipments = await fetch_shipments_from_api()
        email_shipments = fetch_shipments_from_email()
        excel_shipments = load_excel_sources()

        source_shipments: list[ShipmentCreate]
        if not any([api_shipments, email_shipments, excel_shipments]):
            placeholder_data = build_placeholder_api_payload()
            source_shipments = [
                ShipmentCreate(**record, last_source="API") for record in placeholder_data
            ]
        else:
            source_shipments = api_shipments + email_shipments + excel_shipments

        merged = merge_shipments(source_shipments)

        with SessionLocal() as db:
            processed = crud.upsert_shipments(db, merged)
            stored = crud.list_shipments(db, limit=1000)

        pydantic_shipments = [Shipment.model_validate(shipment) for shipment in stored]
        export_shipments(pydantic_shipments)

        return RefreshResponse(refreshed_at=datetime.utcnow(), records_processed=processed)


@app.on_event("startup")
def setup_scheduler():
    scheduler.add_job(
        lambda: asyncio.create_task(refresh_shipments()),
        "interval",
        days=settings.refresh_interval_days,
        id="shipment-refresh",
        replace_existing=True,
    )
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown(wait=False)


@app.post("/refresh", response_model=RefreshResponse)
async def refresh_endpoint(token: str = Depends(require_token)):
    return await refresh_shipments()


@app.get("/shipments", response_model=list[Shipment])
def list_shipments(
    limit: int = 100,
    ref_code: Optional[str] = None,
    status: Optional[str] = None,
    customer: Optional[str] = None,
    db: Session = Depends(get_db),
):
    shipments = crud.list_shipments(db, limit=limit, ref_code=ref_code, status=status, customer=customer)
    return [Shipment.model_validate(shipment) for shipment in shipments]


@app.get("/export")
def export_endpoint(token: str = Depends(require_token)):
    export_path = settings.exports_dir / "Master.xlsx"
    if not export_path.exists():
        raise HTTPException(status_code=404, detail="Export file not found")
    return FileResponse(export_path, filename="Master.xlsx")


@app.post("/excel/upload")
def upload_excel(file: UploadFile = File(...), token: str = Depends(require_token)):
    destination = settings.uploads_dir / Path(file.filename).name
    with destination.open("wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": destination.name}


@app.post("/sources/test")
def sources_test(token: str = Depends(require_token)):
    tests = {
        "api": bool(settings.api_base_url),
        "email": bool(settings.imap_host and settings.imap_username and settings.imap_password),
        "excel": any(settings.uploads_dir.glob("*.xlsx")),
    }
    return tests


@app.get("/")
def root():
    frontend_path = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
    if frontend_path.exists():
        return HTMLResponse(frontend_path.read_text(encoding="utf-8"))
    return {"message": "Lotto Tracking backend is running."}
