from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from User.models import StudentUser

class DocHieuNoiDung(models.Model):
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField()
    anh = models.ImageField(upload_to='dochieu_images/', null=True, blank=True)
    
    def dh_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''

    dh_photo.short_description = 'Image'
    dh_photo.allow_tags = True
    
    def __str__(self):
        return self.tieu_de
class KhoaHocNoiDung(models.Model):
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField()
    anh = models.ImageField(upload_to='khoahoc_images/', null=True, blank=True)
    
    def dh_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''

    dh_photo.short_description = 'Image'
    dh_photo.allow_tags = True
    
    def __str__(self):
        return self.tieu_de
class CauHoi(models.Model):
    TRAC_NGHIEM = 'TN'
    DUNG_SAI = 'DS'
    TU_LUAN = 'TL'
    KEO_THA = 'KT'
    TU_DUY_TOAN_HOC = 'TDTH'
    TU_DUY_DOC_HIEU = 'TDDH'
    TU_DUY_KHOA_HOC = 'TDKH'
    LOAI_CAU_HOI_CHOICES = [
        (TRAC_NGHIEM, 'Trắc nghiệm'),
        (DUNG_SAI, 'Đúng sai'),
        (TU_LUAN, 'Tự luận'),
        (KEO_THA, 'Kéo thả'),  # New choice
    ]
    PHAN_THI_CHOICES = [
        (TU_DUY_TOAN_HOC, 'Tư duy toán học'),
        (TU_DUY_DOC_HIEU, 'Tư duy đọc hiểu'),
        (TU_DUY_KHOA_HOC, 'Tư duy khoa học'),
    ]
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField(default='')
    loai_cau_hoi = models.CharField(
        max_length=2,
        choices=LOAI_CAU_HOI_CHOICES,
        default=TRAC_NGHIEM,
    )
    phan_thi = models.CharField(max_length=4, choices=PHAN_THI_CHOICES, default=TU_DUY_TOAN_HOC)
    anh = models.ImageField(upload_to='cauhoi_images/', null=True, blank=True)
    cach_giai = models.TextField(default='')
    
    
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
    tinh_dung = models.BooleanField(default=False)
    anh = models.ImageField(upload_to='dapan_images/', null=True, blank=True)

    def da_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''

    da_photo.short_description = 'Image'
    da_photo.allow_tags = True

    def __str__(self):
        return self.noi_dung

class DeThi(models.Model):
    DANH_GIA_TU_DUY = 'DGTD'
    LOAI_DE_CHOICES = [
         (DANH_GIA_TU_DUY, 'Đánh giá tư duy'),
    ]
    ten_de_thi = models.CharField(max_length=255, null=False, blank=False)
    loai_de = models.CharField(max_length=50, choices=LOAI_DE_CHOICES, default=DANH_GIA_TU_DUY)
    thoi_gian_thi = models.DurationField(default=timezone.timedelta(minutes=30))
    doc_hieu_noi_dung = models.ForeignKey(DocHieuNoiDung, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.ten_de_thi

class NoiDungDe(models.Model):
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    cau_hoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE)
    diem_so = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(10.00)])
    thu_tu_cau = models.IntegerField(validators=[MinValueValidator(1)])
    doc_hieu_noi_dung = models.ForeignKey(DocHieuNoiDung, on_delete=models.SET_NULL, null=True, blank=True)
    khoa_hoc_noi_dung = models.ForeignKey(KhoaHocNoiDung, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.cau_hoi.noi_dung

class LuotThi(models.Model):
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    nguoi_lam = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='danhgiatuduy_luotthi_set') 
    diem_so = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    thoi_diem_thi = models.DateTimeField(default=timezone.now)
    thoi_gian_hoan_thanh = models.DurationField(default=timezone.timedelta(minutes=0))
    so_cau_dung = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class BaiLam(models.Model):
    luu_bai_thi = models.ForeignKey(LuotThi, on_delete=models.CASCADE)
    dap_an = models.ForeignKey(DapAn, on_delete=models.CASCADE)  # Link to DapAn model
    noi_dung_de = models.ForeignKey(NoiDungDe, on_delete=models.CASCADE, null=True)
    tinh_dung = models.BooleanField(default=False)
    
    def __str__(self):
        return self.noi_dung_de.cau_hoi.noi_dung
