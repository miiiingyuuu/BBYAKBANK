from django.db import models
# from accounts.models import User
# from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.

class DepositProduct(models.Model):
    deposit_code = models.TextField(unique=True)           # 고유 코드(fin_prdt_cd)
    dcls_month = models.CharField(max_length=20)            # 공시제출월
    fin_co_no = models.CharField(max_length=100)            # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)            # 금융회사 명
    fin_prdt_nm = models.TextField(max_length=100)          # 상품 명
    etc_note = models.TextField(blank=True, null=True)      # 기타 정보  
    spcl_cnd = models.TextField(blank=True, null=True)      # 우대조건
    mtrt_int = models.TextField(blank=True, null=True)      # 만기 후 금리
    join_deny = models.IntegerField(blank=True, null=True)  # 가입 한도
    join_member = models.TextField(blank=True, null=True)   # 가입 인원
    join_way = models.TextField(max_length=100)             # 가입 방법
    max_limit = models.IntegerField(blank=True, null=True)  # 최고 한도
    like_user= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_depositproduct')

class DepositOption(models.Model):
    deposit = models.ForeignKey(DepositProduct, on_delete = models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=100) #저축 금리 유형명
    save_trm = models.CharField(max_length=3) #저축 금리
    intr_rate = models.FloatField(null=True) #저축 금리
    intr_rate2 = models.FloatField(null=True) #최고 우대금리
    
class SavingProduct(models.Model):
    saving_code = models.CharField(max_length=100)  # 금융상품 코드 (fin_prdt_cd)
    dcls_month = models.CharField(max_length=20)    # 공시제출월
    fin_co_no = models.CharField(max_length=100)    # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)    # 금융회사 명
    fin_prdt_nm = models.TextField(max_length=100)          # 상품 명
    join_way = models.CharField(max_length=100)     # 가입 방법
    mtrt_int = models.TextField(blank=True, null=True)  # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)  # 우대조건
    join_deny = models.IntegerField(blank=True, null=True)  # 가입제한
    join_member = models.TextField(blank=True, null=True)   # 가입대상
    etc_note = models.TextField(blank=True, null=True)  # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)  # 최고한도
    like_user= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_savingproduct')

class SavingOption(models.Model):
    saving = models.ForeignKey(SavingProduct, on_delete = models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=2) #저축 금리 유형명
    rsrv_type = models.CharField(max_length=10) #적립 유형
    rsrv_type_nm = models.CharField(max_length=10) #적립 유형명
    save_trm = models.CharField(max_length=3) #저축기간[단위:개월]
    intr_rate = models.FloatField(null=True) #저축 금리
    intr_rate2 = models.FloatField(null=True) # 최고 우대금리
    
