"""
Organizations can be created by the ``authenticated`` & ``verified`` users.

Currently lets assume that any django user is both authentic and verified,
we'll later pass the authentication mechanism to a different server that
handles user authentication for us (somewhat similar to Auth0 service).
"""
from django.conf import settings
from django.contrib import admin
from django.db import models

from asap.core.models import Authorable, Timestampable
from asap.core.querysets import AuthorableQuerySet

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class OrganizationQuerySet(AuthorableQuerySet):
    pass


class Organization(Authorable, Timestampable, models.Model):
    """
     * A ``User`` may have multiple organizations registered.
    """
    # the reference to the site module
    # why? we are using django-allauth to manage the social applications
    # and it takes good care of it using the sites framework,
    # so yes basically this relation is just an interface to the power of django-allauth
    # teramatrix.asap.in <---> teramatrix
    # this might turn out to be a separate service in itself :)
    # site = models.OneToOneField(Site)

    # organizations need to have a name at least :)
    name = models.CharField(max_length=64, null=False, blank=False)

    # lets add other attributes as and when required and necessary
    # lazy is the new awesome :P

    # lets change the default manager
    # why? we need to add the organization creator as a member by default
    # will ease things out for access management, at least it seems like it for now
    objects = OrganizationQuerySet.as_manager()

    def __str__(self):
        return self.name


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)
