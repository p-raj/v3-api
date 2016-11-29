from django.contrib import admin
from django.db import models


class Widget(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64, unique=True)

    # need to find a better way :/ probably EAV
    config = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class WidgetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Widget, WidgetAdmin)
