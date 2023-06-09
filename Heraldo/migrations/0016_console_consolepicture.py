# Generated by Django 3.2 on 2023-07-02 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Heraldo', '0015_auto_20230628_0603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Console',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='Heraldo.ConsolePicture/bytes/filename/mimetype')),
            ],
        ),
        migrations.CreateModel(
            name='ConsolePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
        ),
    ]
