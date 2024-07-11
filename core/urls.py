
from django.urls import path
from .views import HomeView, LuyenThiView, DGTDView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('luyenthi/', LuyenThiView.as_view(), name='luyenthi'),
    path('dgtd/', DGTDView.as_view(), name='dgtd'),
]