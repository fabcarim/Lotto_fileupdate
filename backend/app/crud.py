from collections.abc import Iterable
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Shipment
from .schemas import ShipmentCreate


def upsert_shipments(db: Session, shipments: Iterable[ShipmentCreate]) -> int:
    processed = 0
    for shipment_data in shipments:
        existing = db.execute(
            select(Shipment).where(Shipment.ref_code == shipment_data.ref_code)
        ).scalar_one_or_none()

        if existing:
            for field, value in shipment_data.model_dump(exclude_unset=True).items():
                setattr(existing, field, value)
        else:
            db.add(Shipment(**shipment_data.model_dump()))
        processed += 1

    db.commit()
    return processed


def list_shipments(
    db: Session,
    limit: int = 100,
    ref_code: Optional[str] = None,
    status: Optional[str] = None,
    customer: Optional[str] = None,
):
    query = select(Shipment)

    if ref_code:
        query = query.where(Shipment.ref_code.ilike(f"%{ref_code}%"))
    if status:
        query = query.where(Shipment.status.ilike(f"%{status}%"))
    if customer:
        query = query.where(Shipment.customer.ilike(f"%{customer}%"))

    query = query.limit(limit)

    return db.execute(query).scalars().all()


def get_shipments_by_ref(db: Session, ref_codes: Iterable[str]):
    query = select(Shipment).where(Shipment.ref_code.in_(list(ref_codes)))
    return db.execute(query).scalars().all()
