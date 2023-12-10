# Generated by Django 4.2.4 on 2023-11-07 08:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_rename_categoria_p_categoria_pm_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="categoria_pm",
            options={},
        ),
        migrations.AddIndex(
            model_name="categoria_pm",
            index=models.Index(
                condition=models.Q(("name__iexact", True)),
                fields=["name"],
                name="idx_name",
            ),
        ),
        migrations.AddIndex(
            model_name="categoria_pm",
            index=models.Index(
                condition=models.Q(("descripcion__iexact", True)),
                fields=["descripcion"],
                name="idx_descripcion",
            ),
        ),
        migrations.AlterModelTable(
            name="categoria_pm",
            table=None,
        ),
    ]