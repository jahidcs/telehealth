from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from account.serializers import (
    UserRegustrationSerializer,
    UserLoginSerializer,
    ProfileViewSerializer,
    UserChangePasswordSerializer,
    SendPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
)
from account.renderer import UserRenderer

# Create your views here.

def token_generator(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class UserRegistration(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegustrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            print(user)
            token = token_generator(user)
            return Response(
                {
                    'token': token,
                    'message': 'Registration Successfull'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLogin(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                token = token_generator(user)
                return Response(
                    {
                        'token': token,
                        'message': 'Login Successfull'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'errors':{
                            'non_field_errors':['Email or password is not valid']
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        serializer = ProfileViewSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    'message': 'Password Changed !!!'
                },
                status= status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'message':'Password Reset link send. Please check your Email'
            },
            status=status.HTTP_200_OK
        )


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})

        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'message':'Password Reset Successfully'
            },
            status=status.HTTP_200_OK
        )
