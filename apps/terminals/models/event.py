"""
Example Events:
    - Terminal Log Created (provided by Veris)

"""
from django.db import models


class Event(models.Model):
    # we could have gone granular, as in
    # resource_name and action [
    #   (org, create )
    #   (org, delete )
    # ]
    # but we will also have cases like send_mail
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
