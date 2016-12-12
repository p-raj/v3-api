"""
The Events will be registered to the Veris Orchestration Layer.

Example Events:
    - Organization Created (provided by Veris)
    - Terminal Log Created (provided by Veris)
    - Invite Created (provided by Teramatrix)
    - Invite Updated (provided by Teramatrix)

Why Event ?

As mentioned in `Service`, we need to orchestrate the services.
We can approach the orchestration problem in two ways:
    - `Service` polls the data - Look for changes - Fire Events. Not the best solution.
    - Create Events - Push changes. - Events Fired automatically.

These events are provided by a service.
Organization Service can't provide an event
that says a Terminal Log was created. :/

The Service need to register all the events that can be fired.
Any Event that is fired and is not registered will be missed.

"""
from django.contrib import admin
from django.db import models

from apps.pubsub.models.service import Service


class Event(models.Model):
    # the service defines all the events
    # that it can trigger
    service = models.ForeignKey(Service)

    # we could have gone granular, as in
    # resource_name and action [
    #   (org, create )
    #   (org, delete )
    # ]
    # but we will also have cases like send_mail
    # although this can be viewed
    # as resource as well (mail, create) :)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
