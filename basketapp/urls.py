from django.urls import path, re_path
import basketapp.views as basketapp
from basketapp.apps import BasketappConfig


app_name = BasketappConfig.name

urlpatterns = [
    path('', basketapp.index, name='index'),
    path('add/product/<int:pk>/', basketapp.add, name='add'),
    path('delete/basket/item/<int:pk>/', basketapp.delete, name='delete'),
    # re_path(r'^add/product/(?P<pk>\d+)/$', basketapp.add, name='add'),
]
