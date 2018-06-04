# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics, permissions
from .permissions import IsOwner
from django.shortcuts import render
from django.views import View
from rest_framework import generics
from .serializers import *
from .models import *
from django.contrib.auth import login
from social_django.utils import psa
from social_core.backends.facebook import FacebookOAuth2
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from rest_framework import status
from .pagination import PostLimitOffsetPagination,PostPageNumberPagination
from rest_framework.response import Response
from django.contrib.auth.models import User

from django.shortcuts import  get_object_or_404

class CreateView(generics.ListCreateAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer

    def perform_create(self, serializer):
        serializer.save()


class HomeView(View):
    def get(self, request,*args,**kwargs):
        return render(request,"apiv2/home.html",{})


class ReportTagsView(APIView):
    def get(self, request, *args,**kwargs):
        queryset = ReportTag.objects.all();
        serializer = ReportTagSerializer(queryset, many=True)
        return Response(serializer.data);

class ReportView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, *args, **kwargs):

        pagination_class = PostPageNumberPagination
        paginator = pagination_class()

        queryset = Report.objects.all()
        page = paginator.paginate_queryset(queryset, request)

        serializer = ReportSerializer(queryset,  many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
       
        file_serializer = ReportSerializer(data=request.data)  
        tag_pk = request.data.get('tag','')

        if file_serializer.is_valid():
            file_serializer.save(reporter=self.request.user,tag=tag_pk)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)    
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ReportRatingCreateView(generics.ListCreateAPIView):
    queryset = ReportRating.objects.all()
    serializer_class = ReportRatingSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner) 

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user) 

    
# Define an URL entry to point to this view, call it passing the
# access_token parameter like ?access_token=<token>. The URL entry must
# contain the backend, like this:
#
#   url(r'^register-by-token/(?P<backend>[^/]+)/$',
#       'register_by_access_token')



@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    try:
        user = request.backend.do_auth(token)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            # return Response({'token': token.key})
            return JsonResponse({'status':200, 'token': token.key}, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({'status': 401,'data':'Could not authenticate with facebook server. Access key Invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return JsonResponse({'status':400 ,'data': 'Could not authenticate with facebook server.'}, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    permission_classes = []
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)