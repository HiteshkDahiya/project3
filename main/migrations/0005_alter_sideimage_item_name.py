# Generated by Django 5.1.7 on 2025-04-24 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_sideimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sideimage',
            name='item_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
