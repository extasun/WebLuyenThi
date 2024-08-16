from django.db import models
from MonHoc.models import ChuyenDe
from django.utils.safestring import mark_safe
# Create your models here.
# Lý thuyết
class LyThuyet(models.Model):
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField(default='')
    chuyenDe = models.ForeignKey(ChuyenDe, on_delete=models.CASCADE)
    anh = models.ImageField(upload_to='lythuyet_images/', null=True, blank=True)
    def lt_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''
    lt_photo.short_description = 'Image'
    lt_photo.allow_tags = True
    def __str__(self):
        return self.tieu_de
class CauHoi(models.Model):
    TRAC_NGHIEM = 'TN'
    DUNG_SAI = 'CB'
    TU_LUAN = 'TL'

    LOAI_CAU_HOI_CHOICES = [
        (TRAC_NGHIEM, 'Trắc nghiệm'),
        (DUNG_SAI, 'Đúng sai'),
        (TU_LUAN, 'Tự luận'),
    ]
    # Choices for muc_do
    NHAN_BIET = '1'
    THONG_HIEU = '2'
    VAN_DUNG = '3'

    MUC_DO_CHOICES = [
        (NHAN_BIET, 'Nhận biết'),
        (THONG_HIEU, 'Thông hiểu'),
        (VAN_DUNG, 'Vận dụng'),
    ]
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField(default='')
    loai_cau_hoi = models.CharField(max_length=2, choices=LOAI_CAU_HOI_CHOICES, default=TRAC_NGHIEM,)
    muc_do = models.CharField( max_length=1, choices=MUC_DO_CHOICES, default=NHAN_BIET,)
    anh = models.ImageField(upload_to='cauhoi_images/', null=True, blank=True)
    cach_giai = models.TextField(default='')
    lyThuyet = models.ForeignKey(LyThuyet, on_delete=models.CASCADE, null=True, blank=True)
    chuyenDe = models.ForeignKey(ChuyenDe, on_delete=models.CASCADE)
    def ch_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''
    ch_photo.short_description = 'Image'
    ch_photo.allow_tags = True
    def __str__(self):
        return self.noi_dung
class DapAn(models.Model):
    cauHoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE)
    noi_dung = models.TextField(default='')
    tinh_dung =models.BooleanField(default=False)
    anh = models.ImageField(upload_to='dapan_images/', null=True, blank=True)
    thu_tu_dap_an = models.IntegerField(default=1)
    def da_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''
    da_photo.short_description = 'Image'
    da_photo.allow_tags = True
    def __str__(self):
        return self.noi_dung