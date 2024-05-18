import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config_shop.settings')

app = Celery('config_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Для запуска на винде, до этого должна быть установлена библиотека eventlet
# celery -A <your_project> worker -l INFO -P eventlet

# celery_app = Celery("config_shop")
# celery_app.config_from_object("django.conf:settings", namespace="CELERY")
# celery_app.autodiscover_tasks()