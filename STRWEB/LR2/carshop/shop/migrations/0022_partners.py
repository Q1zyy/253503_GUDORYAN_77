# Generated by Django 5.0.6 on 2024-09-18 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_job_employee_job_description_employee_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
