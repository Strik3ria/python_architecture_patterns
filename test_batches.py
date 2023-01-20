from models import Batch, OrderLine
from datetime import date


def create_line_and_batch(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-ref", sku, line_qty)
    )


def test_allocating_to_batch_reduces_available_quantity():
    batch, line = create_line_and_batch("ELEGANT_LAMP", 20, 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = create_line_and_batch("ELEGANT_LAMP", 20, 2)

    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = create_line_and_batch("ELEGANT_LAMP", 2, 20)

    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = create_line_and_batch("ELEGANT_LAMP", 10, 10)

    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "ELEGANT_LAMP", 100, eta=None)
    different_sku_line = OrderLine('order-123', "NOT_SO_ELEGANT_LAMP", 10)

    assert batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = create_line_and_batch("DECORATIVE_TRINKET", 20, 2)
    batch.deallocate(unallocated_line)

    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    batch, line = create_line_and_batch("ANGULAR_DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == 18