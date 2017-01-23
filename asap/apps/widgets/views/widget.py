#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- widgets.views.widget
~~~~~~~~~~~~~~

- This file contains the Widget service views, Every incoming http request to resolve any widget will come here.

 """

# future
from __future__ import unicode_literals

# 3rd party
import requests, uuid

# DRF
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError

# local
from asap.apps.logs import logging
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

# own app
from asap.apps.widgets.models.widget import Widget
from asap.apps.widgets.serializers.widget import WidgetSerializer
from asap.apps.widgets import PROCESS_LOCKER_UPSTREAM_URL


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    """Widget Viewset , responsible for resolving and fetching a widget or fetch multiple widgets.

    """
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = (permissions.AllowAny, )

    lookup_field = 'token'
    actor = 'widget'
    session = uuid.uuid4()
    logging_cls = None

    def make_queryset(self):
        """

        :return: queryset
        """
        queryset = super(WidgetViewSet, self).make_queryset()
        if self.is_nested:
            return queryset

        # TODO
        # return all the widgets
        # available to the requesting user for direct access
        return queryset

    def _create_log_instance(self, request, token):
        """
        :param request : Django request object.
        :param token : widget token, helps in identifying the widget
        :return: logging class instance
        """
        self.logging_cls = logging.ServiceLogging(
                                    self.actor,
                                    token,
                                    self.session,
                                    payload=request.data or dict())

    @detail_route(methods=['post'], )
    def resolve_widget(self, request, **kwargs):
        """Widget POST request handles by this method

        :param request : Django request object.
        :param kwargs: kwargs includes widget token, helps in identifying the widget
        :return: depends on widget response/execution
        """
        # Start logging of Widget
        self._create_log_instance(request, kwargs.get('token'))
        self.logging_cls.initialize()  # initialize widget logging

        response = self._execute_process_locker(request.data or dict())

        return Response(response, status=status.HTTP_200_OK)

    def _execute_process_locker(self, data):
        """

        :return:
        """
        process_locker_token = self.get_object().process_locker_token

        url = str(PROCESS_LOCKER_UPSTREAM_URL).format(
            process_locker_token=process_locker_token
        )
        self.logging_cls.handshake(process_locker_token, data)  # execution handover initiated

        rq = requests.post(url=url,
                           data=data
                           )
        if rq.status_code == requests.codes.ok:
            self.logging_cls.handshake_succeed(process_locker_token, data, rq)  # execution handover status
            return rq.json()

        self.logging_cls.handshake_failed(process_locker_token, data, rq.status_code, rq.json())  # execution handover status
        raise ValidationError(rq.json())

    def finalize_response(self, request, response, *args, **kwargs):
        """Log Process before sending final response

        :param request: django request object
        :param response: response to be sent to client
        :param args: function arguments
        :param kwargs: function keyword arguments
        :return: returns final response

        Note :
            if response code is 2xx then we call success log method else false method will be called
        """
        if self.logging_cls is None:
            self._create_log_instance(request, kwargs.get('token'))

        if str(response.status_code).startswith('2'):
            self.logging_cls.success(response)  # logged as success
        else:
            self.logging_cls.fail(response)  # logged as failure
        return super(WidgetViewSet, self).finalize_response(request, response, *args, **kwargs)