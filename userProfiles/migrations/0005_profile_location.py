# Generated by Django 3.2.4 on 2021-06-05 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfiles', '0004_auto_20210603_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
