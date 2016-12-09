"""
Service ?

We think of orchestrating services. For example:
    - Create a member when user signs up on Terminal
    - Email admins when someone uses Terminal

We need to have a list of Services that can be orchestrated.
This will ultimately be handled by some API Gateway like Kong or Tyk.

Example Service:
    - Organizations & Members (provided by Veris)
    - Terminals (provided by Veris)
    - Invites (provided by Teramatrix)

"""
from django.db import models


class Service(models.Model):
    # name of the service
    # this is meant to be unique as it lists
    # the services we support and makes
    # no sense to list duplicate services :/
    name = models.CharField(max_length=64, unique=True)

    # this model will handle nasty things like
    # client_auth_type (oauth2) or may be some other protocol
    # scopes etc...

    # See: http://stackoverflow.com/a/30441546/1796173
    # Services provided by Veris will trigger web-hooks
    # at least for internal services
    # an organization has been created
    # a member has been added

    def __str__(self):
        return self.name
