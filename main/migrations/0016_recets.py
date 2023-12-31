# Generated by Django 4.2.4 on 2023-11-19 08:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0015_cupones_usado"),
    ]

    operations = [
        migrations.CreateModel(
            name="recets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(blank=True, max_length=100, null=True)),
                ("ingre", models.TextField(blank=True, null=True)),
                ("proce", models.TextField(blank=True, null=True)),
                ("video", models.FileField(blank=True, null=True, upload_to="videos/")),
                (
                    "imagen",
                    models.ImageField(blank=True, null=True, upload_to="recetas/"),
                ),
                ("categoria", models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                "db_table": "recets",
            },
        ),
    ]
