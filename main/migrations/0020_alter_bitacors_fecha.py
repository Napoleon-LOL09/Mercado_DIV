# Generated by Django 4.2.4 on 2023-11-23 21:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0019_bitacors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bitacors",
            name="fecha",
            field=models.DateField(),
        ),
    ]
