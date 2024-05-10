# Для того чтоб аутинтификация проходила по Email, переопределяю бэкэнд аутинтификации Django.
# Потом надо добавить его в settings.py -> AUTHENTICATION_BACKENDS = ['<имя приложения пользователей>.backends.EmailBackend',
#                                                                     'django.contrib.auth.backends.ModelBackend',
#                                                                     ]


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, *kwargs):
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
