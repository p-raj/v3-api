import copy
import coreapi

from django.urls import reverse_lazy


class ServerSchema(object):
    def __init__(self, process):
        """
        :type process: asap.apps.process.models.process.Process
        """
        self.process = process
        self.spec = process.spec

    def build(self):
        return self.document

    @property
    def url(self):
        return str(reverse_lazy('process-execute', kwargs={
            'uuid': self.process.uuid
        }))

    @property
    def document(self):
        return coreapi.Document(
            url=self.url,
            title=self.spec.name,
            description=self.process.description,
            media_type='application/json',
            content=self.content
        )

    @property
    def content(self):
        return {str(self.process.uuid): self.link}

    @property
    def link(self):
        return coreapi.Link(
            url=self.url,
            action='post',
            title=self.process.name,
            description=self.process.name,
            fields=self.fields
        )

    @property
    def fields(self):
        # we won't any field/parameter in path
        # :sunglasses: - chaud mode on :P
        fields = copy.deepcopy(self.spec.fields)
        for _ in fields:
            _.update(location='form')

        return [coreapi.Field(**_) for _ in fields]
