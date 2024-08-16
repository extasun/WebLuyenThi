from django.shortcuts import render
from django.views import View
from MonHoc.models import MonHoc
from LuyenTap.models import DeThi,CauHoi
from DanhGiaTuDuy.models import DeThi as DGTD
from DanhGiaNangLuc.models import DeThi as DGNL
from .forms import DeThiFilterForm
from django.db.models import Count
from LuyenTap.models import LuotThi
from DanhGiaNangLuc.models import LuotThi as LuotThiDGNL
from django.contrib.auth.decorators import login_required
import logging

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
            chuong = form.cleaned_data.get('chuyen_de')  
            bai = form.cleaned_data.get('ly_thuyet')    
            
            if mon_thi:
                queryset = queryset.filter(mon_thi=mon_thi)
            if loai_de:
                queryset = queryset.filter(loai_de=loai_de)
            if sach:
                queryset = queryset.filter(sach=sach)
            if khoi:
                queryset = queryset.filter(khoi=khoi)
            if chuong:
                queryset = queryset.filter(chuyen_de=chuong)
            if bai:
                queryset = queryset.filter(lyThuyet=bai)
        
        search_query = request.GET.get('search')
        if search_query:
            queryset = queryset.filter(ma_de__icontains=search_query) 
        
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
class DGNLView(View):
    def get(self, request):
        user = request.user
        logger = logging.getLogger(__name__)
        queryset = DGNL.objects.filter(loai_de='DGNL')
        thi_da_thi = LuotThiDGNL.objects.filter(nguoi_lam=user)
        
        thi_da_thi_ids = thi_da_thi.values_list('de_thi_id', flat=True)
        
        so_lan_thi = thi_da_thi.values('de_thi_id').annotate(count=Count('id')).order_by('de_thi_id')
        
        so_lan_thi_dict = {item['de_thi_id']: item['count'] for item in so_lan_thi}
        
        context = {
            'listDeThiDGNL': queryset,
            'thi_da_thi_ids': thi_da_thi_ids,
            'so_lan_thi_dict': so_lan_thi_dict,
        }
        return render(request, 'homepage/dgnl.html', context)
class DGNLHNView(View):
    def get(self, request):
        user = request.user
        logger = logging.getLogger(__name__)
        queryset = DGNL.objects.filter(loai_de='DGNLHN')
        thi_da_thi = LuotThiDGNL.objects.filter(nguoi_lam=user)
        
        thi_da_thi_ids = thi_da_thi.values_list('de_thi_id', flat=True)
        
        so_lan_thi = thi_da_thi.values('de_thi_id').annotate(count=Count('id')).order_by('de_thi_id')
        
        so_lan_thi_dict = {item['de_thi_id']: item['count'] for item in so_lan_thi}
        
        context = {
            'listDeThiDGNL': queryset,
            'thi_da_thi_ids': thi_da_thi_ids,
            'so_lan_thi_dict': so_lan_thi_dict,
        }
        return render(request, 'homepage/dgnl.html', context)
     