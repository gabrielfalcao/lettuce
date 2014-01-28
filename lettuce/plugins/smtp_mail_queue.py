import asyncore
import threading

from email.header import decode_header
from email import message_from_string

from smtpd import SMTPServer


from lettuce import after, before


def _parse_header(val):
    result = ''
    elements = decode_header(val)
    for el, enc in elements:
        result += el.decode(enc) if enc and el else el
    return result


def _decode_part(part):
    content = part.get_payload(decode=True)
    charset = part.get_content_charset()
    return content.decode(charset) if charset else content


def _get_content(msg):
    alternatives = []
    if msg.get_content_type() == 'multipart/alternative':
        payload = msg.get_payload()
        body = _decode_part(payload.pop(0))
        alternatives = [_decode_part(part) for part in payload]
    else:
        body = _decode_part(msg)
    return body, alternatives


def _convert_to_django_msg(msg):

    from django.core.mail import EmailMessage, EmailMultiAlternatives

    body, alternatives = _get_content(msg)
    if alternatives:
        email = EmailMultiAlternatives(body=body,
                                       alternatives=alternatives)
    else:
        email = EmailMessage(body=body)
    email.subject = _parse_header(msg['Subject'])
    email.to = _parse_header(msg['To'])
    email.cc = _parse_header(msg.get('Cc', None))
    email.bcc = _parse_header(msg.get('Bcc', None))
    email.from_email = _parse_header(msg['From'])
    return email


def enable():

    from django.conf import settings
    from lettuce.django import mail

    smtp_queue_server = None

    @before.each_scenario
    def start_server(*args, **kwargs):
        global smtp_queue_server
        smtp_queue_server = QueueSMTPServer((settings.LETTUCE_SMTP_QUEUE_HOST,
                                             settings.LETTUCE_SMTP_QUEUE_PORT),
                                            None)
        smtp_queue_server.start()

    @after.each_scenario
    def stop_server(*args, **kwargs):
        global smtp_queue_server
        smtp_queue_server.stop()

    class QueueSMTPServer(SMTPServer, threading.Thread):
        """
        Asyncore SMTP server wrapped into a thread.
        It pushes incoming email messages into lettuce email queue.
        Based on DummyFTPServer from:
        http://svn.python.org/view/python/branches/py3k/Lib/test/test_ftplib.py?revision=86061&view=markup
        """
        def __init__(self, *args, **kwargs):
            threading.Thread.__init__(self)
            SMTPServer.__init__(self, *args, **kwargs)
            self.active_lock = threading.Lock()
            self.active = False
            self.daemon = True

        def process_message(self, peer, mailfrom, rcpttos, data):
            msg = message_from_string(data)
            django_msg = _convert_to_django_msg(msg)
            mail.queue.put(django_msg)

        def start(self):
            assert not self.active
            self.__flag = threading.Event()
            threading.Thread.start(self)

        def run(self):
            self.active = True
            self.__flag.set()
            while self.active and asyncore.socket_map:
                self.active_lock.acquire()
                asyncore.loop(timeout=0.1, count=1)
                self.active_lock.release()
            asyncore.close_all()

        def stop(self):
            assert self.active
            self.active = False
            self.join()
