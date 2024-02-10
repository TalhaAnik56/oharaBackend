from django.db import transaction
from django.dispatch import receiver

from commerce.models import Order, OrderItem, SellerWallet
from commerce.signals import order_delivered


@receiver(order_delivered, sender=Order)
def transfer_money_to_seller_wallet(sender, **kwargs):
    with transaction.atomic():
        order = kwargs["order"]
        order_items = OrderItem.objects.filter(order_id=order.id).select_related(
            "book_item__seller"
        )

        for item in order_items:
            seller = item.book_item.seller
            seller_wallet = SellerWallet.objects.get_or_create(seller=seller)
            total_price = item.quantity * item.unit_price
            seller_wallet.total_earned += total_price
            seller_wallet.balance += total_price
            seller_wallet.save()

        order.money_transferred = True
        order.save()
