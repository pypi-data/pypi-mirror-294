import os
import urllib3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
urllib3.disable_warnings()

class gmail():
    def __init__(self, **kwargs) -> None:
        
        # Outbox Settings
        if 'mailtype' in kwargs.keys(): 
            self.mailtype = kwargs['mailtype']
        else:
            self.mailtype = 'gmail'
        
        if self.mailtype == 'gmail':
            self.server = 'smtp.gmail.com'
            self.port = 587
            if 'gmail_mail' in kwargs.keys() and 'gmail_passkey' in kwargs.keys():
                self.from_mail = kwargs['gmail_mail']
                self.from_passkey = kwargs['gmail_passkey']
            else:
                self.from_mail = os.getenv('gmail_mail')
                self.from_passkey = os.getenv('gmail_passkey')
                
                if not self.from_mail:
                    self.from_mail = input("Sending email address: ")
                    os.environ['gmail_mail'] = self.from_mail

                if not self.from_passkey:
                    self.from_passkey = input("Sending email passkey: ")
                    os.environ['gmail_passkey'] = self.from_passkey
        elif self.mailtype == 'qq':
            raise NotImplementedError('QQ mail is not supported yet')
            if 'qq_mail' in kwargs.keys() and 'qq_passkey' in kwargs.keys():
                self.from_mail = kwargs['qq_mail']
                self.from_passkey = kwargs['qq_passkey']
            else:
                self.from_mail = os.getenv('qq_mail')
                self.from_passkey = os.getenv('qq_passkey')
                
                if not self.from_mail:
                    self.from_mail = input("Sending email address: ")
                    os.environ['qq_mail'] = self.from_mail

                if not self.from_passkey:
                    self.from_passkey = input("Sending email passkey: ")
                    os.environ['qq_passkey'] = self.from_passkey   
        else:
            raise ValueError('The mailtype should be either gmail or qq')

        if 'from_who' in kwargs.keys():
            self.from_who = kwargs['from_who']
        else:
            self.from_who = self.from_mail
    
    def __call__(self, **kwargs):
        if 'to' in kwargs.keys():
            self.to = kwargs['to']
        else:
            raise ValueError('The receiver email should be given')
        if 'from_who' in kwargs.keys():
            self.from_who = kwargs['from_who']
            
        if 'subject' in kwargs.keys():
            self.subject = kwargs['subject']
        else:
            self.subject = 'No Subject'
        
        if 'message' in kwargs.keys():
            self.message = kwargs['message']
        else:
            self.message = 'No Message'
        
        if 'attachment' in kwargs.keys():
            self.attachment = kwargs['attachment']
        else:
            self.attachment = None
        
        if 'mode' in kwargs.keys() and 'message' in kwargs.keys():
            self.mode = kwargs['mode']
        else:
            self.mode = 'plain'

        message = MIMEMultipart()
        message['From'] = f"{self.from_who} <{self.from_mail}>"
        message['To'] = self.to
        message['Subject'] = self.subject

        if self.mode == 'plain':
            message.attach(MIMEText(self.message, 'plain'))
        elif self.mode == 'html':
            message.attach(MIMEText(self.message, 'html'))
        elif self.mode == 'markdown':
            raise NotImplementedError('Markdown is not supported yet')
        else:
            raise ValueError('The mode should be either plain, html or markdown')

        if self.attachment and os.path.exists(self.attachment):
            attach_file_name = os.path.basename(self.attachment)
            with open(self.attachment, 'rb') as attach_file:
                payload = MIMEBase('application', 'octate-stream')
                payload.set_payload((attach_file).read())
                encoders.encode_base64(payload)
                payload.add_header('Content-Disposition', f'attachment; filename= {attach_file_name}')
                message.attach(payload)
        
        try:
            server = smtplib.SMTP(self.server, self.port)
            server.starttls()
            server.login(self.from_mail, self.from_passkey)
            text = message.as_string()
            
            server.sendmail(self.from_mail, self.to, text)
        except Exception as e:
            print(f"failed to send: {e}")
        finally:
            server.quit()



if __name__ == '__main__':
    # Test
    content = """
    <h1>Test</h1>
    <p>Test</p>
    """
    gmail()(to="gao.junbin.cn@gmail.com", subject="Test", message=content, mode='html', attachment='gmail.py')