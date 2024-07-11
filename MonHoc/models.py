from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.
#class bộ sách
class Sach(models.Model):
    ten_bo_sach = models.CharField(max_length=255, null=False, blank=False)
    ten_nxb = models.CharField(max_length=255, null=False, blank=False)
    mo_ta = models.TextField(default='')
    anh = models.ImageField(upload_to='anh_images/', null=True)
    def book_photo(self):
        if self.anh:
            return mark_safe('<img src="{}" width="100" />'.format(self.anh.url))
        return ''
    book_photo.short_description = 'Image'
    book_photo.allow_tags = True
    def __str__(self):
        return self.ten_bo_sach              
# class khối học
class Khoi(models.Model):
    ten_khoi = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.ten_khoi
# class Môn học
class MonHoc(models.Model):
    ten_mon = models.CharField(max_length=255, null=False, blank=False)
    mo_ta = models.TextField(default='')
    def __str__(self):
        return self.ten_mon
# class  Chuyên Dề
class ChuyenDe(models.Model):
    ten_chuyen_de = models.CharField(max_length=255, null=False, blank=False)
    mo_ta = models.TextField(default='')
    khoi = models.ForeignKey(Khoi, on_delete=models.CASCADE)
    monHoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    def __str__(self):
        return self.ten_chuyen_de
