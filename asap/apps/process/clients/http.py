#!/usr/bin/python
# -*- coding: utf-8 -*-

from .base import Client


class HttpClient(Client):
    def execute(self):
        print('executed', self.logging_cls)
