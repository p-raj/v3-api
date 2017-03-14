"""
PSSpec
------

Currently the PSSpec resembles CoreAPI a lot.
The difference is the PSSpec is a subset of a CoreAPI.
i.e It only focuses on one URL/Link of the CoreAPI schema.

"""


class PSSpec(object):
    def __init__(self, schema):
        self.schema = schema

    @property
    def host(self):
        return self.schema.get('host')

    @property
    def url(self):
        # assumption -> the schema has been
        # validated before saving :)
        return '{host}{url}'.format(**self.schema)

    @property
    def name(self):
        return self.schema.get('name')

    @property
    def description(self):
        return self.schema.get('description')

    @property
    def action(self):
        return self.schema.get('action')

    @property
    def fields(self):
        fields = self.schema.get('fields', [])
        return fields
