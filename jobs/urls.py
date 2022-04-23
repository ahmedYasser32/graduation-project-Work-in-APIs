from django.conf.urls import url
from django.urls import path, include
from jobs.views import *

urlpatterns = [

 path('create_job',JobCreation.as_view()),
 path('job_detail/<int:job>',JobDetail.as_view()),
 path('job_apply/<int:job>',JobApply.as_view()),
 path('company_jobs',CompanyJobs.as_view())

]
