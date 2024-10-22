from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import *
from .serializers import *
from django.conf import settings
import requests
from django.db.models import Max
from accounts.models import User
from django.db.models import Q
from collections import Counter

API_KEY = settings.BANK_API_KEY
DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

# 금융 데이터 불러오기
def make_financial_data(request):
    deposit_response = requests.get(DEPOSIT_API_URL).json()
    deposit_baseList = deposit_response.get('result').get('baseList')
    deposit_optionList = deposit_response.get('result').get('optionList')
    
    for li in deposit_baseList:
        if DepositProduct.objects.filter(deposit_code=li.get('fin_prdt_cd')):
            continue
        save_product = {
            'deposit_code': li.get('fin_prdt_cd', '-1'),
            'dcls_month': li.get('dcls_month', '-1'),
            'fin_co_no': li.get('fin_co_no', '-1'),
            'kor_co_nm': li.get('kor_co_nm', '-1'),
            'fin_prdt_nm': li.get('fin_prdt_nm', '-1'),
            'etc_note': li.get('etc_note', '-1'),
            'spcl_cnd': li.get('spcl_cnd', '-1'),
            'mtrt_int': li.get('mtrt_int', '-1'),
            'join_deny': li.get('join_deny', -1),
            'join_member': li.get('join_member', '-1'),
            'join_way': li.get('join_way', '-1'),
            'max_limit': li.get('max_limit', -1),
        }

        serializer = DepositProductSerializer(data=save_product)
        # 유효성 검증
        if serializer.is_valid(raise_exception=True):
            # 유효하다면, 저장
            serializer.save()

    for li in deposit_optionList:
        # 원하는 데이터 추출하기
        prdt_cd = li.get('fin_prdt_cd', '-1')
        product = DepositProduct.objects.get(deposit_code=prdt_cd)
        save_option= {
            'intr_rate_type_nm': li.get('intr_rate_type_nm', '-1'),
            'save_trm': li.get('save_trm', -1),
            'intr_rate': li.get('intr_rate', -1),
            'intr_rate2': li.get('intr_rate2', -1),
        }
        
        serializer = DepositOptionsSerializer(data=save_option)
        # 유효성 검증
        if serializer.is_valid(raise_exception=True):
            # 유효하다면, 저장
            serializer.save(deposit=product)
            
    saving_res = requests.get(SAVING_API_URL).json()
    saving_baseList = saving_res.get('result').get('baseList')
    saving_optionList = saving_res.get('result').get('optionList')
    
    for li in saving_baseList:
        if SavingProduct.objects.filter(saving_code=li.get('fin_prdt_cd')):
            continue
        save_product = {
            'saving_code': li.get('fin_prdt_cd', '-1'),
            'dcls_month': li.get('dcls_month', '-1'),
            'fin_co_no': li.get('fin_co_no', '-1'),
            'kor_co_nm': li.get('kor_co_nm', '-1'),
            'fin_prdt_nm': li.get('fin_prdt_nm', '-1'),
            'join_way': li.get('join_way', '-1'),
            'mtrt_int': li.get('mtrt_int', '-1'),
            'spcl_cnd': li.get('spcl_cnd', '-1'),
            'join_deny': li.get('join_deny', -1),
            'join_member': li.get('join_member', '-1'),
            'etc_note': li.get('etc_note', '-1'),
            'max_limit': li.get('max_limit', -1),
        }
        serializer = SavingProductSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in saving_optionList:
        prdt_cd = li.get('fin_prdt_cd', '-1')
        product = SavingProduct.objects.get(saving_code=prdt_cd)
        save_option = {
            'intr_rate_type_nm': li.get('intr_rate_type_nm', '-1'),
            'rsrv_type': li.get('rsrv_type', '-1'),
            'rsrv_type_nm': li.get('rsrv_type_nm', '-1'),
            'save_trm': li.get('save_trm', -1),
            'intr_rate': li.get('intr_rate', -1), # if option.get('intr_rate', -1) else -1,
            'intr_rate2': li.get('intr_rate2', -1),
        }

        serializer = SavingOptionsSerializer(data=save_option)
        if serializer.is_valid(raise_exception=True):
            serializer.save(saving=product)

    return HttpResponse("금융 데이터 생성 완료")

# ---------------------------------------------------------------------------------------

# 받아온 금융 데이터를 기준으로, deposit, depositdetail, saving, savingdetail 받아오기
@api_view(['GET']) # id 순
def deposit_list(request):
    deposits = DepositProduct.objects.all()
    serializer = DepositProductSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deposit_detail(request, deposit_code):
    deposit = get_object_or_404(DepositProduct, deposit_code=deposit_code)
    if request.method == 'GET':
        serializer = DepositProductSerializer(deposit)
        return Response(serializer.data)    
    

