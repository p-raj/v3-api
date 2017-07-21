from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reversion.admin import VersionAdmin

from asap.apps.runtime.models.runtime import Runtime
from asap.utils.models import Authorable, Timestampable


class Feedback(Authorable, Timestampable, models.Model):
    app = models.ForeignKey(Runtime)

    rating = models.PositiveIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ], default=0)

    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('author', 'app',)

    def __str__(self):
        return '{0}: {1}'.format(self.rating, self.app)


@admin.register(Feedback)
class FeedbackAdmin(VersionAdmin):
    raw_id_fields = ['author']
    list_display = ('id', 'app', 'rating', 'comment')
    search_fields = ('app', 'comment')
    list_filter = ('rating',)
