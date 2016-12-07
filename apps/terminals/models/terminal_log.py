"""
Log is a Resource.

Terminal gathers data using various widgets
& dumps it as it is.

"""

from django.contrib import admin
from django.db import models

from .terminal import Terminal


class TerminalLog(models.Model):
    # a reference to the terminal where the data was captured
    terminal = models.ForeignKey(Terminal,
                                 null=True,
                                 on_delete=models.SET_NULL)

    # let's just keep the data RAW
    # TODO: move to django.contrib.postgres.fields.JSONField
    data = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return self.terminal


class LogAdmin(admin.ModelAdmin):
    raw_id_fields = ['terminal']


admin.site.register(TerminalLog, LogAdmin)
