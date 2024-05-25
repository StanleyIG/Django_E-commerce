from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View, RedirectView
from basketapp.models import BasketItem
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe


@login_required
def index(request):
    # basket_items = BasketItem.objects.filter(user=request.user)
    # basket_items = request.user.basketitem_set.filter()  # SELECT * FROM basket WHERE price_gt=2000
    # basket_items = request.user.basketitem_set.all()  # SELECT * FROM basket
    basket_items = request.user.user_basket.all()  # SELECT * FROM basket
    context = {
        'page_title': 'корзина',
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
    # basket = BasketItem.objects.filter(user=request.user, product=product).first()
    basket = request.user.user_basket.filter(product=pk).first()

    if not basket:
        basket = BasketItem(user=request.user, product=product)  # not in db

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, pk):
    get_object_or_404(BasketItem, pk=pk).delete()
    return HttpResponseRedirect(reverse('basket:index'))

    