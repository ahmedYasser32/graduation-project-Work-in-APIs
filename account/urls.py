from django.conf.urls import url
from django.urls import path, include
from account.views import RegisterAPI, LoginAPI


urlpatterns = [
 path('register/',RegisterAPI.as_view()),
 path('login/',LoginAPI.as_view()),
 path('reset_password_mail/', check_reset_password_mail, name="check_if_account_exists"),
 path('reset_password_check/<str:token>/', check_reset_password_code, name="check_if_account_code"),
 path('reset_password/<str:token>/', reset_password, name="reset_password"),
]

