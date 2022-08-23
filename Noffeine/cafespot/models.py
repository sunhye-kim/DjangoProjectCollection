from email.policy import default
from django.db import models

class Cafe(models.Model):
    name_kor = models.CharField('CafeName(kor)', max_length=100,blank=False)
    name_eng = models.CharField('CafeName(eng)', max_length=100, blank=False)
    tel_num = models.CharField('Tel', max_length=20)
    open_time = models.JSONField('OpenTime', default=dict)
    sns_url = models.CharField('SNS', max_length=100)
    is_operated = models.BooleanField('isOperated', default=True)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_main'
        ordering = ('-modify_dt',)
        verbose_name = 'Cafe Name'
        verbose_name_plural = 'Cafe Names'


class Menu(models.Model):
    cafe_no = models.ForeignKey('CAFE NO', on_delete=models.DO_NOTHING, related_name="Cafe", primary_key=True, db_column="cafe_no")
    menu_name = models.CharField('Menu', max_length=50, blank=False)
    price = models.IntegerField('PRICE', blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'menu_main'
        ordering = ('-modify_dt',)
        verbose_name = 'Menu Name' # 테이블 단수 별칭
        verbose_name_plural = 'Menu Names' # 테이블 복수 별칭


class CafeAddress(models.Model):
    # related_name : 추상 모델에서 관계를 정의할 때 사용
    # on_delete : 외래키가 바라보는 테이블의 값이 삭제될 때
    #   models.DO_NOTHING - 과거 데이터 유지하기 위해서 CASCADE 사용하지 않음
    # db_column : 테이블에 정의될 이름
    cafe_no = models.ForeignKey('Cafe', on_delete=models.DO_NOTHING, related_name="Cafe", primary_key=True, db_column="cafe_no")
    
    state = models.CharField('State', max_length=30, blank=False)
    city = models.CharField('City', max_length=30, blank=False)
    county = models.CharField('County', max_length=30, blank=False)
    detail_addr = models.CharField('DetailAddr', max_length=50, blank=False)

    class Meta:
        db_table = 'cafe_address'
        ordering = ('-cafe_no',)