
from django.urls import path
from .views import HomeView, LuyenThiView, DGTDView, DGNLView, DGNLHNView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('luyenthi/', LuyenThiView.as_view(), name='luyenthi'),
    path('dgtd/', DGTDView.as_view(), name='dgtd'),
    path('dgnl/', DGNLView.as_view(), name='dgnl'),
    path('dgnl_hn/', DGNLHNView.as_view(), name='dgnl_hn'),
]