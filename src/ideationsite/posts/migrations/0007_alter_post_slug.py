# Generated by Django 4.2.7 on 2023-12-08 03:38

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='title', editable=True, max_length=255, populate_from='title', unique=True),
        ),
    ]
