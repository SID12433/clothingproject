# Generated by Django 4.2.5 on 2023-11-07 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yousta', '0003_cloths_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='orderd_date',
            new_name='ordered_date',
        ),
    ]