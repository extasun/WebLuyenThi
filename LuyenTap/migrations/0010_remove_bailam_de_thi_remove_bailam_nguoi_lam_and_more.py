# Generated by Django 5.0.1 on 2024-06-25 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LuyenTap', '0009_bailam_luotthi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bailam',
            name='de_thi',
        ),
        migrations.RemoveField(
            model_name='bailam',
            name='nguoi_lam',
        ),
        migrations.AddField(
            model_name='bailam',
            name='luu_bai_thi',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LuyenTap.luotthi'),
            preserve_default=False,
        ),
    ]
