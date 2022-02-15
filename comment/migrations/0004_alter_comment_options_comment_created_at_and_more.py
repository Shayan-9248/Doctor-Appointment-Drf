# Generated by Django 4.0.2 on 2022-02-15 11:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0003_alter_comment_object_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="comment.comment",
            ),
        ),
    ]
