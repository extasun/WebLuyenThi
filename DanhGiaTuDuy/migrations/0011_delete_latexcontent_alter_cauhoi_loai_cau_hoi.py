# Generated by Django 5.0.6 on 2024-08-16 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DanhGiaTuDuy', '0010_latexcontent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LatexContent',
        ),
        migrations.AlterField(
            model_name='cauhoi',
            name='loai_cau_hoi',
            field=models.CharField(choices=[('TN', 'Trắc nghiệm'), ('CB', 'Đúng sai'), ('TL', 'Tự luận')], default='TN', max_length=2),
        ),
    ]
