from pathlib import Path
from time import time
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models
from PIL import Image


def users_avatars_path(instance, filename):
    # загрузка картинки по пути:
    #   MEDIA_ROOT / user_<username> / avatars / <filename>
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return "user_{0}/avatars/{1}".format(instance.username, f"pic_{num}{suff}")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        "имя пользователя",
        max_length=150,
        unique=True,
        help_text="Не более 150 символов. Только буквы и цифры в формате ASCII.",
        validators=[username_validator],
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
        },
    )
    first_name = models.CharField("имя", max_length=150, blank=True)
    last_name = models.CharField("фамилия", max_length=150, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to=users_avatars_path, blank=True, null=True)
    email = models.CharField(
        "email адрес",
        max_length=256,
        unique=True,
        error_messages={
            "unique": "Пользователь с таким адресом электронной почты уже существует.",
        },
    )
    is_staff = models.BooleanField(
        "статус персонала",
        default=False,  # 0
        help_text="Определяет, может ли пользователь войти в сайт админа.",
    )
    is_active = models.BooleanField(
        "статус активности",
        default=False,  # Активация по почте
        help_text="Активен ли пользователь",
    )
    date_joined = models.DateTimeField("дата регистрации", auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = "email"  # аутентификация по email
    USERNAME_FIELD = "username"  # указываю какое поле должно отображаться в приложении
    # обязательные поля которые необходимо заполнить
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Возвращает полное имя, first_name плюс last_name с пробелом между ними.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Возвращает короткое имя пользователя."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Отправить электронное письмо этому пользователю."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
