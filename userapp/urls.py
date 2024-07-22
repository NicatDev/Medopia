from django.urls import path,include
from .views import RegisterView,VerifyOTPView,LoginUserView,SetGenderView,SetInterestsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_account/', VerifyOTPView.as_view(), name='verify_account'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('set_gender/', SetGenderView.as_view(), name='set_gender'),
    path('set_interests/', SetInterestsView.as_view(), name='set_interests'),
    
]