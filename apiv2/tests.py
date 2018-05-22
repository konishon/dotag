# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .models import Bucketlist, ReportRating
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='first_user')

        self.bucketlist_name = 'Write world class code'
        self.bucketlist = Bucketlist(name=self.bucketlist_name)

        self.reportrating = ReportRating(reporter=user, lat=0, lon=0,land_pollution_rating=0,air_pollution_rating=0,sound_pollution_rating=0,water_pollution_rating=0)


    def test_model_can_create_a_bucketlist(self):
        old_count = Bucketlist.objects.count()
        self.bucketlist.save()
        new_count = Bucketlist.objects.count()
        self.assertNotEqual(old_count,new_count)

    def  test_model_can_create_a_report_rating(self):
        old_count = ReportRating.objects.count()
        self.reportrating.save()
        new_count = ReportRating.objects.count()
        self.assertNotEqual(old_count,new_count)


class ViewTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='first_user')

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.bucketlist_data =  {'name': 'Go to Ibiza', 'reporter': user.id}
        self.response = self.client.post(
            reverse('create'),
            self.bucketlist_data,
            format="json"
        )

    def test_api_can_create_a_bucketlist(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED) 

   
    