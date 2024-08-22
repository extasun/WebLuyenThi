from typing import Any
from django import forms
from django.contrib import admin
from django.db import models
from .models import CauHoi, DapAn, DeThi, NoiDungDe, BaiLam, LuotThi, DocHieuNoiDung, KhoaHocNoiDung

class DapAnInline(admin.TabularInline):
    model = DapAn
    extra = 1
    fields = ('tinh_dung', 'noi_dung', 'anh')
    readonly_fields = ('id',)

class CauHoiAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tieu_de', 'loai_cau_hoi', 'phan_thi', 'anh', 'ch_photo', 'noi_dung', 'cach_giai')
    list_display = ['id', 'tieu_de', 'loai_cau_hoi', 'phan_thi']
    list_display_links = ['tieu_de']
    list_filter = ['tieu_de', 'loai_cau_hoi', 'phan_thi']
    readonly_fields = ('ch_photo',)
    search_fields = ['tieu_de']
    inlines = [DapAnInline]

class DapAnAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tinh_dung', 'noi_dung')
    list_display = ['id', 'tinh_dung', 'noi_dung']
    list_display_links = ['id', 'tinh_dung', 'noi_dung']

class NoiDungDeInline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so', 'thu_tu_cau')
    readonly_fields = ('id',)
class ToanHocNoiDungDeInline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so', 'thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Tư duy toán học"
    verbose_name_plural = "Tư duy toán học"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_thi='TDTH')

class DocHieuNoiDungDeInline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'doc_hieu_noi_dung', 'diem_so', 'thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Tư duy đọc hiểu"
    verbose_name_plural = "Tư duy đọc hiểu"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_thi='TDDH')

class KhoaHocNoiDungDeInline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'khoa_hoc_noi_dung', 'diem_so', 'thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Tư duy khoa học"
    verbose_name_plural = "Tư duy khoa học"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_thi='TDKH')
class DeThiAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('ten_de_thi','ma_de', 'loai_de', 'doc_hieu_noi_dung', 'thoi_gian_thi')
    list_display = ['id', 'ten_de_thi', 'ma_de', 'loai_de', 'doc_hieu_noi_dung', 'thoi_gian_thi']
    list_display_links = ['ten_de_thi']
    list_filter = ['ten_de_thi', 'thoi_gian_thi', 'loai_de', 'doc_hieu_noi_dung']
    search_fields = ['ten_de_thi']
    inlines = [ToanHocNoiDungDeInline, DocHieuNoiDungDeInline, KhoaHocNoiDungDeInline]
class NoiDungDeAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('de_thi', 'cau_hoi', 'diem_so', 'thu_tu_cau')
    list_display = ['id', 'de_thi', 'get_cau_hoi_tieu_de', 'diem_so', 'thu_tu_cau']
    list_display_links = ['id']
    list_filter = ['de_thi']
    search_fields = ['de_thi']

    def get_cau_hoi_tieu_de(self, obj: NoiDungDe) -> str:
        return obj.cau_hoi.tieu_de if obj.cau_hoi else ''
    
    get_cau_hoi_tieu_de.short_description = 'Tiêu đề câu hỏi'

class LuotThiInline(admin.TabularInline):
    model = BaiLam
    extra = 0
    readonly_fields = ('dap_an', 'tinh_dung')
    sortable_by = ['noi_dung_de']
    can_delete = False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

class LuotThiAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('de_thi', 'nguoi_lam', 'diem_so', 'thoi_diem_thi', 'thoi_gian_hoan_thanh', 'so_cau_dung')
    list_display = ['id', 'de_thi', 'nguoi_lam', 'diem_so', 'thoi_diem_thi', 'thoi_gian_hoan_thanh']
    list_display_links = ['id']
    readonly_fields = ['de_thi', 'nguoi_lam', 'diem_so', 'thoi_diem_thi', 'thoi_gian_hoan_thanh', 'so_cau_dung']
    list_filter = ['de_thi', 'nguoi_lam']
    search_fields = ['de_thi', 'nguoi_lam']
    inlines = [LuotThiInline]

class DocHieuNoiDungAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tieu_de', 'noi_dung')
    list_display = ['id', 'tieu_de']
    list_display_links = ['tieu_de']
    search_fields = ['tieu_de']
class KhoaHocNoiDungAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tieu_de', 'noi_dung')
    list_display = ['id', 'tieu_de']
    list_display_links = ['tieu_de']
    search_fields = ['tieu_de']

admin.site.register(CauHoi, CauHoiAdmin)
admin.site.register(DapAn, DapAnAdmin)
admin.site.register(DeThi, DeThiAdmin)
admin.site.register(NoiDungDe, NoiDungDeAdmin)
admin.site.register(LuotThi, LuotThiAdmin)
admin.site.register(BaiLam)
admin.site.register(DocHieuNoiDung, DocHieuNoiDungAdmin)
admin.site.register(KhoaHocNoiDung, KhoaHocNoiDungAdmin)
