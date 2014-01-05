django-backward
===============

.. image:: https://secure.travis-ci.org/thoas/django-backward.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/django-backward

An application to store your previous history in your session engine backend.

With this application you will be able to redirect your users to their previous
location when they tried to access a page where the login is required.

Thanks to `oleiade <https://github.com/oleiade>`_ for the name.

Compatibility
-------------

This library is compatible with:

- python2.6, django1.4
- python2.6, django1.5
- python2.6, django1.6
- python2.7, django1.4
- python2.7, django1.5
- python2.7, django1.6
- python3.3, django1.5
- python3.3, django1.6

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

5. Configure your `Session engine <https://docs.djangoproject.com/en/dev/topics/http/sessions/#configuring-the-session-engine>`_

.. _GitHub: https://github.com/thoas/django-backward
