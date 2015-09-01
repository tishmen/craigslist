import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

log = logging.getLogger('craigslist')


class EmailSender(object):

    def __init__(self):
        self.host = 'smtp.gmail.com'
        self.port = 587

    def connect(self, user, password):
        self.connection = smtplib.SMTP(self.host, self.port)
        self.ehlo()
        self.starttls()
        self.login(user, password)
        log.debug('logged in to {} as {}'.format(self.host, user))

    def disconect(self):
        self.connection.quit()
        log.debug('logged out of {}'.format(self.host))

    def get_message(self, sender, recipient, subject, body, url):
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body + '\n' + url, 'plain'))
        return message.as_string()

    def send(self, name, sender, password, recipients, subject, body):
        log.debug('starting {} sender'.format(name))
        messages = []
        self.connect(sender, password)
        for recipient in recipients:
            message = self.get_message(
                sender, recipient.email, subject, body, recipient.url
            )
            self.connection.sendmail(sender, recipient, message)
            log.debug('sent {}'.format(message))
            messages.append({'message': message})
        self.disconect()
        return messages
