# Generated by Django 4.2.6 on 2023-11-18 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("esign", "0018_document_created_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="created_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
