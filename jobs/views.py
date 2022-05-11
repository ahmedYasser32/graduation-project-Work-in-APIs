from django.db.models import Case, When, Q
from mysite.tasks import CVParsing
from rest_framework import status
from account.models import Account,AccountCode,Profile
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import *
from account.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from cryptography.fernet import InvalidToken
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from cryptography.fernet import Fernet
from mysite.tasks import SendMail
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser,DataAndFiles, BaseParser
from jobs.models import Jobs
from jobs.serializers import JobSerializer,joblistSerializer, CompanyJobSerializer

class JobCreation(APIView):

    authentication_classes     = []
    permission_classes         = [IsAuthenticated]
    serializer_class           = JobSerializer


    @swagger_auto_schema(    operation_description="headers = {'Authorization': 'Token {token}'}  Company token", request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,

    properties={
        'Same data of the response example': openapi.Schema(type=openapi.TYPE_STRING , description='7abeby'),
     }),

     responses={200: serializer_class, 400 : 'Bad Request'})

    def post(self, request, *args, **kwargs):


        if not request.user.is_company:
            context['response'] = 'error'
            context['error'] = 'you are not allowed to access this API'

            return Response(data=context)


        data = request.data.copy()
        context['company'] = request.user.companyprofile
        #set relation
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            #if valid save object and send response
            serializer.save()
            #** turn dictioanries into vars and copy values from serailizer
            context= {**context,**serializer.data.copy()}
            context['response']    = "Success"

            return Response(data=context)



        else:

            context = serializer.errors.copy()
            context['response'] = 'error'
            return Response(data=context)

class JobDetail (APIView):

     authentication_classes     = []
     permission_classes         = []
     serializer_class           = JobSerializer


     @swagger_auto_schema(operation_description="Job primarykey in the url to view the job detail")
     def get(self, request, job):

        context = {}
        job = Jobs.objects.filter(pk=job)
        if job.count() == 0:
            context['response'] = 'error'
            context['error'] = 'job doesnt exist'
            return Response(data=context)

        job_detail=job[0]


        serializer = self.serializer_class(job_detail)
        context= {**context,**serializer.data.copy()}
        context['response']='success'
        return Response(data=context)


class CompanyJobDetail(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyJobSerializer

    @swagger_auto_schema(operation_description="headers = {'Authorization': 'Token {token}'} Company token, job primary key in url")
    def get(self, request, job):
        context = {}
        job = Jobs.objects.filter(pk=job).first()
        if not job:
            context['response'] = 'error'
            context['error'] = "job doesn\'t exist"
            return Response(data=context)
        if not request.user.is_company:
            context['response'] = 'error'
            context['error'] = "not allowed"
            return Response(data=context)




        serializer = self.serializer_class(job)
        context = {**context, **serializer.data}
        context['response'] = 'success'
        return Response(data=context)


class JobApply(APIView):


    authentication_classes     = [IsAuthenticated]
    permission_classes         = []
    serializer_class           = JobSerializer

    @swagger_auto_schema(operation_description="headers = {'Authorization': 'Token {token}'} User token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'job pk': openapi.Schema(type=openapi.TYPE_STRING, description=' In url'),

            }),
        responses={201: JobSerializer, 400: 'Bad Request'})

    def post(self, request, job) :

        context = {}
        job = Jobs.objects.filter(pk=job)
        if job.count() == 0:
            context['response'] = 'error'
            context['error']    = 'job doesnt exist'
            return Response(data=context)

        user = request.user.profile

        # set relation
        job[0].applicants.add(user)
        job.applicantscount = job.applicantscount + 1

        context['user'] = user
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            #if valid save object and send response
            serializer.save()
            #** turn dictioanries into vars and copy values from serailizer
            context= {**context,**serializer.data.copy()}
            context['response']    = "Success"

            return Response(data=context)

class AppliedJobs(APIView):

    authentication_classes     = [IsAuthenticated]
    permission_classes         = []
    serializer_class           = joblistSerializer

    @swagger_auto_schema(operation_description="headers = {'Authorization': 'Token {token}'} User token")
    def get(self, request):
        context = {}
        if  request.user.is_company :
             context['response' ] ='error'
             context['Error']     = 'You are not allowed to access this API'
             return Response(data=context)

        user = request.user.profile
        jobs = Jobs.objects.filter(applicants=user)
        serializer = self.serializer_class(jobs,many=True)
        context['jobs'] = serializer.data
        context['response']='success'
        return Response(data=context)



