# views.py

from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .models import Exchange
from .serializers import ExchangeSerializer

@api_view(['GET'])
def index(request):
    # API URL 설정
    EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&searchdate=20240517&data=AP01'
    print(EXCHANGE_API_URL)
    response = requests.get(EXCHANGE_API_URL)

    if response.status_code != 200:
        return Response({'error': 'Failed to fetch exchange rate data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = response.json()
    if not data:
        return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)

    # 데이터를 저장하기 전에 모든 기존 데이터를 삭제합니다.
    Exchange.objects.all().delete()

    serializer = ExchangeSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
