from django.urls import path,include
from feedapp.views import *

urlpatterns = [
        path('interests/', CategoryListView.as_view(), name='interests'),
]