# Generated by Django 4.2 on 2024-06-09 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp_custom', '0002_customuser_activation_key_expires'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='теги')),
                ('aboutMe', models.TextField(blank=True, max_length=512, verbose_name='о себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'мужской'), ('W', 'женский')], max_length=1, verbose_name='пол')),
            ],
        ),
    ]