import time
start_time = time.time()
from pathlib import Path
from pprint import pprint
from affinda import AffindaAPI, TokenCredential
import pandas as pd
token = "c66179de88e40f465ea1a25ad8c6115676bc0f5a"
#file_pth = Path("Marwancv.pdf")

credential = TokenCredential(token=token)
client = AffindaAPI(credential=credential)

# with open(file_pth, "rb") as f:
#     #reformatted_resume = client.create_reformatted_resume(file=f, file_name=file_pth.name, resume_format='zuDqhDNZ')
#     resume = client.create_resume(file=f)
#

# pprint(resume.as_dict())
#
# all_resumes = client.get_all_resumes()
#pprint(all_resumes.as_dict())
#mo7amed cv
#identifier = 'zuDqhDNZ'

#sonni cv
#identifier = 'neuGGjlM'
#ahmad identifier
#identifier= 'mqfFjAWv'
#aly cv
#identifier='HygHyXbd'
#Marwancv
#identifier= 'IYWDMHYX'
#AHMAD LAST CV
identifier='QbemXfNR'

resume = client.get_resume(identifier=identifier)

resume=resume.as_dict()



pprint(resume['data'].keys())
pprint(resume['meta'])
pprint(resume)

x=0

print(f"{resume['data']['is_resume_probability']}%")

if 'name' in resume['data']:

    firstname = resume['data']['name']['first']
    lastname  = resume['data']['name']['last']
    rawname   = resume['data']['name']['raw']
    print(f" fname :{firstname},Lname :{lastname},fullname :{rawname}")
    x+=2

if  'phone_numbers' in resume['data']:

    if resume['data']['phone_numbers']:
        phonenumber = resume['data']['phone_numbers'][0]
        print(f"Phone number :{phonenumber}")
        x+=1

if 'emails' in resume['data']:

    if resume['data']['emails']:
        email = resume['data']['emails'][0]
        print(f"email is {email}")
        x+=1

if 'date_of_birth'  in resume['data']:
    birthdate=resume['data']['date_of_birth']
    print(f"Birth date is :{birthdate}")
    x+=1


if  'languages' in resume['data']:
    languages= resume['data']['languages']
    print(f"langauges  are : {languages}")
    x+=1

if 'skills' in resume['data']:
    #print(resume['data']['skills'])
    skills_table = pd.DataFrame.from_dict(resume['data']['skills'])
    #print(skills_table)
    skills_list = skills_table.name.values
    skills=', '.join(map(str, skills_list))
    print(f"Skills is {skills}")
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
                print(f" University :{Universities} ")
                x+=1

            if 'accreditation' in resume['data']['education'][i]:

                if 'education_level' in resume['data']['education'][i]['accreditation']:
                        education_level    = resume['data']['education'][i]['accreditation']['education_level']
                        edlevel.append(education_level)
                        edLevel=', '.join(edlevel)
                        x+=1
                        print(f"Education_level :{edLevel}")

                if 'education' in resume['data']['education'][i]['accreditation']:
                        education    = resume['data']['education'][i]['accreditation']['education']

                        fieldofStudy.append(education)
                        StudyFields=', '.join(fieldofStudy)
                        x+=1
                        print(f"Study field:{StudyFields}")


                if 'grade' in resume['data']['education'][i] :
                    gpa = resume['data']['education'][i]['grade']['value']
                    print("gpa loop")

                    gpas.append(gpa)
                    GPA=', '.join(gpas)
                    print(f"Print Gpa is: {GPA}")
                    x+=1


                if 'dates' in resume['data']['education'][i]:
                    year = resume['data']['education'][i]['dates']['completion_date'].split('-')[i]
                    year_of_grad.append(year)
                    year_of_graduation=max(year_of_grad)
                    print(f"Year of grad is :{year_of_graduation}")
                    x+=1


if 'location' in resume['data']:

    if 'country' in resume['data']['location']:
     country = resume['data']['location']['country']
     print(f"Country is : {country}")
     x+=1

    if'state' in resume['data']['location']:
     city    = resume['data']['location']['state']
     print(f"City is :{city}")
     x+=1

    area=resume['data']['location']['raw_input']
    print(f"adress :{area}")
    x+=1

if'work_experience' in  resume['data']:

    if resume['data']['work_experience']:
        length =  len( resume['data']['work_experience'])
        job_title=[]

        x+=1

        for i in range(length):

            job_title.append(resume['data']['work_experience'][i]['job_title'])
            jobs_intrested =', '.join(job_title)
            print(f"Job Title intrested in: {jobs_intrested}")

if 'websites' in resume['data']:
    if resume['data']['websites']:
        website = resume['data']['websites'][0]
        print(f"website: {website}")
        x+=1

if 'linkedin' in resume['data']:
    linkedin = resume['data']['linkedin']
    print(f"linked in: {linkedin}")

print(f"{x} fields have been automatically filled")
print("--- in %s seconds ---" % (time.time() - start_time))


