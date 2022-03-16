import time
start_time = time.time()
from pathlib import Path
from pprint import pprint
from affinda import AffindaAPI, TokenCredential

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
pprint(all_resumes.as_dict())
identifier = 'zuDqhDNZ'
identifier = 'NBxYdVlg'
identifier = 'neuGGjlM'
resume = client.get_resume(identifier=identifier)

print(resume.as_dict())

# all_redacted_resumes = client.get_all_redacted_resumes()
#
# pprint(all_redacted_resumes.as_dict())
# pprint(redacted_resume.as_dict())
# redacted_resume = client.get_redacted_resume(identifier=identifier)

#pprint(redacted_resume.as_dict())
#pprint(reformatted_resume.as_dict())
#all_reformatted_resumes = client.get_all_reformatted_resumes()

#pprint(all_reformatted_resumes.as_dict())
print("--- %s seconds ---" % (time.time() - start_time))
