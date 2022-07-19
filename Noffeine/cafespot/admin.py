from django.contrib import admin
from cafespot.models import Cafe

@admin.register(Cafe) # 어드민 사이트 등록
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name_kor', 'name_eng')