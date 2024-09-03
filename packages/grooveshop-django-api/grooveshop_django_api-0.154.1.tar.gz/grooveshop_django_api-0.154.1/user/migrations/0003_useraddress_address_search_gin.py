# Generated by Django 5.0.3 on 2024-03-31 11:07
import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("country", "0001_initial"),
        ("region", "0001_initial"),
        ("user", "0002_alter_useraddress_options"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="useraddress",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["title", "first_name", "last_name", "city"],
                name="address_search_gin",
                opclasses=[
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                ],
            ),
        ),
    ]
