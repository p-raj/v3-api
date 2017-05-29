"""
PSSpec
------

Currently the PSSpec resembles CoreAPI a lot.
The difference is the PSSpec is a subset of a CoreAPI.
i.e It only focuses on one URL/Link of the CoreAPI schema.

"""
import logging

from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


class PSSpec(object):
    def __init__(self, schema):
        self.schema = schema

    @property
    def host(self):
        return self.schema.get('host')

    @property
    def url_relative(self):
        # assumption -> the schema has been
        # validated before saving :)
        return self.schema.get('url')

    @property
    def name(self):
        return self.schema.get('name')

    @property
    def action(self):
        return self.schema.get('action')

    @property
    def fields(self):
        fields = self.schema.get('fields', [])
        return fields

    @property
    def is_valid(self):
        from asap.apps.process.schema.validator import SchemaValidator
        try:
            SchemaValidator()(self.schema)
            return True
        except ValidationError as e:
            logger.warning(e)
            return False
