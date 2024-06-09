from django.contrib import admin
from authapp_custom import models


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_active", "date_joined"]
    ordering = ["-date_joined"]


@admin.register(models.CustomUserProfile)
class CustomUserProfileAdmin(admin.ModelAdmin):
    list_display = ['tagline', 'aboutMe', 'gender']