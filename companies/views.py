"""from django.shortcuts import render
    from companies.models import CompanyAccount
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from companies.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Register API
class Company_RegisterAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        context = {}
        email = request.data.get('email').lower()


       #check email if already exist send error

        if CompanyAccount.objects.filter(email=email).count()>0:
            context['error_message'] = 'That email is already in use.'
            context['response'] = 'error'
            return Response(data=context)


       # Assign serializer
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            #if valid save object and send response
            account = serializer.save()
            context['email'] = account.email
            context['company_name'] = account.company_name
            context['firstname'] = account.firstname
            context['lastname'] = account.lastname
            context['pk'] = account.pk
            token = Token.objects.get(user=account).key
            context['token'] = token
            context['is_verified'] = account.verified
            return Response(data=context)


        #if not valid return error
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
            context['company_name'] = account.company_name
            context['email'] = email.lower()
            context['token'] = token.key
            context['is_verified'] = account.verified
            context['firstname'] = account.firstname
            context['lastname'] = account.lastname
            print(account)
            print(context)
            return Response(data=context)
        context['response'] = 'Error'
        context['error_message'] = 'Invalid credentials'
        return Response(data=context)


"""