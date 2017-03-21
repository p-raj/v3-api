#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Services
---------

Organizations need to enable services they want to use.

For instance.
 - Runtimes is a completely different service and
    is not concerned with organizations,
    but we might need to be able to filter out
    runtimes for a given organization.

This helps us provide Organization level
abstraction to all the services.

Here we keep track of the services enabled by the organization.

"""
from django.contrib import admin
from django.db import models

from asap.core.models import Authorable, Timestampable
from asap.apps.organizations.models import Organization

# TODO
# move to constants.py
SERVICES = (
    ('runtime', 'Runtimes'),
    ('widget', 'Widgets'),
    ('process', 'Processes'),
    ('member', 'Members'),
)


class Service(Authorable, Timestampable, models.Model):
    # the service name :)
    # ideally we'll have a dynamic registry of services available
    # but let's keep things simple for now
    name = models.CharField(max_length=64, choices=SERVICES,
                            null=False, blank=False)

    # we can have a foreign key here,
    # it seems safe to assume these two resources
    # will always be on the same server
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # the service enabled must have some kind of auth ?
    # let's assume its simple enough for now :)
    # ideally, we have 2 separate servers, 2 separate accounts
    # Organization Service has a OAuth2 client registered with Runtimes/X-Service
    # which authenticates with and provides us the OAuth credentials
    # for each organization, there might be a separate account on Runtime/X-Service
    # currently it corresponds to the locker for each service :/
    service_client_id = models.CharField(max_length=64, null=True, blank=True)

    @property
    def is_enabled(self):
        # FIXME:
        # token may be expired,
        # not sufficient :/
        return bool(self.service_client_id)

    @property
    def date_enabled(self):
        return self.created_at

    def __str__(self):
        return '{name} enabled for {organization}'.format(**{
            'name': self.name,
            'organization': self.organization
        })

    class Meta:
        unique_together = ('organization', 'name',)


class ServiceAdmin(admin.ModelAdmin):
    raw_id_fields = ['organization']
    list_display = ('pk', 'name', 'organization',)


admin.site.register(Service, ServiceAdmin)
