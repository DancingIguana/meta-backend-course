# Generated by Django 4.2.5 on 2023-09-22 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0002_category_menuitem_category"),
    ]

    operations = [
        migrations.RemoveField(model_name="menuitem", name="category",),
    ]
