# Generated by Django 4.2.8 on 2024-01-31 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_quotation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date',
            field=models.CharField(blank=True, default='31/01/24', max_length=100, null=True),
        ),
    ]