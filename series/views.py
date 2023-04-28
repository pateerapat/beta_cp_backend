from django.shortcuts import render
from rest_framework import generics

from .models import Serie
from .serializers import SerieSerializer


class SerieList(generics.ListCreateAPIView):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer


class SerieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer
