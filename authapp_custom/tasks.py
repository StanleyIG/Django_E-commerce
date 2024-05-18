import logging
from typing import Dict, Union
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .utilities import send_activation_notification, send_activation_notification_user_id


@shared_task
def send_activation_notification_task(email_address):
    send_activation_notification_user_id(email_address)
    #send_activation_notification(user['instance'])