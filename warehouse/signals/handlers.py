from django.dispatch import receiver

from warehouse.models import BookItem
from warehouse.signals import stock_out


# For the time being,just print out to check that the signal is well received and working
@receiver(stock_out, sender=BookItem)
def action_for_stock_out(sender, **kwargs):
    book_item = kwargs["book_item"]
    print("I WANT YOU TO SEE THIS")
    print(book_item.book.title)
