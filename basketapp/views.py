from unittest import loader
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View, RedirectView
from basketapp.models import BasketItem
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db import transaction


@login_required
def index(request):
    # basket_items = BasketItem.objects.filter(user=request.user)
    # basket_items = request.user.basketitem_set.filter()  # SELECT * FROM basket WHERE price_gt=2000
    # basket_items = request.user.basketitem_set.all()  # SELECT * FROM basket
    basket_items = request.user.user_basket.all()  # SELECT * FROM basket
    context = {
        'title': 'корзина',
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    # print(request.META.get('HTTP_REFERER'))
    # если пользователя нет в системе, то его редиректнет к странице входа.
    if 'auth' in request.META.get('HTTP_REFERER'):
        # print(request.META.get('HTTP_REFERER').split('/')[3])
        # После успешной авторизации редиректнет на страницу желаемого
        # товара и он сможет продолжить покупку именно этого товара.
        return HttpResponseRedirect(reverse('mainapp:product_page', args=[pk]))
    product = get_object_or_404(Product, pk=pk)
    quantity_product = product.quantity
    # basket = BasketItem.objects.filter(user=request.user, product=product).first()
    basket = request.user.user_basket.filter(product=pk).first()

    if not basket:
        basket = BasketItem(user=request.user, product=product)  # not in db
    
    # в setiings для DATABASES установлена глобальная настройка 'ATOMIC_REQUESTS': True, что означет 
    # использовать атомарные транзакции для всех контроллеров.
    # Тут я продемонтстрировал пример того как это работает.
    # Пользователь добавляет товар в корзину, в корзине quantity увеличивается, а в продуктах quantity уменьшается.
    # Я намеренно создал ошибку присвоив ключу связанной таблицы Category строкой значение product.category = 'hello'.
    # Это подняло ошибку, сработал ExceptionMiddleware и отренедерилась страничка с 500 кодом ошибки.
    # Без 'ATOMIC_REQUESTS': True, либо без дикоратора либо без менеджера контекста, несмотря на ошибку первый запрос на сохранение
    # basket.save() сработал бы, что привело бы к последующим ошибкам, конфликтам, расинхронизации и несостыковкам данных.
    # if basket.quantity < quantity_product:
        # цепочка запросов делается в одной тразакции, если будет ошибка в одном запросе, то откатятся все.
    if quantity_product:
        basket.quantity += 1
        product.quantity -= 1
        basket.save()
        # product.category = 'hello'
        product.save()
    else:
        product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, pk):
    get_object_or_404(BasketItem, pk=pk).delete()
    basket_items = BasketItem.objects.filter(user=request.user).order_by('add_datetime')
    context = {
        'basket_items': basket_items #request.user.user_basket.all(),
    }

    basket_items = render_to_string(
        'basketapp/inc/inc__basket_items.html',
        context=context,
        request=request,
    )

    return JsonResponse({
        'basket_items': basket_items,
        # 'basket_cost': request.user.basket_cost(),
        # 'basket_total_quantity': request.user.basket_total_quantity(),
    })
    #return HttpResponseRedirect(reverse('basket:index'))


def change(request, pk, quantity):
    basket_item = BasketItem.objects.filter(pk=pk).first()
    if quantity == 0:
        basket_item.delete()
    else:
        basket_item.quantity = quantity
        basket_item.save()
    
    basket_items = BasketItem.objects.filter(user=request.user).order_by('add_datetime')
    context = {
        'basket_items': basket_items #request.user.user_basket.all(),
    }

    basket_items = render_to_string(
        'basketapp/inc/inc__basket_items.html',
        context=context,
        request=request,
    )

    return JsonResponse({
        'basket_items': basket_items,
        # 'basket_cost': request.user.basket_cost(),
        # 'basket_total_quantity': request.user.basket_total_quantity(),
        # 'basket_item': basket_item,
    })
