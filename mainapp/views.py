from django.shortcuts import render

from mainapp.models import ProductCategory


def index(request):
    context = {
        # 'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    categories = ProductCategory.objects.all()

    context = {
        'page_title': 'каталог',
        'categories': categories,
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    # from json, from pickle, from db
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
