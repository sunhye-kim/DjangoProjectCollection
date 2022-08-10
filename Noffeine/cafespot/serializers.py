from rest_framework import serializers
from . import models

import datetime

class CafeSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name_kor = serializers.CharField(help_text='카페이름(한국어)')
    name_eng = serializers.CharField(help_text='카페이름(영어)')
    tel_num = serializers.CharField(help_text='전화번호', required=False)
    open_time = serializers.JSONField(help_text='영업시간')
    sns_url = serializers.CharField(help_text='SNS url', required=False)
    create_dt = serializers.DateTimeField(help_text='등록시간', default=datetime.datetime.now())
    modify_dt = serializers.DateTimeField(help_text='수정시간', default=datetime.datetime.now())

    class Meta:
        model = models.Cafe 
        fields = '__all__' # 모든 필드를 json으로 만들겠다.
        read_only_fields = ['id','create_dt']
        
    # 이걸 지정하지 않으면 레코드명이 제대로 표현되지 않음
    def __str__(self):
        return self.name_kor
    
    def create(self, validated_data):
        print("create@@")
        return models.Cafe.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.sns_url = validated_data.get('sns_url', instance.sns_url)
        instance.tel_num = validated_data.get('tel_num', instance.tel_num)
        instance.save()
        return instance


class CafeMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu 
        fields = '__all__' # 모든 필드를 json으로 만들겠다.

