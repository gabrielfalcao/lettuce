"""
Email backend that sends mails to a multiprocessing queue
"""
from lettuce.django import mail
from django.core.mail.backends.base import BaseEmailBackend


class QueueEmailBackend(BaseEmailBackend):

    def send_messages(self, messages):
        for message in messages:
            mail.queue.put(message)
        return len(messages)
