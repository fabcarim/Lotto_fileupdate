from __future__ import annotations

import re
from typing import List

from imapclient import IMAPClient

from .schemas import ShipmentCreate
from .settings import settings

AWB_REGEX = re.compile(r"\b\d{11,14}\b")
CONTAINER_REGEX = re.compile(r"\b[A-Z]{4}\d{7}\b")


def _connect_client() -> IMAPClient:
    client = IMAPClient(settings.imap_host)
    client.login(settings.imap_username, settings.imap_password)
    client.select_folder(settings.imap_folder)
    return client


def fetch_shipments_from_email() -> List[ShipmentCreate]:
    if not (settings.imap_host and settings.imap_username and settings.imap_password):
        return []

    shipments: List[ShipmentCreate] = []
    try:
        client = _connect_client()
    except Exception:
        return []

    try:
        messages = client.search("UNSEEN")
        for msg_id in messages:
            response = client.fetch(msg_id, ["BODY[TEXT]"])
            body = response[msg_id][b"BODY[TEXT]"]
            text = body.decode("utf-8", errors="ignore")

            ref_code = _extract_reference(text)
            shipments.append(
                ShipmentCreate(
                    ref_code=ref_code,
                    status="Email update",
                    notes=text[:500],
                    last_source="MAIL",
                )
            )
    finally:
        try:
            client.logout()
        except Exception:
            pass

    return shipments


def _extract_reference(text: str) -> str:
    match = AWB_REGEX.search(text) or CONTAINER_REGEX.search(text)
    return match.group(0) if match else "EMAIL-UNKNOWN"
