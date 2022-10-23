from django.urls import path
from .models import CafeMain
from . import views

# from django.conf.urls import url

urlpatterns = [
    path('', views.CafeLV.as_view(), name='index'),
    path('<int:cafe_no>/', views.CafeDetailView.as_view()),
    path('menu/', views.CafeMenuLV.as_view()),
    path('menu/<int:cafe_no>/', views.CafeMenuDV.as_view()),

    path('address/', views.CafeAddressDV.as_view()),

    path('test/', views.CafeViewSet.as_view({'get':'list', 'post':'create'}))
    
]