from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from basketapp.models import BasketItem
from ordersapp.models import OrderItem


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=BasketItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    print('pre_save', type(sender), sender, instance)
    if instance.pk:
        print('да')
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=BasketItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    print('pre_save', type(sender), sender, instance)
    instance.product.quantity += instance.quantity
    instance.product.save()