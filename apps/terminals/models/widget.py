"""
Widget is a Resource.

Initially Widgets will be shipped by Veris.
Later we may open developing Widgets to other developers, and build a Widget Store.


A Widget defines a `Process`, or may be a set of `Processes`.
A Widget can have multiple `States`.

A Process is a set of `Actions` that a user may perform by interacting with Widget.
An `Action` has the ability to directly alter the `State` of `Widget`.

An `Interaction` with the Widget may invoke an `Action` on the widget,
the `Interaction` may involve a state change of the Widget.


The Widget Author may define a set of `Configurations`
that help Consumers of the Widget to extend the functionality when required.
Example:
    Login Widget provided by Veris comes with a boolean configuration **is_mfa_enabled** ?

** Widgets are built separately on the clients as of now.

"""
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
