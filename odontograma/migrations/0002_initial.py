# Generated by Django 5.0.2 on 2024-03-19 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('odontograma', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedure',
            name='dentist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.dentist'),
        ),
        migrations.AddField(
            model_name='procedure',
            name='medical_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odontograma.medicalrecord'),
        ),
    ]
