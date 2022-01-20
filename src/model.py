from datetime import date
from typing import Optional, Set, Any

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
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()  # NO REPEATED orderlines can be used.

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def avaliable_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    # an orderline can only be allocated if there is a corresponding batch with a matching SKU
    # and the avaliable_quantity being less than or equal to the quantity ordered.
    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.avaliable_quantity >= line.qty

    def __repr__(self) -> str:
        return f"{type(self).__name__}(reference={self.reference}, sku={self.sku}, eta={self.eta}, purchased_quantity={self._purchased_quantity}, allocated_quantity={self.allocated_quantity}, avaliable_quantity={self.avaliable_quantity})"

    # defines behavior for entity equality, we must explicit state the __eq__ and __hash__ methods.
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            return False
        # if they're both of the same instance, lets check if the references are the same.
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)
