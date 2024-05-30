import os
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from io import BytesIO, StringIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from PIL import Image, ImageOps

from authapp_custom.forms import CustomUserCreationForm, WidgetMixin #, resize_uploaded_image


def resize_uploaded_image(image, max_width, max_height):
    """Функции передаётся 1 из объектов, если пользователь не 
       добавлял свой аватар, или не изменял, то функция вернёт None
    """
    size = (max_width, max_height)

    # Если загруженный файл находится в памяти
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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.help_text = ''

    
    def clean_age(self):
        data = self.cleaned_data.get("age")
        if data:
            if data < 10 or data > 100:
                raise forms.ValidationError("кажите действительный возраст!")
        return data
    

    def clean_avatar(self):
        arg_as_str = "avatar"
        avatar = self.cleaned_data.get(arg_as_str)
        # avatar_new = BytesIO(avatar.read())
        # image = Image.open(avatar_new)
        # image.thumbnail((200, 200))
        # image_file = BytesIO()
        # image.save(image_file, 'jpeg')
        # avatar.file = image_file
        # уменьшить размер
        resize_uploaded_image(avatar, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        return avatar


    
    # def clean_avatar(self):
    #     arg_as_str = "avatar"
    #     avatar = self.cleaned_data.get(arg_as_str)
    #     avatar_new = StringIO(avatar.read())
    #     image = Image.open(avatar_new)
    #     image.thumbnail((200, 200))
    #     image_file = StringIO()
    #     image.save(image_file, 'jpeg')
    #     avatar.file = image_file
    #     # уменьшить размер
    #     #resize_uploaded_image(image, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
    #     return avatar 
