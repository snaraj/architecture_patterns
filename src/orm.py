from sqlalchemy import Column, Table, String, Integer
from sqlalchemy.orm import registry

import model  # The ORM imports the domain model, not the other way around.

mapper_registry = (
    registry()
)  # Serves as the basis for maintaining a collection of mappings, and provides configurational hooks used to map classes.

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(225)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(225)),
)

mapper_registry.map_imperatively(model.OrderLine, order_lines)
