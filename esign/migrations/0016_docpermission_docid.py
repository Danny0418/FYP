# Generated by Django 4.2.6 on 2023-11-18 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("esign", "0015_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="docpermission",
            name="docID",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
