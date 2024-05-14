import os
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError



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
                #if field_name == 'email':
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


class CustomLoginView(WidgetMixin, AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
