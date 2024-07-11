import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LuyenTap', '0013_dethi_sach'),
        ('MonHoc', '0005_alter_sach_anh'),
    ]

    operations = [
        migrations.AddField(
            model_name='dethi',
            name='khoi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MonHoc.khoi'),
        ),
    ]
