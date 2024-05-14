from django.shortcuts import render
from mainapp.models import ProductCategory, Product
from django.db import transaction
from django.utils import timezone


def index(request):
    context = {
        # 'page_title': 'главная',
        'error': None,
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    # ProductCategory.objects.create(name='Категория 1')
    # categories = ProductCategory.objects.all()
    # Product.objects.create(name='офисный стул', category_id=1) или Product.objects.create(name='стулья', category_id=categories) Можно передать ЭК категории
    # ленивые вычисления для объектов QurySet всего лишь создают
    # объект запроса, а сам запрос будет только при рендеринге страницы и отображении её в браузере.
    # Так-что даже если categories = ProductCategory.objects.all() был вызван раньше чем создание новых записей,
    # то фактический запрос будет в момент вызова при рендеринге запроса, и я увижу все актульные записи.
    products = Product.objects.all()
    # намеренно не дам совершится запросам
    # в базе ничего не сохранилось

    # но вместо ошибки отправился ответ в Json  сописанием ошибки, чтоб этот ответ мог обработать js скрипт например
    # with transaction.atomic():
    #     Product(name='Продукт 1', category_id=5).save()
    #     Product(name='Продукт 2', category_id=5).save()
    #     Product(name='Продукт 3').save()

    # тоже самое но без transaction.atomic()
    # Первые 2 до ошибки обязательно будут сохранены, что практически будет означать начало бед и мучений.
    # Product(name='Продукт 1', category_id=5).save()
    # Product(name='Продукт 2', category_id=5).save()
    # Product(name='Продукт 3').save()

    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql_psycopg2",
    #         "NAME": os.environ.get('POSTGRES_DB'),
    #         "USER": os.environ.get('POSTGRES_USER'),
    #         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    #         "HOST": "localhost",
    #         'PORT': '5432',
    #         'ATOMIC_REQUESTS': True,
    #     }
    # }
    # Так-же я могу определить настройки для тарнзакций глоьально 'ATOMIC_REQUESTS': True, и тогда 
    # не будет необходимости навешивать декоратор transaction.atomic() либо делать запросы
    # в контексте transaction.atomic() внутри самой вьюхи.
    # Тут ещё есть нюанс, что обрабатывать ошибки надо только в middleware и ни в коем
    # случае не в блоке try exept, иначе Django посчитает что раз ошибка обработана, тогда он сделает 
    # ряд запросов как есть минуя другие, и в итоге будет покарёжаная БД.

    context = {
        'page_title': 'каталог',
        'categories': products,
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


def error_redirect(request):

    context = {}
    return render(request, 'error_pages/page_500.html', context)
