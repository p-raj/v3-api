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

import uuid

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


class Publishable(models.Model):
    """
    Some entities might be either published.
        i.e The entity will be visible to all whether
        or not the user has access to them.

    eg. Apps marketplace (Default Apps)

    """
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Humanizable(models.Model):
    """
    Any Entity that needs a human friendly name
    & a description to describe __why__ it was created!!
    """
    name = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    """
    Almost entities need to keep record of the
    time when they were created/modified.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UniversallyIdentifiable(models.Model):
    """
    All the entities that need a random key
    for universal identification should extend this.
    """
    # uuid as the name suggests is there to provide
    # a random universally unique identifier
    # this will be used in URLs to make it the urls non obvious
    # for eg. /r/1/ ---> /r/3b546b31-67aa-448c-b3f2-ed906268b08c/
    # the former one can lead to /r/2/
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True
