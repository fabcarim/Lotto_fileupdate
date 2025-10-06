from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import httpx

from .schemas import ShipmentCreate
from .settings import settings


async def fetch_shipments_from_api() -> List[ShipmentCreate]:
    """Fetch shipment records from the external API.

    The function gracefully handles a missing configuration by returning an
    empty list so the MVP can run without external dependencies.
    """
    if not settings.api_base_url:
        return []

    headers = {}
    if settings.api_token:
        headers["Authorization"] = f"Bearer {settings.api_token}"

    try:
        async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
            response = await client.get("/shipments", headers=headers)
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPError:
        return []

    shipments: List[ShipmentCreate] = []
    for record in payload:
        shipments.append(ShipmentCreate(**record, last_source="API"))
    return shipments


def build_placeholder_api_payload() -> List[Dict[str, Any]]:
    now = datetime.utcnow().strftime("%Y-%m-%d")
    return [
        {
            "supplier": "Demo Supplier",
            "device_type": "Accessory",
            "ref_code": "API-DEMO-001",
            "carrier": "API Logistics",
            "qty": 100,
            "pickup_date": now,
            "ship_date": now,
            "eta": now,
            "status": "In transit",
            "last_event": "Departed origin",
            "last_location": "Warehouse 1",
            "last_update": now,
            "order_code": "PO-API-001",
            "customer": "Demo Customer",
            "weight": 25.5,
            "volume": 1.2,
            "pieces": 10,
            "cost": 1200.0,
            "notes": "Generated from placeholder data.",
        }
    ]
