from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone

from jobs.models import Jobs


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        exclude = ['applicants','company','applicantscount','id']


class joblistSerializer(serializers.ModelSerializer):

    logo = serializers.SerializerMethodField()

    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Jobs
        fields = ('logo', 'created_at','applicantscount','salary','company')

    def get_logo(self, job):
        if job.company.user.file:
            return job.company.user.file.url
        return ''

    def get_created_at(self, job):
        return naturaltime(job.created_at)




