from django.core.mail import EmailMessage
import threading

class SendMail(threading.Thread):
    def __init__(self, subject, body, to):
        self.subject = subject
        self.body = body
        self.to = to
        threading.Thread.__init__(self)

    def run(self):
        message = EmailMessage(self.subject, self.body, 'master.clean.dcl@gmail.com', [self.to])
        return message.send()
