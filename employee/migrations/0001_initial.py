# Generated by Django 5.1.1 on 2024-09-26 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.CharField(editable=False, max_length=9, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('email_address', models.EmailField(max_length=254)),
                ('phone_number', models.IntegerField()),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=2)),
                ('employee_cafe', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emp', to='cafe.employeecafe')),
            ],
        ),
    ]
