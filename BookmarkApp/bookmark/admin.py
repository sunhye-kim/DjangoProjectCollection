from django.contrib import admin
from bookmark.models import Bookmark

@admin.register(Bookmark) # 어드민 사이트 등록
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
