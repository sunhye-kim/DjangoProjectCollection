from django.db import models

class Bookmark(models.Model):
    title = models.CharField('TITLE', max_length=100, blank=True)
    url = models.URLField('URL', unique=True) # 'URL' 문구는 별칭


    # 객체를 문자열로 표현할 떄 사용하는 함수
    # 장고에서 모델 클래스의 객체는 테이블에 들어있는 레코드 하나를 의미
    def __str__(self):
        return self.title
