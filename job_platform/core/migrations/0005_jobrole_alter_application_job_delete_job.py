# Generated by Django 5.2.3 on 2025-06-17 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_remove_company_private_code_alter_companyuser_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobRole",
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
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("salary_min", models.DecimalField(decimal_places=2, max_digits=10)),
                ("salary_max", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "employment_type",
                    models.CharField(
                        choices=[
                            ("full-time", "Full-time"),
                            ("part-time", "Part-time"),
                            ("contract", "Contract"),
                        ],
                        max_length=15,
                    ),
                ),
                ("location", models.CharField(max_length=100)),
                (
                    "experience_level",
                    models.CharField(
                        choices=[
                            ("entry", "Entry"),
                            ("mid", "Mid"),
                            ("senior", "Senior"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("open", "Open"), ("closed", "Closed")],
                        default="open",
                        max_length=10,
                    ),
                ),
                ("keywords", models.TextField(blank=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.company"
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="application",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.jobrole"
            ),
        ),
        migrations.DeleteModel(
            name="Job",
        ),
    ]
