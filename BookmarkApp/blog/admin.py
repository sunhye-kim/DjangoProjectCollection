from django.contrib import admin
from blog.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt',) # Pist 객체를 보여줄 때, 출력할 컬럼
    list_filter = ('modify_dt',) # modify_dt 컬럼을 사용하는 필터 사이드바 보여주도록 지정
    search_fields = ('title', 'content')  # 검색박스를 표시하고, 입력된 단어는 title, content 컬럼에서 검색하도록
    prepopulated_fields = {'slug': ('title',)} # slug 필드는 title 필드를 사용해 미리 채워지도록
    