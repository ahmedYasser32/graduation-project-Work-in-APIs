from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        context = {}
        email = request.data.get('email').lower()


       #check email if already signed up send error

        if Account.objects.filter(email=email).count()>0:
            context['error_message'] = 'That email is already in use.'
            context['response'] = 'error'
            return Response(data=context)


       # Assign serializer
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            #if valid save object and send response
            account = serializer.save()
            context['email'] = account.email
            context['pk'] = account.pk
            token = Token.objects.get(user=account).key
            context['token'] = token
            context['is_verified'] = account.verified
            return Response(data=context)


        #if not valid return error
        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context)






