from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone

from jobs.models import Jobs


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        exclude = ['applicants']


class joblistSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Jobs
        fields = ('logo', 'created_at',)

    def get_logo(self, job):
        return job.company.user.file.url

    def get_created_at(self, job):
        return naturaltime(job.created_at)




