from rest_framework import serializers

from companies.models import Account


class RegistrationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ['email','company_name', 'firstname', 'lastname', 'password', 'is_staff',  'verified',]
		extra_kwargs = {
				'password': {'write_only': True, 'min_length': 8, 'max_length': 50},
		}


	def	save(self) :

		account = Account(
			email=self.validated_data['email'],
			firstname=self.validated_data['firstname'],
			lastname=self.validated_data['lastname'],
			companyname=self.validates_data['company_name'],
				)
		password = self.validated_data['password']
		account.set_password(password)
		account.save()
		return account
