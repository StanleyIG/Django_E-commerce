from django.contrib.auth import get_user_model
from django.db import models
from mainapp.models import Product
# from authapp_custom.models import CustomUser


# class BasketQuerySet(models.QuerySet):
#     """
#     При срабатывании запроса на удаление корзины self.request.user.user_basket.all().delete()
#     в контроллере OrderCreate будет вызван переопределённый метод delete у QuerySet.
#     """
#     def delete(self):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete()


class BasketItem(models.Model):
    # objects = BasketQuerySet.as_manager()

    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_basket'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)

    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(using=None, keep_parents=False)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - \
    #             self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity

    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)

    @classmethod
    def get_item(cls, pk):
        return cls.objects.filter(pk=pk).first()
