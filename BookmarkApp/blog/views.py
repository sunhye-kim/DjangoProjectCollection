
from django.views.generic import ListView, DetailView
from django.views.generic import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post

# Create your views here.

#-- ListView
class PostLV(ListView):
    model = Post
    template_name = 'blog/posst_all.html'
    context_object_name = 'posts'
    paginate_by = 2


#-- DetailView
class PostDV(DetailView):
    model = Post   # 다른 속성들은 지정하지 않았으므로, 디폴트값 사용


#-- ArchiveView
class PostAV(ArchiveIndexView): # 테이블로부터 객체 리스트를 가져와, 날짜 필드를 기준으로 최신 객체를 먼저 출력
    model = Post
    date_field = 'modify_dt' # 변경 날짜가 최근인 포스트를 먼저 출력

class PostYAV(YearArchiveView): # 날짜 필드의 연도를 기준으로 객체 리스트를 가져와 객체들이 속한 월을 리스트로 출력, 날짜 필드의 연도 파라미터는 URLconf에서 추출해 뷰로 넘겨줌
    model = Post
    date_field = 'modify_dt' # 기준이 되는 필드
    make_object_list = True # 해당 연도에 해당하는 객체의 리스트를 만들어서 템플릿에 넘겨줌, 템플릿 파일에서 object_list 컨텍스트 변수 사용 가능. default = False

class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'
