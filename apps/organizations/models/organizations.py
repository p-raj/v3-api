"""
Organizations can be created by the ``authenticated`` & ``verified`` users.

Currently lets assume that any django user is both authentic and verified,
we'll later pass the authentication mechanism to a different server that
handles user authentication for us (somewhat similar to Auth0 service).
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.db import models


User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class OrganizationQuerySet(models.QuerySet):
    """
    A custom queryset? Yeah, let's make an assumption that the user
    creating the organization needs will always be a member of the organization with
    some defined ``role`` or ``permission``.
    """

    def create(self, **kwargs):
        # create not called ? strange ? - no
        # admin panel calls Model.save directly
        # we can do this there on a deeper level,
        # but actually this is the right place as
        # we'll be calling ``objects.create``

        # no, no, no, we don't want to change the default functionality at all :)
        obj = super(OrganizationQuerySet, self).create(**kwargs)

        # let's just added the user who created the organization
        # as the member of the organization as well
        # lazy import to prevent cyclic imports
        from .members import Member
        Member.objects.create(**{
            'user': obj.user,
            'organization': obj
        })

        return obj


class Organization(models.Model):
    """
    Organization model directly extends `models.Model`, yeah only for now.
    We'll surely do something about it. Pakka!!

     * A ``User`` may have multiple organizations registered.
    """
    # the reference to the site module
    # why? we are using django-allauth to manage the social applications
    # and it takes good care of it using the sites framework,
    # so yes basically this relation is just an interface to the power of django-allauth
    # teramatrix.veris.in <---> teramatrix
    site = models.OneToOneField(Site)

    # let's consider the we are enabling organization management
    # i.e a user can manage resources provided by Veris himself or
    # he can create an organization, & add users to help him do the same.
    user = models.ForeignKey(User)

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
