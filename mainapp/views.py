import random
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



class ProductListView(TemplateView):
    template_name = 'mainapp/products.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.hot_product = get_hot_product()
        self._related_products = related_products(self.hot_product)

    def get_context_data(self, **kwargs):
        # либо так
        # hot_product = get_hot_product()
        # _related_products = related_products(hot_product)
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'каталог'
        context['categories'] = get_menu()
        context['hot_product'] = self.hot_product # hot_product
        context['related_products'] = self._related_products # _related_products
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


# class CatalogView(TemplateView):
#     template_name = 'mainapp/catalog.html'

#     def get_context_data(self, pk=None, **kwargs):
#         context = super(CatalogView, self).get_context_data(**kwargs)
#         if pk == 0:
#             category = {'pk': 0, 'name': 'Все'}
#             products = Product.objects.all()
#         else:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             products = Product.objects.filter(category=category)
#         context.update({
#             'page_title': 'каталог',
#             'categories': get_menu(),
#             'category': category,
#             'products': products,
#         })

#         return context


class CatalogView(ListView):
    model = Product
    template_name = 'mainapp/catalog.html'
    paginate_by = 3

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        category_pk = self.kwargs.get('pk')
        if category_pk == 0:
            category = {'pk': 0, 'name': 'Все'}
            # products2 = ProductCategory.objects.prefetch_related('products') # Почему это запрос не работает не понятно, начиная с джанго 4.0
            # products2 = ProductCategory.objects.prefetch_related('product_set')
            # print(products2)
            products = Product.objects.all().prefetch_related('category')
        else:
            category = get_object_or_404(ProductCategory, pk=category_pk)
            # в шаблоне каталог я добавил тэг который выводит категорию в карточках товара
            # <p>{{ product.category.name }}</p>
            # products = Product.objects.filter(category=category)
            # в первом запросе я получу все продукты, но если обращаться к <p>{{ product.category.name }}</p>
            # то он дополнительно сделает ещё несколько запросов для каждого продукта чтобы получить наименование категории
            # SELECT "mainapp_productcategory"."id",
            #     "mainapp_productcategory"."name",
            #     "mainapp_productcategory"."description"
            # FROM "mainapp_productcategory"
            # WHERE "mainapp_productcategory"."id" = 1
            # LIMIT 21
            products = Product.objects.filter(category=category).prefetch_related('category')
            # если мне нужно дополнительно выводить информацию по категории продукта в карточках продукта, то можно сделать запрос через 
            # prefetch_related() чтобы загрузить список категорий и товаров в 2 запроса и не делать в дальнейшем доп запросы для категорий.
            # products2 = ProductCategory.objects.filter(pk=category_pk).prefetch_related('product_set')
            # В данном случае prefetch_related('category') предварительно загружает связанные объекты ProductCategory 
            # для всех объектов Product, отфильтрованных по category.
            # print(products2) # QuerySet категорий
            # print(products2[0].name) # категория <name>
            # print(products2[0].product_set.all()) # QuerySet продуктов. Все продукты из категории <name>


        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'page_title': 'каталог',
            'categories': get_menu(),
            'category': category,
            'products': page_obj,
            'page_obj': page_obj,
        })

        return context


# class CatalogView(ListView):
#     model = Product
#     template_name = 'mainapp/catalog.html'
#     paginate_by = 3

#     def get_context_data(self, *kwargs):
#         context = super().get_context_data(*kwargs)
#         category_pk = self.kwargs.get('pk')
#         if category_pk == 0:
#             category = {'pk': 0, 'name': 'Все'}
#             products = Product.objects.all()
#         else:
#             # category = get_object_or_404(ProductCategory, pk=category_pk)
#             category = get_object_or_404(ProductCategory, pk=category_pk)
#             products2 = ProductCategory.objects.filter(id=category_pk).prefetch_related('product')
#             print(products2)
#             products = Product.objects.filter(category=category)

#         paginator = Paginator(products, self.paginate_by)
#         page_number = self.request.GET.get('page', 1)
#         page_obj = paginator.get_page(page_number)

#         context.update({
#             'page_title': 'каталог',
#             'categories': get_menu(),
#             'category': category,
#             'products': page_obj,
#             'page_obj': page_obj,
#         })

#         return context


# class CatalogView(ListView):
#     model = Product
#     template_name = 'mainapp/catalog.html'
#     paginate_by = 2

#     def get_context_data(self, *kwargs):
#         context = super().get_context_data(*kwargs)
#         category_pk = self.kwargs.get('pk')
#         if category_pk == 0:
#             category = {'pk': 0, 'name': 'Все'}
#             products = Product.objects.all()
#         else:
#             category = get_object_or_404(ProductCategory, pk=category_pk)
#             products = Product.objects.filter(category=category)

#         paginator = Paginator(products, self.paginate_by)
#         page_number = self.request.GET.get('page', 1)
#         page_obj = paginator.get_page(page_number)
#         context.update({
#             'page_title': 'каталог',
#             'categories': get_menu(),
#             'category': category,
#             'products': page_obj,
#             'num_pages': paginator.num_pages,
#         })

#         return context



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
