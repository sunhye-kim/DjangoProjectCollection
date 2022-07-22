from django.urls import path
from .models import Cafe
from . import views

urlpatterns = [
    path('', views.CafeList.as_view(), name='index'),
    path('<int:cafe_no>/', views.CafeDetailView.as_view()),
    # path('Detail/', views.CafeDetailView.as_view()),
]