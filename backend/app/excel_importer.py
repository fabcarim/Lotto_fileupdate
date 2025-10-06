from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import pandas as pd

from .schemas import ShipmentCreate
from .settings import settings


EXCEL_COLUMNS = [
    "supplier",
    "device_type",
    "ref_code",
    "carrier",
    "qty",
    "pickup_date",
    "ship_date",
    "eta",
    "final_destination",
    "status",
    "last_event",
    "last_location",
    "last_update",
    "order_code",
    "customer",
    "weight",
    "volume",
    "pieces",
    "cost",
    "notes",
]


def _load_excel_file(path: Path) -> List[ShipmentCreate]:
    if not path.exists():
        return []

    df = pd.read_excel(path)
    df = df[[col for col in EXCEL_COLUMNS if col in df.columns]]
    shipments = []
    for record in df.to_dict(orient="records"):
        ref_code = record.get("ref_code")
        if not ref_code or pd.isna(ref_code):
            continue
        shipments.append(ShipmentCreate(**record, last_source="EXCEL"))
    return shipments


def load_excel_sources() -> List[ShipmentCreate]:
    shipments: List[ShipmentCreate] = []
    sources: Iterable[Path] = [
        settings.excel_source_one,
        settings.excel_source_two,
    ]

    for source in sources:
        if isinstance(source, Path):
            shipments.extend(_load_excel_file(source))

    for file in settings.uploads_dir.glob("*.xlsx"):
        shipments.extend(_load_excel_file(file))

    return shipments
