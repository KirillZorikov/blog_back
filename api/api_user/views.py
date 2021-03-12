from django.contrib.auth import logout
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from posts.models import User
from . import serializers
from .utils import authenticate_user


# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)

class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'signup': serializers.UserSignupSerializer,
        'change_password': serializers.ChangeUserPasswordSerializer,
        'update_profile': serializers.UpdateUserSerializer,
    }
    permission_classes = (AllowAny,)

    @action(detail=False, methods=('post',))
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        user = authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',))
    def logout(self, request):
        logout(request)
        return Response({'success': 'Successfully logged out'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',))
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=('patch',))
    def change_password(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Password updated successfully.'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=('patch',))
    def update_profile(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Profile updated successfully.'},
                        status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]