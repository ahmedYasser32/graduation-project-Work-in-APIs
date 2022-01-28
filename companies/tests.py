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

    def test_company_registiration(self):
        data={"email":"test@localhosst.app","firstname":"test",
          "lastname":"case","company_name":"testC",
          "password":"some_strng_pass","is_staff":"false"
            ,"verified":"false","is_company":"true"}

        response = self.client.post("/api/company/register/",data)

        self.assertEqual(response.status_code, 200)

    def test_company_login(self):
        data={"email":"test@localhosst.app",
          "password":"some_strng_pass"}

        response = self.client.post("/api/company/login/",data)

        self.assertEqual(response.status_code, 200)


