from django.urls import path
from django.views.generic import ListView, DetailView
from cafespot.views import CafeLV, CafeDV
from cafespot.models import Cafe

urlpatterns = [
    path('cafe/', ListView.as_view(model=Cafe), name='index'),
    path('cafe/<int:pk>', DetailView.as_view(model=Cafe), name='detail'),
]