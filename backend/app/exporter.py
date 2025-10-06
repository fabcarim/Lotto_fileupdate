from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, List

import pandas as pd
from pydantic import BaseModel

from .schemas import ShipmentCreate
from .settings import settings

EXPORT_FILENAME = "Master.xlsx"
EXPORT_COLUMNS = list(ShipmentCreate.model_fields.keys())


def export_shipments(shipments: Iterable[Any]) -> Path:
    rows: List[dict] = []
    for shipment in shipments:
        if isinstance(shipment, BaseModel):
            rows.append(shipment.model_dump())
        elif isinstance(shipment, dict):
            rows.append(shipment)
        elif hasattr(shipment, "__dict__"):
            rows.append({k: v for k, v in shipment.__dict__.items() if not k.startswith("_")})
        else:
            rows.append(dict(shipment))

    df = pd.DataFrame(rows)
    if df.empty:
        df = pd.DataFrame(columns=EXPORT_COLUMNS)
    else:
        missing = [column for column in EXPORT_COLUMNS if column not in df.columns]
        for column in missing:
            df[column] = None
        df = df[EXPORT_COLUMNS]

    export_path = settings.exports_dir / EXPORT_FILENAME
    df.to_excel(export_path, index=False)
    return export_path
