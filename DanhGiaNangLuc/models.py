from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from User.models import StudentUser
class CauHoi(models.Model):
    LANGUAGE_CHOICES = (
        ('vi', 'Tiếng Việt'),
        ('en', 'Tiếng Anh'),
    )
    SUBJECT_CHOICES = (
        ('ly', 'Vật Lý'),
        ('hoa', 'Hóa Học'),
        ('sinh', 'Sinh Học'),
        ('su', 'Lịch Sử'),
        ('dia', 'Địa Lý'),
        ('gdcd', 'Giáo Dục Công Dân'),
    )
    LOAI_CAU_HOI_CHOICES = [
        ('TN', 'Trắc nghiệm'),
        ('DS', 'Đúng sai'),
        ('TL', 'Tự luận'),
        ('KT', 'Kéo thả'),
        ('CB', 'Chọn nhiều đáp án đúng')
    ]
    PHAN_2_CHOICES = [
        ('TH', 'Toán học'),
        ('TDLG', 'Tư duy logic'),
        ('PTSL', 'Phân tích số liệu'),
    ]
    tieu_de = models.CharField(max_length=255, null=False, blank=False)
    noi_dung = models.TextField()
    loai_cau_hoi = models.CharField(
        max_length=2,
        choices=LOAI_CAU_HOI_CHOICES,
        default='TN',
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, blank=True, null=True)
    subject = models.CharField(max_length=4, choices=SUBJECT_CHOICES, blank=True, null=True)
    phan_2 = models.CharField(max_length=4, choices=PHAN_2_CHOICES, blank=True, null=True)
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
         ('DGNL', 'Đánh giá năng lực'),
    ]
    ten_de_thi = models.CharField(max_length=255, null=False, blank=False)
    loai_de = models.CharField(max_length=50, choices=LOAI_DE_CHOICES, default='DGNL')
    ma_de = models.CharField(max_length=50, unique=True, default=timezone.now)
    thoi_gian_thi = models.DurationField(default=timezone.timedelta(minutes=30))    
    def __str__(self):
        return self.ten_de_thi
class NoiDungDe(models.Model):
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    cau_hoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE)
    diem_so = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(10.00)], default=1)
    thu_tu_cau = models.IntegerField(validators=[MinValueValidator(1)])
    def save(self, *args, **kwargs):
        if not self.pk:  # chỉ áp dụng khi đối tượng chưa tồn tại trong database
            last_item = NoiDungDe.objects.filter(de_thi=self.de_thi).order_by('-thu_tu_cau').first()
            if last_item:
                self.thu_tu_cau = last_item.thu_tu_cau + 1
            else:
                self.thu_tu_cau = 1
        super().save(*args, **kwargs)
    def __str__(self):
        return self.cau_hoi.noi_dung
class LuotThi(models.Model):
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    nguoi_lam = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='danhgianangluc_luotthi_set')
    diem_so = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Điểm số từ 0 đến 10"
    )
    thoi_diem_thi = models.DateTimeField(default=timezone.now)
    thoi_gian_hoan_thanh = models.DurationField(default=timezone.timedelta(minutes=0))
    so_cau_dung = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Lượt thi"
        verbose_name_plural = "Các lượt thi"
        ordering = ['-thoi_diem_thi']

    def __str__(self):
        return f"Lượt thi của {self.nguoi_lam.username} - Đề thi: {self.de_thi.ten_de_thi}"

    def save(self, *args, **kwargs):
        if self.diem_so > 10:
            self.diem_so = 10
        elif self.diem_so < 0:
            self.diem_so = 0
        super().save(*args, **kwargs)

    @property
    def ket_qua(self):
        return "Đạt" if self.diem_so >= 50 else "Không đạt"

class BaiLam(models.Model):
    luot_thi = models.ForeignKey(LuotThi, on_delete=models.CASCADE, related_name='bai_lams', null=True)
    dap_an = models.ForeignKey(DapAn, on_delete=models.CASCADE)
    noi_dung_de = models.ForeignKey(NoiDungDe, on_delete=models.CASCADE, null=True)
    tinh_dung = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Bài làm"
        verbose_name_plural = "Các bài làm"
        unique_together = ['luot_thi', 'noi_dung_de']

    def __str__(self):
        return f"Bài làm: {self.noi_dung_de.cau_hoi.tieu_de} - Lượt thi: {self.luot_thi}"

    def clean(self):
        if self.dap_an.cauHoi != self.noi_dung_de.cau_hoi:
            raise ValidationError("Đáp án phải thuộc về câu hỏi trong nội dung đề.")

    def save(self, *args, **kwargs):
        self.clean()
        self.tinh_dung = self.dap_an.tinh_dung
        super().save(*args, **kwargs)

    @property
    def cau_hoi(self):
        return self.noi_dung_de.cau_hoi

    @property
    def diem(self):
        return self.noi_dung_de.diem_so if self.tinh_dung else 0

