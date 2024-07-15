# Generated by Django 5.0.6 on 2024-07-13 18:58

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CauHoi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tieu_de', models.CharField(max_length=255)),
                ('noi_dung', models.TextField(default='')),
                ('loai_cau_hoi', models.CharField(choices=[('TN', 'Trắc nghiệm'), ('DS', 'Đúng sai'), ('TL', 'Tự luận'), ('KT', 'Kéo thả')], default='TN', max_length=2)),
                ('phan_thi', models.CharField(choices=[('NN', 'Ngôn ngữ'), ('PTSL', 'Toán học, tư duy logic và phân tích số liệu'), ('TDKH', 'Giải quyết vấn đề')], default='NN', max_length=7)),
                ('anh', models.ImageField(blank=True, null=True, upload_to='cauhoi_images/')),
                ('cach_giai', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='DeThi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_de_thi', models.CharField(max_length=255)),
                ('loai_de', models.CharField(choices=[('DGNL', 'Đánh giá năng lực')], default='DGNL', max_length=50)),
                ('thoi_gian_thi', models.DurationField(default=datetime.timedelta(seconds=1800))),
            ],
        ),
        migrations.CreateModel(
            name='MonHoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_mon', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DapAn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noi_dung', models.TextField(default='')),
                ('tinh_dung', models.BooleanField(default=False)),
                ('anh', models.ImageField(blank=True, null=True, upload_to='dapan_images/')),
                ('cauHoi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaNangLuc.cauhoi')),
            ],
        ),
        migrations.CreateModel(
            name='LuotThi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diem_so', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('thoi_diem_thi', models.DateTimeField(default=django.utils.timezone.now)),
                ('thoi_gian_hoan_thanh', models.DurationField(default=datetime.timedelta(0))),
                ('so_cau_dung', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('de_thi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaNangLuc.dethi')),
                ('nguoi_lam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='danhgianangluc_luotthi_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NoiDungDe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diem_so', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(10.0)])),
                ('thu_tu_cau', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cau_hoi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaNangLuc.cauhoi')),
                ('de_thi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaNangLuc.dethi')),
            ],
        ),
        migrations.CreateModel(
            name='BaiLam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tinh_dung', models.BooleanField(default=False)),
                ('dap_an', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaNangLuc.dapan')),
                ('luu_bai_thi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaNangLuc.luotthi')),
                ('noi_dung_de', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DanhGiaNangLuc.noidungde')),
            ],
        ),
    ]
