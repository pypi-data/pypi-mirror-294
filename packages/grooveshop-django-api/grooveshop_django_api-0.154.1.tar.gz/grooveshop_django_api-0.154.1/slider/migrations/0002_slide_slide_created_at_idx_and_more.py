# Generated by Django 5.0.3 on 2024-03-31 12:31
import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("slider", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="slide",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["created_at"], name="slide_created_at_idx"),
        ),
        migrations.AddIndex(
            model_name="slide",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["updated_at"], name="slide_updated_at_idx"),
        ),
        migrations.AddIndex(
            model_name="slide",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["sort_order"], name="slide_sort_order_idx"),
        ),
        migrations.AddIndex(
            model_name="slide",
            index=django.contrib.postgres.indexes.BTreeIndex(
                fields=["date_start"], name="slider_slid_date_st_65e1d1_btree"
            ),
        ),
        migrations.AddIndex(
            model_name="slide",
            index=django.contrib.postgres.indexes.BTreeIndex(
                fields=["date_end"], name="slider_slid_date_en_f1dc56_btree"
            ),
        ),
        migrations.AddIndex(
            model_name="slider",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["created_at"], name="slider_created_at_idx"),
        ),
        migrations.AddIndex(
            model_name="slider",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["updated_at"], name="slider_updated_at_idx"),
        ),
    ]
