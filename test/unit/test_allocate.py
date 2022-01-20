import pytest

from src.model import Batch, OrderLine, allocate, OutOfStock
from datetime import datetime, timedelta


# OrderLine should give preference to Batch in stock over Batch that is not yet avaliable
def test_prefers_current_stock_batches_to_shipment():
    avaliable_batch = Batch("in-stock-batch", "NIGHT-LAMP", 20, None)
    shipment_batch = Batch("shipment-batch", "NIGHT-LAMP", 30, datetime.now() + timedelta(1))
    line = OrderLine(orderid="order-4B2A", sku="NIGHT-LAMP", qty=15)

    allocate(line, [avaliable_batch, shipment_batch])

    assert avaliable_batch.avaliable_quantity == 5
    assert shipment_batch.avaliable_quantity == 30


# When there is no avaliable stock immediately, allocate should prefer quickest avaliable incoming Batch
def test_prefers_earlier_batch():
    early_batch = Batch("early-batch", "NIGHT-LAMP", 50, datetime.now() + timedelta(1))
    medium_batch = Batch("medium-batch", "NIGHT-LAMP", 50, datetime.now() + timedelta(3))
    late_batch = Batch("late-batch", "NIGHT-LAMP", 50, datetime.now() + timedelta(8))

    line = OrderLine(orderid="order-42b1", sku="NIGHT-LAMP", qty=50)
    allocate(line, [early_batch, medium_batch, late_batch])

    assert early_batch.avaliable_quantity == 0
    assert medium_batch.avaliable_quantity == 50
    assert late_batch.avaliable_quantity == 50


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-ref", "POSTER", 100, None)
    shipment_batch = Batch("shipment-ref", "POSTER", 50, datetime.now() + timedelta(1))

    line = OrderLine(orderid="order-42b1", sku="POSTER", qty=50)
    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


# Handling out of stock test
def test_raise_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1", "SMALL-FORK", 10, datetime.now())
    allocate(OrderLine(orderid="order-1b4c", sku="SMALL-FORK", qty=10), [batch])

    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine(orderid="order2", sku="SMALL-FORK", qty=1), [batch])
