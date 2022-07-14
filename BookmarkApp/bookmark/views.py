from django.shortcuts import render

from django.views.generic import ListView, DetailView # 제네릭 뷰를 사용하기 위함
from bookmark.models import Bookmark

class BookmarkLV(ListView):
    model = Bookmark

class BookmarkDV(DetailView):
    model = Bookmark