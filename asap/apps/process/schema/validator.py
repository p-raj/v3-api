from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from asap.apps.process.schema.spec import PSSpec


class SchemaValidator(object):
    def __call__(self, value):
        if type(value) != dict:
            raise ValidationError(
                _('Expect dictionary, got {type}'.format(type=type(value)))
            )

        errors = []

        spec = PSSpec(value)
        if not spec.host:
            errors.append(_('`schema.host` field is required, eg. apis.veris.in'))

        if not spec.url_relative:
            errors.append(_('`schema.url` field is required, eg. /pets/{id}/'))

        if not spec.name:
            errors.append(_('`schema.name` field is required, eg. name of the process'))

        if not spec.action:
            errors.append(_('`schema.action` field is required, eg. get, post..'))

        # TODO:
        # validate each field
        # for field in spec.fields:
        #     errors.append(_('`schema.fields` field is required, eg. apis.veris.in'))

        if errors:
            raise ValidationError(errors)

    def __eq__(self, other):
        return isinstance(other, self.__class__)
