from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from datetime import timedelta
from django.utils import timezone
from .models import DeThi, NoiDungDe, LuotThi, BaiLam
from .models import CauHoi, DapAn
from django.db.models import Q
from django.utils import timezone
from User.models import StudentUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
class Thi(View):
    def get(self, request):
        return render(request, 'exam.html')
class DGNLSelectSubject(LoginRequiredMixin, View):
    login_url = '/Userlogin/'

    def get(self, request, idde):
        de_thi = get_object_or_404(DeThi, id=idde)
        subjects = CauHoi.SUBJECT_CHOICES
        context = {
            'de_thi': de_thi,
            'subjects': subjects,
        }
        return render(request, 'select_subjects.html', context)

    def post(self, request, idde):
        selected_subjects_keys = request.POST.getlist('mon_hoc')  # Lấy danh sách key từ form
        selected_subjects = []

        # Tạo danh sách tuples (key, value) từ selected_subjects_keys
        for key in selected_subjects_keys:
            for choice_key, choice_value in CauHoi.SUBJECT_CHOICES:
                if key == choice_key:
                    selected_subjects.append((key, choice_value))
                    break

        if len(selected_subjects) != 3:
            return redirect('DanhGiaNangLuc:select_subjects', idde=idde)

        request.session['selected_subjects'] = selected_subjects
        return redirect('DanhGiaNangLuc:dgnl_id', idde=idde)

class DGNL(LoginRequiredMixin, View):
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

            # Lấy danh sách môn học đã chọn từ session
            selected_subjects = request.session.get('selected_subjects', [])
            
            for noiDungDe in SetNoiDungDe:
                # Lọc câu hỏi theo môn học đã chọn
                if noiDungDe.cau_hoi.subject in [subject[0] for subject in selected_subjects] or noiDungDe.cau_hoi.language or noiDungDe.cau_hoi.phan_2:
                    SetDapAn = DapAn.objects.filter(cauHoi=noiDungDe.cau_hoi)
                    list_dapAn = list(SetDapAn)
                    dict_cauhoi_list_dapan[noiDungDe] = list_dapAn

            lenkeys = len(dict_cauhoi_list_dapan)
            thoi_gian_thi = int(deThi.thoi_gian_thi.total_seconds())
            content = {
                'DeThi': deThi, 
                'dictCHDA': dict_cauhoi_list_dapan,
                'lenkeys': lenkeys,
                'student': student,
                'tthi': thoi_gian_thi,
                'selected_subjects': selected_subjects, # Truyền các môn học đã chọn vào context
            }
            return render(request, 'dgnl.html', content)
def SaveBai(luotthix, dapan, noidungde, tinhdung):
        bai_lam = BaiLam(
            luu_bai_thi = luotthix,
            dap_an = dapan,
            noi_dung_de = noidungde,
            tinh_dung = tinhdung,
        )
        bai_lam.save()

