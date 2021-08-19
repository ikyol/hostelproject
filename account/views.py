from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import *
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Вы успешно зарегистрировались!", 201)


class ActivateView(APIView):
    # def get(self, request, email, activation_code):
    #     User = get_user_model()
    #     user = get_object_or_404(User, activation_code=activation_code)
    #     user.is_active = True
    #     user.activation_code = ''
    #     user.save()
    #     return Response('Ваш аккаунт успешно активирован', 200)

    def get(self, request, activation_code):
        user = MyUser.objects.get(activation_code=activation_code)
        if not user:
            return Response('This user does not exist', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Аккаунт успешно активирован', 200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли из аккаунта', 200)


class ForgotPasswordView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(MyUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(email=user.email, activation_code=user.activation_code, status='reset_password')
        return Response('Измените пароль', status=200)


class CompleteResetPassword(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Пароль успешно изменен', status=200)
