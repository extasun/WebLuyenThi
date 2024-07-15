from django.contrib import admin
from .models import CauHoi, DapAn, DeThi, NoiDungDe, LuotThi, BaiLam
from django.utils.html import format_html

class DapAnInline(admin.TabularInline):
    model = DapAn
    extra = 1

class CauHoiAdmin(admin.ModelAdmin):
    list_display = ('noi_dung', 'loai_cau_hoi', 'language', 'subject', 'ch_photo')
    list_filter = ('loai_cau_hoi', 'language', 'subject')
    inlines = [DapAnInline]
    readonly_fields = ('ch_photo',)

    def ch_photo(self, obj):
        return obj.ch_photo()
    ch_photo.short_description = 'Image'

class NoiDungDeInline(admin.TabularInline):
    model = NoiDungDe
    extra = 1

class DeThiAdmin(admin.ModelAdmin):
    list_display = ('ten_de_thi', 'loai_de', 'thoi_gian_thi')
    inlines = [NoiDungDeInline]

class BaiLamAdmin(admin.ModelAdmin):
    list_display = ('luu_bai_thi', 'dap_an', 'noi_dung_de', 'tinh_dung')
    list_filter = ('luu_bai_thi__de_thi', 'tinh_dung')
    search_fields = ('luu_bai_thi__nguoi_lam__username', 'noi_dung_de__cau_hoi__noi_dung')

    def dap_an(self, obj):
        return format_html('<img src="{}" width="50"/>', obj.dap_an.anh.url) if obj.dap_an.anh else '-'
    dap_an.short_description = 'Choice Image'

admin.site.register(CauHoi, CauHoiAdmin)
admin.site.register(DapAn)
admin.site.register(DeThi, DeThiAdmin)
admin.site.register(NoiDungDe)
admin.site.register(LuotThi)
admin.site.register(BaiLam, BaiLamAdmin)