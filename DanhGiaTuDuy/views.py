from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from datetime import timedelta
from django.utils import timezone
from .models import DeThi, NoiDungDe, LuotThi, BaiLam, KhoaHocNoiDung
from .models import CauHoi, DapAn
from django.db.models import Q
from django.utils import timezone
from User.models import StudentUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
import re
# Create your views here.
class Thi(View):
    def get(self, request):
        return render(request, 'exam.html')
class DGTD(LoginRequiredMixin, View):
    login_url = '/Userlogin/'
    
    def get(self, request, idde=None):
        if idde is None:
            return render(request, 'exam.html')
        else:
            student_id = request.session['id']
            student = StudentUser.objects.get(id=student_id)
            deThi = get_object_or_404(DeThi, id=idde)
            dict_cauhoi_list_dapan = dict()
            SetNoiDungDe = NoiDungDe.objects.filter(de_thi=deThi).order_by('thu_tu_cau')
            khoa_hoc_noi_dung_list = KhoaHocNoiDung.objects.all()
            for noiDungDe in SetNoiDungDe:
                SetDapAn = DapAn.objects.filter(cauHoi=noiDungDe.cau_hoi)
                list_dapAn = list(SetDapAn)
                dict_cauhoi_list_dapan[noiDungDe] = list_dapAn

            lenkeys = len(dict_cauhoi_list_dapan)
            thoi_gian_thi = int(deThi.thoi_gian_thi.seconds)
            content = {
                'DeThi': deThi, 
                'dictCHDA': dict_cauhoi_list_dapan,
                'lenkeys': lenkeys,
                'student': student,
                'tthi': thoi_gian_thi,
                'khoa_hoc_noi_dung_list': khoa_hoc_noi_dung_list,
            }
            return render(request, 'quiz.html', content)


def SaveBai(luot_thi, dap_an, noi_dung_de, tinh_dung, answer_text=None):
    bai_lam = BaiLam.objects.create(
        luu_bai_thi=luot_thi,
        noi_dung_de=noi_dung_de,
        dap_an=dap_an,
        tinh_dung=tinh_dung,
        answer_text=answer_text
    )
    return bai_lam

