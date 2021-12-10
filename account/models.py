from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

"""
def upload_location(instance, filename, **kwargs):
	file_path = 'account/{filename}'.format(
			filename=filename
		)
	return file_path
"""

class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	image = models.ImageField(null= True, blank= True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	is_vendor = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def save(self, *args, **kwargs):
		first_char = self.username.__str__()[0]
		self.image = f'/static/img/{first_char}.png'
		super(Account, self).save(*args, **kwargs)

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class LocationDetail(models.Model):
	building_name_number = models.CharField(max_length=40, default="")
	floor_number = models.CharField(max_length=10, default="")
	apartmentNumber = models.CharField(max_length=10, default="")
	longitude = models.DecimalField(max_digits=12, decimal_places=10, default=0)
	latitude = models.DecimalField(max_digits=12, decimal_places=10, default=0)


class Location(models.Model):
	user = models.OneToOneField(Account, on_delete=models.CASCADE)
	location = models.ManyToManyField(LocationDetail)

class PhoneDetail(models.Model):
	phone = models.CharField(max_length=13, default='')

class Phone(models.Model):
	user = models.OneToOneField(Account, on_delete=models.CASCADE)
	phone = models.ManyToManyField(PhoneDetail)
