from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from .models import Order, OrderItem, Product
from django.views.generic.detail import DetailView
from django.db import transaction
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from mainapp.models import ProductCategory
from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem
from authapp_custom.models import CustomUser
from django.db.models import Prefetch


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        basket_items = self.request.user.user_basket.all()
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=len(basket_items) 
            if basket_items and len(basket_items) else 1
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            formset = OrderFormSet()
            # for num, form in enumerate(formset.forms):
            # zip(), filter(), map()
            for form, basket_item in zip(formset.forms, basket_items):
                form.initial['product'] = basket_item.product
                form.initial['quantity'] = basket_item.quantity
                form.initial['price'] = basket_item.product.price


        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            # form.instance это сама модель Order
            form.instance.user = self.request.user
            self.object = form.save()  # Order object
            if orderitems.is_valid():
                orderitems.instance = self.object  # one to many
                orderitems.save()
                # orderitems.save(view='order_create')
            # Очень важно !!!
            # В данном коде метод delete() не метод класса Model! Он принадлежит QuerySet'у, который возвращает метод all().
            self.request.user.user_basket.all().delete()  # применяется к QuerySet

        # удаляем пустой заказ
        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    # def get_queryset(self):
    #      return Order.objects.prefetch_related(
    #      Prefetch('orderitems',
    #               queryset=OrderItem.objects.select_related('product', 'product__category'))
    #  ).filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )

        if self.request.POST:
            formset = OrderFormSet(
                self.request.POST, self.request.FILES,
                instance=self.object
            )
        else:
            # formset = OrderFormSet(instance=self.object)
            # order_items = self.object.orderitems.prefetch_related(Prefetch('product__category'))
            order_items = self.object.orderitems.select_related('product', 'product__category')
            formset = OrderFormSet(
                instance=self.object,
                data=self.request.GET or None,
                queryset=order_items
            )
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляю пустой заказ
        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super().form_valid(form)


class OrderDetail(DetailView):
    model = Order

    # def get_object(self):
    #     print('get_object')
    #     return get_object_or_404(Order, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return Order.objects.prefetch_related(
            Prefetch('orderitems',
                     queryset=OrderItem.objects.select_related('product__category'))
        ).filter(pk=self.kwargs.get('pk'))
    # def get_queryset(self):
    #     return Order.objects.prefetch_related(
    #         Prefetch('orderitems',
    #                  queryset=OrderItem.objects.select_related('product').select_related('product__category'))
    #     ).filter(pk=self.kwargs.get('pk'))


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:index')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:index'))
