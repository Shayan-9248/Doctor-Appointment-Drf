# Generated by Django 4.0.2 on 2022-02-13 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0010_rename_name_doctor_doctor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='doctor',
            new_name='name',
        ),
    ]
