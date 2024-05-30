from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from mainapp.models import ProductCategory, Product

from authapp_custom.forms import CustomUserCreationForm, WidgetMixin, resize_uploaded_image


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class AdminShopUserCreateForm(WidgetMixin, UserCreationForm):
    IMAGE_WIDTH = 100
    IMAGE_HEIGHT = 100

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'first_name', 'last_name', 'is_superuser',
            'is_staff', 'is_active', 'password1', 'password2',
            'email', 'age', 'avatar'
        )
        field_classes = {"username": UsernameField}

    
    def clean_age(self):
        data = self.cleaned_data.get("age")
        if data:
            if data < 10 or data > 100:
                raise forms.ValidationError("кажите действительный возраст!")
        return data
    

    def clean_avatar(self):
        arg_as_str = "avatar"
        avatar = self.cleaned_data.get(arg_as_str)
        resize_uploaded_image(avatar, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        return avatar


class AdminShopUserUpdateForm(WidgetMixin, UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username', 'first_name', 'last_name', 'is_superuser',
            'is_staff', 'is_active', 'password',
            'email', 'age', 'avatar'
        )
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data.get("age")
        if data:
            if data < 10 or data > 100:
                raise forms.ValidationError("кажите действительный возраст!")
        return data


class AdminProductCategoryCreateForm(WidgetMixin, forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class AdminProductUpdateForm(WidgetMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'