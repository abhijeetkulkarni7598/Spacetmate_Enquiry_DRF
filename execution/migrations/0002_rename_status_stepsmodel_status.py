# Generated by Django 4.1.3 on 2024-01-22 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stepsmodel',
            old_name='Status',
            new_name='status',
        ),
    ]