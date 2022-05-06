
from django.core.mail import EmailMessage
import threading
import pandas as pd
from affinda import AffindaAPI, TokenCredential
class SendMail(threading.Thread):

    def __init__(self, subject, body, to):
        self.subject = subject
        self.body = body
        self.to = to
        threading.Thread.__init__(self)

    def run(self):
        message = EmailMessage(self.subject, self.body, 'master.clean.dcl@gmail.com', [self.to])
        return message.send()



class CVParsing(threading.Thread):

    def extractData(self,resume):

        extractedData=dict()

        x=0
        if 'data' in resume:

            print(f"{resume['data'].get('is_resume_probability')}%")
            if 'name' in resume['data']:
                firstname = resume['data']['name']['first']
                lastname  = resume['data']['name']['last']
                rawname   = resume['data']['name']['raw']
                #print(f" fname :{firstname},Lname :{lastname},fullname :{rawname}")
                extractedData['firstname'] = firstname
                extractedData['lastname'] = lastname
                extractedData['fullname'] = rawname
                x+=2

            if  'phone_numbers' in resume['data']:
                if resume['data']['phone_numbers']:
                    phonenumber = resume['data']['phone_numbers'][0]
                    #print(f"Phone number :{phonenumber}")
                    extractedData['phone_number'] = phonenumber
                    x+=1

            if 'emails' in resume['data']:
                if resume['data']['emails']:
                    email = resume['data']['emails'][0]
                    #print(f"email is {email}")
                    extractedData['email'] = email
                    x+=1

            if 'date_of_birth'  in resume['data']:
                birthdate = resume['data']['date_of_birth']
                #print(f"Birth date is :{birthdate}")
                extractedData['birthdate'] = birthdate
                x+=1

            if  'languages' in resume['data']:
                languages= resume['data']['languages']
                #print(f"langauges  are : {languages}")
                #list
                extractedData['langauges'] = languages
                x+=1

            if 'skills' in resume['data']:
                #print(resume['data']['skills'])
                skills_table = pd.DataFrame.from_dict(resume['data']['skills'])
                #print(skills_table)
                skills_list = skills_table.name.values
                #print(f"Skills is {skills_list}")
                extractedData['skills'] = skills_list
                x+=1

            if 'education' in resume['data']:
                organization=[]
                edlevel=[]
                gpas=[]
                year_of_grad=[]
                fieldofStudy=[]

                if resume['data']['education']:

                 for i in range(len(resume['data']['education'])):

                     if 'organization' in resume['data']['education'][i]:

                         University     = resume['data']['education'][i]['organization']
                         organization.append(University)
                         Universities=', '.join(organization)
                         #print(f" University :{Universities} ")
                         #list
                         extractedData['university'] = Universities[-1]

                     if 'accreditation' in resume['data']['education'][i]:

                         if 'education_level' in resume['data']['education'][i]['accreditation']:
                            education_level    = resume['data']['education'][i]['accreditation']['education_level']
                            edlevel.append(education_level)
                            edLevel=', '.join(edlevel)
                            extractedData['education_level']=edLevel
                            #print(f"Education_level :{edLevel}")

                         if 'education' in resume['data']['education'][i]['accreditation']:
                             education    = resume['data']['education'][i]['accreditation']['education']
                             fieldofStudy.append(education)
                             StudyFields=', '.join(fieldofStudy)
                             extractedData['study_fields']=StudyFields


                     if 'grade' in resume['data']['education'][i] :
                         gpa = resume['data']['education'][i]['grade']['value']
                         #print("gpa loop")
                         gpas.append(gpa)
                         GPA=', '.join(gpas)
                         extractedData['gpa']=GPA

                     if 'dates' in resume['data']['education'][i]:
                         year = resume['data']['education'][i]['dates']['completion_date'].split('-')[i]
                         year_of_grad.append(year)
                         year_of_graduation=max(year_of_grad)
                         extractedData['yearofgrad']=year_of_graduation

                 if organization :
                     x+=1


                 if edlevel:
                     x+=1


                 if gpas :
                     x+=1


                 if year_of_grad :
                     x+=1


                 if  fieldofStudy :
                     x+=1


            if 'location' in resume['data']:
                if 'country' in resume['data']['location']:
                    country = resume['data']['location']['country']
                    #print(f"Country is : {country}")
                    extractedData['country']=country
                    x+=1

                if'state' in resume['data']['location']:
                    city    = resume['data']['location']['state']
                    #print(f"City is :{city}")
                    extractedData['city']=city
                    x+=1

                area=resume['data']['location']['raw_input']
                extractedData['area']=area
                x+=1

            if'work_experience' in  resume['data']:
                job_title=[]
                if resume['data']['work_experience']:
                    length =  len( resume['data']['work_experience'])
                    x+=1

                    for i in range(length):
                        job_title.append(resume['data']['work_experience'][i]['job_title'])
                        jobs_intrested =', '.join(job_title)


                    if job_title :
                        x+=1
                        extractedData['job_titles']=job_title

            if 'websites' in resume['data']:
                if resume['data']['websites']:
                    website = resume['data']['websites'][0]
                    extractedData['website']=website
                    x+=1

            if 'linkedin' in resume['data']:
                linkedin = resume['data']['linkedin']
                extractedData['linkedin']=linkedin

            #print(f"{x} fields have been automatically filled")
            extractedData['fieldscompleted']=x

            #print(extractedData)
            return extractedData

    def __init__(self, file):
        self.file = file
        self.response = {}
        threading.Thread.__init__(self)

    def run(self):
        token = "d77e5245c2dec09326e46b5239fd34036b3a0e3d"
        credential = TokenCredential(token=token)
        client = AffindaAPI(credential=credential)
        resume = client.create_resume(file=self.file.open('rb'))
        #identifier = 'zuDqhDNZ'
        #resume = client.get_resume(identifier=identifier)
        self.response = self.extractData(resume.as_dict())

    def join_with_return(self):

        self.join()
        return self.response




