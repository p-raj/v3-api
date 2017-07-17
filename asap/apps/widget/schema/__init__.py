import copy
import json

from rest_framework import response
from rest_framework.reverse import reverse_lazy
from rest_framework_swagger.renderers import OpenAPIRenderer

renderer = OpenAPIRenderer()
context = {
    'response': response.Response()
}

swagger_dict = {
    'swagger': '2.0',
    'info': {
        'title': '',
        'version': '1.0.0'
    },
    'paths': {},
    'definitions': {},
    'securityDefinitions': {}
}


def generate(widget):
    # move these lame tasks to some place else
    # and make these smart
    schema = copy.deepcopy(swagger_dict)

    # update the open API spec title to match the widget uuid
    schema.get('info').update(title=str(widget.uuid))

    # copy the path that the process represents
    # change the path
    for process in widget.processes.all():
        process_schema = json.loads(
            renderer.render(
                process.schema_server, 'application/json', context
            ).decode()
        )
        widget_proxy = reverse_lazy('widget-action', kwargs={
            'widget_uuid': str(widget.uuid),
            'action': process.uuid
        })
        schema['paths'][str(widget_proxy)] = process_schema.get('paths') \
            .get('/api/v1/processes/{0}/execute/'.format(process.uuid))
    return schema
