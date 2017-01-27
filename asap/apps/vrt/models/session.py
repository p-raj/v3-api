import uuid

from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from asap.apps.vrt.models.runtime import Runtime
from asap.core.models import Timestampable


class Session(Timestampable, models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text=_('A unique identifier for each Session along with Runtime. '
                    'Non-editable, to be generated by system itself.'),
    )

    # session must be associated to a runtime
    runtime = models.ForeignKey(Runtime)

    # to store the session data
    # all the widget data resolved/unresolved will kept in a session
    # as discussed earlier
    # for example: { w1: {}, w2: {} }
    # it seems it will be easier to apply rules if we have this
    data = JSONField(blank=True, null=True, default={})

    # the runtime session may expire as well,
    # for instance the session from the user app may not expire
    # but may expire when initiated via the terminal
    expires_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_expired(self):
        """
        We will not let anyone edited expired sessions.

        :return:
        """
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    def __str__(self):
        return '{0}'.format(self.uuid)

    class Meta:
        unique_together = ('uuid', 'runtime')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    raw_id_fields = ['runtime']
