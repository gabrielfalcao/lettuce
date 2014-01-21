"""
Extra steps to test django mail steps
"""

import yaml

from django.core import mail

from lettuce import step
from lettuce.django.steps.mail import *


STEP_PREFIX = r'(?:Given|And|Then|When) '


def mail_send(data):
    email = mail.EmailMessage(**data)
    email.send()


@step(r'I send a test email$')
def mail_send_simple(step):
    """
    Send a test, predefined email
    """
    mail_send({
        'from_email': 'test-no-reply@infoxchange.net.au',
        'to': ['other-test-no-reply@infoxchange.au'],
        'subject': 'Lettuce Test',
        'body': 'This is a test email sent from lettuce, right to your door!',
    })


# send email with yaml
@step(r'I send a test email with the following set:$')
def mail_send_yaml(step):
    """
    Send a test email from loaded yaml
    """

    mail_send(yaml.load(step.multiline))
