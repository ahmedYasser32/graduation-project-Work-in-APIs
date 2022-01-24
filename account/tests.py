import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from account.serializers import RegistrationSerializer
from account.models import Account
# Create your tests here.

class RegistirationTestCase(APITestCase):

    def test_registiratio(self):
        data={"email":"test@localhost.app",'firstname':"test",
          'lastname':"case", 'password':"some_strng_pass" }
        response = self.client.post("api/account/register/",data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

