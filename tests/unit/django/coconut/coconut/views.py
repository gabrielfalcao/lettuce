
import time

from django.views.generic import View
from django.http import HttpResponse

class WaitView(View):
    def get(self, *args, **kwargs):
        time.sleep(3)
        return HttpResponse("OK")
