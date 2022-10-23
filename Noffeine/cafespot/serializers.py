from rest_framework import serializers
from . import models

import datetime

class CafeSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.CafeMain
        # fields = ('cafe_no', 'name_kor', 'name_eng', 'tel_num', 'open_time', 'sns_url', )
        fields = '__all__'
        address = serializers.StringRelatedField(many=True)
        
    # 이걸 지정하지 않으면 레코드명이 제대로 표현되지 않음
    # def __str__(self):
    #     return self.name
    
    # def create(self, validated_data):
    #     return models.CafeMain.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.sns_url = validated_data.get('sns_url', instance.sns_url)
    #     instance.tel_num = validated_data.get('tel_num', instance.tel_num)
    #     instance.save()
    #     return instance
    
    # # to_representation : Object instances 형식을 사전(Dictionary) 형태로 변경
    # def to_representation(self, instance):
    #     # self.fields 중에서 id 필드를 다시 직렬화해 부모의 테이블에서 가져오게함
    #     self.fields['id'] = MenuRepresentationSerializer(read_only=True)
    #     return super(CafeSerializers, self).to_representation(instance)


class CafeSubNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CafeSubName
        # fields = ('cafe_no', 'name_kor', 'name_eng', 'tel_num', 'open_time', 'sns_url', )
        fields = '__all__'


class CafeFranchiseSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.CafeFranchise
        # fields = ('cafe_no', 'name_kor', 'name_eng', 'tel_num', 'open_time', 'sns_url', )
        fields = '__all__'


# MenuSerializer는 CafeSerializer를 불러와야하기 때문에,
# CafeSerializer, MenuSerializer 순으로 선언
class MenuSerializer(serializers.ModelSerializer):
    # 여러개의 메뉴가 있으므로 many 매개변수는 True로 사용
    # 카페 데이터 조회 시, 메뉴 데이터를 수정하지 않으므로 read_only 매개변수도 True 로 사용
    menu = CafeSerializers(many=True, read_only=True)

    class Meta:
        model = models.CafeMenu 
        fields = '__all__' # 모든 필드를 json으로 만들겠다.


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
    class Meta:
        model = models.CafeAddress 
        fields = '__all__' # 모든 필드를 json으로 만들겠다.
