from django.contrib import admin
from .models import LyThuyet, CauHoi, DapAn
from django.utils.html import format_html
from django.urls import path, reverse
from django.http import HttpResponseRedirect

# Hành động chuyển hướng
def view_selected_objects(self, request, queryset):
    if queryset.count() == 1:
        obj = queryset.first()
        url = reverse('admin:view_cauhoi', args=[obj.pk])
        return HttpResponseRedirect(url)
    else:
        self.message_user(request, "Please select only one object to view.", level='error')

view_selected_objects.short_description = 'View selected objects'
# Ly Thuyet
class LyThuyetDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('tieu_de', 'chuyenDe', 'noi_dung', 'anh')
    list_display = [
        'id',
        'tieu_de',
        'get_chuyen_de',
        'short_noi_dung',  
        'display_image'
    ]
    list_display_links = [
        'tieu_de',
    ]
    list_filter = [
        'chuyenDe',
    ]
    def get_chuyen_de(self, obj):
        return obj.chuyenDe.ten_chuyen_de
    get_chuyen_de.short_description = 'Chuyên đề'
    def short_noi_dung(self, obj):
        if len(obj.noi_dung) > 100:
            return obj.noi_dung[:100] + '...'
        return obj.noi_dung

    short_noi_dung.short_description = 'Nội dung'
    def display_image(self, obj):
        if obj.anh:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.anh.url)
        return ""
    display_image.short_description = 'Ảnh'
#Câu hỏi
class DapAnInline(admin.TabularInline):
    model = DapAn
    extra = 1  # Số lượng form rỗng để hiển thị cho việc nhập liệu
    fields = ('tinh_dung', 'noi_dung', 'anh', 'thu_tu_dap_an')
    readonly_fields = ('id',)
    
class CauHoiDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('chuyenDe', 'tieu_de', 'loai_cau_hoi', 'muc_do', 'lyThuyet', 'anh', 'ch_photo', 'noi_dung', 'cach_giai')
    list_display = [
        'id',
        'chuyenDe', 
        'tieu_de', 
        'loai_cau_hoi', 
        'muc_do', 
        'lyThuyet'
    ]
    list_display_links = [
        'tieu_de',    
    ]
    list_filter = [
        'chuyenDe',
        'tieu_de', 
        'loai_cau_hoi', 
        'muc_do', 
        'lyThuyet'
    ]
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

# Register your models here.
admin.site.register(LyThuyet, LyThuyetDisplay)
admin.site.register(CauHoi, CauHoiDisplay)
admin.site.register(DapAn, DapAnDisplay)