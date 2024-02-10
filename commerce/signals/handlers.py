from django.dispatch import receiver

from commerce.models import Order, SellingHistory
from commerce.signals import order_delivered


# aita arektu perfect korte hobe, like taka je seller er account e pouchaye dichi sheitar akta confirmation and akbarer beshi taka seller er account e dhukbe nah.
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
        for item in order.orderitem_set.all().select_related("book_item__seller")
    ]

    SellingHistory.objects.bulk_create(selling_history_objects)
