from rest_framework import serializers
from . import models

import datetime


class CafeSerializers(serializers.ModelSerializer):
    cafe_id = serializers.CharField(read_only=True)  # FK 때문에 선언

    class Meta:
        model = models.CafeMain
        fields = "__all__"
        # address = serializers.StringRelatedField(many=True)


class CafeSubNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CafeSubName
        # fields = ('cafe_no', 'name_kor', 'name_eng', 'tel_num', 'open_time', 'sns_url', )
        fields = "__all__"


class CafeFranchiseSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.CafeFranchise
        # fields = ('cafe_no', 'name_kor', 'name_eng', 'tel_num', 'open_time', 'sns_url', )
        fields = "__all__"


# MenuSerializer는 CafeSerializer를 불러와야하기 때문에,
# CafeSerializer, MenuSerializer 순으로 선언
class MenuSerializer(serializers.ModelSerializer):
    # 여러개의 메뉴가 있으므로 many 매개변수는 True로 사용
    # 카페 데이터 조회 시, 메뉴 데이터를 수정하지 않으므로 read_only 매개변수도 True 로 사용
    menu = CafeSerializers(many=True, read_only=True)

    class Meta:
        model = models.CafeMenu
        fields = "__all__"  # 모든 필드를 json으로 만들겠다.


# MenuRepresentationSerializer는 MenuSerializer와 클래스 형태가 비슷하나
# menu 필드를 사용하지 않음
#
class MenuRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CafeMenu
        fields = ("id", "menu_name", "price")


# MenuSerializer는 CafeSerializer를 불러와야하기 때문에,
# CafeSerializer, MenuSerializer 순으로 선언
class CafeAddressSerializer(serializers.ModelSerializer):
    cafe_id = serializers.CharField(
        source="cafe_main.name", read_only=True
    )  # FK 때문에 선언
    # cafe_id = serializers.StringRelatedField(source='cafe_main', read_only=True)

    class Meta:
        model = models.CafeAddress
        fields = "__all__"  # 모든 필드를 json으로 만들겠다.
