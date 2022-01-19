from src.model import Batch, OrderLine
from datetime import date

# abstraction so that we do not have to repeat these lines
def make_batch_and_line(sku: str, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine(orderid="order-ref", sku=sku, qty=line_qty),
    )


# test that allocate function works properly, updating the avaliable_quantity attribute
def test_allocating_to_a_batch_reduces_the_avaliable_quantity():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    batch.allocate(line)

    assert batch.avaliable_quantity == 18


def test_can_allocate_if_avaliable_greater_than_required():
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)

    assert large_batch.can_allocate(small_line)


def test_can_allocate_if_avaliable_less_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)

    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_avaliable_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 20, 20)

    assert batch.can_allocate(line)


def test_can_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "NIGHT LAMP", 100, eta=None)
    different_sku_line = OrderLine(orderid="order-123", sku="DAY LAMP", qty=10)

    assert batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_line():
    batch, unallocated_line = make_batch_and_line("NIGHT-LAMP", 20, 2)
    batch.deallocate(unallocated_line)

    assert batch.avaliable_quantity == 20


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)

    assert batch.avaliable_quantity == 18
