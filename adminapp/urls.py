from django.urls import path
import adminapp.views as adminapp
from adminapp.apps import AdminappConfig


app_name = AdminappConfig.name

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('user/create/', adminapp.user_create, name='user_create'),
]
