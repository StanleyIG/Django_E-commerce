from django.urls import path
from authapp_custom import views
from authapp_custom.apps import AuthappCustomConfig
from authapp_custom.views import user_activate

app_name =  AuthappCustomConfig.name

urlpatterns = [
    path("", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('register/done/,', views.RegisterDoneView.as_view(), name='done'),
    path('activate/<str:sign>/', user_activate, name='activate'),
]