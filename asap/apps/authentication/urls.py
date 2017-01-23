#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from asap.apps.authentication.views.login import LoginView
from asap.apps.authentication.views.token import RefreshTokenView
from asap.apps.authentication.views.users import UserViewSet
from asap.router import Router

router = Router()
router.register('users', UserViewSet)

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^token/$', RefreshTokenView.as_view()),
]
