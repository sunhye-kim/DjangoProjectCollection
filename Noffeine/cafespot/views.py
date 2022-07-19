from django.http import Http404
from django.db import transaction

from requests import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cafe
from .serializers import CafeSerializers

from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

import json

class CafeList(APIView):
    @swagger_auto_schema(tags=['카페 데이터 저장하기'], request_body=CafeSerializers)
    @transaction.atomic
    def post(self, request):
        serializer = CafeSerializers(data=request.data)

        print(serializer)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


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
