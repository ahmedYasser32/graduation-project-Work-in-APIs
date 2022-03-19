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
#identifier = 'zuDqhDNZ'
#sonni cv
identifier = 'neuGGjlM'
resume = client.get_resume(identifier=identifier)
resume=resume.as_dict()
#pprint(resume.as_dict())
pprint(resume['data'].keys())
pprint(resume['meta'])

if 'name' in resume['data']:

    firstname=resume['data']['name']['first']
    lastname=resume['data']['name']['last']
    rawname=resume['data']['name']['raw']
    print(f" fname :{firstname},Lname :{lastname},fullname :{rawname}")

if  'phone_numbers' in resume['data'] :
    phonenumber=resume['data']['phone_numbers'][0]
    print(f"Phone number :{phonenumber}")

if 'emails' in resume['data']:
    email = resume['data']['emails'][0]
    print(f"email is {email}")

if 'date_of_birth'  in resume['data']:
    birthdate=resume['data']['date_of_birth']
    print(f"Birth date is :{birthdate}")

if  'languages' in resume['data']:
    languages= resume['data']['languages']
    print(f"langauges  are : {languages}")

if 'skills' in resume['data']:
    print(resume['data']['skills'])
    skills_table = pd.DataFrame.from_dict(resume['data']['skills'])
    print(skills_table)
    skills_list=skills_table.name.values
    skills=', '.join(map(str, skills_list))
    print(f"Skills is {skills}")

if 'education' in resume['data']:

    organization = resume['data']



# pprint(all_redacted_resumes.as_dict())
# pprint(redacted_resume.as_dict())
# redacted_resume = client.get_redacted_resume(identifier=identifier)

#pprint(redacted_resume.as_dict())
#pprint(reformatted_resume.as_dict())
#all_reformatted_resumes = client.get_all_reformatted_resumes()

#pprint(all_reformatted_resumes.as_dict())
print("--- %s seconds ---" % (time.time() - start_time))
