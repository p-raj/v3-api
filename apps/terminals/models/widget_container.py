from django.contrib import admin
from django.db import models


class WidgetContainer(models.Model):
    screen = models.ForeignKey('terminals.Screen')

    # the unique code representing the widget
    widget = models.CharField(max_length=64)

    order = models.PositiveIntegerField()
    is_required = models.BooleanField(default=True)

    # need to find a better way :/ probably EAV
    config = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{screen} [{order}]: {widget}'.format(**{
            'screen': self.screen,
            'widget': self.widget,
            'order': self.order
        })


class WidgetContainerInline(admin.StackedInline):
    model = WidgetContainer


class WidgetContainerAdmin(admin.ModelAdmin):
    raw_id_fields = ['screen']


admin.site.register(WidgetContainer, WidgetContainerAdmin)
