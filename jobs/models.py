from django.db import models
from companies.models import CompanyProfile
from account.models import Profile

class Jobs(models.Model):

    company                 =  models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    job_title               =  models.CharField(max_length=20,default="junior")
    job_category            =  models.CharField(max_length=20,default="IT")
    job_type                =  models.CharField(max_length=20,default="fulltime")
    #education_level_choices =  [("ST","Student"),("BCH","Bachelor"),("UG","UnderGrad"),("MST","Masters"),("PHD","PHD")]
    description             =  models.CharField(max_length=1000)
    requirements            =  models.CharField(max_length=1000)
    education_level         =  models.CharField(max_length=20)
    experience              =  models.CharField(max_length=2)
    career_level            =  models.CharField(max_length=20,default="Junior")
    salary                  =  models.CharField(max_length=10,null=True)
    isConfidential          =  models.BooleanField(default=True)
    applicants              =  models.ManyToManyField(Profile,blank=True)
    created_at              =  models.DateTimeField(auto_now_add=True,null=True)
    applicantscount         = models.PositiveSmallIntegerField(default=0)




