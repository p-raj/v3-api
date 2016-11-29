from django.contrib import admin
from django.db import models

from .widget import Widget


class Screen(models.Model):
    name = models.CharField(max_length=64)
    help_text = models.TextField(null=True, blank=True)

    widgets = models.ManyToManyField(Widget, related_name='widget_containers',
                                     through='terminals.WidgetContainer')

    order = models.PositiveIntegerField()


class ScreenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Screen, ScreenAdmin)
