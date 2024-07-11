# Generated by Django 5.0.6 on 2024-07-10 19:16

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DanhGiaTuDuy', '0002_cauhoi_dapan'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeThi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_de_thi', models.CharField(max_length=255)),
                ('loai_de', models.CharField(choices=[('DGTD', 'Đánh giá tư duy')], default='DGTD', max_length=50)),
                ('thoi_gian_thi', models.DurationField(default=datetime.timedelta(seconds=1800))),
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
                ('de_thi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.dethi')),
                ('nguoi_lam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='danhgiatuduy_luotthi_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NoiDungDe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diem_so', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(10.0)])),
                ('thu_tu_cau', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cau_hoi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.cauhoi')),
                ('de_thi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.dethi')),
            ],
        ),
        migrations.CreateModel(
            name='BaiLam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tinh_dung', models.BooleanField(default=False)),
                ('dap_an', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.dapan')),
                ('luu_bai_thi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.luotthi')),
                ('noi_dung_de', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DanhGiaTuDuy.noidungde')),
            ],
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
