from django.contrib import admin
from .models import Khoi, MonHoc, ChuyenDe, Sach
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
#design Chuyên đề
class ChuyenDeDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('ten_chuyen_de', 'monHoc', 'khoi', 'mo_ta')
    list_display = [
        'id',
        'ten_chuyen_de',
        'monHoc',
        'khoi',  
        'mo_ta'
    ]
    list_display_links = [
        'ten_chuyen_de'
    ]
    list_filter = [
        'monHoc',
        'khoi'
    ]
# design Môn học
class MonHocDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('ten_mon', 'mo_ta')
    list_display = [
        'id',
        'ten_mon',
        'short_mo_ta'
    ]
    list_display_links = [
        'ten_mon'
    ]
    def short_mo_ta(self, obj):
        if len(obj.mo_ta) > 100:
            return obj.mo_ta[:100] + '...'
        return obj.mo_ta

    short_mo_ta.short_description = 'Mô tả'
    # Sách display
class SachDisplay(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_bottom = False
    actions_on_top = True
    fields = ('ten_bo_sach', 'ten_nxb', 'mo_ta', 'anh', 'book_photo')
    list_display = [
        'id',
        'book_photo',
        'ten_bo_sach',
        'ten_nxb',
    ]
    list_display_links = [
        'id',
        'ten_bo_sach',
    ]
    list_filter = [
        'ten_bo_sach',
        'ten_nxb'
    ]
    readonly_fields = ('book_photo',)
# Register your models here.
admin.site.register(Khoi)
admin.site.register(MonHoc, MonHocDisplay)
admin.site.register(ChuyenDe, ChuyenDeDisplay)
admin.site.register(Sach, SachDisplay)