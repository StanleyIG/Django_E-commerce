from django.urls import path
import ordersapp.views as ordersapp
from ordersapp.apps import OrdersappConfig


app_name = OrdersappConfig.name

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='index'),
    path('create/', ordersapp.OrderCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', ordersapp.OrderDetail.as_view(), name='order_read'),
    path('update/<int:pk>/', ordersapp.OrderUpdate.as_view(), name='order_update'),
]
