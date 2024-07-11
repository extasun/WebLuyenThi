from django.urls import path
from .views import Thi, DGTD, ChamThi
app_name = 'luyentap'
urlpatterns = [
    path('thi/', Thi.as_view(), name= 'thi'),
    path('dgtd/', DGTD.as_view(), name= 'dgtd'),
    path('dgtd/<int:idde>/', DGTD.as_view(), name= 'dgtd_id'),
    path('chamthi/', ChamThi.as_view(), name='chamthi'),
]