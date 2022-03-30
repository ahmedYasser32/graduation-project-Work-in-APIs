from django.shortcuts import render
from jobs.models import Jobs
from jobs.serializers import JobSerializer

class JobCreation(APIView):

    authentication_classes     = []
    permission_classes         = []
    serializer_class           = JobSerializer


    @swagger_auto_schema(request_body=openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={
        'is_authenticates': openapi.Schema(type=openapi.TYPE_STRING , description='email'),
     }),
     responses={200: serializer_class, 400 : 'Bad Request'})
    def post(self, request, *args, **kwargs):


        if not request.user.is_company:
            context['response'] = 'error'
            context['error'] = 'you are not allowed to access this API'

            return Response(data=context)


        data = request.data.copy()
        context['company'] =  request.user.companyprofile
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
