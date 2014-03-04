"""
Step definitions for working with Django email.
"""
from smtplib import SMTPException

from django.core import mail

from lettuce import step


STEP_PREFIX = r'(?:Given|And|Then|When) '
CHECK_PREFIX = r'(?:And|Then) '
EMAIL_PARTS = ('subject', 'body', 'from_email', 'to', 'bcc', 'cc')
GOOD_MAIL = mail.EmailMessage.send


@step(CHECK_PREFIX + r'I have sent (\d+) emails?')
def mail_sent_count(step, count):
    """
    Then I have sent 2 emails
    """
    count = int(count)
    assert len(mail.outbox) == count, "Length of outbox is {0}".format(count)


@step(r'I have not sent any emails')
def mail_not_sent(step):
    """
    I have not sent any emails
    """
    return mail_sent_count(step, 0)


@step(CHECK_PREFIX + (r'I have sent an email with "([^"]*)" in the ({0})'
                      '').format('|'.join(EMAIL_PARTS)))
def mail_sent_content(step, text, part):
    """
    Then I have sent an email with "pandas" in the body
    """
    assert any(text in getattr(email, part)
               for email
               in mail.outbox
               ), "An email contained expected text in the {0}".format(part)


@step(CHECK_PREFIX + r'I have sent an email with the following in the body:')
def mail_sent_content_multiline(step):
    """
    I have sent an email with the following in the body:
    \"""
    Name: Mr. Panda
    \"""
    """
    return mail_sent_content(step, step.multiline, 'body')


@step(STEP_PREFIX + r'I clear my email outbox')
def mail_clear(step):
    """
    I clear my email outbox
    """
    mail.EmailMessage.send = GOOD_MAIL
    mail.outbox = []


def broken_send(*args, **kwargs):
    """
    Broken send function for email_broken step
    """
    raise SMTPException("Failure mocked by lettuce")


@step(STEP_PREFIX + r'sending email does not work')
def email_broken(step):
    """
    Break email sending
    """
    mail.EmailMessage.send = broken_send
