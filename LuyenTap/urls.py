from django.urls import path
from .views import Thi, Online, ChamThi
app_name = 'luyentap'
urlpatterns = [
    path('thi/', Thi.as_view(), name= 'thi'),
    path('/online/', Online.as_view(), name= 'dgtd'),
    path('/online/<int:idde>/', Online.as_view(), name= 'dgtd_id'),
    path('chamthi/', ChamThi.as_view(), name='chamthi'),
]