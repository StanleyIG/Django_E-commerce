import os
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from .signals import post_register
from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


def resize_uploaded_image(image, max_width, max_height):
    """Функции передаётся 1 из объектов, если пользователь не 
       добавлял свой аватар, или не изменял, то функция вернёт None
    """
    size = (max_width, max_height)

    if isinstance(image, InMemoryUploadedFile):
        print('InMemoryUploadedFile')
        memory_image = BytesIO(image.read())
        pil_image = PilImage.open(memory_image)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = 'JPEG' if img_format == 'JPG' else img_format

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)

        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)

        #new_image = ContentFile(new_image.getvalue())
        #return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)
        image.file = new_image

    # Если загруженный файл находится в памяти
    # if isinstance(image, InMemoryUploadedFile):
    #     print('InMemoryUploadedFile')
    #     memory_image = BytesIO(image.read())
    #     pil_image = PilImage.open(memory_image)
    #     img_format = os.path.splitext(image.name)[1][1:].upper()
    #     img_format = 'JPEG' if img_format == 'JPG' else img_format

    #     if pil_image.width > max_width or pil_image.height > max_height:
    #         pil_image.thumbnail(size)

    #     new_image = BytesIO()
    #     pil_image.save(new_image, format=img_format)

    #     new_image = ContentFile(new_image.getvalue())
    #     return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)

    # Если загруженный файл находится на диске
    elif isinstance(image, TemporaryUploadedFile):
        path = image.temporary_file_path()
        print(f'TemporaryUploadedFile: {path}')
        pil_image = PilImage.open(path)

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)
            pil_image.save(path)
            image.size = os.stat(path).st_size

    return image


class WidgetMixin:
    """Отдельный миксин, пригодится для других форм"""
    widget_attrs = {
        "style": "background-color: black !important; color: white;",
    }

    field_placeholders = {
        "username": "введите логин или email",
        "email": "Email должен быть уникальным",
        "password1": 'введите пароль',
        "password1": 'введите пароль',
        "password2": 'подтвердите пароль'

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяея стили к всем полям ввода

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.widget.attrs.update(self.widget_attrs)
            field.help_text = ''
            # чекаю есть ли placeholder для данного поля, если есть, то применяю его
            placeholder = self.field_placeholders.get(field_name)
            if isinstance(self, CustomUserCreationForm):
                # if field_name == 'email':
                field.widget.attrs.update({"placeholder": placeholder})
            else:
                field.widget.attrs.update({"placeholder": placeholder})


class CustomUserCreationForm(WidgetMixin, UserCreationForm):
    field_order = [
        "username",
        "password1",
        "password2",
        "email",
    ]

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
        )
        field_classes = {"username": UsernameField}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        if commit:
            user.save()
        # post_register.send(CustomUserCreationForm, instance=user)
        # для Celery
        post_register.send(sender=CustomUserCreationForm,
                           email=self.cleaned_data['email'],
                           username=self.cleaned_data['username'])
        return user


class CustomLoginView(WidgetMixin, AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class CustomUserChangeForm(forms.ModelForm):
    IMAGE_WIDTH = 100
    IMAGE_HEIGHT = 100

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "avatar",
        )
        field_classes = {"username": UsernameField}

    def clean_avatar(self):
        arg_as_str = "avatar"
        if arg_as_str in self.changed_data and self.instance.avatar:
            if os.path.exists(self.instance.avatar.path):
                os.remove(self.instance.avatar.path)
        avatar = self.cleaned_data.get(arg_as_str)
        #print(type(avatar))
        # уменьшить размер, если был передан объект файла изображения
        #resize_uploaded_image(avatar, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        return avatar #self.cleaned_data.get(arg_as_str)

    def clean_age(self):
        data = self.cleaned_data.get("age")
        if data:
            if data < 10 or data > 100:
                raise ValidationError("кажите действительный возраст!")
        return data
