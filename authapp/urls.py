from django.urls import path
from authapp import views
from authapp.apps import AuthappConfig

app_name =  AuthappConfig.name

urlpatterns = [
    path('', views.registration, name='registr'),
    path('login', views.login, name='login'),
]