from datetime import date
from typing import Optional

from pydantic import BaseModel


class OrderLine(BaseModel):
    orderid: str
    sku: str
    qty: int

    class Config:
        frozen = True  # instances of OrderLine will be Immutable


class Batch:
    def __init__(self, reference: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.reference = reference
        self.sku = sku
        self.avaliable_quantity = qty
        self.eta = eta

    def allocate(self, line: OrderLine) -> None:
        self.avaliable_quantity -= line.qty
