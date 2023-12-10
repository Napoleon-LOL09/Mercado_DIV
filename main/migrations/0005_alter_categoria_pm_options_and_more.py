# Generated by Django 4.2.4 on 2023-11-07 08:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_categoria_pm_options_categoria_pm_idx_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="categoria_pm",
            options={"verbose_name": "Categoria", "verbose_name_plural": "Categorias"},
        ),
        migrations.RemoveIndex(
            model_name="categoria_pm",
            name="idx_name",
        ),
        migrations.RemoveIndex(
            model_name="categoria_pm",
            name="idx_descripcion",
        ),
        migrations.AlterModelTable(
            name="categoria_pm",
            table="categoria_pm",
        ),
    ]
