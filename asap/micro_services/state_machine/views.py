#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_services.state_machine.views
~~~~~~~~~~~~~~

- This file contains state_machine micro-service views, every HTTP request/router points to this file.
"""

# future
from __future__ import unicode_literals

# 3rd party
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# Django


# local


# own app
from asap.micro_services.state_machine.models import TransactionLifeCycle, TransactionStateMachine, HttpService


class TransactionStateViewSet(viewsets.GenericViewSet):
    """States viewset , it controls general functions of states like create new, change and get current state

    """
    model = TransactionStateMachine
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny, )

    def create_initial_state(self, task_identifier):
        """

        :return:
        """
        pass

    def get_current_state(self, task_identifier):
        """

        :return:
        """
        pass

    def get_complete_transaction_life_cycle(self, task_identifier):
        """

        :return:
        """
        pass

    def change_state(self, task_identifier):
        """

        :return:
        """
        pass
