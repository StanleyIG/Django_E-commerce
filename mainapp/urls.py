from django.urls import path, re_path
from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('', views.MaininAppView.as_view(), name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('category/<int:pk>/products/', views.CatalogView.as_view(), name='catalog'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_page'),
    path('product/<int:pk>/price/', views.product_price),
]
