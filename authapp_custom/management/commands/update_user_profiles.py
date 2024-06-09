from django.core.management.base import BaseCommand

from authapp_custom.models import CustomUser, CustomUserProfile


class Command(BaseCommand):
    help = 'Создание профилей пользователей'

    def handle(self, *args, **options):
        for user in CustomUser.objects.filter(customuserprofile__isnull=True):
            CustomUserProfile.objects.create(user=user)
