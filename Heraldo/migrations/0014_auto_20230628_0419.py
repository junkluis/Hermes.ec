# Generated by Django 3.2 on 2023-06-28 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Heraldo', '0013_tarifas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarifas',
            name='kilogramos',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='tarifas',
            name='libras',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='tarifas',
            name='toneladas',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='tarifas',
            name='toneladas_diez',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='tarifas',
            name='toneladas_seis',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='truck',
            name='capacity',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='truck',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='truck',
            name='log',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='latitud',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='longitud',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
    ]
