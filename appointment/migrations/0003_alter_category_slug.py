# Generated by Django 4.0.2 on 2022-02-13 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointment", "0002_alter_category_options_alter_doctor_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
