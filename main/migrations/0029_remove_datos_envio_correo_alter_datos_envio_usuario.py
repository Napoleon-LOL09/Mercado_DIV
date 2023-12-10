# Generated by Django 4.2.4 on 2023-11-27 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0028_remove_carrito_productos"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="datos_envio",
            name="correo",
        ),
        migrations.AlterField(
            model_name="datos_envio",
            name="usuario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]