from django.http import Http404, JsonResponse
from django.shorcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from cafespot.services.cafe_main import CafeMainService
from cafespot.models import CafeMain
from cafespot.serializers import serializers


class CafeLV(APIView):
    def __init__(self):
        self.default_page = "1"
        self.default_page_size = "10"

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

        page_num = self.check_numeric(page)
        page_size_num = self.check_numeric(page_size)

        cafe_main_data = CafeMainService.get_cafe_main(page_num, page_size_num)

        return Response(cafe_main_data, status=status.HTTP_200_OK)

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
        if data["is_franchise"] is True and not data.get("franchise"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # sub_name 3개 이상 저장되었을 때 에러 처리
        if data.get("sub_names"):
            sub_names = data.get("sub_names")
            if len(sub_names) > 3:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        set_cafe_main_data = CafeMainService.set_cafe_main(data)

        return Response(set_cafe_main_data.data, status=status.HTTP_201_CREATED)

    def get_object(self, cafe_no):
        return get_object_or_404(CafeMain, pk=cafe_no)

    def check_numeric(self, checked_data):
        if checked_data.isnumeric():
            return int(checked_data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CafeDetailView(APIView):
    def get_object(self, cafe_no):
        return get_object_or_404(CafeMain, pk=cafe_no)

    @swagger_auto_schema(tags=["지정한 데이터의 상세 정보를 불러옵니다."], responses={200: "Success"})
    def get(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)
        data_serializer = serializers.CafeSerializers(cafe_data)
        return Response(data_serializer.data)

    @swagger_auto_schema(
        tags=["지정한 데이터의 상세 정보를 수정합니다."],
        responses={200: "Success"},
        request_body=serializers.CafeSerializers,
    )
    def put(self, request, cafe_no):
        cafe_data = self.get_object(cafe_no)

        # 수정할  인스턴스, 수정할 내용
        update_serializer = serializers.CafeSerializers(cafe_data, data=request.data)

        if update_serializer.is_valid():
            # save()를 통해 serializer의 update()메소드 실행,
            # DB 인스턴스 업데이트
            update_serializer.save()
            return Response(update_serializer.data, status=status.HTTP_200_OK)

        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["지정한 데이터의 상세 정보를 삭제합니다."], responses={200: "Success"})
    def delete(self, cafe_no):
        post = self.get_object(cafe_no)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
