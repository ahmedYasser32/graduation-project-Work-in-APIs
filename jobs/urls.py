from django.conf.urls import url
from django.urls import path, include
from jobs.views import *

urlpatterns = [

 path('create_job',JobCreation.as_view()),

]
