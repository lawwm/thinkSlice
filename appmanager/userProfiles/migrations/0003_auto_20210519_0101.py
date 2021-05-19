# Generated by Django 3.2.3 on 2021-05-18 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfiles', '0002_auto_20210518_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='qualifications',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_tutor_reviews',
            field=models.IntegerField(default=0),
        ),
    ]