from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from requests import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

import json

from .models import CafeAddress, CafeMain, CafeMenu
from . import serializers

from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


class CafeLV(APIView):
    def __init__(self):
        self.default_page = "1"
        self.default_page_size = "10"

    """
    HTTP Method : GET
    Parameter Example : 
        http://127.0.0.1:8000/cafespot/?page=1&page_size=10
    """
    @swagger_auto_schema(operation_summary='카페 전체 데이터 리스트',
        operation_description="""
            카페 리스트 데이터 가져오기
            """,
        tags=['cafe']
    )
    def get(self, request):
        print(request)
        page = request.GET.get("page", self.default_page)
        page_size = request.GET.get("page_size", self.default_page_size)

        print(page, page_size)
        # 숫자 에러 처리
        if page.isnumeric():
            page = int(page or 1)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if page_size.isnumeric():
            page_size = int(page_size or 10)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        limit_cnt = page_size * page
        offset_cnt = limit_cnt - page_size

        """
            주소 데이터가 없는 경우 처리를 해야함
        """
        # queryset = CafeMain.objects.select_related('cafe_id')
        # print("############### query set")
        # print(queryset)
        # serializer = serializers.CafeSerializers(queryset, many=True)

        queryset = CafeMain.objects.all()
        serializer = serializers.CafeSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """
    HTTP Method : POST
    Parameter Example : 
        {
            "name_kor": "스타벅스 정발산2점",
            "name_eng": "starbucks jungbalsan2",
            "tel_num": "031-941-1112",
            "sns_url": "https://facebook.com/starbucks_jungbalsan2",
            "open_time": "07:00:00"
        }
    """
    @swagger_auto_schema(tags=['카페 데이터를 추가 합니다.'], responses={200: 'Success'}, request_body=serializers.CafeSerializers)
    def post(self, request):
        data = request.data

        # 프랜차이즈라고 표기했으나 프랜차이즈 데이터가 없는 경우
        if data['is_franchised'] == True and not data.get('franchise'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cafemain_serializer = serializers.CafeSerializers(data=data)
        if cafemain_serializer.is_valid():
            cafemain_serializer.save()

        # return JsonResponse(cafemain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cafe_id = int(cafemain_serializer.data['cafe_id'])
        if data.get('franchise'):
            caferanchise_data = data.get('franchise')
            caferanchise_data['cafe_id'] = cafe_id
            cafefranchise_serializer = serializers.CafeFranchiseSerializers(data=caferanchise_data)
            print(cafefranchise_serializer.is_valid())
            if cafefranchise_serializer.is_valid():
                cafefranchise_serializer.save()
        
        cafeaddress_serializer = {}
        if data.get('address'):
            cafeaddress_data = data.get('address')
            cafeaddress_data['cafe_id'] = cafe_id
            cafeaddress_serializer = serializers.CafeAddressSerializer(data=cafeaddress_data)
            if cafeaddress_serializer.is_valid():
                cafeaddress_serializer.save()

        return Response(cafemain_serializer.data, status=status.HTTP_201_CREATED)



        # post_serializer = serializers.CafeSerializers(data=request.data)
        # if post_serializer.is_valid():
        #     post_serializer.save()

        #     # 카페 데이터 저장 시 주소 데이터도 같이 저장할 수 있도록 처리
        #     post_serializer = serializers.CafeAddressSerializer(data=request.data)
        #     if post_serializer.is_valid():
        #         post_serializer.save()
        #         return Response(post_serializer.data, status = status.HTTP_201_CREATED)
        #     else:
        #         return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #     # return Response(post_serializer.data, status = status.HTTP_201_CREATED)

        # else:
        #     return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CafeDetailView(APIView):
    def get_object(self, cafe_no):
        try:
            return CafeMain.objects.get(pk=cafe_no)
        except CafeMain.DoesNotExist:
            return Http404
    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 불러옵니다.'], responses={200: 'Success'})
    def get(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)
        data_serial = serializers.CafeSerializers(cafe_data)
        return Response(data_serial.data)

    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 수정합니다.'], responses={200: 'Success'}, request_body=serializers.CafeSerializers)
    def put(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)

        #수정할  인스턴스, 수정할 내용
        update_serial  = serializers.CafeSerializers(cafe_data, data=request.data)

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


class CafeMenuLV(APIView):
    def get(self, request, cafeno, format=None):
        cafe_lv = get_object_or_404(CafeMain, cafe_no=cafeno)
        serializer = serializers.MenuSerializer(cafe_lv)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CafeMenuDV(APIView):
    def get(self, request, cafeno, menuname, format=None):
        cafe_dv = get_object_or_404(CafeMain, cafe_no=cafeno, menu_name=menuname)
        serializer = serializers.MenuSerializer(cafe_dv)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        post_serializer = serializers.MenuSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            menu_id = kwargs.get('id')
            user_object = CafeMenu.objects.get(id=menu_id)
 
            update_user_serializer = serializers.MenuSerializer(user_object, data=request.data)
            if update_user_serializer.is_valid():
                update_user_serializer.save()
                return Response(update_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            menu_id = kwargs.get('id')
            user_object = CafeMenu.objects.get(id=menu_id)
            user_object.delete()
            return Response("test ok", status=status.HTTP_200_OK)


class CafeAddressDV(APIView):
    def get(self, request, format=None):
        cafe_no = request.GET.get("cafe_no", None)

        if cafe_no:
            cafe_address_dv = get_object_or_404(CafeAddress, cafe_no=cafe_no)
            serializer = serializers.CafeAddressSerializer(cafe_address_dv)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
    
    """
    HTTP Method : POST
    Parameter Example : 
        {
            "cafe_no": 2,
            "state": "고양시",
            "city": "경기도",
            "county": "일산동구",
            "detail_addr": "무궁화로 237"
        }
    """
    def post(self, request):
        print(request)
        post_serializer = serializers.CafeAddressSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        if kwargs.get('cafe_no') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            cafe_no = kwargs.get('cafe_no')
            user_object = CafeAddress.objects.get(id=cafe_no)
 
            update_user_serializer = serializers.CafeAddressSerializer(user_object, data=request.data)
            if update_user_serializer.is_valid():
                update_user_serializer.save()
                return Response(update_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        if kwargs.get('cafe_no') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            cafe_no = kwargs.get('cafe_no')
            cafe_address_object = CafeAddress.objects.get(id=cafe_no)
            cafe_address_object.delete()
            return Response("test ok", status=status.HTTP_200_OK)