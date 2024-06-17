from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F, Max
from django.db.models.expressions import RawSQL

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'F'
    SENT_TO_PROCEED = 'S'
    PROCEEDED = 'P'
    PAID = 'D'
    READY = 'Y'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    @property
    def is_forming(self):
        return self.status == self.FORMING

    @property
    def total_quantity(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity, items)))

    # def get_product_type_quantity(self):
    #     items = self.orderitems.all()
    #     return len(items)

    # @property
    # def total_cost(self):
    #     items = self.orderitems.all()
    #     return sum(list(map(lambda x: x.quantity * x.product.price, items)))
    @property
    def total_cost(self):
        return self.orderitems.annotate(
            total_item_cost=F('quantity') * F('product__price')
        ).aggregate(total_cost=Sum('total_item_cost'))['total_cost']

    # переопределяем метод, удаляющий объект
    # def delete(self):
    #     for item in self.orderitems.select_related('order'):
    #         item.product.quantity += item.quantity
    #         item.product.save()

    #     self.is_active = False
    #     self.save()
    #     super(self.__class__, self).delete()

    # def delete(self):
    #     # Предзагрузка связанных продуктов и orderitem
    #     # select_related для orderitem, чтобы получить order,
    #     # prefetch_related для product, чтобы получить все productы
    #     order_items = self.orderitems.select_related(
    #         'order').prefetch_related('product')
    #     # print(order_items.query)
    #     # Обновление количества продуктов, связанных с элементами заказа
    #     for order_item in order_items:
    #         product = order_item.product  # Получение связанного продукта
    #         product.quantity += order_item.quantity  # Увеличение количества
    #         product.save()  # Сохранение обновленного продукта

    #     # Обновление статуса заказа
    #     self.is_active = False
    #     self.save()

    #     # Удаление заказа
    #     super(self.__class__, self).delete()


# class OrderItemQuerySet(models.QuerySet):

#     def delete(self, *args, **kwargs):
#         print('QerySet del сработал')
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super(OrderItemQuerySet, self).delete(*args,  **kwargs)


class OrderItem(models.Model):
    # objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - \
                self.__class__.get_item(self.pk).quantity
        else:
            print('else', self.quantity)
            if self.order.user.user_basket.exists():
                print('енсть корзина')
                pass
            else:
                self.product.quantity -= self.quantity

        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - \
    #             self.__class__.get_item(self.pk).quantity
    #     else:
    #         print('else', self.quantity)
    #         # Проверка get_item, если нет объекта заказа, то вычитаю 0, если есть, то получю атрибут quantity у заказа
    #         self.product.quantity -= 0 if self.__class__.get_item(self.pk) is None else self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - \
    #             self.__class__.get_item(self.pk).quantity
    #     else:
    #         if self.order.orderitems.exists():
    #             self.product.quantity -= self.quantity
    #         else:
    #             self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, *kwargs)

    # def delete(self, using=None, keep_parents=False):
    #     print('delete orderitem')
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(using=None, keep_parents=False)

    @classmethod
    def get_item(cls, pk):
        return cls.objects.filter(pk=pk).first()
