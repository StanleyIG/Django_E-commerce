from django.dispatch import Signal, receiver
# from .utilities import send_activation_notification
from .tasks import send_activation_notification_task
from django.db.models.signals import post_save
from authapp_custom.models import CustomUser, CustomUserProfile

post_register = Signal()


@receiver(post_register)
def post_register_dispatcher(sender, **kwargs):
    email, username = kwargs['email'], kwargs['username']
    # send_activation_notification(kwargs['instance'])
    # send_activation_notification_task.delay(kwargs) таска Celery ожидает простые типы данных python, но QurySet например
    send_activation_notification_task.delay(email, username)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUserProfile.objects.create(user=instance)
    else:
        instance.customuserprofile.save()
    
