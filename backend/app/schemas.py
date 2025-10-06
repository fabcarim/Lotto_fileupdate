from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ShipmentBase(BaseModel):
    supplier: Optional[str] = None
    device_type: Optional[str] = None
    ref_code: str
    carrier: Optional[str] = None
    qty: Optional[int] = None
    pickup_date: Optional[str] = None
    ship_date: Optional[str] = None
    eta: Optional[str] = None
    final_destination: Optional[str] = None
    status: Optional[str] = None
    last_event: Optional[str] = None
    last_location: Optional[str] = None
    last_update: Optional[str] = None
    order_code: Optional[str] = None
    customer: Optional[str] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    pieces: Optional[int] = None
    cost: Optional[float] = None
    notes: Optional[str] = None
    last_source: Optional[str] = None


class ShipmentCreate(ShipmentBase):
    pass


class Shipment(ShipmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RefreshResponse(BaseModel):
    refreshed_at: datetime
    records_processed: int
