
from django.db import models
#from django_mysql.models import ListCharField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




class MyAccountManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')


		user = self.model(
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, email, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class CompanyAccount(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= None
    firstname               = models.CharField(max_length=150)
    lastname                = models.CharField(max_length=150)
    company_name            = models.CharField(max_length=150)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    verified                = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class CompanyProfile(models.Model):
    industries=[("T","Tech"),("ARCH","Architecture")
		,("TR","Translation"),("DES","Design"),("MA","Media and Advertising"),("ME","Medicine")]
    company_types=[("PRV","Private company"),("PUB","Public Company"),("NPO","Non Profit Organization")]
    company_sizes=[("SB","Small Business"),("ME","Mid Market enterprise"),("EN","Enterprise")]
    Company = models.OneToOneField(CompanyAccount,on_delete=models.CASCADE,primary_key=True,)
    logo= models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    size_of_company = models.CharField(max_length=25,choices=company_sizes,)
    company_industries=models.CharField(max_length=25,choices=industries,)
    company_type=models.CharField(max_length=25,choices=company_types,)
    no_of_employees = models.CharField(max_length=9)
    isInternational=models.BooleanField()
    headquarters = models.CharField(max_length=30)
    founded_at   = models.DateTimeField()



   #Multiple locations??
    #locations = ListCharField(
        #base_field=CharField(max_length=10),
        #size=6,
        #max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    #)



