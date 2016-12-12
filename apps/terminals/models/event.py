"""
Example Events:
    - Terminal Log Created (provided by Veris)

Convention:
    table_name:(create|read|update|delete)

"""
from django.contrib import admin
from django.db import models


class Event(models.Model):
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
