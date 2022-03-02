from django.shortcuts import render
from account.models import Account
from companies.models import CompanyProfile
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from companies.serializers import RegistrationSerializer,CompanyProfileSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Register API
class Company_RegisterAPI(APIView):
    authentication_classes     = []
    permission_classes         = []
    serializer_class           = RegistrationSerializer


    def post(self, request, *args, **kwargs):
        context = {}
        email                 = request.data.get('email')
        email = email.lower() if email else None



       #check email if already exist send error


        if Account.objects.filter(email=email).count()>0:
            context['error_message'] = 'That email is already in use.'
            context['response'] = 'error'
            return Response(data=context)




       # Assign serializer
        data = request.data.copy()
        data['is_company'] = True
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            #if valid save object and send response
            account = serializer.save()
            context['email'] = account.email
            context['pk'] = account.pk
            #token = Token.objects.get(user=account).key
            #context['token'] = token
            context['is_verified'] = account.verified
            context['is_company']  = account.is_company
            context['response']    = "Success"

            return Response(data=context)



        else:
            context = serializer.errors.copy()
            context['response'] = 'error'
            return Response(data=context)


# Register API 2
class CompanyProfileAPI(APIView):
    authentication_classes     = []
    permission_classes         = []
    serializer_class           = CompanyProfileSerializer

    def post(self, request, *args, **kwargs):
        context = {}
        email = request.data.get('email')
        email = email.lower() if email else None
        account        =Account.objects.filter(email=email)
        company_name = request.data.get('company_name')


       #check email if already exist send error

        if account.count() == 0:
            context['error_message'] = 'Account not found.'
            context['response'] = 'error'
            return Response(data=context)

        if CompanyProfile.objects.filter(company_name=company_name).count()>0:
            context['error_message'] = 'That company name is already in use.'
            context['response'] = 'error'
            return Response(data=context)


       # Assign serializer
        account = account[0]
        account.firstname = request.data.get('firstname', '')
        account.lastname = request.data.get('lastname', '')
        account.save()
        data = request.data.copy()
        #set relation
        data['user'] = account.pk
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            #if valid save object and send response
            serializer.save()
            context['email']       = account.email
            context['is_verified'] = account.verified
            context['is_company']  = account.is_company
            context['firstname']   = account.firstname
            context['lastname']    = account.lastname
            #** turn dictioanries into vars and copy values from serailizer
            context= {**context,**serializer.data.copy()}
            context['response']    = "Success"

            return Response(data=context)



        else:
            context = serializer.errors.copy()
            context['response'] = 'error'
            return Response(data=context)


class Company_LoginAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        context = {}
        email = request.data.get('email')
        password = request.data.get('password')
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['token'] = token.key
            context['is_verified'] = account.verified
            print(account)
            print(context)
            return Response(data=context)
        context['response'] = 'Error'
        context['error_message'] = 'Invalid credentials'
        return Response(data=context)

#Company profile setup
class CompanyProfileSetup(APIView):
    authentication_classes     = []
    permission_classes         = []
    serializer_class           = CompanyProfileSerializer

    def post(self, request, *args, **kwargs):

        context = {}
        email = request.data.get('email')
        email = email.lower() if email else None
        account     = Account.objects.select_related('companyprofile').filter(email=email)




        if account.count() == 0:
            #print("inside if")
            context['response'] = 'Error'
            context['error_message'] = 'email not registered'
            return Response(data=context)

        account = account[0]

        data = request.data.copy()
        serializer=self.serializer_class(account.companyprofile, data=data, partial=True)


        if serializer.is_valid():
            #if valid save object and send response
            serializer.save()

            context['email']       = account.email
            context['is_company']  = account.is_company
            context['firstname']   = account.firstname
            context['lastname']    = account.lastname
            #** turn dictioanries into vars and copy values from serailizer
            context= {**context,**serializer.data.copy()}

            context['response']    = "Success"

            return Response(data=context)



        else:

            context = serializer.errors.copy()
            context['response'] = 'error'
            return Response(data=context)

