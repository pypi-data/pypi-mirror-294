# Generated by Django 5.0.4 on 2024-04-11 11:43
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0004_order_order_created_at_idx_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="orderitem",
            options={
                "ordering": ["-sort_order"],
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
            },
        ),
    ]
