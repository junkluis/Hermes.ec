# Generated by Django 3.2 on 2023-10-20 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Heraldo', '0032_auto_20231019_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='distancia',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='peso',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tarifa',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=100, null=True),
        ),
    ]
