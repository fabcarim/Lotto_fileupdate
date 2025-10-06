from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    supplier = Column(String, nullable=True)
    device_type = Column(String, nullable=True)
    ref_code = Column(String, nullable=False, index=True)
    carrier = Column(String, nullable=True)
    qty = Column(Integer, nullable=True)
    pickup_date = Column(String, nullable=True)
    ship_date = Column(String, nullable=True)
    eta = Column(String, nullable=True)
    final_destination = Column(String, nullable=True)
    status = Column(String, nullable=True)
    last_event = Column(String, nullable=True)
    last_location = Column(String, nullable=True)
    last_update = Column(String, nullable=True)
    order_code = Column(String, nullable=True)
    customer = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    pieces = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    last_source = Column(String, nullable=True)
