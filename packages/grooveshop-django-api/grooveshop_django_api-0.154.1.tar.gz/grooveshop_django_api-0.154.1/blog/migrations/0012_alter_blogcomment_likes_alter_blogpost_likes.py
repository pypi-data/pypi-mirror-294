# Generated by Django 5.0.4 on 2024-04-18 12:03
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0011_alter_blogcommenttranslation_content_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogcomment",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                related_name="liked_comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                related_name="liked_blog_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
