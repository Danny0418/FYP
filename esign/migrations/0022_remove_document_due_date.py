# Generated by Django 4.2.6 on 2023-11-19 09:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("esign", "0021_alter_document_due_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="due_date",
        ),
    ]
