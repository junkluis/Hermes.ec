# Generated by Django 3.2 on 2023-06-27 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Heraldo', '0011_alter_order_location_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('latitud', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('longitud', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
        ),
    ]
