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
    cafe_no = models.IntegerField('CAFE NO', blank=False)
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
    cafe_no = models.ForeignKey('Cafe', on_delete=models.CASCADE)
    state = models.CharField('State', max_length=30, blank=False)
    city = models.CharField('City', max_length=30, blank=False)
    county = models.CharField('County', max_length=30, blank=False)
    detail_addr = models.CharField('DetailAddr', max_length=50, blank=False)

    class Meta:
        db_table = 'cafe_address'
        ordering = ('-cafe_no',)