from django.views.generic import ListView, DetailView
from cafespot.models import Cafe, Menu, CafeAddress

class CafeLV(ListView):
    model = Cafe

class CafeDV(DetailView):
    model = Cafe