@method_decorator(csrf_protect, name='dispatch')
class ChamThi(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            selected_answers = {}
            dict_bailam_dapandung = {}
            diem = 0
            so_caudung = 0
            student = StudentUser.objects.get(id=request.session['id'])
            ma_de_thi = request.POST.get('DeThiInput')
            de_thi = get_object_or_404(DeThi, id=int(ma_de_thi))
            
            thoi_gian_con_lai_str = request.POST.get('thoiGianInput')
            thoi_gian_con_lai = self.parse_time(thoi_gian_con_lai_str)
            thoi_gian_hoan_thanh = de_thi.thoi_gian_thi - thoi_gian_con_lai

            SetNoiDungDe = NoiDungDe.objects.filter(de_thi=de_thi).order_by('thu_tu_cau')
            
            for key, value in request.POST.items():
                if key.startswith('answer_'):
                    parts = key.split('_')
                    question_number = parts[1]
                    noi_dung_de = SetNoiDungDe.filter(thu_tu_cau=int(question_number)).first()
                    if noi_dung_de:
                        if noi_dung_de not in selected_answers:
                            selected_answers[noi_dung_de] = []
                        if len(parts) > 2:  # Câu hỏi CB
                            dap_an_id = parts[2]
                            selected_answers[noi_dung_de].append((dap_an_id, value))
                        else:  # Câu hỏi TN hoặc TL
                            selected_answers[noi_dung_de].append(value)

            with transaction.atomic():
                luot_thi = LuotThi.objects.create(
                    de_thi=de_thi,
                    nguoi_lam=student,
                    thoi_diem_thi=timezone.now(),
                    thoi_gian_hoan_thanh=thoi_gian_hoan_thanh
                )

                for noi_dung_de in SetNoiDungDe:
                    bai_lam_list = []
                    values = selected_answers.get(noi_dung_de, [])
                    
                    if noi_dung_de.cau_hoi.loai_cau_hoi == 'CB':
                        cau_dung = 0
                        all_correct = True
                        for dap_an_id, value in values:
                            dapAn = DapAn.objects.filter(id=dap_an_id).first()
                            if dapAn:
                                tinh_dung = dapAn.tinh_dung
                                answer_text = dapAn.noi_dung
                                bai_lam = SaveBai(luot_thi, dapAn, noi_dung_de, tinh_dung, answer_text=answer_text)
                                
                                # Check if the answer is correct
                                is_correct = (value == 'dung' and tinh_dung) or (value == 'sai' and not tinh_dung)
                                
                                bai_lam_list.append({
                                    'cau_hoi': noi_dung_de.cau_hoi,
                                    'dap_an': dapAn,
                                    'trang_thai': 'Đã chọn' if value == 'dung' else 'Không chọn',
                                    'tinh_dung': is_correct  # Add tinh_dung for each answer
                                })
                                
                                if is_correct:
                                    cau_dung += 1
                                else:
                                    all_correct = False

                        # Tính điểm cho câu hỏi CB
                        if cau_dung == 1:
                            diem += 0.1
                        elif cau_dung == 2:
                            diem += 0.25
                        elif cau_dung == 3:
                            diem += 0.5
                        elif cau_dung == 4:
                            diem += 1
                            so_caudung += 1
                        
                        # Add overall tinh_dung for the entire CB question
                        for item in bai_lam_list:
                            if item['cau_hoi'] == noi_dung_de.cau_hoi:
                                item['tinh_dung_overall'] = all_correct
                    elif noi_dung_de.cau_hoi.loai_cau_hoi == 'TN':
                        for value in values:
                            dapAn = DapAn.objects.filter(id=value).first()
                            if dapAn:
                                tinh_dung = dapAn.tinh_dung
                                answer_text = dapAn.noi_dung
                                bai_lam = SaveBai(luot_thi, dapAn, noi_dung_de, tinh_dung, answer_text=answer_text)
                                bai_lam_list.append({
                                    'cau_hoi': noi_dung_de.cau_hoi,
                                    'dap_an': dapAn,
                                    'trang_thai': 'Đã chọn',
                                    'tinh_dung': tinh_dung
                                })
                                if tinh_dung:
                                    so_caudung += 1
                                    diem += noi_dung_de.diem_so
                    
                    elif noi_dung_de.cau_hoi.loai_cau_hoi == 'TL':
                        answer_text = values[0] if values else ""
                        dapAn = DapAn.objects.filter(cauHoi=noi_dung_de.cau_hoi, tinh_dung=True).first()
                        if dapAn and answer_text.lower().strip() == dapAn.noi_dung.lower().strip():
                            tinh_dung = True
                            so_caudung += 1
                            diem += noi_dung_de.diem_so
                        else:
                            tinh_dung = False
                        bai_lam = SaveBai(luot_thi, dapAn, noi_dung_de, tinh_dung, answer_text=answer_text)
                        bai_lam_list.append({
                            'cau_hoi': noi_dung_de.cau_hoi,
                            'dap_an': dapAn,
                            'trang_thai': 'Đã trả lời',
                            'tinh_dung': tinh_dung,
                            'answer_text': answer_text
                        })

                    dict_bailam_dapandung[noi_dung_de] = {
                        'bai_lam_list': bai_lam_list,
                        'dapan_list': list(DapAn.objects.filter(cauHoi=noi_dung_de.cau_hoi, tinh_dung=True)),
                        'dapan_sai_list': list(DapAn.objects.filter(cauHoi=noi_dung_de.cau_hoi, tinh_dung=False)),
                    }

                luot_thi.diem_so = diem
                luot_thi.so_cau_dung = so_caudung
                luot_thi.save()

            tong_so_cau = SetNoiDungDe.count()
            so_cau_sai = tong_so_cau - so_caudung
            ty_le_dung = round((so_caudung / tong_so_cau) * 100, 2) if tong_so_cau > 0 else 0

            context = {
                'LuotThi': luot_thi,
                'TongSoCau': tong_so_cau,
                'dictBLDA': dict_bailam_dapandung,
                'so_cau_dung': so_caudung,  
                'so_cau_sai': so_cau_sai,
                'ty_le_dung': ty_le_dung,
            }


            return render(request, 'danhgiatuduy_result.html', context)
        return render(request, 'homepage/index.html')

    def parse_time(self, time_str):
        parts = time_str.split(':')
        if len(parts) == 2:
            return timedelta(minutes=int(parts[0]), seconds=int(parts[1]))
        elif len(parts) == 3:
            return timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
        else:
            raise ValueError("Invalid time format")