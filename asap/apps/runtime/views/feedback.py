#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from rest_framework import viewsets

from asap.apps.runtime.serializers.feedback import Feedback, FeedbackSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

logger = logging.getLogger(__name__)


class FeedbackViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    lookup_parent = [
        ('app_uuid', 'app__uuid')
    ]
    lookup_fields = (
        'app', 'comment'
    )
    ordering_fields = (
        'created_at', 'modified_at',
        'rating'
    )
