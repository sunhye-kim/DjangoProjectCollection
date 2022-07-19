from os import stat
from django.http import Http404
from django.db import transaction
from django.utils import timezone

from requests import Response
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cafe
from .serializers import CafeSerializers

from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

import json

class CafeList(APIView):
    # @swagger_auto_schema(tags=['카페 데이터 저장하기'], request_body=CafeSerializers)
    # @transaction.atomic
    # def post(self, request):
    #     try:
    #         r_data = json.loads(request.body)
    #         r_cafe_name_kor = r_data['name_kor']
    #         r_cafe_name_eng = r_data['name_eng']
    #         r_open_time = r_data['open_time']
    #         r_tel_num = r_data['tel_num']

    #     except:
    #         return Response({"message": "Check parameters"}, status=status.HTTP_400_BAD_REQUEST)

    #     # 데이터 존재 여부 확인
    #     # cafe_data_data = (Cafe.objects.
    #     #                             filter(Q(type=r_type) & Q(name=r_name)))

    #     cafe_data = Cafe()
    #     cafe_data.name_kor = r_cafe_name_kor
    #     cafe_data.name_eng = r_cafe_name_eng
    #     cafe_data.tel_num = r_tel_num
    #     cafe_data.open_time = r_open_time
    #     cafe_data.create_dt = timezone.now()
    #     cafe_data.modify_dt = timezone.now()

    #     cafe_data.save()

 
    #     return_data = {
    #         "detail": "success",
    #         "status" : 200
    #     }
        
    #     return Response(return_data, status = status.HTTP_201_CREATED)


    @swagger_auto_schema(operation_summary='카페 데이터 저장하기',
        operation_description="""
            카페 데이터 저장저장저장저앙
            """,
        tags=['cafe'], 
        request_body=CafeSerializers
    )
    @transaction.atomic
    def post(self, request, format=None):
        post_serializer = CafeSerializers(data=request.data)
        if post_serializer.is_valid():
            return Response(status = status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary='카페 데이터 가져와가ㅏ져와',
        operation_description="""
            카페 데이터 가져오기
            """,
        tags=['cafe']
    )
    def get(self, request):
        queryset = Cafe.objects.all()
        serializer = CafeSerializers(queryset, many=True)

        return Response(serializer.data)


class CafeDetailView(APIView):
    def get_object(self, cafe_no):
        try:
            return Cafe.objects.get(pk=cafe_no)
        except Cafe.DoesNotExist:
            return Http404
    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 불러옵니다.'], responses={200: 'Success'})
    def get(self, request, cafe_no):
        post = self.get_object(cafe_no)
        serializer = CafeSerializers(post)
        return Response(serializer.data)

    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 수정합니다.'], responses={200: 'Success'})
    def put(self, request, cafe_no):
        post = self.get_object(cafe_no)
        serializer = CafeSerializers(post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 삭제합니다.'], responses={200: 'Success'})
    def delete(self, request, cafe_no):
        post = self.get_object(cafe_no)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
