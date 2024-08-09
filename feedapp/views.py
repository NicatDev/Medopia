from django.shortcuts import render
from rest_framework.generics import ListAPIView
from feedapp.serializers import CategorySerializer
from feedapp.models import Category
# Create your views here.

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
