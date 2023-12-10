# Generated by Django 4.2.4 on 2023-11-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0024_coment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="coment_user",
            name="tipo",
            field=models.CharField(
                choices=[
                    ("LIKE", "Like"),
                    ("DISLIKE", "Dislike"),
                    ("COMENTARIO", "Comentario"),
                ],
                default=0,
                max_length=10,
            ),
            preserve_default=False,
        ),
    ]