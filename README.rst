django-backward
===============

.. image:: https://secure.travis-ci.org/thoas/django-backward.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/django-backward

A Django application to store your previous history and action using differents
backends.

With this application you will be able to redirect your users to their previous
location when they tried to access a page where the login is required.

.. image:: http://cl.ly/image/371E2R0L3n2h/backward_redirect.png

You will be also able to record previous action which needed login required.

For example, if your user is not logged in your application and try to execute
an action which required authentication (e.g.: an user clicks on a button to follow another user),
this application will record parameters (even on POST) and execute the last action
when your user will be successfully logged.

.. image:: http://cl.ly/image/3B2E0H2M0j1C/backward_action.png

Thanks to `oleiade <https://github.com/oleiade>`_ for the name.

Installation
------------

1. Either check out the package from GitHub_ or it pull from a release via PyPI ::

    pip install django-backward


2. Add ``backward.middleware.BackwardMiddleware`` to your ``MIDDLEWARE_CLASSES`` ::

    MIDDLEWARE_CLASSES = (
        'backward.middleware.BackwardMiddleware',
    )

3. Add ``backward.urls`` to your ``urls.py`` ::

    # urls.py

    from django.conf.urls import patterns, url, include

    urlpatterns = patterns(
        '',

        url(r'^backward/', include('backward.urls')),
    )

4. Set ``settings.LOGIN_REDIRECT_URL`` as mentioned in your ``urls.py`` for example ::

    # settings.py

    LOGIN_REDIRECT_URL = '/backward/login/redirect/'

5. Configure your `Session engine <https://docs.djangoproject.com/en/dev/topics/http/sessions/#configuring-the-session-engine>`_ if you are using the default backend

6. Use the decorator ``backward.decorators.login_required`` if your views need authentication


Configuration
-------------

``BACKEND_BACKEND_CLASS``
.........................

The backend used to store information.

The default backend class is ``backward.backends.session.SessionBackend``.

``backwards.backends.session.SessionBackend``
.............................................

Store information in ``request.session`` using your `Session engine <https://docs.djangoproject.com/en/dev/topics/http/sessions/#configuring-the-session-engine>`_

``backwards.backends.session.CookieBackend``
............................................

Store information in ``request.COOKIES``, you can configure a few things:

- ``BACKWARD_MAX_AGE``: the age used to set an expiration date to the cookie
- ``BACKWARD_COOKIE_DOMAIN``: the domain name used for the cookie
- ``BACKWARD_COOKIE_SECURE``: if this is set to True, the cookie will be marked as **secure**, which means browsers may ensure that the cookie is only sent under an HTTPS connection.

.. _GitHub: https://github.com/thoas/django-backward
