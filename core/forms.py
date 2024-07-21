from django import forms
from MonHoc.models import MonHoc, Sach, ChuyenDe, Khoi
from NoiDung.models import LyThuyet

# class DeThiFilterForm(forms.Form):
#     khoi = forms.ModelChoiceField(queryset=Khoi.objects.all(), required=False, label='Khối')
#     sach = forms.ModelChoiceField(queryset=Sach.objects.all(), required=False, label='Sách')
#     mon_thi = forms.ModelChoiceField(queryset=MonHoc.objects.all(), required=False, label='Môn thi')
#     chuyen_de = forms.ModelChoiceField(queryset=ChuyenDe.objects.all(), required=False, label='Chương')
#     ly_thuyet = forms.ModelChoiceField(queryset=LyThuyet.objects.all(), required=False, label='Bài')
#     def __init__(self, *args, **kwargs):
#         super(DeThiFilterForm, self).__init__(*args, **kwargs)

#         # Nếu có 'khoi' trong dữ liệu, lọc 'chuyen_de' theo 'khoi'
#         if 'khoi' in self.data:
#             try:
#                 khoi_id = int(self.data.get('khoi'))
#                 self.fields['chuyen_de'].queryset = ChuyenDe.objects.filter(khoi_id=khoi_id).order_by('ten_chuyen_de')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to all ChuyenDe queryset
#         elif self.initial.get('khoi'):
#             self.fields['chuyen_de'].queryset = ChuyenDe.objects.filter(khoi=self.initial['khoi']).order_by('ten_chuyen_de')

#         # Nếu có 'mon_thi' trong dữ liệu, lọc 'chuyen_de' theo 'mon_thi'
#         if 'mon_thi' in self.data:
#             try:
#                 mon_thi_id = int(self.data.get('mon_thi'))
#                 self.fields['chuyen_de'].queryset = self.fields['chuyen_de'].queryset.filter(monHoc_id=mon_thi_id)
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to all ChuyenDe queryset
#         elif self.initial.get('mon_thi'):
#             self.fields['chuyen_de'].queryset = self.fields['chuyen_de'].queryset.filter(monHoc=self.initial['mon_thi'])

#          # Nếu có 'chuyen_de' trong dữ liệu, lọc 'ly_thuyet' theo 'chuyen_de'
#         if 'chuyen_de' in self.data:
#             try:
#                 chuyen_de_id = int(self.data.get('chuyen_de'))
#                 self.fields['ly_thuyet'].queryset = LyThuyet.objects.filter(chuyenDe_id=chuyen_de_id).order_by('tieu_de')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty LyThuyet queryset
#         elif self.initial.get('chuyen_de'):
#             self.fields['ly_thuyet'].queryset = LyThuyet.objects.filter(chuyenDe=self.initial['chuyen_de']).order_by('tieu_de')
from django import forms
from MonHoc.models import MonHoc, Sach, ChuyenDe, Khoi
from NoiDung.models import LyThuyet

class DeThiFilterForm(forms.Form):
    khoi = forms.ModelChoiceField(queryset=Khoi.objects.all(), required=False, label='Khối')
    sach = forms.ModelChoiceField(queryset=Sach.objects.all(), required=False, label='Sách')
    mon_thi = forms.ModelChoiceField(queryset=MonHoc.objects.all(), required=False, label='Môn thi')
    chuyen_de = forms.ModelChoiceField(queryset=ChuyenDe.objects.all(), required=False, label='Chương')
    ly_thuyet = forms.ModelChoiceField(queryset=LyThuyet.objects.all(), required=False, label='Bài')

    def __init__(self, *args, **kwargs):
        super(DeThiFilterForm, self).__init__(*args, **kwargs)

        # Nếu có 'khoi' trong dữ liệu, lọc 'chuyen_de' theo 'khoi'
        if 'khoi' in self.data:
            try:
                khoi_id = int(self.data.get('khoi'))
                self.fields['chuyen_de'].queryset = ChuyenDe.objects.filter(khoi_id=khoi_id).order_by('ten_chuyen_de')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to all ChuyenDe queryset
        elif self.initial.get('khoi'):
            self.fields['chuyen_de'].queryset = ChuyenDe.objects.filter(khoi=self.initial['khoi']).order_by('ten_chuyen_de')

        # Nếu có 'mon_thi' trong dữ liệu, lọc 'chuyen_de' theo 'mon_thi'
        if 'mon_thi' in self.data:
            try:
                mon_thi_id = int(self.data.get('mon_thi'))
                self.fields['chuyen_de'].queryset = self.fields['chuyen_de'].queryset.filter(monHoc_id=mon_thi_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to all ChuyenDe queryset
        elif self.initial.get('mon_thi'):
            self.fields['chuyen_de'].queryset = self.fields['chuyen_de'].queryset.filter(monHoc=self.initial['mon_thi'])

        # Nếu có 'chuyen_de' trong dữ liệu, lọc 'ly_thuyet' theo 'chuyen_de'
        if 'chuyen_de' in self.data:
            try:
                chuyen_de_id = int(self.data.get('chuyen_de'))
                self.fields['ly_thuyet'].queryset = LyThuyet.objects.filter(chuyenDe_id=chuyen_de_id).order_by('tieu_de')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty LyThuyet queryset
        elif self.initial.get('chuyen_de'):
            self.fields['ly_thuyet'].queryset = LyThuyet.objects.filter(chuyenDe=self.initial['chuyen_de']).order_by('tieu_de')

