# Generated by Django 3.2 on 2023-10-20 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Heraldo', '0033_auto_20231019_2237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tiempo_partida',
        ),
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