from django.contrib import admin
from cafespot.models import CafeMain

@admin.register(CafeMain) # 어드민 사이트 등록
class CafeAdmin(admin.ModelAdmin):
    list_display = ['main_name']