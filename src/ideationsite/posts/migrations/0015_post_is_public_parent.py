# Generated by Django 4.2.7 on 2024-01-13 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_post_slug_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_public_parent',
            field=models.BooleanField(default=False),
        ),
    ]