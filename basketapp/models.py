from django.contrib.auth import get_user_model
from django.db import models
from mainapp.models import Product
# from authapp_custom.models import CustomUser


class BasketItem(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)