@method_decorator(csrf_protect, name='dispatch')
class ChamThi(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            selected_answers = {}
            dict_bailam_dapandung = dict()
            diem = 0
            so_caudung = 0
            student_id = request.session['id']
            student = StudentUser.objects.get(id=student_id)
            # Lấy giá trị của DeThi
            ma_de_thi = request.POST.get('DeThiInput', None) 
            de_thi_x = get_object_or_404(DeThi, id=int(ma_de_thi))   
            thoi_gian_con_lai_str = request.POST.get('thoiGianInput', None)     
            thoi_gian_thi = de_thi_x.thoi_gian_thi
            if thoi_gian_con_lai_str:
                # Tách chuỗi thoi_gian_con_lai theo dấu hai chấm
                parts = thoi_gian_con_lai_str.split(':') 
                # Chuyển đổi chuỗi thành các giá trị giờ, phút, giây
                if len(parts) == 2:
                    # Nếu chỉ có phút và giây
                    m, s = map(int, parts)
                    h = 0
                elif len(parts) == 3:
                    # Nếu có giờ, phút và giây
                    h, m, s = map(int, parts)
                else:
                    # Xử lý trường hợp định dạng không hợp lệ
                    raise ValueError("Invalid time format for thoi_gian_con_lai")
            thoi_gian_con_lai = timedelta(hours=h, minutes=m, seconds=s)
            thoi_gian_hoan_thanh = thoi_gian_thi - thoi_gian_con_lai
            SetNoiDungDe = NoiDungDe.objects.filter(de_thi=de_thi_x).order_by('thu_tu_cau')
            tong_so_cau = len(SetNoiDungDe)
            tong_cau_tn = 0
            tong_cau_ngan = 0
            tn_dung = 0
            ngan_dung = 0
            list_diem_DS = list()
            for key in request.POST:
                if key.startswith('group'):
                    question_number = key[5:]  # Lấy số thứ tự câu hỏi từ key
                    try:
                        noi_dung_de_temp = SetNoiDungDe.filter(thu_tu_cau=question_number).first()
                        selected_answers[noi_dung_de_temp] = request.POST.getlist(key)
                    except NoiDungDe.DoesNotExist:
                        print(f"Không tìm thấy NoiDungDe với thu_tu_cau={question_number}")
                    #selected_answers[SetNoiDungDe.get(thu_tu_cau=question_number)] = request.POST.getlist(key)
            try:
                with transaction.atomic():
                    luot_thi = LuotThi(
                        de_thi=de_thi_x,  # Lỗi sẽ xảy ra ở đây
                        nguoi_lam=student, 
                        diem_so=0,
                        thoi_diem_thi=timezone.now(),
                        thoi_gian_hoan_thanh=timedelta(minutes=0),
                        so_cau_dung=0
                    )
                    luot_thi.save()
                    for noi_dung_de, value in selected_answers.items():      
                        if noi_dung_de is not None:
                            if noi_dung_de.cau_hoi.loai_cau_hoi == 'TN':
                                tong_cau_tn += 1
                                dapAn = DapAn.objects.filter(id=value[0]).first()
                                if dapAn.tinh_dung == True:
                                    tn_dung +=1
                                    so_caudung += 1
                                    diem += noi_dung_de.diem_so
                                    SaveBai(luot_thi, dapAn, noi_dung_de, True)
                                else:
                                    SaveBai(luot_thi, dapAn, noi_dung_de, False)
                            elif noi_dung_de.cau_hoi.loai_cau_hoi == 'DS':
                                check_sai = False
                                diem_cau_nay = 0
                                list_da_dung = DapAn.objects.filter(cauHoi=noi_dung_de.cau_hoi, tinh_dung=True)
                                diem_thanh_phan = round((noi_dung_de.diem_so/len(list_da_dung)),2) if len(list_da_dung) != 0 else noi_dung_de.diem_so
                                for i in value:
                                    dapAnDS = DapAn.objects.get(id=i)
                                    print(dapAnDS.noi_dung)
                                    if list_da_dung.filter(id=i).exists():
                                        diem_cau_nay += diem_thanh_phan
                                        SaveBai(luot_thi, dapAnDS, noi_dung_de, True)
                                    else:
                                        SaveBai(luot_thi, dapAnDS, noi_dung_de, False)
                                        check_sai = True
                                        diem_cau_nay -= (diem_thanh_phan if diem_cau_nay!=0 else 0)
                                if diem_cau_nay != 0 and not check_sai:
                                    so_caudung += 1
                                    diem += diem_cau_nay
                                    string = str('Câu '+str(noi_dung_de.thu_tu_cau)+": "+str(diem_cau_nay))
                                    list_diem_DS.append(string) 
                                else:
                                    string = str('Câu '+str(noi_dung_de.thu_tu_cau)+": 0")
                                    list_diem_DS.append(string)
                            else :
                                tong_cau_ngan += 1
                                str_dap_an = str(value[0])
                                list_da_dung = DapAn.objects.filter(cauHoi=noi_dung_de.cau_hoi, tinh_dung=True)
                                da_sai = DapAn.objects.filter(tinh_dung=False, cauHoi = noi_dung_de.cau_hoi).first()
                                for str_da_dung in list_da_dung:
                                    if str_da_dung.noi_dung == str_dap_an.lower():
                                        so_caudung += 1
                                        diem += noi_dung_de.diem_so
                                        ngan_dung += 1
                                        SaveBai(luot_thi, str_da_dung, noi_dung_de, True)
                                        break
                                    else:
                                        SaveBai(luot_thi, da_sai, noi_dung_de, False)
            except Exception as e:
                print(f'Đã xảy ra lỗi: {e}')        
            luot_thi.diem_so = diem
            luot_thi.so_cau_dung = so_caudung
            luot_thi.thoi_gian_hoan_thanh = thoi_gian_hoan_thanh
            luot_thi.save()
            danh_sach_bai_lam = BaiLam.objects.filter(luu_bai_thi=luot_thi).select_related('noi_dung_de').order_by('noi_dung_de__thu_tu_cau')
            for noidungde in SetNoiDungDe:
                bai_lam_list = danh_sach_bai_lam.filter(Q(noi_dung_de=noidungde) | Q(noi_dung_de__isnull=True))
                dapAnDung = DapAn.objects.filter(cauHoi=noidungde.cau_hoi, tinh_dung = True)
                dict_bailam_dapandung[noidungde] = {
                    'bai_lam_list': list(bai_lam_list),
                    'dapan_list': list(dapAnDung)
                }
            context = {
                'LuotThi': luot_thi,
                'TongSoCau': tong_so_cau,
                'dictBLDA': dict_bailam_dapandung,
                'tong_tn': tong_cau_tn,
                'tn_dung': tn_dung,
                'tong_ngan': tong_cau_ngan,
                'ngan_dung': ngan_dung,
                'diem_DS': list_diem_DS,
            }
            print(list_diem_DS)
            # print(ma_de_thi)
            # print(thoi_gian_hoan_thanh)
            # print(dict_bailam_dapandung)
            return render(request, 'result.html', context)
        return render(request, 'homepage/index.html')
    