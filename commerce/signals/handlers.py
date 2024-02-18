from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from commerce.models import Order, OrderItem, SellerWallet
from commerce.signals import order_delivered, seller_confirmed
from community.models import Seller


@receiver(post_save, sender=Seller)
def create_seller_wallet_for_new_seller(sender, **kwargs):
    if kwargs["created"]:
        seller = kwargs["instance"]
        SellerWallet.objects.create(seller=seller)


@receiver(order_delivered, sender=Order)
def transfer_money_to_seller_wallet(sender, **kwargs):
    with transaction.atomic():
        order = kwargs["order"]
        if order.money_transferred:
            return

        order_items = OrderItem.objects.filter(order_id=order.id).select_related(
            "book_item__seller"
        )

        for item in order_items:
            seller = item.book_item.seller
            seller_wallet = SellerWallet.objects.get(seller=seller)
            total_price = item.quantity * item.unit_price
            seller_wallet.total_earned += total_price
            seller_wallet.balance += total_price
            seller_wallet.save()

        order.money_transferred = True
        order.save()


@receiver(seller_confirmed, sender=Order)
def order_is_being_confirmed(sender, **kwargs):
    with transaction.atomic():
        order = kwargs["order"]
        order_items = OrderItem.objects.filter(order_id=order.id)

        for item in order_items:
            if item.confirmed_by_seller == False:
                return

        order.order_status = "C"
        order.save()
