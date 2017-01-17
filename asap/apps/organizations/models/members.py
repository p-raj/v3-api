"""
Any Organization without members might only be used for testing purposes
or for evaluating Veris platform
just like we evaluated Auth0, Okta & many others :D
"""
from django.conf import settings
from django.contrib import admin
from django.db import models

from .organizations import Organization


User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Member(models.Model):
    """
    Member model should be seen as a through mapping between
    users from the authentication server and the organizations on this server.

    * A ``User`` may be added as a member for multiple Organizations,
      and may have different ``roles`` assigned. We'll see ``roles`` later :)
    """
    # let's consider the we are enabling organization management
    # i.e a user can manage resources provided by Veris himself or
    # he can create an organization, & add users to help him do the same.
    # a member will always be a Veris user, not saying an active user,
    # a mapping to user should ideally exist, let's say that a shadow user
    # which will help us merge profiles
    user = models.ForeignKey(User)

    # we can have a foreign key here,
    # it seems safe to assume these two resources will always be on the same server
    # no point in keeping members after the organization has been deleted
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # the organization service has decided to integrate with VRT service
    # and provide VRTs to the members of the organization if requested by admin
    # so, the membership information may additionally contain
    # a reference to the runtimes made available by the organization
    # to this member
    # the VRT service provide a way to group the runtimes together,
    # so no need to maintain multiple runtimes for a member here,
    # we'll keep a reference to the locker (group)
    # provided by the runtime service instead for each member
    runtime_locker_uuid = models.CharField(max_length=64, null=True, blank=True)

    # let's keep the date member was added,
    # although the name says date_joined
    # TODO
    # we'll see what to do with this
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{user} is a member of {organization}'.format(**{
            'user': self.user_id,
            'organization': self.organization
        })


class MemberAdmin(admin.ModelAdmin):
    raw_id_fields = ['organization']


admin.site.register(Member, MemberAdmin)
