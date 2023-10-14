# Generated by Django 4.2.5 on 2023-10-01 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0002_remove_cart_unit_price"),
    ]

    operations = [
        migrations.RemoveField(model_name="orderitem", name="unit_price",),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="LittleLemonAPI.order"
            ),
        ),
    ]
