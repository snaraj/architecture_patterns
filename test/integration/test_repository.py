from src.model import Batch, OrderLine
from src.repository import SqlAlchemyRepository


# Testing that the 'add' method from repository.py works correctly.
def test_repository_can_save_a_batch(session):
    batch = Batch("Batch-1", "NIGHT-LAMP", 100, eta=None)

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    # Use raw SQL to verify that the right data has been saved
    rows = list(session.execute('SELECT reference, sku, _purchased_quantity, eta FROM "BATCHES"'))

    assert rows == [("Batch-1", "NIGHT-LAMP", 100, None)]


# Testing the repository.get() function.
def insert_order_line(session):
    session.execute("INSERT INTO order_lines (orderid, sku, qty)" 'VALUES("order1", "GENERIC-SOFA", 12)')

    [[orderline_id]] = session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku", dict(orderid="order1", sku="GENERIC-SOFA")
    )

    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eat)" '   VALUES(:batch_id, "LONG-SOFA", 100, None',
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        "SELECT id FROM batches WHERE reference=:batch_id AND sku='LONG-SOFA'", dict(batch_id=batch_id)
    )

    return batch_id


def insert_allocation(session, orderline_id, batch1_id):
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)" "   VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch1_id=batch1_id),
    )


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, orderline_id, batch1_id)
    insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine("order1", "GENERIC-SOFA", 12),
    }
