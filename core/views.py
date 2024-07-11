from django.shortcuts import render
from django.views import View
from MonHoc.models import MonHoc
from LuyenTap.models import DeThi,CauHoi
from DanhGiaTuDuy.models import DeThi as DGTD
from .forms import DeThiFilterForm
# Create your views here.
class HomeView(View):
    def get(self, request):
        SetMonHoc = MonHoc.objects.all()
        SetDeThi = DeThi.objects.all()
        list_de_thi_active = list(SetDeThi[:5])
        if len(SetDeThi) > 5:
            list_de_thi_hidden = list(SetDeThi[5:10])
        else:
            list_de_thi_hidden = list_de_thi_active
        context = {
            'listMonHoc': SetMonHoc,
            'listDeThiActive' : list_de_thi_active,
            'listDeThiHidden' : list_de_thi_hidden,
        }
        return render(request, 'homepage/index.html', context)
class LuyenThiView(View):
    def get(self, request):
        form = DeThiFilterForm(request.GET)
        queryset = DeThi.objects.all()

        if form.is_valid():
            mon_thi = form.cleaned_data.get('mon_thi')
            loai_de = form.cleaned_data.get('loai_de')
            sach = form.cleaned_data.get('sach')
            khoi = form.cleaned_data.get('khoi')
            chuyen_de = form.cleaned_data.get('chuyen_de')
            ly_thuyet = form.cleaned_data.get('ly_thuyet')
            
            if mon_thi:
                queryset = queryset.filter(mon_thi=mon_thi)
            if loai_de:
                queryset = queryset.filter(loai_de=loai_de)
            if sach:
                queryset = queryset.filter(sach=sach)
            if khoi:
                queryset = queryset.filter(khoi=khoi)
            if chuyen_de:
                queryset = queryset.filter(noidungde__cau_hoi__chuyenDe=chuyen_de).distinct()
            if ly_thuyet:
                queryset = queryset.filter(noidungde__cau_hoi__lyThuyet=ly_thuyet).distinct()    
        context = {
            'form': form,
            'listDeThiActive': queryset,
        }
        return render(request, 'homepage/luyenthi.html', context)
class DGTDView(View):
    def get(self, request):
        queryset = DGTD.objects.filter(loai_de=DGTD.DANH_GIA_TU_DUY)
        context = {
            'listDeThiDGTD': queryset,
        }
        return render(request, 'homepage/dgtd.html', context)

        