# Generated by Django 4.2.7 on 2023-12-29 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug_alias',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
