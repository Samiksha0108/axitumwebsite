# Generated by Django 5.2.3 on 2025-06-28 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_companyuser_resume"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobrole",
            name="posted_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.companyuser",
            ),
        ),
    ]
