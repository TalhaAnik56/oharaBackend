from django.db import transaction
from django.dispatch import receiver

from commerce.models import Order, OrderItem, SellingHistory
from commerce.signals import order_delivered


@receiver(order_delivered, sender=Order)
def transfer_records_to_selling_history(sender, **kwargs):
    with transaction.atomic():
        order = kwargs["order"]
        order_items = OrderItem.objects.filter(order_id=order.id).select_related(
            "book_item__seller"
        )
        selling_history_objects = [
            SellingHistory(
                order=order,
                book_item=item.book_item,
                seller=item.book_item.seller,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in order_items
        ]

        SellingHistory.objects.bulk_create(selling_history_objects)
