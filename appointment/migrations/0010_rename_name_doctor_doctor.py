# Generated by Django 4.0.2 on 2022-02-13 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("appointment", "0009_rename_doctor_doctor_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="doctor",
            old_name="name",
            new_name="doctor",
        ),
    ]
