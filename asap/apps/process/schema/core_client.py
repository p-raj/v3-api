import coreapi
from django.conf import settings


class ClientSchema(object):
    def __init__(self, spec):
        """
        :type spec: asap.apps.process.schema.spec.PSSpec
        """
        self.spec = spec

    def build(self):
        return self.document

    @property
    def document(self):
        return coreapi.Document(
            url=self.spec.host,
            title=self.spec.name,
            media_type='application/json',
            content=self.content
        )

    @property
    def content(self):
        # TODO
        # the key 'api' is static :/
        return {'api': self.link}

    @property
    def link(self):
        return coreapi.Link(
            url=getattr(settings, 'V3__API_GATEWAY') + self.spec.url_relative,
            action=self.spec.action,
            fields=self.fields
        )

    @property
    def fields(self):
        return [coreapi.Field(**_) for _ in self.spec.fields]

    def validate(self):
        # TODO:
        pass
