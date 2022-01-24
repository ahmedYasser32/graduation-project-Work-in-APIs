from django.conf.urls import url
from django.urls import path, include
from .views import RegisterAPI, LoginAPI
urlpatterns = [
 path('register/',RegisterAPI.as_view()),
 path('login/',LoginAPI.as_view()),
]
