# Generated by Django 4.0.2 on 2022-02-13 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("appointment", "0005_alter_appointment_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointment",
            name="category",
        ),
        migrations.DeleteModel(
            name="Category",
        ),
    ]