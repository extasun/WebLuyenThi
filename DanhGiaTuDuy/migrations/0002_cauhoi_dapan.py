# Generated by Django 5.0.6 on 2024-07-10 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DanhGiaTuDuy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CauHoi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tieu_de', models.CharField(max_length=255)),
                ('noi_dung', models.TextField(default='')),
                ('loai_cau_hoi', models.CharField(choices=[('TN', 'Trắc nghiệm'), ('DS', 'Đúng sai'), ('TL', 'Tự luận'), ('KT', 'Kéo thả')], default='TN', max_length=2)),
                ('anh', models.ImageField(blank=True, null=True, upload_to='cauhoi_images/')),
                ('cach_giai', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='DapAn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noi_dung', models.TextField(default='')),
                ('tinh_dung', models.BooleanField(default=False)),
                ('anh', models.ImageField(blank=True, null=True, upload_to='dapan_images/')),
                ('cauHoi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.cauhoi')),
            ],
        ),
    ]
