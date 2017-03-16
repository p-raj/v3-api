#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Process Locker
--------------

Process Locker ?

A widget can maintain the states of multiple processes.
If Widget & Process were a part of the same service. There might have been
a direct relation either through `ForeignKey` of `ManyToManyField`.
But we have been making sure that these can be separated out easily
on different servers as different services.

So, instead of:
            --- Process
            |
Widget <------- Process
            |
            --- Process

we have:
                                --- Process
                                |
Widget <---> ProcessLocker -------- Process
                                |
                                --- Process

Process Locker is just an interface to ease
the listing of Processes associated to a widget.

"""
import jwt

from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from asap.apps.process.models.process import Process
from asap.core.models import Authorable, Timestampable, \
    UniversallyIdentifiable


class ProcessLocker(Authorable, Timestampable,
                    UniversallyIdentifiable, models.Model):
    """
    Process Locker is the collection of Processes which will be called based on some rules.
    Every Locker will have a token which will be shared with Widget.
    """
    # this uuid may be used to access many processes
    # associated with it
    # each process may have a unique token associated to it
    # we'll do that in the through mapping
    processes = models.ManyToManyField(Process)

    # fields removed:
    # is_publish - process locker is just an
    #   interface as explained above
    #   a widget may add/remove process to the locker
    #   whenever it wishes, until the widget is published.
    #   and this will be a part of widget service
    # name - process locker is an invisible entity only visible
    #   to us, only for our convenience

    rules = JSONField(
        _('Process rules'),
        null=True, blank=True,
        help_text=_('Rules config, tells us which process will be called based on what rules.'),
    )

    @cached_property
    def token(self):
        """
        returns a new token every time
        unless the same instance
        is accessing the property again
        :return:
        """
        # thought of abstracting it out
        # but not sure about it yet,
        # since the generation data will vary
        return self.encode(self.__payload__())

    def verify(self, token):
        try:
            payload = self.decode(token)
            return payload.get('locker') == self.__payload__().get('locker')
        except jwt.DecodeError:
            return False

    def __str__(self):
        return 'Process Locker {0}'.format(self.pk)

    def __payload__(self):
        return {
            'locker': str(self.uuid),
            'created_at': str(timezone.now())
        }

    @classmethod
    def encode(cls, data):
        return jwt.encode(data, key=settings.JWT_SECRET).decode()

    @classmethod
    def decode(cls, token):
        return jwt.decode(token, key=settings.JWT_SECRET)


@admin.register(ProcessLocker)
class ProcessLockerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'uuid')
