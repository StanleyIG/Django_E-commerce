from django.dispatch import Signal, receiver
# from .utilities import send_activation_notification
from .tasks import send_activation_notification_task


post_register = Signal()


@receiver(post_register)
def post_register_dispatcher(sender, **kwargs):
    print('Сигнал сработал')
    email, username = kwargs['email'], kwargs['username']
    # send_activation_notification(kwargs['instance'])
    # send_activation_notification_task.delay(kwargs) таска Celery ожидает простые типы данных python, но QurySet например
    send_activation_notification_task.delay(email, username)
    
