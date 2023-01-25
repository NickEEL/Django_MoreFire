# Generated by Django 4.1.1 on 2023-01-23 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mfevents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Gallery name')),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('edited_dt', models.DateTimeField(auto_now=True, verbose_name='Date edited')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mfevents.mfevent')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Photo', max_length=50, verbose_name='Photo name')),
                ('photo', models.ImageField(null=True, upload_to='photos/', verbose_name='Photo')),
                ('portrait', models.BooleanField(default=False, verbose_name='Portrait? True/False')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Photo info.')),
                ('created_dt', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('edited_dt', models.DateTimeField(auto_now=True, verbose_name='Date edited')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='galleries.gallery')),
            ],
        ),
    ]
