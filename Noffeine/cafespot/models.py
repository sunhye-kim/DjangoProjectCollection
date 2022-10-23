from django.db import models

class CafeMain(models.Model):
    cafe_id = models.BigAutoField(primary_key=True)
    main_name = models.CharField('CafeName(Main)', max_length=165, blank=False)
    is_operated = models.BooleanField('isOperated', default=1)
    is_franchise = models.BooleanField('isFranchised', default=False) # 컬럼명 확인
    phone = models.CharField('phone', max_length=15)
    hours = models.JSONField('OpenTime', default=dict)
    sns = models.JSONField('SNS', default=dict)
    registrant = models.CharField('registrant', max_length=20)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_main'
        ordering = ('-modify_dt',)
        verbose_name = 'Cafe Main'
        # verbose_name_plural = 'Cafe Mains'


class CafeSubName(models.Model):
    cafe_sub_name_id = models.BigAutoField(primary_key=True)
    sub_name = models.CharField('CafeName(Sub)', max_length=100, blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    cafe_id = models.ForeignKey(CafeMain, on_delete=models.DO_NOTHING, related_name='cafe_sub_name', db_column='cafe_id')

    class Meta:
        db_table = 'cafe_sub_name'
        ordering = ('-modify_dt',)
        verbose_name = 'Cafe Name'
        verbose_name_plural = 'Cafe Names'


class CafeFranchise(models.Model):
    cafe_id = models.OneToOneField(CafeMain, primary_key=True, on_delete=models.DO_NOTHING, related_name='cafe_franchise', db_column='cafe_id')
    branch_name = models.CharField('Menu', max_length=100, blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_franchise'
        ordering = ('-modify_dt',)
        verbose_name = 'Menu Franchise' # 테이블 단수 별칭
        verbose_name_plural = 'Menu Franchises' # 테이블 복수 별칭


class CafeMenu(models.Model):
    menu_id = models.BigAutoField(primary_key=True)
    name = models.CharField('Menu', max_length=40, blank=False)
    price = models.PositiveIntegerField('PRICE', blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    cafe_id = models.ForeignKey(CafeMain, on_delete=models.DO_NOTHING, related_name='cafe_menu', db_column='cafe_id')

    class Meta:
        db_table = 'cafe_menu'
        ordering = ('-modify_dt',)
        verbose_name = 'Menu Name' # 테이블 단수 별칭
        verbose_name_plural = 'Menu Names' # 테이블 복수 별칭


class CafeMenuImage(models.Model):
    menu_image_id = models.BigAutoField(primary_key=True)
    image_url = models.CharField('Menu', max_length=2000, blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    cafe_id = models.ForeignKey(CafeMain, on_delete=models.DO_NOTHING, related_name='cafe_menu_image', db_column='cafe_id')

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

    cafe_id = models.OneToOneField(CafeMain, primary_key=True, on_delete=models.DO_NOTHING, related_name='cafe_address', db_column='cafe_id')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    sido = models.CharField('시도', max_length=40, blank=False)
    sigungu = models.CharField('시군구', max_length=40, blank=False)
    doro = models.CharField('도로명', max_length=40, blank=False)
    doro_code = models.CharField('도로명코드', max_length=10, blank=False)
    sangse = models.CharField('상세주소', max_length=165, blank=True, default=None)

    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        db_table = 'cafe_address'
        ordering = ('-cafe_id',)

