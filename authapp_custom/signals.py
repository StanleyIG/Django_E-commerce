from django.dispatch import Signal, receiver
from .utilities import send_activation_notification


post_register = Signal()


@receiver(post_register)
def post_register_dispatcher(sender, **kwargs):
    #print('Сигнал сработал')
    #print(kwargs)
    send_activation_notification(kwargs['instance'])
