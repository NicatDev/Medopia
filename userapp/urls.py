from django.urls import path,include
from .views import RegisterView,VerifyOTPView,LoginUserView,UserUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_account/', VerifyOTPView.as_view(), name='verify_account'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user_update/', UserUpdateView.as_view(), name='user_update'),

    
]