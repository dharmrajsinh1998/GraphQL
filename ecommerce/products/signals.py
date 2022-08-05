from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import Order


@receiver(m2m_changed, sender=Order.products.through)
def calculate_quantity_and_price(sender, action, instance, **kwargs):
    """
    - Calculating dynamicaaly product quy and price based
    on product and save to order model
    """
    if action in ["post_add", "post_remove"]:
        products = instance.products.aggregate(qty=Sum("qty"), price=Sum("price"))
        instance.total_price = products.get("price")
        instance.total_qty = products.get("qty")
        instance.save()
