# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Bucketlist(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class ReportTag(models.Model):
    created_by = models.ForeignKey('auth.User',
        related_name='tag_created_by',
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Report(models.Model):
    reporter = models.ForeignKey('auth.User',
        related_name='report',
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(ReportTag, related_name='report_tags')
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    comment = models.TextField()    
    photo = models.FileField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return str(self.id)
class ReportRating(models.Model):
    reporter = models.ForeignKey('auth.User',
        related_name='reportrating',
        on_delete=models.CASCADE
    )
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    land_pollution_rating = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
     )
    air_pollution_rating = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    sound_pollution_rating = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    water_pollution_rating = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.lat

# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)