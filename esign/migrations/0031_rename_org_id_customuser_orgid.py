# Generated by Django 4.2.7 on 2023-11-26 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esign', '0030_customuser_org_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='org_ID',
            new_name='orgID',
        ),
    ]