@api_view(['GET'])
def depositOption_list(request, deposit_code):
    deposit = get_object_or_404(DepositProduct, deposit_code=deposit_code)
    deposit_options = DepositOption.objects.filter(deposit=deposit)

    if request.method == 'GET':
        serializer = DepositOptionsSerializer(deposit_options, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def depositOption_detail(request, deposit_code, depositOption_pk):
    deposit = get_object_or_404(DepositProduct, deposit_code=deposit_code)
    deposit_option = get_object_or_404(DepositOption, pk=depositOption_pk, deposit=deposit)

    if request.method == 'GET':
        serializer = DepositOptionsSerializer(deposit_option)
        return Response(serializer.data)
    

@api_view(['GET']) # id 순
def saving_list(request):
    savings = SavingProduct.objects.all()
    # print(savings)
    serializer = SavingProductSerializer(savings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def saving_detail(request, saving_code):
    saving = get_object_or_404(SavingProduct, saving_code=saving_code)
    if request.method == 'GET':
        serializer = SavingProductSerializer(saving)
        return Response(serializer.data)

    
@api_view(['GET'])
def savingOption_list(request, saving_code):
    saving = get_object_or_404(SavingProduct, saving_code=saving_code)
    saving_options = SavingOption.objects.filter(saving=saving)

    if request.method == 'GET':
        serializer = SavingOptionsSerializer(saving_options, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def savingOption_detail(request, saving_code, savingOption_pk):
    savingOption = get_object_or_404(SavingOption, pk=savingOption_pk)
    if request.method == 'GET':
        serializer = SavingOptionsSerializer(savingOption)
        return Response(serializer.data)
    
# ---------------------------------------------------------------------------------------

# 6개월~36개월
@api_view(['GET'])
def get_deposits(request, save_trm):
    deposits = DepositProduct.objects.filter(depositoption__save_trm=save_trm).order_by('depositoption__intr_rate')

    serializer = DepositProductSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_savings(request, save_trm):
    savings = SavingProduct.objects.filter(savingoption__save_trm=save_trm).order_by('savingoption__intr_rate')

    serializer = SavingProductSerializer(savings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_reverse_deposits(request, save_trm):
    deposits = DepositProduct.objects.filter(depositoption__save_trm=save_trm).order_by('-depositoption__intr_rate')

    serializer = DepositProductSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_reverse_savings(request, save_trm):
    savings = SavingProduct.objects.filter(savingoption__save_trm=save_trm).order_by('-savingoption__intr_rate')

    serializer = SavingProductSerializer(savings, many=True)
    return Response(serializer.data)

# --------------------------------------------------------------------------

@api_view(['GET','POST','DELETE'])
# @permission_classes([IsAuthenticated])
def like_deposit(request, deposit_code):
    deposit = get_object_or_404(DepositProduct, deposit_code=deposit_code)
    if request.method == 'GET':
        # likes = DepositProduct.objects.all()
        deposit_likes = request.user.like_depositproduct.all()
        serializer = LikeDepositSerializer(deposit_likes, many=True)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user in deposit.like_user.all():
            deposit.like_user.remove(request.user)
            return Response({ "detail": "삭제되었습니다." }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "detail": "삭제할 항목이 없습니다." }, status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'POST':
        if request.user not in deposit.like_user.all():
            deposit.like_user.add(request.user)
            serializer = LikeDepositSerializer(deposit, data=request.data, partial=True)
            # print('1')
            if serializer.is_valid(raise_exception=True):
                # print('2')
                serializer.save()
                return Response({ "detail": "상품이 추가되었습니다." }, status=status.HTTP_200_OK)
        else:
            return Response({ "detail": "이미 상품이 존재합니다." }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','POST','DELETE'])
# @permission_classes([IsAuthenticated])
def like_saving(request, saving_code):
    saving = get_object_or_404(SavingProduct, saving_code=saving_code)
    if request.method == 'GET':
        saving_likes = request.user.like_savingproduct.all()
        serializer = LikeSavingSerializer(saving_likes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user in saving.like_user.all():
            saving.like_user.remove(request.user)
            return Response({ "detail": "삭제되었습니다." }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "detail": "삭제할 항목이 없습니다." }, status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'POST':
        if request.user not in saving.like_user.all():
            saving.like_user.add(request.user)
            serializer = LikeSavingSerializer(saving, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({ "detail": "상품이 추가되었습니다." }, status=status.HTTP_200_OK)
        else:
            return Response({ "detail": "이미 상품이 존재합니다." }, status=status.HTTP_400_BAD_REQUEST)
        
# -----------------------------------------------------------------------------------------

@api_view(['GET'])
def get_bank_deposit(request, kor_co_nm):
    if DepositProduct.objects.filter(kor_co_nm=kor_co_nm).exists():
        deposits = DepositProduct.objects.filter(kor_co_nm=kor_co_nm)
        serializer = DepositProductSerializer(deposits, many=True)
        return Response(serializer.data)
    else:
        return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_bank_saving(request, kor_co_nm):
    if SavingProduct.objects.filter(kor_co_nm=kor_co_nm).exists():
        savings = SavingProduct.objects.filter(kor_co_nm=kor_co_nm)
        serializer = SavingProductSerializer(savings, many=True)
        return Response(serializer.data)
    else:
        return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def user_likes(request):
    if request.user.is_authenticated:
        # print('1')
        liked_products = request.user.like_depositproduct.all()
        serializer = DepositProductSerializer(liked_products, many=True)
        # serializer1 = DepositProductSerializer(liked_products, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
def user_likes2(request):
    if request.user.is_authenticated:
        print('1')
        liked_products2 = request.user.like_savingproduct.all()
        serializer = SavingProductSerializer(liked_products2, many=True)
        # serializer1 = DepositProductSerializer(liked_products, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)    
    

@api_view(['DELETE'])
def user_likes_delete(request,product_id,user_id):
    if request.user.is_authenticated:
        dproduct = DepositProduct.objects.get(id=product_id)
        dproduct.like_user.remove(request.user)
        return Response({'result': 'delete_success'})
    else:
        return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def user_likes2_delete(request,product_id,user_id):
    if request.user.is_authenticated:
        dproduct = SavingProduct.objects.get(id=product_id)
        dproduct.like_user.remove(request.user)
        return Response({'result': 'delete_success'})
    else:
        return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


