# Generated by Django 4.2.6 on 2023-11-15 04:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("esign", "0003_remove_document_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "orgID",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("phone_no", models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
    ]
