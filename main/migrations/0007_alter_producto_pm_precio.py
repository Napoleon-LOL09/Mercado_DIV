# Generated by Django 4.2.4 on 2023-11-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_producto_pm"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto_pm",
            name="precio",
            field=models.IntegerField(),
        ),
    ]
