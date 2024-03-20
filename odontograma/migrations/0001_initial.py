# Generated by Django 5.0.2 on 2024-03-19 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asma', models.BooleanField()),
                ('anemia', models.BooleanField()),
                ('diabetes', models.BooleanField()),
                ('hipertensao', models.BooleanField()),
                ('alergia', models.BooleanField()),
                ('epilepsia', models.BooleanField()),
                ('herpes', models.BooleanField()),
                ('hiv', models.BooleanField()),
                ('tuberculose', models.BooleanField()),
                ('hepatite', models.BooleanField()),
                ('cancer', models.BooleanField()),
                ('doenca_cardiaca', models.BooleanField()),
                ('doenca_renal', models.BooleanField()),
                ('traumatismo_craniano', models.BooleanField()),
                ('doencas_osseas', models.BooleanField()),
                ('sifiles', models.BooleanField()),
                ('outros', models.CharField(max_length=100)),
                ('frequencia_cardiaca', models.CharField(max_length=100)),
                ('pressao_arterial', models.CharField(max_length=100)),
                ('faz_tratamento_medico_atual', models.BooleanField()),
                ('qual_tratamento', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procedure', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('color', models.CharField(max_length=100)),
                ('tooth_face', models.CharField(max_length=100)),
                ('number_tooth', models.IntegerField()),
            ],
        ),
    ]
