import random
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator


locations = [
    {
        'city': 'Москва',
                'phone': '+7-888-888-8888',
                'email': 'info@shop.ru',
                'address': 'В пределах МКАД',
    },
    {
        'city': 'Санкт-Петербург',
                'phone': '+7-555-333-1111',
                'email': 'spb@shop.ru',
                'address': 'В пределах КАД',
    },
    {
        'city': 'Казань',
                'phone': '+7-853-777-7777',
                'email': 'mail@shop.ru',
                'address': 'Центр',
    }
]


def get_hot_product():
    products_id = Product.objects.values_list('id', flat=True)
    hot_product_id = random.choice(products_id)
    return Product.objects.get(pk=hot_product_id)


def related_products(product):
    return Product.objects.filter(category=product.category).exclude(id=product.id)


class MaininAppView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'главная'
        return context


class ProductListView(TemplateView):
    template_name = 'mainapp/products.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.hot_product = get_hot_product()
        self._related_products = related_products(self.hot_product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'каталог'
        context['hot_product'] = self.hot_product  # hot_product
        # _related_products
        context['related_products'] = self._related_products
        return context


class ProductDetailView(TemplateView):
    template_name = 'mainapp/product_page.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'продукт',
            'product': get_object_or_404(Product, pk=pk),
        })
        return context


class CatalogView(ListView):
    model = Product
    template_name = 'mainapp/catalog.html'
    paginate_by = 3

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        category_pk = self.kwargs.get('pk')
        if category_pk == 0:
            category = {'pk': 0, 'name': 'Все'}
            products = Product.objects.all().prefetch_related('category')
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            products = Product.objects.filter(
                category=category).prefetch_related('category')

        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'page_title': 'каталог',
            'category': category,
            'products': page_obj,
            'page_obj': page_obj,
        })

        return context


class ContactView(TemplateView):
    template_name = 'mainapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context.update({
            'page_title': 'контакты',
            'locations': locations,
        })
        return context


def product_price(request, pk):
    product = Product.objects.filter(pk=int(pk)).first()
    return JsonResponse({'price': product and product.price or 0})
