from rest_framework import serializers
from .models import *

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit', )

class DepositProductSerializer(serializers.ModelSerializer):
    depositoption_set = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProduct
        fields = '__all__'
        read_only_fields = ('like_user',)
        
class DepositOptionSerializer2(serializers.ModelSerializer):
    class DepositProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositProduct
            fields = '__all__'
    deposit = DepositProductSerializer()
    class Meta:
        model = DepositOption
        fields = '__all__'
        
class LikeDepositSerializer(serializers.ModelSerializer):
    depositoption_set = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProduct
        fields = ('deposit_code', 'fin_prdt_nm', 'kor_co_nm', 'depositoption_set')

# ----------------------------------------------------------------------
        
class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving', )

class SavingProductSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProduct
        fields = '__all__'
        read_only_fields = ('like_user',)
        
class SavingOptionSerializer2(serializers.ModelSerializer):
    class SavingProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = SavingProduct
            fields = '__all__'
    saving = SavingProductSerializer()
    class Meta:
        model = SavingOption
        fields = '__all__'

class LikeSavingSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProduct
        fields = ('saving_code','fin_prdt_nm','kor_co_nm', 'savingoption_set')