from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone

from jobs.models import Jobs

class JobSerializer(serializers.ModelSerializer):
       class Meta:
        model  = Jobs
        exclude =['applicants']

class joblistSerializer(serializers.ModelSerializer) :
    class Meta :
        model= Jobs
