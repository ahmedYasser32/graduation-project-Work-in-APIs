import time
start_time = time.time()
from pathlib import Path
from pprint import pprint
from affinda import AffindaAPI, TokenCredential
import pandas as pd
token = "c66179de88e40f465ea1a25ad8c6115676bc0f5a"
file_pth = Path("AhmedyasserCV.pdf")

credential = TokenCredential(token=token)
client = AffindaAPI(credential=credential)

with open(file_pth, "rb") as f:
    reformatted_resume = client.create_reformatted_resume(file=f, file_name=file_pth.name, resume_format='zuDqhDNZ')
    redacted_resume = client.create_redacted_resume(file=f)
    resume = client.create_resume(file=f)

pprint(resume.as_dict())

all_resumes = client.get_all_resumes()
#pprint(all_resumes.as_dict())
#mo7amed cv
#dentifier = 'zuDqhDNZ'

#sonni cv
identifier = 'neuGGjlM'

resume = client.get_resume(identifier=identifier)

resume=resume.as_dict()

pprint(resume.keys())

pprint(resume['data'].keys())
pprint(resume['meta'])
x=0

print(f"{resume['data']['is_resume_probability']}%")

if 'name' in resume['data']:

    firstname = resume['data']['name']['first']
    lastname  = resume['data']['name']['last']
    rawname   = resume['data']['name']['raw']
    print(f" fname :{firstname},Lname :{lastname},fullname :{rawname}")
    x+=2
if  'phone_numbers' in resume['data'] :
    phonenumber=resume['data']['phone_numbers'][0]
    print(f"Phone number :{phonenumber}")
    x+=1

if 'emails' in resume['data']:
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
    skills_list=skills_table.name.values
    skills=', '.join(map(str, skills_list))
    print(f"Skills is {skills}")
    x+=1

if 'education' in resume['data']:
    if 'organization' in resume['data']['education'][0]:
        University     = resume['data']['education'][0]['organization']
        print(f" University :{University} ")
        x+=1
    if 'accreditation' in resume['data']['education'][0]:
        education_level    = resume['data']['education'][0]['accreditation']['education']
        print(f"education level:{education_level}")
        x+=1

    if 'dates' in resume['data']['education'][0]:
     year_of_graduation = resume['data']['education'][0]['dates']['completion_date'].split('-')[0]
     print(f"Year of graduation:{year_of_graduation}")
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

# if 'work_experience' in resume['data']:
#      job_titles=[]
#      for i in range(len(resume['data']['work_experience'])):
#          job_titles[i]= resume['data']['work_experience'][i]["job_title"]
#
#

#pprint(resume)

# pprint(all_redacted_resumes.as_dict())
# pprint(redacted_resume.as_dict())
# redacted_resume = client.get_redacted_resume(identifier=identifier)

#pprint(redacted_resume.as_dict())
#pprint(reformatted_resume.as_dict())
#all_reformatted_resumes = client.get_all_reformatted_resumes()

#pprint(all_reformatted_resumes.as_dict())
print(f"{x} fields have been automatically filled")
print("--- in %s seconds ---" % (time.time() - start_time))
