from django.dispatch import receiver

from commerce.models import Order, SellingHistory
from commerce.signals import order_delivered


@receiver(order_delivered, sender=Order)
def transfer_money_to_seller_account(sender, **kwargs):
    order = kwargs["order"]
    selling_history_objects = [
        SellingHistory(
            order=order,
            book_item=item.book_item,
            seller=item.book_item.seller,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        for item in order.orderitem_set.all()
    ]

    SellingHistory.objects.bulk_create(selling_history_objects)
