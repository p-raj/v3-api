from django.contrib import admin
from django.db import models

from .widget_container import WidgetContainer, WidgetContainerInline


class Screen(models.Model):
    name = models.CharField(max_length=64)
    help_text = models.TextField(null=True, blank=True)

    widgets = models.ManyToManyField(WidgetContainer,
                                     related_name='widget_containers')

    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ScreenAdmin(admin.ModelAdmin):
    inlines = [
        WidgetContainerInline
    ]


admin.site.register(Screen, ScreenAdmin)
