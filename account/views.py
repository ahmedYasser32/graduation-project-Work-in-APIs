from account.models import Account,AccountCode
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import *
from account.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import pytz
from datetime import datetime
from cryptography.fernet import InvalidToken
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from cryptography.fernet import Fernet
from mysite.tasks import SendMail


# Register API
class RegisterAPI(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        print(request.data.get('email````'))
        context = {}
        email = request.data.get('email').lower()


       #check email if already exist send error

        if Account.objects.filter(email=email).count()>0:
            context['error_message'] = 'That email is already in use.'
            context['response'] = 'error'
            return Response(data=context)


       # Assign serializer
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            #if valid save object and send response
            account = serializer.save()
            context['email'] = account.email
            context['firstname'] = account.firstname
            context['lastname'] = account.lastname
            context['pk'] = account.pk
            token = Token.objects.get(user=account).key
            context['token'] = token
            context['is_verified'] = account.verified
            context['is_company'] = account.is_company
            context['response'] = 'success'
            return Response(data=context)


        #if not valid return error
        context = serializer.errors.copy()
        context['response'] = 'error'
        return Response(data=context)



class LoginAPI(APIView):
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
            context['response'] = 'success'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['token'] = token.key
            context['is_verified'] = account.verified
            context['is_company'] = account.is_company
            context['firstname'] = account.firstname
            context['lastname'] = account.lastname
            print(account)
            print(context)
            return Response(data=context)
        context['response'] = 'Error'
        context['error_message'] = 'Invalid credentials'
        return Response(data=context)



def encryption(token, mode, key):
    # create object fernet to encrypt or decrypt
	fernet = Fernet(key)
    #e = encrypt
	if mode == 'e':
        #encode token then encrypt
		encMessage = fernet.encrypt(token.encode())
		return encMessage.decode()
    #d = decrypted
	elif mode=='d':
        #decrypt message
		try:
			decMessage = fernet.decrypt(token.encode()).decode()
		except InvalidToken:
			decMessage = ''
		return decMessage
	return None


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def check_reset_password_mail(request):
	if request.method == 'POST':
		data = {}
		email = request.data.get('email').lower()
		try:
			account = Account.objects.get(email=email)
		except Account.DoesNotExist:
			data['response'] = 'error'
			data['error_msg'] = "Account does not exist"
			return Response(data)

		codes = AccountCode.objects.filter(user= account.pk)
		tz = pytz.timezone('UTC')
		now = datetime.now(tz)

		if codes.count()==0:
			codes = AccountCode.objects.create(user=account, date=now , date2=now , date3=now)
			codes.renew_reset_password()
			codes.save()
		else:
			codes = codes[0]
			codes.renew_reset_password()
		period = (codes.date2 - codes.date).seconds // 60

		if codes.freeze:
			x = (now - codes.date3).seconds // 60
			if x < 60:
				return Response({'response': 'error', 'error_msg': f'you are blocked for {60 - x} minutes'})

		x = (now - codes.date2).days

		if x >= 1:
			codes.foul_count -= 1
			codes.resend_count = 0
			codes.block = False
		if not codes.block:
			if codes.resend_count < 10:

				if period < 60:
					codes.resend_count += 1
					codes.date2 = now
				else:

					codes.resend_count = 1
					codes.date = now
					codes.date2 = now
			else:
				if codes.foul_count >= 2:
					codes.block = True
					codes.save()
					return Response({'response':'error', 'error_msg':'you are blocked for one day'})
				if codes.freeze:
					codes.freeze = False
					codes.resend_count = 0
					codes.date = now
					codes.date2 = now
				else:
					codes.date3 = now
					codes.freeze = True
					codes.date2 = now
					codes.date = now
					codes.save()
					return Response({'response': 'error', 'error_msg': f'you are blocked for {60} minutes'})

				if codes.foul_count >= 2:
					codes.block = True
					codes.save()
					return Response({'response':'error', 'error_msg':'you are blocked for one day'})
				else:
					codes.foul_count += 1
					codes.resend_count = 1
		else:
			return Response({'response': 'error', 'error_msg': 'you are blocked for one day'})

		codes.save()
		subject = f'hi {account.firstname}, this mail is for your new password'
		body = f'your reset password code is: {codes.reset_password}'
		SendMail(subject,body, email).start()
		data['response'] = 'success'
		key = b'S5RsmrVWsyxD9XU07M1pp3Iza-iJX7QT8KEo52-E5l4='
		t = Token.objects.get(user=account).key
		token = encryption(t, 'e', key)
		data['token'] = token
		data['email'] = account.email
		return Response(data)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def check_reset_password_code(request, token):
	data = {}
	email = request.data.get('email').lower()
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		data['response'] = 'error'
		data['error_msg'] = "Account does not exist"
		return Response(data)

	key = b'S5RsmrVWsyxD9XU07M1pp3Iza-iJX7QT8KEo52-E5l4='
	token = encryption(token, 'd', key)
	account_token = Token.objects.get(user=account).key
	if token != account_token:
		data['response'] = 'error'
		data['error_msg'] = "Account does not exist"
		return Response(data)

	if request.method == 'POST':

		reset_password_code = request.data.get('code')

		codes = AccountCode.objects.filter(user=account.pk)
		if codes.count() == 0:
			return Response({'response':'error'})
		if reset_password_code == codes[0].reset_password:
			key = b'TQXelGorbDLwLdhklkXcDpySpMiW8jHuMzw3tpH-gok='
			token = encription(token, 'e', key)
			data['response'] = 'success'
			data['token'] = token
			data['email'] = account.email
			return Response(data)
		data['response'] = 'error'
		data['error_msg'] = 'invalid code'
		return Response(data)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def reset_password(request, token):
	data = {}
	email = request.data.get('email')
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		data['response'] = 'error'
		data['error_msg'] = "Account does not exist"
		return Response(data)


	key = b'TQXelGorbDLwLdhklkXcDpySpMiW8jHuMzw3tpH-gok='
	token = encription(token, 'd', key)
	account_token = Token.objects.get(user=account).key
	if token != account_token:
		data['response'] = 'error'
		data['error_msg'] = "Account does not exist"
		return Response(data)


	if request.method == 'POST':


		password = request.data.get('password')
		password2 = request.data.get('password2')

		try:
			validate_password(password)
		except ValidationError as val_err:
			data['response'] = 'error'
			data['error_msg'] = ' '.join(val_err.messages)
			return Response(data)

		if password != password2:
			data['response'] = 'error'
			data['error_msg'] = 'Passwords must match.'
			return Response(data)


		account.set_password(password)
		account.save()
		data['response'] = 'success'

		#codes = AccountCode.objects.filter(user=account.pk)
	    #if codes.count()>0:
		#	codes[0].

		return Response(data)


