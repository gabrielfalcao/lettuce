"""
Step definitions for working with Django email.
"""

from django.core import mail

from lettuce import step


STEP_PREFIX = r'(?:Given|And|Then|When) '
CHECK_PREFIX = r'(?:And|Then) '
EMAIL_PARTS = ('subject', 'body', 'from_email', 'to', 'bcc', 'cc')


@step(CHECK_PREFIX + r'I have sent (\d+) emails?')
def mail_sent_count(step, count):
    """
    Then I have sent 2 emails
    """
    count = int(count)
    assert len(mail.outbox) == count, "Length of outbox is {0}".format(count)


@step(CHECK_PREFIX + (r'I have sent an email with "([^"]*)" in the ({0})'
                      '').format('|'.join(EMAIL_PARTS)))
def mail_sent_content(step, text, part):
    """
    Then I have sent an email with "pandas" in the body
    """
    for email in mail.outbox:
        if text in getattr(email, part):
            return True

    assert False, "An email contained expected text in the {0}".format(part)


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
    mail.outbox = []
