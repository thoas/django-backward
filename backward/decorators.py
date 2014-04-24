from functools import wraps

from django.contrib import messages
from django.utils.decorators import available_attrs
from django.http import HttpResponseRedirect


def user_passes_test(test_func, login_url=None, message=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    if not login_url:
        from .utils import get_login_url
        login_url = get_login_url()

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            if message is not None:
                messages.info(request, message, fail_silently=True)

            response = HttpResponseRedirect(login_url)

            if request.method != 'GET':
                from .helpers import save_next_action

                data = {
                    'action': request.META.get('PATH_INFO'),
                    'args': args,
                    'kwargs': kwargs,
                    'method': request.method,
                    'parameters': {
                        'POST': request.POST.urlencode() if request.POST else None,
                    }
                }

                save_next_action(request, response, data)

            return response
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator


def login_required(function=None, message=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        message=message,
        login_url=login_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
