from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken
from .validators import validate_phone_number
from feedapp.models import Category


AUTH_PROVIDERS ={'email':'email'}



class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('unselected', 'unselected'),
)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=False)
    phone = models.CharField(max_length=15, validators=[validate_phone_number],null=True,blank=True)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, blank=True, null=True, related_name='accounts_users',related_query_name='user',)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    gender = models.CharField(max_length=200,choices=GENDER_CHOICES,default='unselected')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='accounts_users',
        related_query_name='user',
    )
    USERNAME_FIELD = "email"

    interests = models.ManyToManyField(Category,blank=True)

    objects = UserManager()

    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"



class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    otp=models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"{self.user.email} - otp code"
