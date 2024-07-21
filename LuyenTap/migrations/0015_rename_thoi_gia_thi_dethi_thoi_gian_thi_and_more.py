# Generated by Django 5.0.6 on 2024-07-20 23:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LuyenTap', '0014_dethi_khoi'),
        ('MonHoc', '0005_alter_sach_anh'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dethi',
            old_name='thoi_gia_thi',
            new_name='thoi_gian_thi',
        ),
        migrations.AddField(
            model_name='dethi',
            name='chuyen_de',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MonHoc.chuyende'),
        ),
    ]
