# Generated by Django 4.2.6 on 2023-11-19 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='whatever-slug'),
            preserve_default=False,
        ),
    ]