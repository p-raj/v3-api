#!/usr/bin/python
# -*- coding: utf-8 -*-


# future
from __future__ import unicode_literals

# 3rd party
import requests, ujson
from tabulate import tabulate

# Django
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError

# own app
from asap.apps.process import models


class BaseClass(object):
    """Base class of functional Test Cases, here we will write functions to fetch common data like
       users, organizations, memberships etc etc.

    """
    client = None
    upstream_url = None
    access_token = None  # user access token
    token_type = None  # access token type
    runtime_uuid = None  # runtime token
    runtime_locker_uuid = None  # runtime locker token
    session = None  # Runtime session token
    widget_token = None  # widget token
    raw_data = None  # raw data to be sent to process
    all_process = []  # all process which needs to be resolved.
    resolved_process = None  # resolved process
    resolved_data = dict()  # resolved process response

    def __init__(self):
        """

        """
        username = input("Enter username: ")
        password = input("Enter password: ")
        print('\n')

        self._client(), self._upstream_url()

        self._login(username, password)

        self.execute_process()

    def _client(self):
        """

        """
        self.client = requests

    def _upstream_url(self):
        """

        :return:
        """
        self.upstream_url = getattr(settings, 'SERVER_URL', 'http://0.0.0.0:8000')

    def _get_service_url(self, router_name, *args, **kwargs):
        """

        :param router_name: router name yoo want to request.
        :return: return service url
        """
        router = reverse(router_name, args=[*args], kwargs={**kwargs})
        return '{0}{1}'.format(self.upstream_url, router)

    def _login(self, username, password):
        """login user into veris.

        :param username: user username.
        :param password: user password.
        :return: user token , if successfully authenticated.
        """
        url = self._get_service_url('micro_service_v1:login')
        response = self.client.post(url, data={'username': username, 'password': password})

        assert response.status_code == 200, 'Login failed with status code {0}'.format(response.status_code)

        self.access_token = response.json().get('access_token')
        self.token_type = response.json().get('token_type')

        # next step would be to select membership from available membership cards
        self.select_membership()

    def _get_memberships(self):
        """get memberships of authenticated user
        """
        url = self._get_service_url('member-list')
        response = self.client.get(url, headers={'Authorization': '{0} {1}'.format(self.token_type, self.access_token)})
        assert response.status_code == 200, 'get membership failed with status code {0}'.format(response.status_code)

        return response.json()

    def _get_runtimes(self):
        """get runtime attached with a specific membership card of authenticated user
        """
        url = self._get_service_url('micro_service_v1:runtime-locker-runtime-list', runtime_locker_uuid=self.runtime_locker_uuid)
        response = self.client.get(url, headers={'Authorization': '{0} {1}'.format(self.token_type, self.access_token)})
        assert response.status_code == 200, 'get runtimes failed with status code {0}'.format(response.status_code)

        return response.json()

    def _get_widgets(self):
        """get all widgets in a runtime
        """
        url = self._get_service_url('micro_service_v1:runtime-widget-proxy-list', uuid=self.runtime_uuid)
        response = self.client.get(url, headers={'Authorization': '{0} {1}'.format(self.token_type, self.access_token)})
        assert response.status_code == 200, 'get widgets failed with status code {0}'.format(response.status_code)

        self.session = response.headers.get('X-VRT-SESSION')
        return response.json()

    def select_membership(self):
        """
        """
        arr = []
        for membership in self._get_memberships().get('results'):
            arr.append({
                'member': membership.get('user'),
                'token': membership.get('runtime_locker_uuid')
            })
        print('Following memberships are available you can select any one membership token (runtime-locker)\n')
        print(tabulate(arr, headers="keys", tablefmt="grid"))
        print('\n')

        self.runtime_locker_uuid = input('Enter Membership Token from above table : ')

        print('\n')

        # next step would be to select runtime from available runtimes.
        self.select_runtimes()

    def select_runtimes(self):
        """
        """
        arr = []
        for runtime in self._get_runtimes().get('results'):
            arr.append({
                'runtime': runtime.get('url'),
                'token': runtime.get('uuid')
            })
        print('Following Runtimes are available you can select any one runtime token\n')
        print(tabulate(arr, headers="keys", tablefmt="grid"))
        print('\n')

        self.runtime_uuid = input('Enter Runtime Token from above table : ')

        print('\n')

        self.select_widgets()

    def select_widgets(self):
        """
        """
        arr = []
        for widget in self._get_widgets().get('results'):
            process =[]
            self.widget_token = widget.get('token')
            for i in widget.get('schema').get('paths'):
                if widget.get('schema').get('paths').get(i).get('post'):
                    process.append(str(widget.get('schema').get('paths').get(i).get('post').get('operationId')))
                if widget.get('schema').get('paths').get(i).get('get'):
                    process.append(str(widget.get('schema').get('paths').get(i).get('get').get('operationId')))

            arr.append({
                'name': widget.get('name'),
                'token': process
            })

            self.all_process.append(process)

        print('Following Widgets are available you can resolve any one widget.Select any token to resolve(process-token)\n')
        print(tabulate(arr, headers="keys", tablefmt="grid"))
        print('\n')

        self.resolved_process = str(input('Enter Widget token from above table : '))
        self.raw_data = input('Enter raw-data to be sent must be in json format: ')

        print('\n')

    def execute_process(self):
        """resolve a process
        """
        # self.all_process is a list of lists so we will make it a single list
        self.all_process = [item for sublist in self.all_process for item in sublist]

        url = self._get_service_url('micro_service_v1:runtime-widget-proxy-detail-action',
                                    uuid=self.runtime_uuid,
                                    widget_uuid=self.widget_token,
                                    action=self.resolved_process)
        response = self.client.post(
                    url,
                    headers={'Authorization': '{0} {1}'.format(self.token_type, self.access_token),
                             'X-VRT-SESSION': self.session,
                             'content-type': 'application/json'},
                    data=ujson.dumps(self.raw_data))

        # if a process raise any error then show the error to the user and ask him wether he wants to
        # proceed or not.
        if response.status_code != 200:
            try:
                print(response.json())
            except:
                print(response.text)
            print('try again ....')
            print('/n')

            # get raw data from user again
            self.raw_data = input('Enter raw-data to be sent must be in json format:')

            self.execute_process()

        # if process successfully resolved then removed that process from all_process list
        self.all_process.remove(self.resolved_process)

        # save recently resolved process response
        self.resolved_data[self.resolved_process] = response.json()

        # if there are still un-resolved process exists then ask user to resolve them or cancel
        if self.all_process:
            print('un-resolved processes ... ')
            print('/n')
            print(self.all_process)

            self.resolved_process = str(input('Enter token from above table or "cancel" To exit : '))

            # if user chooses cancel option then return True and show him the resolved processes data.
            if self.resolved_process == 'cancel':
                print('Resolved data is as follows :')
                print(self.resolved_data)
                return True
            else:
                self.resolved_process = str(input('Enter token from above table or "cancel" To exit : '))

            self.raw_data = input('Enter raw-data to be sent must be in dictionary format: ')
            print('/n')
            self.execute_process()

        print('All process are resolved.')
        print('/n')

        print('Resolved data is as follows :')
        print('/n')

        print(self.resolved_data)
