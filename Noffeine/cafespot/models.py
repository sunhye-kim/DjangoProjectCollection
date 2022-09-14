from email.policy import default
from django.db import models

class CafeMain(models.Model):
    cafe_id = models.AutoField(primary_key=True)
    name = models.CharField('CafeName(Main)', max_length=165, blank=False)
    # name_eng = models.CharField('CafeName(eng)', max_length=100, blank=False)
    is_operated = models.BooleanField('isOperated', default=True)
    is_franchised = models.BBooleanField('isFranchised', default=False)
    phone = models.CharField('phone', max_length=20)
    # tel_num = models.CharField('Tel', max_length=20)
    hours = models.JSONField('OpenTime', default=dict)
    # open_time = models.JSONField('OpenTime', default=dict)
    sns = models.JSONField('SNS', default=dict)
    # sns_url = models.CharField('SNS', max_length=100)
    registrant = models.CharField('registrant', max_length=20)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_main'
        ordering = ('-modify_dt',)
        verbose_name = 'Cafe Name'
        verbose_name_plural = 'Cafe Names'


class CafeFranchise(models.Model):
    cafe_id = models.ForeignKey('CafeMain', primary_key=True, on_delete=models.DO_NOTHING, related_name='M_cafe_no', db_column='cafe_id')
    # cafe_no = models.ForeignKey('CafeMain', on_delete=models.DO_NOTHING, related_name='M_cafe_no', db_column='cafe_no')
    branch_name = models.CharField('Menu', max_length=50, blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_franchise'
        ordering = ('-modify_dt',)
        verbose_name = 'Menu Franchise' # 테이블 단수 별칭
        verbose_name_plural = 'Menu Franchises' # 테이블 복수 별칭


class CafeMenu(models.Model):
    cafe_id = models.ForeignKey('CafeMain', primary_key=True, on_delete=models.DO_NOTHING, related_name='M_cafe_no', db_column='cafe_id')
    # cafe_no = models.ForeignKey('CafeMain', on_delete=models.DO_NOTHING, related_name='M_cafe_no', db_column='cafe_no')
    menu_name = models.CharField('Menu', max_length=50, blank=False)
    price = models.IntegerField('PRICE', blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_menu'
        ordering = ('-modify_dt',)
        verbose_name = 'Menu Name' # 테이블 단수 별칭
        verbose_name_plural = 'Menu Names' # 테이블 복수 별칭


class CafeMenuImage(models.Model):
    cafe_id = models.ForeignKey('CafeMain', primary_key=True, on_delete=models.DO_NOTHING, related_name='M_cafe_no', db_column='cafe_id')
    # cafe_no = models.ForeignKey('CafeMain', on_delete=models.DO_NOTHING, related_name='M_cafe_no', db_column='cafe_no')
    image_url = models.CharField('Menu', max_length=2000, blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_menu_image'
        ordering = ('-modify_dt',)
        verbose_name = 'Menu Name Image' # 테이블 단수 별칭
        verbose_name_plural = 'Menu Name Images' # 테이블 복수 별칭


class CafeAddress(models.Model):
    # related_name : 추상 모델에서 관계를 정의할 때 사용
    # on_delete : 외래키가 바라보는 테이블의 값이 삭제될 때
    #   models.DO_NOTHING - 과거 데이터 유지하기 위해서 CASCADE 사용하지 않음
    # db_column : 테이블에 정의될 이름

    cafe_id = models.ForeignKey(CafeMain, primary_key=True, on_delete=models.DO_NOTHING, related_name="CA_cafe_no", db_column="cafe_id")
    # cafe_no = models.ForeignKey(CafeMain, on_delete=models.DO_NOTHING, related_name="CA_cafe_no", db_column="cafe_no")
    latitude = models.DecimalField(max_digits=6)
    longitude = models.DecimalField(max_digits=6)
    sido = models.CharField('시도', max_length=40, blank=False)
    sigungu = models.CharField('시군구', max_length=40, blank=False)
    doro = models.CharField('도로명', max_length=40, blank=False)
    doro_code = models.CharField('도로명코드', max_length=10, blank=False)
    sangse = models.CharField('상세주소', max_length=165, blank=False)
    # state = models.CharField('State', max_length=30, blank=False)
    # city = models.CharField('City', max_length=30, blank=False)
    # county = models.CharField('County', max_length=30, blank=False)
    # detail_addr = models.CharField('DetailAddr', max_length=50, blank=False)

    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_address'
        ordering = ('-cafe_id',)

