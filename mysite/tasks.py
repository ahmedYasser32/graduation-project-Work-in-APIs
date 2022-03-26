
from django.core.mail import EmailMessage
import threading
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
    def __init__(self, file):
        self.file = file
        self.response= None
        threading.Thread.__init__(self)

    def run(self):
        token = "c66179de88e40f465ea1a25ad8c6115676bc0f5a"
        credential = TokenCredential(token=token)
        client = AffindaAPI(credential=credential)
        resume = client.create_resume(file=self.file.open('rb'))
        #identifier = 'zuDqhDNZ'
        #resume = client.get_resume(identifier=identifier)
        self.response= resume.as_dict()

    def join_with_return(self):
        self.join()
        return self.response




