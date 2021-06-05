# Generated by Django 3.2.3 on 2021-06-03 11:07

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import userProfiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfiles', '0003_alter_profile_duration_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='duration_classes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(12)]), blank=True, default=userProfiles.models.Profile.emptyList, size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
    ]