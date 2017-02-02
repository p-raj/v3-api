#!/usr/bin/python
# -*- coding: utf-8 -*-


# future
from __future__ import unicode_literals

# Django
from django.core.management import BaseCommand

# local
from asap.tests import base


class Command(BaseCommand):
    help = "logbook functional test command"

    # A command must define handle()
    def handle(self, *args, **options):
        """

        """
        base.BaseClass()