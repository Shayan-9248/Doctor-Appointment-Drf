# Generated by Django 4.0.2 on 2022-02-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointment", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
        migrations.AlterField(
            model_name="doctor",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to="media/%Y-%m-%d/"),
        ),
    ]
