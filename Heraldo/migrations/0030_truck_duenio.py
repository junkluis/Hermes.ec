# Generated by Django 3.2 on 2023-10-20 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Heraldo', '0029_order_tiempo_partida'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='duenio',
            field=models.CharField(default='TRANSPFLOR S.A', max_length=100),
        ),
    ]
