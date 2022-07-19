from django.urls import path
from .models import Cafe
from . import views

urlpatterns = [
    path('', views.CafeList.as_view(), name='index'),
    path('<int:cafe_no>/', views.CafeList.as_view())
    # path('<int:pk>', views.CafeDetail.as_view(model=Cafe), name='detail'),
]