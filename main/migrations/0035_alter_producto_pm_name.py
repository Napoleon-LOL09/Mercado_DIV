# Generated by Django 4.2.4 on 2023-12-04 00:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0034_alter_datos_envio_guardado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto_pm",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]