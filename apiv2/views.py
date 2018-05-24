# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics, permissions
from .permissions import IsOwner
from django.shortcuts import render
from rest_framework import generics
from .serializers import BucketlistSerializer, ReportRatingSerializer
from .models import Bucketlist, ReportRating
from django.contrib.auth import login
from social_django.utils import psa
from social_core.backends.facebook import FacebookOAuth2
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

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