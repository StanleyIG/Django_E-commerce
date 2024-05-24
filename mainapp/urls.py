from django.urls import path, re_path
from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('products/', views.products, name='products'),
#     path('contact/', views.contact, name='contact'),
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    # path('products/category/<int:pk>/', mainapp.products, name='catalog'),
    # path('category/<int:pk>/products/', mainapp.products, name='catalog'),
    # re_path(r'^category/(?P<pk>\d+)/products/$', views.catalog, name='catalog'),
    path('category/<int:pk>/products/', views.CatalogView.as_view(), name='catalog'),
    # path('contact/', views.contact, name='contact'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
