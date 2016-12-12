"""
TriggerAction is just mapping between
`Trigger` & `Action` as the name suggests.

Fire these `Action`s when this `Trigger` happens.

"""
from django.contrib import admin
from django.db import models

from apps.pubsub.models.action import Action
from apps.pubsub.models.trigger import Trigger


class TriggerAction(models.Model):
    trigger = models.ForeignKey(Trigger)

    # a single trigger may invoke multiple actions
    # See: http://stackoverflow.com/a/30441546/1796173
    actions = models.ManyToManyField(Action)

    # here we might have rules/conditions whether to
    # complete the action or abort if some condition is met!!

    # NOTES:
    # adding actions individually instead of using a M2M gives
    # more power if we decide to add rules. We can have a through mapping
    # for that as well, but it won't make any sense to extend a useless relation

    def __str__(self):
        return '{trigger}: {actions}'


@admin.register(TriggerAction)
class TriggerActionAdmin(admin.ModelAdmin):
    pass
