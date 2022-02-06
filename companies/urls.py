from django.conf.urls import url
from django.urls import path, include
from companies.views import Company_RegisterAPI, Company_LoginAPI, CompanyProfileAPI
urlpatterns = [
 path('register/',Company_RegisterAPI.as_view()),
 path('register/profile',CompanyProfileAPI.as_view()),
 path('login/',Company_LoginAPI.as_view()),
]
