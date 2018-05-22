from rest_framework import serializers
from .models import Bucketlist, ReportRating

class BucketlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')

class ReportRatingSerializer(serializers.ModelSerializer):

    reporter = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = ReportRating
        fields = ('reporter','id','lat','lon','land_pollution_rating','air_pollution_rating','sound_pollution_rating','water_pollution_rating')     
        # read_only_fields = ('date_created','id','lat','lon','land_pollution_rating','air_pollution_rating','sound_pollution_rating','water_pollution_rating')