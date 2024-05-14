from django.urls import path
from authapp_custom import views
from authapp_custom.apps import AuthappCustomConfig

app_name =  AuthappCustomConfig.name

urlpatterns = [
    path("", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('done/,', views.RegisterDoneView.as_view(), name='done'),
]