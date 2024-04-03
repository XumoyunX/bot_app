# Generated by Django 5.0.3 on 2024-03-25 09:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_users_akp'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='ball',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='users',
            name='chat_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
