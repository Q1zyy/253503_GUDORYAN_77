# Generated by Django 5.0.6 on 2024-09-18 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_partners'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='partners'),
        ),
    ]
