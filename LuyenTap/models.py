from django.db import models
from MonHoc.models import MonHoc, Sach, Khoi, ChuyenDe
from datetime import timedelta
from django.utils import timezone
from NoiDung.models import CauHoi, DapAn, LyThuyet
from User.models import StudentUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class DeThi(models.Model):
    DE_KIEM_TRA_HOC_KI = 'HK'
    DE_KIEM_TRA_GIUA_KI = 'GK'
    KHAO_SAT_CHAT_LUONG_DAU_NAM = 'KSCL'
    KIEM_TRA_15P = 'KT15P'
    KIEM_TRA_1T = 'KT1T'
    LOAI_DE_CHOICES = [
        (DE_KIEM_TRA_HOC_KI, 'Đề kiểm tra học kì'),
        (DE_KIEM_TRA_GIUA_KI, 'Đề kiểm tra giữa kì'),
        (KHAO_SAT_CHAT_LUONG_DAU_NAM, 'Đề khảo sát chất lượng đầu năm'),
        (KIEM_TRA_15P, 'Đề kiểm tra 15 phút'),
        (KIEM_TRA_1T, 'Đề kiểm tra 1 tiết'),
    ]
    ten_de_thi = models.CharField(max_length=255, null=False, blank=False)
    mon_thi = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    loai_de = models.CharField(max_length=50, choices=LOAI_DE_CHOICES, default=DE_KIEM_TRA_GIUA_KI)
    sach = models.ForeignKey(Sach, null=True, on_delete=models.CASCADE)
    khoi = models.ForeignKey(Khoi, on_delete=models.CASCADE, null=True)
    chuyen_de = models.ForeignKey(ChuyenDe, on_delete=models.CASCADE, null=True)
    lyThuyet = models.ForeignKey(LyThuyet, on_delete=models.CASCADE, null=True, blank=True)
    trang_thai = models.BooleanField(default=False)
    ma_de = models.CharField(max_length=50, unique=True, default=timezone.now)
    thoi_gian_thi = models.DurationField(default=timedelta(minutes=30))
    def __str__(self):
        return self.ten_de_thi
class NoiDungDe(models.Model):
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    cau_hoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE)
    diem_so = models.FloatField(validators=[MinValueValidator(0.01),MaxValueValidator(10.00),])
    thu_tu_cau = models.IntegerField(validators=[MinValueValidator(1)])
    def __str__(self):
        return self.cau_hoi.noi_dung
class LuotThi(models.Model):
    de_thi =  models.ForeignKey(DeThi, on_delete=models.CASCADE)
    nguoi_lam = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    diem_so = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100),] )
    thoi_diem_thi = models.DateTimeField(default=timezone.now)
    thoi_gian_hoan_thanh = models.DurationField(default=timedelta(minutes=0))
    so_cau_dung = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class BaiLam(models.Model): 
    luu_bai_thi = models.ForeignKey(LuotThi, on_delete=models.CASCADE)
    dap_an = models.ForeignKey(DapAn, on_delete=models.CASCADE)
    noi_dung_de = models.ForeignKey(NoiDungDe, on_delete=models.CASCADE, null=True)
    tinh_dung = models.BooleanField(default=False)
    answer_text = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.noi_dung_de.cau_hoi.noi_dung
