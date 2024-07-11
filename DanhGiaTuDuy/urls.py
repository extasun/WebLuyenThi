# urls.py
from django.urls import path
from .views import ChamThi, DGTD
app_name = 'DanhGiaTuDuy'
urlpatterns = [
    path('chamthi/', ChamThi.as_view(), name='chamthi'),
    path('ok/', DGTD.as_view(), name= 'dgtd'),
    path('dgtd/<int:idde>/', DGTD.as_view(), name= 'dgtd_id'),
]