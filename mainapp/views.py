import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from mainapp.models import ProductCategory, Product


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
        'city': 'Хабаровск',
                'phone': '+7-444-777-3333',
                'email': 'mail@shop.ru',
                'address': 'Центр',
    }
]


def get_hot_product():
    # products = Product.objects.all()
    products_id = Product.objects.values_list('id', flat=True)
    hot_product_id = random.choice(products_id)
    return Product.objects.get(pk=hot_product_id)


def related_products(product):
    return Product.objects.filter(category=product.category).exclude(id=product.id)


def get_menu():
    return ProductCategory.objects.all()


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    hot_product = get_hot_product()
    _related_products = related_products(hot_product)

    context = {
        'page_title': 'каталог',
        'categories': get_menu(),
        'hot_product': hot_product,
        'related_products': _related_products,
    }
    return render(request, 'mainapp/products.html', context)


class ProductListView(TemplateView):
    template_name = 'mainapp/products.html'

    def get_context_data(self, **kwargs):
        hot_product = get_hot_product()
        _related_products = related_products(hot_product)
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'каталог'
        context['categories'] = get_menu()
        context['hot_product'] = hot_product
        context['related_products'] = _related_products
        return context


class ProductDetailView(TemplateView):
    template_name = 'mainapp/product_page.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'продукт',
            'categories': get_menu(),
            'product': get_object_or_404(Product, pk=pk),
        })
        return context


# def product_page(request, pk):
#     context = {
#         'page_title': 'продукт',
#         'categories': get_menu(),
#         'product': get_object_or_404(Product, pk=pk),
#     }
#     return render(request, 'mainapp/product_page.html', context)

# def products(request):
#     context = {
#         'page_title': 'каталог',
#         'categories': get_menu(),
#     }
#     return render(request, 'mainapp/products.html', context)


# def catalog(request, pk):
#     if int(pk) == 0:
#         category = {'pk': 0, 'name': 'Все'}
#         products = Product.objects.all()
#     else:
#         category = get_object_or_404(ProductCategory, pk=pk)
#         products = Product.objects.filter(category=category)
#     context = {
#         'page_title': 'каталог',
#         'categories': get_menu(),
#         'category': category,
#         'products': products,
#     }
#     return render(request, 'mainapp/catalog.html', context)


class CatalogView(TemplateView):
    template_name = 'mainapp/catalog.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)
        if pk == 0:
            category = {'pk': 0, 'name': 'Все'}
            products = Product.objects.all()
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category=category)
        context.update({
            'page_title': 'каталог',
            'categories': get_menu(),
            'category': category,
            'products': products,
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


def contact(request):
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
            'city': 'Хабаровск',
            'phone': '+7-444-777-3333',
            'email': 'mail@shop.ru',
            'address': 'Центр',
        }
    ]

    context = {
        'page_title': 'контакты',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', context)
