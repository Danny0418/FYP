# Generated by Django 4.2.7 on 2023-11-26 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esign', '0029_remove_customuser_orgid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='org_ID',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
