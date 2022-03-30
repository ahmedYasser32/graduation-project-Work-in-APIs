from django.db import models
from companies.models import CompanyProfile
from account.models import Profile

class Jobs(models.Model):

    company                 =  models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    education_level_choices =  [("ST","Student"),("BCH","Bachelor"),("UG","UnderGrad"),("MST","Masters"),("PHD","PHD")]
    description             =  models.CharField(max_length=1000)
    requirements            =  models.CharField(max_length=1000)
    education_level         =  models.CharField(max_length=15,choices=education_level_choices,default="BCH")
    experience              =  models.CharField(max_length=2)
    salary                  =  models.CharField(max_length=10)
    isConfidential          =  models.BooleanField(default=True)
    applicants              =  models.ManyToManyField(Profile)

