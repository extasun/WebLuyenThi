from django.contrib import admin
from .models import CauHoi, DapAn, DeThi, NoiDungDe, LuotThi, BaiLam
from django.utils.html import format_html
from django.db.models import Q
from django.urls import reverse
from django.db.models import Sum
class DapAnInline(admin.TabularInline):
    model = DapAn
    extra = 1

class CauHoiAdmin(admin.ModelAdmin):
    list_display = ('noi_dung', 'loai_cau_hoi', 'language', 'subject', 'phan_2', 'ch_photo')
    list_filter = ('loai_cau_hoi', 'language', 'subject', 'phan_2')
    inlines = [DapAnInline]
    readonly_fields = ('ch_photo',)

    def ch_photo(self, obj):
        return obj.ch_photo()
    ch_photo.short_description = 'Image'

class NoiDungDeInline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
class Phan11Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so','thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Phần 1: Tiếng Việt"
    verbose_name_plural = "Phần 1: Tiếng Việt"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__language='vi')
class Phan12Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so','thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Phần 1: Tiếng Anh"
    verbose_name_plural = "Phần 1: Tiếng Anh"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__language='en')
class Phan21Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so','thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Phần 2: Toán Học"
    verbose_name_plural = "Phần 2: Toán Học"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_2='TH')
class Phan22Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so','thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Phần 2: Tư duy logic"
    verbose_name_plural = "Phần 2: Tư duy logic"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_2='TDLG')
class Phan23Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so', 'thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Phần 2: Phân tích số liệu"
    verbose_name_plural = "Phần 2: Phân tích số liệu"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_2='PTSL')
class Phan3Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so', 'thu_tu_cau')
    readonly_fields = ('id',)
    verbose_name = "Phần 3: Giải quyết vấn đề"
    verbose_name_plural = "Phần 3: Giải quyết vấn đề"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__subject__isnull=False)
class DeThiAdmin(admin.ModelAdmin):
    list_display = ('ten_de_thi', 'loai_de', 'ma_de', 'thoi_gian_thi')
    inlines = [Phan11Inline, Phan12Inline, Phan21Inline, Phan22Inline, Phan23Inline, Phan3Inline]

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
class DapAnAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tinh_dung', 'noi_dung')
    list_display = ['id', 'tinh_dung', 'noi_dung']
    list_display_links = ['id', 'tinh_dung', 'noi_dung']
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
admin.site.register(BaiLam) 
admin.site.register(CauHoi, CauHoiAdmin)
admin.site.register(DapAn, DapAnAdmin)
admin.site.register(DeThi, DeThiAdmin)
admin.site.register(NoiDungDe, NoiDungDeAdmin)
admin.site.register(LuotThi, LuotThiAdmin)

