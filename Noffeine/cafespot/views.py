from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from .models import CafeAddress, CafeMain, CafeMenu
from . import serializers


class CafeLV(APIView):
    def __init__(self):
        self.default_page = "1"
        self.default_page_size = "10"

    def get_object(self, cafe_no):
        try:
            return CafeMain.objects.get(pk=cafe_no)
        except CafeMain.DoesNotExist:
            return Http404

    def check_numeric(self, checked_data):
        if checked_data.isnumeric():
            return int(checked_data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """
    HTTP Method : GET
    Parameter Example : 
        http://127.0.0.1:8000/cafespot/?page=1&page_size=10
    """

    @swagger_auto_schema(
        operation_summary="카페 전체 데이터 리스트",
        operation_description="""
            카페 리스트 데이터 가져오기
        """,
        tags=["cafe"],
    )
    def get(self, request):
        page = request.GET.get("page", self.default_page)  # 페이지 번호
        page_size = request.GET.get(
            "page_size", self.default_page_size
        )  # 한 페이지에 보여줄 데이터 개수

        # str -> int 형변환
        offset_cnt = 10 * (self.check_numeric(page) - 1)
        limit_cnt = self.check_numeric(page_size)

        # 주소 데이터가 없는 경우 처리를 해야함
        queryset = CafeMain.objects.select_related("cafe_address")[
            offset_cnt : offset_cnt + limit_cnt
        ]
        # print(queryset.query)

        serializer = serializers.CafeSerializers(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    HTTP Method : POST
    Parameter Example : 
        {
            "address": {
                "latitude": "1.1",
                "longitude": "1.1",
                "sido": "Goyang-si",
                "sigungu": "Ilsandong-gu",
                "doro": "sanduro",
                "doro_code": "111",
                "sangse": "sangse"
            },
            "main_name": "스타벅스 정발산2점",
            "is_operated": "True",
            "is_franchise": "True",
            "franchise": {
                "branch_name": "스타벅스"
            },
            "phone": "031-941-1112",
            "hours": {
                "mon": "07:00 ~ 20:00",
                "tue": "07:00 ~ 20:00",
                "wed": "07:00 ~ 20:00",
                "thur": "07:00 ~ 20:00",
                "fri": "07:00 ~ 20:00",
                "sat": "07:00 ~ 20:00",
                "sun": "07:00 ~ 20:00"
            },
            "sns_url": "https://facebook.com/starbucks_jungbalsan2",
            "registrant": "sunhye",
            "sub_names": [
                {
                    "sub_name": "starbucks"
                }
            ]
        }
    """

    @swagger_auto_schema(
        tags=["카페 데이터를 추가 합니다."],
        responses={200: "Success"},
        request_body=serializers.CafeSerializers,
    )
    def post(self, request):
        data = request.data

        # 프랜차이즈라고 표기했으나 프랜차이즈 데이터가 없는 경우
        if data["is_franchise"] == True and not data.get("franchise"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # sub_name 3개 이상 저장되었을 때 에러 처리
        if data.get("sub_names"):
            sub_names = data.get("sub_names")
            if len(sub_names) > 3:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        cafemain_serializer = serializers.CafeSerializers(data=data)

        if cafemain_serializer.is_valid():
            cafemain_serializer.save()
        else:  # 카페 메인 데이터가 저장되지 않으면 에러 띄우고 종료
            return JsonResponse(
                cafemain_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        cafe_id = int(cafemain_serializer.data["cafe_id"])

        if data.get("address"):
            cafeaddress_data = data.get("address")
            cafeaddress_data["cafe_id"] = cafe_id
            print(cafeaddress_data)
            cafeaddress_serializer = serializers.CafeAddressSerializer(
                data=cafeaddress_data
            )
            if cafeaddress_serializer.is_valid():
                cafeaddress_serializer.save()
            else:  # 주소 데이터에서 에러나면 main 데이터 삭제
                cafe_main = self.get_object(cafe_id)
                cafe_main.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if data.get("sub_names"):
            # 서브네임 여러개일 때 처리
            for _sub_name in sub_names:
                cafe_sub_name_data = _sub_name
                cafe_sub_name_data["cafe_id"] = cafe_id
                cafesubname_serializer = serializers.CafeSubNameSerializer(
                    data=cafe_sub_name_data
                )
                if cafesubname_serializer.is_valid():
                    cafesubname_serializer.save()

        if data.get("franchise"):
            data["franchise"]["cafe_id"] = cafe_id
            cafefranchise_serializer = serializers.CafeFranchiseSerializers(
                data=data["franchise"]
            )

            if cafefranchise_serializer.is_valid():
                cafefranchise_serializer.save()

        return Response(cafemain_serializer.data, status=status.HTTP_201_CREATED)


class CafeDetailView(APIView):
    def get_object(self, cafe_no):
        try:
            return CafeMain.objects.get(pk=cafe_no)
        except CafeMain.DoesNotExist:
            return Http404

    @swagger_auto_schema(tags=["지정한 데이터의 상세 정보를 불러옵니다."], responses={200: "Success"})
    def get(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)
        data_serial = serializers.CafeSerializers(cafe_data)
        return Response(data_serial.data)

    @swagger_auto_schema(
        tags=["지정한 데이터의 상세 정보를 수정합니다."],
        responses={200: "Success"},
        request_body=serializers.CafeSerializers,
    )
    def put(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)

        # 수정할  인스턴스, 수정할 내용
        update_serial = serializers.CafeSerializers(cafe_data, data=request.data)

        if update_serial.is_valid():
            # save()를 통해 serializer의 update()메소드 실행,
            # DB 인스턴스 업데이트
            update_serial.save()
            return Response(update_serial.data, status=status.HTTP_201_CREATED)
        return Response(update_serial.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["지정한 데이터의 상세 정보를 삭제합니다."], responses={200: "Success"})
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
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        if kwargs.get("id") is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            menu_id = kwargs.get("id")
            user_object = CafeMenu.objects.get(id=menu_id)

            update_user_serializer = serializers.MenuSerializer(
                user_object, data=request.data
            )
            if update_user_serializer.is_valid():
                update_user_serializer.save()
                return Response(update_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        if kwargs.get("id") is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            menu_id = kwargs.get("id")
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
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        if kwargs.get("cafe_no") is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            cafe_no = kwargs.get("cafe_no")
            user_object = CafeAddress.objects.get(id=cafe_no)

            update_user_serializer = serializers.CafeAddressSerializer(
                user_object, data=request.data
            )
            if update_user_serializer.is_valid():
                update_user_serializer.save()
                return Response(update_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        if kwargs.get("cafe_no") is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            cafe_no = kwargs.get("cafe_no")
            cafe_address_object = CafeAddress.objects.get(id=cafe_no)
            cafe_address_object.delete()
            return Response("test ok", status=status.HTTP_200_OK)
