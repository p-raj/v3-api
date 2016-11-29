from django.contrib import admin
from django.db import models

from .screen import Screen
from .widget import Widget


class WidgetContainer(models.Model):
    screen = models.ForeignKey(Screen)
    widget = models.ForeignKey(Widget)

    order = models.PositiveIntegerField()
    is_required = models.BooleanField(default=True)

    # need to find a better way :/ probably EAV
    config = models.TextField(null=True, blank=True)


class WidgetContainerAdmin(admin.ModelAdmin):
    pass


admin.site.register(WidgetContainer, WidgetContainerAdmin)
