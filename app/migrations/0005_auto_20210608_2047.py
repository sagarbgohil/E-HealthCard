# Generated by Django 3.2.3 on 2021-06-08 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210608_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('organization', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='designation',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='doctor',
            name='licence_id',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='doctor',
            name='patient_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.patient'),
        ),
        migrations.AlterField(
            model_name='healthinfo',
            name='blood_grp',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='healthinfo',
            name='emergency_num',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='healthinfo',
            name='height',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='healthinfo',
            name='medication',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='healthinfo',
            name='weight',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address_1',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='VerifiedBy',
            fields=[
                ('verified_by_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.admin')),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Paramedics',
            fields=[
                ('paramedics_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('vehicle_licence_num', models.BigIntegerField()),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('meta_data_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('created_date', models.DateField()),
                ('last_modify_date', models.DateField()),
                ('last_login_date', models.DateField()),
                ('verified_date', models.DateField()),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='AllergiesTable',
            fields=[
                ('allergies_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('allergies', models.CharField(max_length=30)),
                ('health_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.healthinfo')),
            ],
        ),
    ]