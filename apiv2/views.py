# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics, permissions
from .permissions import IsOwner
from django.shortcuts import render
from rest_framework import generics
from .serializers import BucketlistSerializer, ReportRatingSerializer
from .models import Bucketlist, ReportRating

class CreateView(generics.ListCreateAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer

    def perform_create(self, serializer):
        serializer.save()

class ReportRatingCreateView(generics.ListCreateAPIView):
    queryset = ReportRating.objects.all()
    serializer_class = ReportRatingSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner) 

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user) 