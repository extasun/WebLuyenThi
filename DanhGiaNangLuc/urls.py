# urls.py
from django.urls import path
from .views import ChamThi, DGNL, DGNLSelectSubject
app_name = 'DanhGiaNangLuc'
urlpatterns = [
    path('chamthi/', ChamThi.as_view(), name='chamthi'),
    path('ok/', DGNL.as_view(), name= 'dgnl'),
    path('dgnl/<int:idde>/', DGNL.as_view(), name= 'dgnl_id'),
    path('dgnl/<int:idde>/select-subjects/', DGNLSelectSubject.as_view(), name='select_subjects'),
]