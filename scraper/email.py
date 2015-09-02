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
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.login(user, password)
        log.debug('logged in to {} as {}'.format(self.host, user))

    def disconect(self):
        self.connection.quit()
        log.debug('logged out of {}'.format(self.host))

    def get_message(self, sender, recipient, subject, body):
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        return message.as_string()

    def send(self, name, sender, password, recipients, subject, body):
        log.debug('starting {} sender'.format(name))
        messages = []
        self.connect(sender, password)
        for recipient in recipients.all():
            body += '\n\n' + recipient.url
            message = self.get_message(
                sender, recipient.email, subject, body
            )
            self.connection.sendmail(sender, recipient.email, message)
            log.debug('sent message from {} to {}'.format(
                sender, recipient.email)
            )
            messages.append(
                {
                    'sender': sender,
                    'recipient': recipient.email,
                    'subject': subject,
                    'body': body,
                }
            )
        self.disconect()
        return messages
