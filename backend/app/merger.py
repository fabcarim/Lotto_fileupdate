from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List

from .schemas import ShipmentCreate

PRIORITY = {
    "eta": ["API", "MAIL", "EXCEL"],
    "status": ["API", "MAIL", "EXCEL"],
    "cost": ["EXCEL", "API", "MAIL"],
    "carrier": ["MAIL", "API", "EXCEL"],
}


def merge_shipments(sources: Iterable[ShipmentCreate]) -> List[ShipmentCreate]:
    grouped: Dict[str, List[ShipmentCreate]] = defaultdict(list)
    for shipment in sources:
        grouped[shipment.ref_code].append(shipment)

    merged: List[ShipmentCreate] = []
    for ref_code, items in grouped.items():
        base = items[0].model_copy()
        base.last_source = items[0].last_source

        for item in items[1:]:
            base = _apply_priority(base, item)

        merged.append(base)

    return merged


def _apply_priority(current: ShipmentCreate, candidate: ShipmentCreate) -> ShipmentCreate:
    data = current.model_dump()
    candidate_data = candidate.model_dump()

    for field, value in candidate_data.items():
        if value in (None, ""):
            continue

        if field in PRIORITY:
            choice = _compare_priority(field, data.get(field), current.last_source, value, candidate.last_source)
            if choice == "candidate":
                data[field] = value
                data["last_source"] = candidate.last_source
        else:
            data[field] = value
            data["last_source"] = candidate.last_source

    return ShipmentCreate(**data)


def _compare_priority(field: str, current_value, current_source, candidate_value, candidate_source):
    if current_value in (None, ""):
        return "candidate"
    if candidate_value in (None, ""):
        return "current"

    order = PRIORITY.get(field, [])
    try:
        current_rank = order.index(current_source)
    except ValueError:
        current_rank = len(order)
    try:
        candidate_rank = order.index(candidate_source)
    except ValueError:
        candidate_rank = len(order)

    return "candidate" if candidate_rank < current_rank else "current"
