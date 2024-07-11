# Generated by Django 5.0.1 on 2024-06-28 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NoiDung', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CachGiai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noi_dung', models.TextField(default='')),
                ('anh', models.ImageField(blank=True, null=True, upload_to='dapan_images/')),
                ('cauHoi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NoiDung.cauhoi')),
            ],
        ),
    ]
