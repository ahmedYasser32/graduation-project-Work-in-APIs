from django.conf.urls import url
from django.urls import path, include
from companies.views import Company_RegisterAPI, Company_LoginAPI, CompanyProfileAPI,CompanyProfileSetup
urlpatterns = [
 path('register/',Company_RegisterAPI.as_view()),
 path('register/2',CompanyProfileAPI.as_view()),
 path('login/',Company_LoginAPI.as_view()),
 path('Profile_setup/',CompanyProfileSetup.as_view()),
]
