# Generated by Django 4.2.4 on 2023-11-22 08:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0018_rename_video_recets_videoo"),
    ]

    operations = [
        migrations.CreateModel(
            name="bitacors",
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
                ("nombre", models.CharField(blank=True, max_length=20, null=True)),
                ("fecha", models.DateTimeField()),
                ("comentario", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "bitacors",
            },
        ),
    ]
