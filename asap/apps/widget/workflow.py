import functools

from rest_framework.reverse import reverse

from asap.core.workflow import MistralWorkflowBuilder


class WidgetWorkflowBuilder(MistralWorkflowBuilder):
    def __init__(self, widget, *args, **kwargs):
        super(WidgetWorkflowBuilder, self).__init__(*args, **kwargs)
        self.widget = widget

    def get_workflow_name(self):
        return 'widget_{widget}'.format(widget=self.uuid)

    def get_workflow_description(self):
        return self.widget.description

    def get_workflow_type(self):
        return 'direct'

    def get_tasks(self):
        tasks = {
            'process_{process}'.format(process=_.get('uuid')[:6]):
                self.__task_process(self.get_process_id(_))
            for _ in self.processes_json
        }
        publish_process_tasks = {
            'publish_process_{process}'.format(process=_.get('uuid')[:6]):
                self.__task_publish_process_status(self.get_process_id(_))
            for _ in self.processes_json
        }
        change_template_tasks = {
            'change_template_{template}'.format(template=key):
                self.__task_change_visible_template(key)
            for key, value in self.template.items()
        }
        tasks.update(**publish_process_tasks)
        tasks.update(**change_template_tasks)
        return tasks

    def get_workflow_inputs(self):
        return [
            'session'
        ]

    @staticmethod
    def get_process_id(process):
        return process.get('uuid')

    @property
    def uuid(self):
        return self.widget.uuid

    @property
    def rules(self):
        return self.widget.rules

    @property
    def processes_json(self):
        return self.widget.processes_json or []

    @property
    def template(self):
        return self.widget.template or {}

    def __rules_success(self, process_id):
        if not self.rules:
            return []

        assert type(self.rules) == list, \
            'rules need to an array, each rule should have ' \
            '- trigger, ' \
            '- action, ' \
            '- list of conditions'
        return [
            '{process_name} : {rule}'.format(**{
                'process_name': 'process_{0}'.format(_.get('action').get('uuid')[:6]),
                'rule': '<% {0} %>'.format(
                    functools.reduce(
                        lambda c1, c2: '{0} and {1}'.format(c1, c2),
                        _.get('conditions')
                    )
                )
            })
            if _.get('conditions') else
            '{process_name}'.format(**{
                'process_name': 'process_{0}'.format(_.get('action').get('uuid')[:6]),
            })

            for _ in self.rules
            if _.get('trigger').get('uuid') == process_id
        ]

    def __task_process(self, process_id):
        from asap.apps.widget.views.process_service import KEYSTORE_SERVER
        task = {
            'workflow': 'process_reversed',
            'input': {
                'url': '{store}/<% $.session %>/get/'.format(
                    store=KEYSTORE_SERVER
                ),
                'process': 'http://172.20.0.1:8000' + reverse('widget-process-proxy', kwargs={
                    'uuid': self.uuid,
                    'process_uuid': process_id
                }),
                'headers': {
                    'Process': process_id,
                    'Widget': str(self.uuid),
                    'Content-Type': 'application/json'
                }
            },
            'publish': {
                process_id: '<% task(process_{process}).result %>'.format(
                    process=process_id[:6]
                )
            },
            'publish-on-error': {
                process_id: '<% task(process_{process}).result %>'.format(
                    process=process_id[:6]
                )
            },
            'on-success': [
                'publish_process_{process}'.format(process=process_id[:6])
            ],
            'on-error': [
                'publish_process_{process}'.format(process=process_id[:6])
            ]
        }

        rules = self.__rules_success(process_id)
        if rules:
            task['on-success'].append(*rules)
        return task

    def __task_publish_process_status(self, process_id):
        from asap.apps.widget.views.process_service import KEYSTORE_SERVER
        task = {
            'action': 'std.http',
            'input': {
                'url': '{store}/<% $.session %>/set/'.format(
                    store=KEYSTORE_SERVER
                ),
                'headers': {
                    'Process': process_id,
                    'Widget': str(self.uuid),
                    'Content-Type': 'application/json'
                },
                'body': '<% task(process_{process}).result %>'.format(
                    process=process_id[:6]
                )
            }
        }
        return task

    def __task_change_visible_template(self, template_name):
        from asap.apps.widget.views.process_service import KEYSTORE_SERVER
        task = {
            'workflow': 'change_widget_template',
            'input': {
                'url': '{store}/<% $.session %>/set/'.format(
                    store=KEYSTORE_SERVER
                ),
                'template': template_name,
                'widget': str(self.uuid)
            }
        }
        return task
