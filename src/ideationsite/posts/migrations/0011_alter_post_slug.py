# Generated by Django 4.2.7 on 2023-12-09 00:59

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, max_length=255, populate_from='title', unique=True),
        ),
    ]
