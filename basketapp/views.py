from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from basketapp.models import BasketItem
from mainapp.models import Product


def index(request):
    pass


def add(request, pk):
    # print(pk, type(pk))
    product = get_object_or_404(Product, pk=pk)
    basket = BasketItem.objects.filter(user=request.user, product=product).first()
    # basket = request.user.basketitem_set.filter(product=pk).first()

    if not basket:
        basket = BasketItem(user=request.user, product=product)  # not in db

    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
