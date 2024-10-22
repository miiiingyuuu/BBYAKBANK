from django.db import models
from django.contrib.auth.models import AbstractUser
from finance.models import DepositProduct
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    age = models.IntegerField(default=20)
    gender = models.IntegerField(default=1)
    salary = models.IntegerField(default=-1) #급여
    wealth = models.IntegerField(default=-1) #자산
    tendency = models.IntegerField(default=1) # 저축 성향
    deposit = models.ManyToManyField(DepositProduct, blank=True, related_name="joined") #가입 상품
