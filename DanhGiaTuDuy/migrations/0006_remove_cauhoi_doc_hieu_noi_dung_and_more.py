# Generated by Django 5.0.6 on 2024-07-12 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DanhGiaTuDuy', '0005_dochieunoidung_cauhoi_doc_hieu_noi_dung'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cauhoi',
            name='doc_hieu_noi_dung',
        ),
        migrations.AddField(
            model_name='dethi',
            name='doc_hieu_noi_dung',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.dochieunoidung'),
        ),
    ]