class CompanyJobs(APIView):
    authentication_classes     = []
    permission_classes         = []
    serializer_class           = joblistSerializer


    @swagger_auto_schema(operation_description="Email of the company in the url to get a list of the jobs created by the company")
    def get(self, request,email=None):

        context={}

        if not email:
            email = request.data.get('email')

        companies = CompanyProfile.objects.filter(user__email=email)


        if companies.count() > 0:
            company=companies[0]

        else:
          context['response'] = 'error'
          context['error_msg'] = 'invalid email'
          return Response(data=context)

        context['company_name'] = company.company_name
        context['company_location'] =  company.location
        jobs = Jobs.objects.filter(company=company)
        serializer = self.serializer_class(jobs,many=True)
        #context= {**context,**serializer.data.copy()}
        context['jobs'] = serializer.data
        context['response']='success'
        return Response(data=context)





class HomeScreen(APIView):

    authentication_classes     = []
    permission_classes         = []
    serializer_class           = joblistSerializer

    @swagger_auto_schema(operation_description="Home Screen, in the url ?email=\"\" and ?filter= to filter categories",
        responses={201: joblistSerializer, 400: 'Bad Request'})
    def get(self, requests):
        context={}
        #retrieve from url

        email  = request.GET.get('email')
        filter = request.GET.get('filter')
        jobs   = Jobs.objects.all()

        if filter:

            query  = Q(jobs.filter(job_category=filter))
        else:

            query   = Q()

        account = Account.objects.filter(email=email)

        if account.count()==0 :

            jobs.filter(query)
            serializer = self.serializer_class(jobs,many=True)
            context['jobs'] = serializer.data
            context['response']='success'
            return Response(data=context)




        if account :

            user  = account[0].profile

        else :
            context['response']='error'
            context['error_msg']='account does not exist'
            return Response(data=context)

        joblist = Jobs.objects.filter(query).annotate(

            first_query=Case(

                When(Q(job_category__icontains=user.careers_intrests) & Q(career_level__icontains=user.career_level)&
                     Q(job_title__icontains=user.job_title_looking_for)
                &Q(education_level__icontains=user.education_level ) & Q(requirements__icontains=user.skills) & Q(salary__bte=user.min_salary),
                then=('created_at')),
                default=None
            ),
            second_q=Case(
                When(Q(job_category__icontains=user.careers_intrests) & Q(career_level__icontains=user.career_level)&
                     Q(job_title__icontains=user.job_title_looking_for)& Q(job_title__icontains=user.job_title_looking_for)
                &Q(education_level__icontains=user.education_level ) & Q(requirements__icontains=user.skills) | Q(salary__bte=user.min_salary)

            )),
            third_q=Case(
                When(Q(job_category__icontains=user.careers_intrests)  & Q(career_level__icontains=user.career_level)&  Q(job_title__icontains=user.job_title_looking_for)
                &Q(education_level__icontains=user.education_level ) | Q(requirements__icontains=user.skills) | Q(salary__bte=user.min_salary)

            )),fourth_q=Case(
                When(Q(job_category__icontains=user.careers_intrests)  & Q(career_level__icontains=user.career_level)&  Q(job_title__icontains=user.job_title_looking_for)
                |Q(education_level__icontains=user.education_level ) | Q(requirements__icontains=user.skills) | Q(salary__bte=user.min_salary)

            )),fifth_q=Case(
                When(Q(job_category__icontains=user.careers_intrests)  & Q(career_level__icontains=user.career_level) | Q(job_title__icontains=user.job_title_looking_for)
                |Q(education_level__icontains=user.education_level ) | Q(requirements__icontains=user.skills) | Q(salary__bte=user.min_salary)

            )
            ),sixth_q=Case(
                When(Q(job_category__icontains=user.careers_intrests) | Q(career_level__icontains=user.career_level) | Q(job_title__icontains=user.job_title_looking_for)
                |Q(education_level__icontains=user.education_level ) | Q(requirements__icontains=user.skills) | Q(salary__bte=user.min_salary)

            )
                    )

        ).order_by(
            '-first_query',  '-second_q', '-third_q','-fourth_q','-fifth_q',
            '-created_at'
        )

        serializer = self.serializer_class(joblist, many=True)
        context['jobs'] = serializer.data
        context['response'] = 'success'
        return Response(data=context)

    class RecommendedUsers(APIView):
         authentication_classes     = [IsAuthenticated]
         permission_classes         = []
         serializer_class           = ApplicantSerializer

         @swagger_auto_schema(operation_description=" I want the job id in the url ?job_id=\" ",
          responses={201: joblistSerializer, 400: 'Bad Request'})
         def get(self, requests):
             context={}
             jobs = Jobs.objects.filter(pk=job)
             if job.count() == 0:
                 context['response'] = 'error'
                 context['error'] = 'job doesnt exist'

                 return Response(data=context)

         job = job[0]

         userslist = Profile.objects.annotate()























