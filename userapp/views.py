from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import OneTimePassword, User
from .serializers import *
from rest_framework import status, generics, permissions, viewsets
from project.utils import send_generated_otp_to_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Q 
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
#done

class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            user_instance = serializer.save()
            user_data = serializer.data
       
            otp = get_random_string(length=4, allowed_chars='0123456789') 
            OneTimePassword.objects.create(user=user_instance, otp=otp)  
            
            email_body = f"Medopia hesabını aktivləşdirmək üçün otp: {otp}"
            email = EmailMessage(
                "Medopia hesabını aktivləşdir!",
                email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[user_instance.email]
            )

            email.send(fail_silently=False)

            return Response({
                        'data': user_data,
                        'message': 'User registered successfully'
                    }, status=status.HTTP_201_CREATED)
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#done
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




#done
class VerifyOTPView(GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({'access': serializer.validated_data['access_token'],'refresh':serializer.validated_data['refresh_token']}, status=status.HTTP_200_OK)



class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={200: UserUpdateSerializer()},
        request_body=UserUpdateSerializer,
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

