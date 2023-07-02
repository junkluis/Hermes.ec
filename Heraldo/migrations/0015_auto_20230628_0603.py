# Generated by Django 3.2 on 2023-06-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Heraldo', '0014_auto_20230628_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='distancia',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='peso',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tarifa',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
    ]