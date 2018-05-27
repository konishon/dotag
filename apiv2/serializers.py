from rest_framework import serializers
from .models import *

class BucketlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class ReportTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTag
        fields = ('name','id')    

class ReportRatingSerializer(serializers.ModelSerializer):

    reporter = serializers.ReadOnlyField(source='reporter.username')
    class Meta:
        model = ReportRating
        fields = ('reporter','id','lat','lon','land_pollution_rating','air_pollution_rating','sound_pollution_rating','water_pollution_rating')     
        # read_only_fields = ('date_created','id','lat','lon','land_pollution_rating','air_pollution_rating','sound_pollution_rating','water_pollution_rating')

class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source='reporter.username')
    tag  = ReportTagSerializer(read_only=True, many=True)
    
    class Meta:
        model = Report
        fields = ('reporter','lat', 'lon','photo','tag')        