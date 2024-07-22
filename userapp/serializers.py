from .models import User, OneTimePassword,Category

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError

#done
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2= serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields = ['email', 'first_name', 'last_name' , 'password', 'password2', 'phone']

    def validate(self, attrs):
        password=attrs.get('password', '')
        password2 =attrs.get('password2', '')
        if password !=password2:
            raise serializers.ValidationError("Parollar uyğun gəlmir")
         
        return attrs

    def create(self, validated_data):
        user= User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
            )
        user.is_active = False
        user.set_password(validated_data.get('password')) 
        user.save()   
        return user
    
#done
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token', 'is_admin']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Etibarsız etimadnamələr, yenidən cəhd edin.")

        tokens = user.tokens()
        
   
        return {
            'email': user.email,
            'access_token': str(tokens.get('access')),
            'refresh_token': str(tokens.get('refresh')),
   
        }

    
    
#done
class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        otp = data['otp']
        email = data['email']

        try:
            otp_record = OneTimePassword.objects.get(otp=otp)
            user = User.objects.get(email=email)
            data['user'] = user
            user.is_active = True
            user.save()
        except OneTimePassword.DoesNotExist:
            raise serializers.ValidationError('Invalid OTP.')

        token, created = Token.objects.get_or_create(user=user)
        tokens = user.tokens()
        data['access_token'] = str(tokens.get('access'))
        data['refresh_token'] = str(tokens.get('refresh'))
        otp_record.delete()
        return data


#genderSerializer

class UserGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['gender']

    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance

class UserInterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['interests']

