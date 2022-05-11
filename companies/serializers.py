from rest_framework   import serializers
from companies.models import Review
from account.models   import Account
from companies.models import CompanyProfile


class CompanyRegistrationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ['email', 'firstname', 'lastname', 'password', 'is_staff',  'verified','is_company']
		extra_kwargs = {
				'password': {'write_only': True, 'min_length': 8, 'max_length': 50},
		}


	def	save(self) :

		account = Account(
		email=self.validated_data['email'], is_company= True)
		password = self.validated_data['password']

		account.set_password(password)
		account.save()
		return account

class CompanyProfileSerializer(serializers.ModelSerializer):

	class Meta:
		model = CompanyProfile
		fields = '__all__'

class LogoSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields = ['logo']
    def get_logo(self, job):
        if job.company.user.file:
            return job.company.user.file.url
        return ''


class ReviewSereializier(serializers.ModelSerializer):
	class Meta :
		model   = Review
		fields  = '__all__'



