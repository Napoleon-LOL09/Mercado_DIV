# Generated by Django 4.2.4 on 2023-11-27 04:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0026_datos_envio"),
    ]

    operations = [
        migrations.AddField(
            model_name="datos_envio",
            name="mesaño",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="datos_envio",
            name="segu",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="datos_envio",
            name="tarjeta",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="datos_envio",
            name="titular",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
