# Generated by Django 4.2.6 on 2023-11-16 13:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("esign", "0012_rename_document_signature_docid"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Signature",
        ),
    ]