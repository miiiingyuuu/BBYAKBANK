# accounts/views.py
from rest_framework import generics, permissions
from .serializers import UserSerializer,CustomUserDetailsSerializer, DepositProductSerializer
from .models import User
from dj_rest_auth.views import LoginView, UserDetailsView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from math import sqrt
UserModel = get_user_model()

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['PUT'])
def modify(request):
    if request.method == 'PUT':
        person = UserModel.objects.get(id=request.user.id)
        serializer = UserSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # 추가: 회원 정보 수정 엔드포인트
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# ------------------------------------------------------------------------------

def calculate_difference(user1, user2):
    difference = sqrt(
        (user1.age - user2.age) ** 2 +
        (user1.gender - user2.gender) ** 2 +
        (user1.salary - user2.salary) ** 2 +
        (user1.wealth - user2.wealth) ** 2 +
        (user1.tendency - user2.tendency) ** 2
    )
    return difference

def find_similar_users(user):
    users = User.objects.exclude(id=user.id)
    differences = []

    for other_user in users:
        difference = calculate_difference(user, other_user)
        differences.append((other_user, difference))

    differences.sort(key=lambda x:x[1])
    similar_users = [user for user, _ in differences[:10]]

    return similar_users

class UserRecommendationsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        similar_users = find_similar_users(user)
        deposit_products = []

        for user in similar_users:
            deposit_products.extend(user.deposit.all())

        serializer = DepositProductSerializer(deposit_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)