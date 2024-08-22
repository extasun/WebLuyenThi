from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from User.models import StudentUser
class DoanCauHoi(models.Model):
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField()
    anh = models.ImageField(upload_to='doancauhoi_images/', null=True, blank=True)
    
    def dh_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''

    dh_photo.short_description = 'Image'
    dh_photo.allow_tags = True
    
    def __str__(self):
        return self.tieu_de
class CauHoi(models.Model):
    PHAN1_CHOICES = (
        ('p1', 'Toán học và xử lý số liệu'),
    )
    SUBJECT_CHOICES = (
        ('ly', 'Vật Lý'),
        ('hoa', 'Hóa Học'),
        ('sinh', 'Sinh Học'),
        ('su', 'Lịch Sử'),
        ('dia', 'Địa Lý'),
    )
    LOAI_CAU_HOI_CHOICES = [
        ('TN', 'Trắc nghiệm'),
        ('CB', 'Đúng sai'),
        ('TL', 'Tự luận'),
    ]
    PHAN2_CHOICES = [
        ('p2', 'Văn học và ngôn ngữ'),
    ]
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField()
    loai_cau_hoi = models.CharField(
        max_length=2,
        choices=LOAI_CAU_HOI_CHOICES,
        default='TN',
    )
    phan1 = models.CharField(max_length=2, choices=PHAN1_CHOICES, blank=True, null=True)
    subject = models.CharField(max_length=4, choices=SUBJECT_CHOICES, blank=True, null=True)
    phan2 = models.CharField(max_length=4, choices=PHAN2_CHOICES, blank=True, null=True)
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
    noi_dung = models.CharField(max_length=200)
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
    LOAI_DE_CHOICES = [
         ('DGNLHN', 'Đánh giá năng lực Hà Nội'),
    ]
    ten_de_thi = models.CharField(max_length=255, null=False, blank=False)
    loai_de = models.CharField(max_length=50, choices=LOAI_DE_CHOICES, default='DGNLHN')
    ma_de = models.CharField(max_length=50, unique=True, default=timezone.now)
    thoi_gian_thi = models.DurationField(default=timezone.timedelta(minutes=30))    
    def __str__(self):
        return self.ten_de_thi
class NoiDungDe(models.Model):
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    cau_hoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE)
    diem_so = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(10.00)], default=1)
    thu_tu_cau = models.IntegerField(validators=[MinValueValidator(1)])
    doan_cau_hoi = models.ForeignKey(DoanCauHoi, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.cau_hoi.noi_dung
class LuotThi(models.Model):
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    nguoi_lam = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='dgnlhanoi_luotthi_set') 
    diem_so = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    thoi_diem_thi = models.DateTimeField(default=timezone.now)
    thoi_gian_hoan_thanh = models.DurationField(default=timezone.timedelta(minutes=0))
    so_cau_dung = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class BaiLam(models.Model):
    luu_bai_thi = models.ForeignKey('LuotThi', on_delete=models.CASCADE, null=True)
    dap_an = models.ForeignKey(DapAn, on_delete=models.CASCADE)  # Link to DapAn model
    noi_dung_de = models.ForeignKey(NoiDungDe, on_delete=models.CASCADE, null=True)
    tinh_dung = models.BooleanField(default=False)
    answer_text = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.noi_dung_de.cau_hoi.noi_dung