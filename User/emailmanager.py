import smtplib

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_sender = "hmavlanov79@gmail.com"
smtp_password = 'npag mczy sjpr xyuy'


class EmailManager:
    def __init__(self, receiver, subject, message):
        self.sender = smtp_sender
        self.receiver = receiver
        self.subject = subject
        self.message = message

    def send_email(self):
        email = f"Subject: {self.subject}\n\n{self.message}"
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_sender, smtp_password)
            server.sendmail(smtp_sender, self.receiver, email)
            server.quit()
            return True
        except smtplib.SMTPException as e:
            print(f'Error: {e}')
            return False
