# Generated by Django 3.2.5 on 2021-07-08 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_rename_date_started_chat_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
