from os import stat
from urllib.request import Request
from django.http import Http404
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
        # print(post_serializer)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status = status.HTTP_201_CREATED)
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
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CafeDetailView(APIView):
    def get_object(self, cafe_no):
        try:
            return Cafe.objects.get(pk=cafe_no)
        except Cafe.DoesNotExist:
            return Http404
    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 불러옵니다.'], responses={200: 'Success'})
    def get(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)
        data_serial = CafeSerializers(cafe_data)
        return Response(data_serial.data)

    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 수정합니다.'], responses={200: 'Success'}, request_body=CafeSerializers)
    def put(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)

        #수정할  인스턴스, 수정할 내용
        update_serial  = CafeSerializers(cafe_data, data=request.data)

        if update_serial.is_valid():
            # save()를 통해 serializer의 update()메소드 실행,
            # DB 인스턴스 업데이트
            update_serial.save()
            return Response(update_serial.data, status = status.HTTP_201_CREATED)
        return Response(
            update_serial.errors, 
            status = status.HTTP_400_BAD_REQUEST)

    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 삭제합니다.'], responses={200: 'Success'})
    def delete(self, request, cafe_no):
        post = self.get_object(cafe_no)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
