from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def simple(request):
    return HttpResponse('Ok')


@login_required
def login_simple(request):
    return HttpResponse('Ok')
