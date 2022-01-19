from src.model import Batch, OrderLine
from datetime import date


def test_allocating_to_a_batch_reduces_the_avaliable_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine(orderid="order-ref", sku="SMALL-TABLE", qty=2)

    batch.allocate(line)

    assert batch.avaliable_quantity == 18
