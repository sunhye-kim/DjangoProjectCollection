from django.urls import path, re_path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostLV_as_view(), name='index'),
    path('post/', views.PostSB.as_view, name='post_list'),
]