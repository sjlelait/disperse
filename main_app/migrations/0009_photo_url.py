# Generated by Django 4.1.7 on 2023-04-20 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_remove_photo_url_photo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]