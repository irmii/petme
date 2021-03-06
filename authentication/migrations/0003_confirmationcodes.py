# Generated by Django 3.1.1 on 2021-08-04 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_is_email_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, verbose_name='Код подтверждения')),
                ('created', models.DateTimeField(verbose_name='Дата и время генерации кода')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_confirmation_codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
