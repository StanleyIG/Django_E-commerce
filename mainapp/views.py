from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def get_menu():
    return ProductCategory.objects.all()


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {
        'page_title': 'каталог',
        'categories': get_menu(),
    }
    return render(request, 'mainapp/products.html', context)


def catalog(request, pk):
    if int(pk) == 0:
        category = {'pk': 0, 'name': 'Все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(category=category)
    context = {
        'page_title': 'каталог',
        'categories': get_menu(),
        'category': category,
        'products': products,
    }
    return render(request, 'mainapp/catalog.html', context)


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