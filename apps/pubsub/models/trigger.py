"""
`Trigger` on Veris Orchestration Server is a `WebHook` on Resource Server.

Resource Server fires `WebHook` when an event occurs.
The `WebHook` invokes a `Trigger` on Orchestration Server.

"""
from django.db import models

from apps.pubsub.models.event import Event


class Trigger(models.Model):
    event = models.ForeignKey(Event)

    # let's just keep the data RAW
    # TODO: move to django.contrib.postgres.fields.JSONField
    payload = models.CharField(max_length=64, null=False, blank=False)
