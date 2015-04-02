from django.http import HttpResponse
from django.core.urlresolvers import reverse

from backward.decorators import login_required

from django.views.decorators.http import require_http_methods


def simple(request):
    return HttpResponse('Ok')


@login_required
def login_simple(request):
    return HttpResponse('Ok')


@login_required
@require_http_methods(['POST'])
def action_simple(request, *args, **kwargs):
    for k, v in request.POST.items():
        request.session[k] = v

    request.session['sent'] = True

    return HttpResponse(reverse('login_simple'))
