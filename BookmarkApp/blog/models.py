
from django.db import models
from django.urls import reverse # URL 패던을 만들어주는 장고의 내장함수

class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple desctiption text.')
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    # 필드 속성 외에 필요한 파라미터는 Meta 내부 클래스로 정의
    class Meta:
        # 테이블 별칭은 단수/복수로 가질 수 있음
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        
        # 데이터베이스에 저장되는 테이블의 이름, 
        # 이걸 생략하면 "앱명_모델클래스명"으로 테이블명 지정
        db_table = 'blog_posts'

        # modify_dt 컬럼을 기준으로 내림차순 정렬
        ordering = ('-modify_dt',)
    
    def __str__(self): # 객체의 문자열을 객세.title 속성으로 표시되도록 함
        return self.title
    
    def get_absolute_url(self): # 메소드가 정의된 객체를 지칭하는 URL을 반환, reverse() 호출
        return reverse('blog:post_detail', args=(self.slug,))
    
    def get_previous(self): # 장고 내장함수인 get_previous_by_modify_dt() 호출, 최신 포스트를 먼저 보여준다.
        return self.get_previous_by_modify_dt()
    
    def get_next(self): # modify_dt 컬럼을 기준으로 다음 포스트 반환
        return self.get_next_by_modify_dt()

