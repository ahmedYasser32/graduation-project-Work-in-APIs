from account.models import Account
from django.db import models
#from django_mysql.models import ListCharField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



#remove class MyAccountManager(BaseUserManager):

#remove class CompanyAccount(AbstractBaseUser):

class CompanyProfile(models.Model):

    #Lists of choices
    industries         =  [("T","Tech"),("ARCH","Architecture")
		,("TR","Translation"),("DES","Design"),("MA","Media and Advertising"),("ME","Medicine")]

    company_types      =  [("PRV","Private company"),("PUB","Public Company"),("NPO","Non Profit Organization")]

    company_sizes      = [("SB","Small Business"),("ME","Mid Market enterprise"),("EN","Enterprise")]

    #Data

    #make company related to Account model

    user               = models.OneToOneField(Account,on_delete=models.CASCADE,primary_key=True,)
    #image attribute
    logo               = models.BinaryField(null=True, editable=True)
    content_type       = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    size_of_company    = models.CharField(max_length=25,choices=company_sizes,default='SB')
    company_name       = models.CharField(max_length=25,null = True)


    size_of_company    = models.CharField(max_length=25,choices=company_sizes,default='SB')
    company_industries = models.CharField(max_length=25,choices=industries,default='T')
    company_type       = models.CharField(max_length=25,choices=company_types,default='PRV')
    mobile_number      = models.CharField(max_length=13,null=True)
    job_title          = models.CharField(max_length=25,null=True)
    no_of_employees    = models.CharField(max_length=9,null=True)
    isInternational    = models.BooleanField(null=True)
    headquarters       = models.CharField(max_length=30,null=True)
    founded_at         = models.DateTimeField(null=True)

    """ #Multiple locations??
    locations = ListCharField(
        base_field=CharField(max_length=10),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    )
"""


