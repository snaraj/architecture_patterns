from sqlalchemy import Column, ForeignKey, Table, String, Integer, Date
from sqlalchemy.orm import registry, relationship

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

batches = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(225)),
    Column("sku", String(225)),
    Column("eta", Date, nullable=True),
    Column("_purchased_quantity", Integer, nullable=False),
)

allocations = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)

mapper_registry.map_imperatively(model.OrderLine, order_lines)
mapper_registry.map_imperatively(
    model.Batch,
    batches,
    properties={
        "_allocations": relationship(
            model.OrderLine,
            secondary=allocations,
            collection_class=set,
        )
    },
)
