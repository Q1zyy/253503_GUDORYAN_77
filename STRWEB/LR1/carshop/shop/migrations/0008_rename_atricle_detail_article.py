# Generated by Django 5.0.6 on 2024-05-23 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_rename_part_supplierpart_detail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detail',
            old_name='atricle',
            new_name='article',
        ),
    ]