from django.http import HttpResponse


def simple(request):
    return HttpResponse('Ok')
