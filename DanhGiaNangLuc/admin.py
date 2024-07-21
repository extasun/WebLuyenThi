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
    fields = ('cau_hoi', 'diem_so')
    readonly_fields = ('id',)
    verbose_name = "Phần 1: Tiếng Việt"
    verbose_name_plural = "Phần 1: Tiếng Việt"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__language='vi')
class Phan12Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so')
    readonly_fields = ('id',)
    verbose_name = "Phần 1: Tiếng Anh"
    verbose_name_plural = "Phần 1: Tiếng Anh"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__language='en')
class Phan21Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so')
    readonly_fields = ('id',)
    verbose_name = "Phần 2: Toán Học"
    verbose_name_plural = "Phần 2: Toán Học"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_2='TH')
class Phan22Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so')
    readonly_fields = ('id',)
    verbose_name = "Phần 2: Tư duy logic"
    verbose_name_plural = "Phần 2: Tư duy logic"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_2='TDLG')
class Phan23Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so')
    readonly_fields = ('id',)
    verbose_name = "Phần 2: Phân tích số liệu"
    verbose_name_plural = "Phần 2: Phân tích số liệu"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__phan_2='PTSL')
class Phan3Inline(admin.TabularInline):
    model = NoiDungDe
    extra = 1
    fields = ('cau_hoi', 'diem_so')
    readonly_fields = ('id',)
    verbose_name = "Phần 3: Giải quyết vấn đề"
    verbose_name_plural = "Phần 3: Giải quyết vấn đề"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cau_hoi__subject__isnull=False)
class DeThiAdmin(admin.ModelAdmin):
    list_display = ('ten_de_thi', 'loai_de', 'ma_de', 'thoi_gian_thi')
    inlines = [Phan11Inline, Phan12Inline, Phan21Inline, Phan22Inline, Phan23Inline, Phan3Inline]

class BaiLamInline(admin.TabularInline):
    model = BaiLam
    extra = 0
    readonly_fields = ('noi_dung_de', 'cau_hoi', 'dap_an', 'tinh_dung', 'diem')
    fields = ('noi_dung_de', 'cau_hoi', 'dap_an', 'tinh_dung', 'diem')
    can_delete = False
    ordering = ('noi_dung_de__thu_tu_cau',)

    def has_add_permission(self, request, obj=None):
        return False

    def cau_hoi(self, obj):
        return obj.noi_dung_de.cau_hoi.noi_dung
    cau_hoi.short_description = 'Câu hỏi'

    def diem(self, obj):
        return obj.noi_dung_de.diem_so if obj.tinh_dung else 0
    diem.short_description = 'Điểm'
@admin.register(LuotThi)
class LuotThiAdmin(admin.ModelAdmin):
    list_display = ['id', 'de_thi', 'nguoi_lam', 'diem_so', 'so_cau_dung', 'thoi_gian_hoan_thanh', 'thoi_diem_thi']
    list_filter = ['de_thi', 'nguoi_lam', 'thoi_diem_thi']
    search_fields = ['de_thi__ten_de_thi', 'nguoi_lam__username']
    readonly_fields = ['de_thi', 'nguoi_lam', 'diem_so', 'so_cau_dung', 'thoi_diem_thi', 'thoi_gian_hoan_thanh', 'tong_diem']
    inlines = [BaiLamInline]

    def tong_diem(self, obj):
        return obj.bai_lams.filter(tinh_dung=True).aggregate(total=Sum('noi_dung_de__diem_so'))['total'] or 0
    tong_diem.short_description = 'Tổng điểm'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('de_thi', 'nguoi_lam').prefetch_related('bai_lams')
class DapAnAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tinh_dung', 'noi_dung')
    list_display = ['id', 'tinh_dung', 'noi_dung']
    list_display_links = ['id', 'tinh_dung', 'noi_dung']
@admin.register(BaiLam)
class BaiLamAdmin(admin.ModelAdmin):
    list_display = ['id', 'cau_hoi', 'dap_an', 'tinh_dung', 'diem']
    list_filter = ['tinh_dung', 'luot_thi__de_thi', 'noi_dung_de__cau_hoi__subject']
    search_fields = ['luot_thi__nguoi_lam__username', 'noi_dung_de__cau_hoi__noi_dung']
    readonly_fields = ['luot_thi', 'noi_dung_de', 'dap_an', 'tinh_dung', 'diem']

    def cau_hoi(self, obj):
        return obj.noi_dung_de.cau_hoi.noi_dung
    cau_hoi.short_description = 'Câu hỏi'

    def diem(self, obj):
        return obj.noi_dung_de.diem_so if obj.tinh_dung else 0
    diem.short_description = 'Điểm'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('luot_thi', 'noi_dung_de__cau_hoi', 'dap_an')
admin.site.register(CauHoi, CauHoiAdmin)
admin.site.register(DapAn, DapAnAdmin)
admin.site.register(DeThi, DeThiAdmin)
admin.site.register(NoiDungDe)

