from rest_framework import serializers
from .models import *
import ast
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

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

    def create(self, validated_data):
        tags =validated_data.pop('tag')
        report=Report.objects.create(**validated_data)
        report.save()
        for tag in ast.literal_eval(tags):
             tag = ReportTag.objects.get(id=tag)
             report.tag.add(tag)
        return report     

    class Meta:
        model = Report
        fields = ('id','reporter','lat', 'lon','photo','comment','tag')        


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email','password')        