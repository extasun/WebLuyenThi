from django.contrib import admin
from .models import  DeThi, NoiDungDe, BaiLam, LuotThi
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
    fields = ('ma_de', 'ten_de_thi', 'mon_thi', 'thoi_gian_thi', 'sach', 'loai_de', 'khoi', 'chuyen_de', 'lyThuyet')
    list_display = [
        'id',
        'ten_de_thi', 
        'mon_thi', 
        'thoi_gian_thi',
        'loai_de',
        'sach',
        'chuyen_de',
    ]
    list_display_links = [
        'ten_de_thi',    
    ]
    list_filter = [
        'ten_de_thi', 
        'mon_thi', 
        'thoi_gian_thi',
        'loai_de',
        'sach',
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