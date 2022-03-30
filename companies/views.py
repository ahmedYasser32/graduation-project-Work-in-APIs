
from rest_framework.parsers import MultiPartParser, JSONParser
from django.shortcuts import render
from account.models import Account
from companies.models import CompanyProfile
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from companies.serializers import CompanyRegistrationSerializer,CompanyProfileSerializer, LogoSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
# Register API
class Company_RegisterAPI(APIView):

    authentication_classes     = []
    permission_classes         = []
    serializer_class           = CompanyRegistrationSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
        'password': openapi.Schema(type=openapi.TYPE_STRING  , description='password')
    }),
    responses={200: CompanyRegistrationSerializer,400: 'Bad Request'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
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
            token = Token.objects.get(user=account).key
            context['token'] = token
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

    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
         'email': openapi.Schema(type=openapi.TYPE_STRING , description='email and the rest of the data from response'),
       }),
     responses={200: CompanyProfileSerializer,400: 'Error'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
        context = {}
        print(request.data)
        email = request.data.get('email')
        print(email)
        email = email.lower() if email else None
        print(email)
        account        =Account.objects.filter(email=email)
        print(account)
        company_name = request.data.get('company_name')
        print(company_name)


       #check email if already exist send error

        if account.count() == 0:
            context['error_message'] = 'Account not found.'
            context['response'] = 'error'
            return Response(data=context)

        print(CompanyProfile.objects.filter(company_name=company_name))
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

    @swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
        'password': openapi.Schema(type=openapi.TYPE_STRING  , description='password')
    }),
    responses={200: CompanyRegistrationSerializer,400: 'Bad Request'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
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
            profile_created = False
            try:
                company_profile = account.companyprofile
                serializer = self.serializer_class(company_profile)
                context.update(serializer.data)
                profile_created = True
            except Account.companyprofile.RelatedObjectDoesNotExist:
                pass

            context['profile_created'] = profile_created


            return Response(data=context)

        context['response'] = 'Error'
        context['error_message'] = 'Invalid credentials'
        return Response(data=context)

#Company profile setup
class CompanyProfileSetup(APIView):
    authentication_classes     = []
    permission_classes         = []
    serializer_class           = CompanyProfileSerializer


    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
         'email': openapi.Schema(type=openapi.TYPE_STRING , description='email + the rest of the data from response'),
     }),
    responses={200: CompanyProfileSerializer,400: 'Error'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')

        context = {}
        email = request.data.get('email')
        email = email.lower() if email else None
        #companyprofile = CompanyProfile class in database #select related = join in sql
        account     = Account.objects.select_related('companyprofile').filter(email=email)




        if account.count() == 0:
            #print("inside if")
            context['response'] = 'Error'
            context['error_message'] = 'email not registered'
            return Response(data=context)

        account = account[0]

        data = request.data.copy()
        try:
            company_profile = account.companyprofile

        except Account.companyprofile.RelatedObjectDoesNotExist:
            context = {"response":"error", "error_msg":"company profile not exist"}
            return Response(data=context)



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


class LogoUploadView(APIView):

    permission_classes = []
    parser_class = (MultiPartParser, JSONParser)



    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
     'email': openapi.Schema(type=openapi.TYPE_STRING , description='email in the url'),
     'logo' :  openapi.Schema(type=openapi.TYPE_FILE , description='.pdf or imgs '),
     }),
     responses={201: LogoSerializer , 400 : 'Bad Request'})
    def post(self, request, *args, **kwargs):
        print(f'\n{request.data}')
        #print(dir(request.stream.body))
        context={}
        #to retrieve email from url
        email = request.GET.get('email')
        print(request.data)
        #print(dir(request.stream))

        email = email.lower() if email else None
        account = Account.objects.filter(email=email)

        if account.count() == 0:
            context['response'] = 'Error'
            context['error_message'] = 'email not found'
            return Response(data=context)

        account = account[0]

        context['file'] = request.FILES.get('logo')

        file_serializer = LogoSerializer(account ,data=context)

        if file_serializer.is_valid():
            file_serializer.save()
            context= {**context,**file_serializer.data.copy()}
            context['response']    = "Success"
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
