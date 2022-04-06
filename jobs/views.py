from mysite.tasks import CVParsing
from rest_framework import status
from account.models import Account,AccountCode,Profile
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import *
from account.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from cryptography.fernet import InvalidToken
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from cryptography.fernet import Fernet
from mysite.tasks import SendMail
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser,DataAndFiles, BaseParser
from jobs.models import Jobs
from jobs.serializers import JobSerializer

class JobCreation(APIView):

    authentication_classes     = []
    permission_classes         = [IsAuthenticated]
    serializer_class           = JobSerializer


    @swagger_auto_schema(    operation_description="headers = {'Authorization': 'Token {token}'}", request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,

    properties={
        'Same data of the response example': openapi.Schema(type=openapi.TYPE_STRING , description='7abeby'),
     }),
     responses={200: serializer_class, 400 : 'Bad Request'})

    def post(self, request, *args, **kwargs):


        if not request.user.is_company:
            context['response'] = 'error'
            context['error'] = 'you are not allowed to access this API'

            return Response(data=context)


        data = request.data.copy()
        context['company'] =  request.user.companyprofile
        #set relation
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            #if valid save object and send response
            serializer.save()
            #** turn dictioanries into vars and copy values from serailizer
            context= {**context,**serializer.data.copy()}
            context['response']    = "Success"

            return Response(data=context)



        else:
            context = serializer.errors.copy()
            context['response'] = 'error'
            return Response(data=context)
