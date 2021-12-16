from rest_framework import serializers

from account.models import Account


class RegistrationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ['email', 'firstname', 'lastname', 'password', 'is_staff',  'verified',]
		extra_kwargs = {
				'password': {'write_only': True, 'min_length': 8, 'max_length': 50},
		}


	def	save(self) :

		account = Account(
					email=self.validated_data['email'],
				)
		password = self.validated_data['password']
		account.set_password(password)
		account.save()
		return account

