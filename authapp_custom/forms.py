import os
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from .signals import post_register


class WidgetMixin:
    """Отдельный миксин, пригодится для других форм"""
    widget_attrs = {
        "style": "background-color: black !important; color: white;",
    }

    field_placeholders = {
        "username": "введите логин или email",
        "email": "Email должен быть уникальным",
        "password": 'введите пароль',
        "password1": 'введите пароль',
        "password2": 'подтвердите пароль'

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяея стили к всем полям ввода

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.widget.attrs.update(self.widget_attrs)

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
        return self.cleaned_data.get(arg_as_str)

    def clean_age(self):
        data = self.cleaned_data.get("age")
        if data:
            if data < 10 or data > 100:
                raise ValidationError("кажите действительный возраст!")
        return data
