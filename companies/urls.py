from django.conf.urls import url
from django.urls import path, include
from companies.views import RegisterAPI, LoginAPI
urlpatterns = [
 path('Register/',RegisterAPI.as_view()),
 path('Login/',LoginAPI.as_view()),
]
