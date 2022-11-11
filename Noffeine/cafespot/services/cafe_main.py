from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.response import Response

from cafespot.models import CafeMain
from cafespot.serializers import serializers

class CafeMainService:
    def get_cafe_main(self, page:int, limit_cnt:int):
        offset_cnt = 10 * (page - 1)

        queryset = CafeMain.objects.select_related("cafe_address")[
                   offset_cnt: offset_cnt + limit_cnt
                   ]

        serializer = serializers.CafeSerializers(queryset, many=True)

        return serializer.data

    def set_cafe_main(self, request_data: dict):
        cafe_main_serializer = serializers.CafeSerializers(data=request_data)

        if cafe_main_serializer.is_valid():
            cafe_main_serializer.save()
        else:  # 카페 메인 데이터가 저장되지 않으면 에러 띄우고 종료
            return JsonResponse(
                cafe_main_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        cafe_id = int(cafe_main_serializer.data["cafe_id"])

        if request_data.get("address"):
            cafe_address_data = request_data.get("address")
            cafe_address_data["cafe_id"] = cafe_id
            print(cafe_address_data)
            cafe_address_serializer = serializers.CafeAddressSerializer(
                data=cafe_address_data
            )
            if cafe_address_serializer.is_valid():
                cafe_address_serializer.save()
            else:  # 주소 데이터에서 에러나면 main 데이터 삭제
                cafe_main = self.get_object(cafe_id)
                cafe_main.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if request_data.get("sub_names"):
            # 서브네임 여러개일 때 처리
            for _sub_name in request_data.get("sub_names"):
                cafe_sub_name_data = _sub_name
                cafe_sub_name_data["cafe_id"] = cafe_id
                cafe_sub_name_serializer = serializers.CafeSubNameSerializer(
                    data=cafe_sub_name_data
                )
                if cafe_sub_name_serializer.is_valid():
                    cafe_sub_name_serializer.save()

        if request_data.get("franchise"):
            request_data["franchise"]["cafe_id"] = cafe_id
            cafe_franchise_serializer = serializers.CafeFranchiseSerializers(
                data=request_data["franchise"]
            )

            if cafe_franchise_serializer.is_valid():
                cafe_franchise_serializer.save()

