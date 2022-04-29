from django.conf.urls import url
from django.urls import path, include
from jobs.views import *

urlpatterns = [

 path('create_job',JobCreation.as_view()),
 path('job_detail/<int:job>',JobDetail.as_view()),
path('company_job_detail/<int:job>',CompanyJobDetail.as_view()),
 path('job_apply/<int:job>',JobApply.as_view()),
 path('company_jobs/<str:email>',CompanyJobs.as_view()),
 path('user_jobs',AppliedJobs.as_view()),

]
