# Generated by Django 4.2.7 on 2023-12-06 03:46

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_post_content_rendered_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=markdownfield.models.MarkdownField(blank=True, null=True, rendered_field='content_rendered'),
        ),
    ]