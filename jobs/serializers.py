from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from account.models import Profile
from jobs.models import Jobs

class ApplicantSerializer(serializers.ModelSerializer):
    email     = serializers.CharField(source='user.email')
    firstname = serializers.CharField(source='user.firstname')
    lastname  = serializers.CharField(source='user.lastname')
    class Meta:
        model = Profile
        fields = ('email', 'firstname', 'lastname')

class CompanyJobSerializer(serializers.ModelSerializer):
    applicants = ApplicantSerializer(many=True, read_only=True)
    class Meta:
        model = Jobs
        exclude = []


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        exclude = ['applicants','applicantscount']


class joblistSerializer(serializers.ModelSerializer):

    logo = serializers.SerializerMethodField()

    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Jobs
        fields = ('logo', 'created_at', 'applicantscount', 'salary', 'company', 'id', 'job_type')

    def get_logo(self, job):
        if job.company.user.file:
            return job.company.user.file.url
        return ''

    def get_created_at(self, job):
        return naturaltime(job.created_at)




