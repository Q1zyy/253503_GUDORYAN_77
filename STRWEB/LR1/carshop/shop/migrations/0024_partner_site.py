# Generated by Django 5.0.6 on 2024-09-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_partner_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='site',
            field=models.URLField(null=True),
        ),
    ]
