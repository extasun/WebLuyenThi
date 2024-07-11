from typing import Any
from django.contrib import admin
from .models import CauHoi, DapAn, DeThi, NoiDungDe, BaiLam, LuotThi
class DapAnInline(admin.TabularInline):
    model = DapAn
    extra = 1  # Số lượng form rỗng để hiển thị cho việc nhập liệu
    fields = ('tinh_dung', 'noi_dung', 'anh')
    readonly_fields = ('id',)

class CauHoiDisplay(admin.ModelAdmin):
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
# Đáp án
class DapAnDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tinh_dung', 'noi_dung')
    list_display = [
        'id',
        'tinh_dung',
        'noi_dung'
    ]
    list_display_links = [
        'id',
        'tinh_dung',
        'noi_dung'
    ]
#De Thi
class NoiDungDeInline(admin.TabularInline):
    model = NoiDungDe
    extra = 1  # Số lượng form rỗng để hiển thị cho việc nhập liệu
    fields = ('cau_hoi', 
              'diem_so', 
              'thu_tu_cau')
    #template = 'admin/vertical_inline.html'
    readonly_fields = ('id',)
class DeThiDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('ten_de_thi', 'loai_de', 'thoi_gian_thi' )
    list_display = [
        'id',
        'ten_de_thi', 
        'loai_de',
        'thoi_gian_thi',
    ]
    list_display_links = [
        'ten_de_thi',    
    ]
    list_filter = [
        'ten_de_thi', 
        'thoi_gian_thi',
        'loai_de',
    ]
    search_fields = ['ten_de_thi']
    inlines = [NoiDungDeInline]
# Nội Dung đề
class NoiDungDeDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('de_thi', 'cau_hoi', 'diem_so', 'thu_tu_cau')
    list_display = [
        'id',
        'de_thi', 
        'get_cau_hoi_tieu_de', 
        'diem_so', 
        'thu_tu_cau'
    ]
    list_display_links = [
        'id',   
    ]
    list_filter = [
        'de_thi', 
    ]
    search_fields = ['de_thi']
    def get_cau_hoi_tieu_de(self, obj):
        return obj.cau_hoi.tieu_de if obj.cau_hoi else ''

    get_cau_hoi_tieu_de.short_description = 'Tiêu đề câu hỏi'
# Lượt thi
class BaiLamInline(admin.TabularInline):
    model = BaiLam
    extra = 0
    readonly_fields = ('dap_an', 'tinh_dung')
    sortable_by = [BaiLam.noi_dung_de]
    can_delete = False
    def has_change_permission(self, request, obj=None):
        return False
class LuotThiDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('de_thi', 'nguoi_lam', 'diem_so', 'thoi_diem_thi', 'thoi_gian_hoan_thanh', 'so_cau_dung')
    list_display = [
        'id',
        'de_thi', 
        'nguoi_lam', 
        'diem_so', 
        'thoi_diem_thi', 
        'thoi_gian_hoan_thanh'
    ]
    list_display_links = [
        'id',   
    ]
    readonly_fields = ['de_thi', 'nguoi_lam', 'diem_so', 'thoi_diem_thi', 'thoi_gian_hoan_thanh', 'so_cau_dung']
    list_filter = [
        'de_thi', 
        'nguoi_lam', 
    ]
    search_fields = ['de_thi', 'nguoi_lam']
    inlines = [BaiLamInline]
# Register your models here.
admin.site.register(DeThi, DeThiDisplay)
admin.site.register(NoiDungDe, NoiDungDeDisplay)
admin.site.register(BaiLam)
admin.site.register(LuotThi, LuotThiDisplay)
admin.site.register(CauHoi, CauHoiDisplay)
admin.site.register(DapAn, DapAnDisplay)