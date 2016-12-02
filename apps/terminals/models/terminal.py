"""
Terminal is a Resource.

### Previously:
 - Terminal was a part of Organization, making it tightly coupled with Organization.
 - A User can not create a terminal unless he creates Organization & Venues.
 - A Venue `Address` dictates where to **expect** the terminal. A venue may have address
    but that doesn't guarantee the locations of terminals.

User App, is it a terminal ? to which organization it is bound ?
Veris ? Why do we need one ?
Do we really need one ?

Let's follow a slightly different path and try to see our
beloved terminal from a new perspective.

 - Terminal is a standalone Resource.
 - It can be created by any `User`. User may or may not have any organizations.
 - If the User has an `Organization`, he can bind the membership definition using `Rules/Scopes`.
 - Terminal uses Location API across different platforms to update its location.

Let's encounter some cases / doubts:

 - Nested Venues ? Why we made nested venues ? or even venues ?.
    Venues: [group of T] [Hierarchy of T => Lift is accessible to all, but not the Data Center]
        - A group of terminals having same *properties/settings !
        - Give access to child venues and you have access to parent venues.
            Conclusion: for easier access management for `users` & `groups`.

    React Principles to rescue. Let's try Composition instead of Inheritance.
        - A terminal has some resources `Properties/Settings`.
        - Create a Property and assign it to multiple Terminals.
        - Define access and use it for multiple terminals.

    Give N members of X Org access to T Terminals. Done :+1:
    * Only condition: Admin must have access to all :arrow_up: resources.

 - How will Organizations manage Terminals ?
    A `User` having both Organizations & Terminals can define Rules like:
        - Org X & Org Y can manage Terminal T. :+1:
        - Org X can manage T1, T2, T5. Org Y can manage T2 & T3. :+1:

 - Show Nearby Terminals. Done. :+1:

"""

from django.conf import settings
from django.contrib import admin
from django.db import models

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Terminal(models.Model):
    # a user may add N number of terminals
    # let's assume terminal creation is meant to be free
    # we'll think about the business model later
    user = models.ForeignKey(User)

    # let's just keep a name for terminal :)
    name = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return self.name


class TerminalAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


admin.site.register(Terminal, TerminalAdmin)
