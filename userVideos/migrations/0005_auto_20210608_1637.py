# Generated by Django 3.2.4 on 2021-06-08 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userVideos', '0004_rename_numofcomments_video_num_of_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocomments',
            name='has_replies',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='videocomments',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userVideos.videocomments'),
        ),
    ]