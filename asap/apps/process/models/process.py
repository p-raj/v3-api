#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Process
-------

Process is the singular unit, a __task__ that can be executed.
From our perspective it might be the smallest unit of task as well,
but from the 3rd party developers perspective, it may be huge.

For instance.

A Process may be
 - Send Email
 - Send a Push
 - Call a single API
 - Execute a python script


### Schema:

First, we except schema X (let's call it PSSpec[Process Schema Spec]),
it contains the set of keys we need to complete any process.
** It may be dependent of the type of process for now.

There are 2 conversions of the PSSpec. PSSpec creates 2 CoreAPI Documents.
 - Doc1 (Client). We are using CoreAPI client to call the resource server and return response.
 - Doc2 (Server). Now we need to create a CoreAPI document that will be served to other services/clients,
    so that the client can call the process server.

Eg.
            -----  PSSpec  -----
            |                   |
        Client                Server

Client (/api/v1/members/)
Server (/api/v1/processes/<uuid>/execute/)

(Incoming Req.)                                             (Outgoing req.)
--------------> [/api/v1/processes/<uuid>/execute/] -------> [/api/v1/members/] ---
                                                                                    |
--------------> [/api/v1/processes/<uuid>/execute/] <-------------------------------
(Outgoing Resp.)                                             (Incoming resp.)


"""

from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from reversion.admin import VersionAdmin

from asap.apps.process.schema.spec import PSSpec
from asap.apps.process.schema.validator import SchemaValidator
from asap.core.models import Authorable, Humanizable, Timestampable, UniversallyIdentifiable
from asap.utils import to_pascal_case

# TODO
# move to constants.py

# the types of process that we'll be supporting
# currently the plan is to focus on
# processes that can be called over HTTP
TYPE_HTTP = 'http'

# as per discussion with @PR, we do understand
# the need to remove any dependency of the API gateway
# we should be able to do switch the API gateway whenever possible
# although `how ?` is not clear, and we have a time crunch
# so marking it as TODO
TYPES = [
    (TYPE_HTTP, _('HTTP Process'))
]


class ProcessManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid),


class Process(Authorable, Humanizable, Timestampable,
              UniversallyIdentifiable, models.Model):
    # the process will eventually support different protocols
    # may be even direct scripts ?
    # only time will tell, so let's just create
    # some room for adding different types of processes
    type = models.CharField(blank=False, null=False, max_length=32,
                            choices=TYPES, default=TYPE_HTTP)

    # the schema we'll define for the process
    # the schema may vary according to the type of process
    # for example, the upstream url or the origin url makes sense
    # for HTTP process but not for a python script
    schema = JSONField(
        _('schema'), default={},
        blank=True, null=False,
        validators=[SchemaValidator()]
    )

    @property
    def spec(self):
        """
        :rtype: asap.apps.process.schema.spec.PSSpec
        """
        return PSSpec(self.schema)

    @property
    def client(self):
        """
        All the clients are located in the package
        `asap.apps.process.clients`.
        :return:
        """
        from asap.apps.process import clients
        return getattr(clients, self.__build_client_module_name())(self.schema_client)

    @property
    def schema_client(self):
        from asap.apps.process.schema import ClientSchema
        return ClientSchema(self.spec).build()

    @property
    def schema_server(self):
        from asap.apps.process.schema import ServerSchema
        return ServerSchema(self).build()

    def natural_key(self):
        return self.uuid

    class Meta:
        verbose_name_plural = _('Processes')

    def __build_client_module_name(self):
        """
        All the clients are located in the package
        `asap.apps.process.clients`.

        Clients follow the convention of
        {PascalCaseType}Client.

        for example:
        for type 'http' - the client can be accessed by the name HttpClient
        :return:
        """
        return '{0}Client'.format(to_pascal_case(self.type))

    def __str__(self):
        return 'Process {0}'.format(self.name)

    def has_permission(self, token):
        # TODO
        # whole thing doesn't feel right,
        # although it works :/
        import jwt
        from asap.apps.process.models.process_locker import ProcessLocker
        try:
            payload = ProcessLocker.decode(token)
        except jwt.DecodeError:
            return False
        return bool(self.processlocker_set.filter(uuid=payload.get('locker')).count())


@admin.register(Process)
class Admin(VersionAdmin):
    list_display = ('pk', 'name', 'uuid')
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'description', 'uuid')
