#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.auth.views.login import LoginView
from asap.auth.views.token import RefreshTokenView
from django.conf.urls import url

from asap.auth.views.users import UserViewSet
from asap.router import Router

router = Router()
router.register('users', UserViewSet)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^token/$', RefreshTokenView.as_view(), name='refresh-token'),
]
