# Generated by Django 3.2.3 on 2021-06-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_patient_patient_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='password',
            field=models.CharField(default='', max_length=200),
        ),
    ]
