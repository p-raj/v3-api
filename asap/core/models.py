#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- core.models
~~~~~~~~~~~~~~

- This file contains Abstract models of Veris Project.
"""

# future
from __future__ import unicode_literals

# Django
from django.conf import settings
from django.db import models


User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Authorable(models.Model):
    """
    Each entity will be added by someone, some ``Author``.
    An Entity cannot magically appear in the system. ;)

    - Organization
    - Runtime
    """
    author = models.ForeignKey(User, related_name='author_%(app_label)s_%(class)s')

    class Meta:
        abstract = True


class Timestampable(models.Model):
    """
    Almost entities need to keep record of the
    time when they were created/modified.
    """
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
