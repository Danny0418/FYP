# Generated by Django 4.2.7 on 2023-11-26 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('esign', '0031_rename_org_id_customuser_orgid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='orgID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='esign.organization'),
        ),
    ]