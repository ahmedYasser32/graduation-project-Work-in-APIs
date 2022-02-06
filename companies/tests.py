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
    def setUp(self):
        self.email=Account.objects.create(email='test@localhosst.app')
        self.email.set_password('some_strng_pass')
        self.email.save()

    def test_company_registiration(self):
        data={"email":"tesst@localhosst.app",
          "password":"some_strng_pass","is_staff":"false"
            ,"is_verified":"false","is_company":"true"}

        response = self.client.post("/api/company/register/",data)

        self.assertEqual(response.status_code, 200)


    def test_company_registiration_two(self):

        data={"email":"test@localhosst.app","firstname":"test",
          "lastname":"case","company_name":"testC","job_title":"TR",
        "mobile_number":"012","company_industries":"TR","size_of_company":"SB",
          "password":"some_strng_pass","is_staff":"false"
            ,"verified":"false","is_company":"true"}


        response = self.client.post("/api/company/register/2",data)
        print("registiration 2 response:",response.data)


        self.assertEqual(response.status_code, 200)

    def test_company_login(self):
        data={"email":"test@localhosst.app",
          "password":"some_strng_pass"}

        response = self.client.post("/api/company/login/",data)

        self.assertEqual(response.status_code, 200)
        print("Login response :",response.data)


