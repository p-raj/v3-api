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

        tasks.update(**self.__task_start())
        tasks.update(**self.__task_end())
        tasks.update(**self.__task_session_publish())
        tasks.update(**self.__task_session_fetch())
        return tasks

    def get_task_defaults(self):
        return {
            'on-complete': [
                'session.publish'
            ]
        }

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
                'key': str(self.widget.uuid),
                'value': {
                    process_id[:6]: '<% task(process_{process}).result %>'.format(
                        process=process_id[:6]
                    )
                }
            },
            'publish-on-error': {
                'key': str(self.widget.uuid),
                'value': {
                    process_id[:6]: '<% task(process_{process}).result %>'.format(
                        process=process_id[:6]
                    )
                }
            }
        }
        return task

    def __task_start(self):
        return {
            'start': {
                'action': 'std.noop',
                'publish': {
                    'key': str(self.widget.uuid),
                    'value': {
                        'execution': '<% execution().id %>',
                        'template': 'init',
                        'data': {
                            'data.uuid': '<% $.session %>',
                            'data.value': {
                                'key': 'value'
                            }
                        }
                    }
                }
            }
        }

    def __task_end(self):
        return {
            'end': {
                'action': 'std.noop',
                'publish': {
                    'key': str(self.widget.uuid),
                    'value': {
                        'execution': '<% execution().id %>',
                        'template': 'resolved'
                    }
                },
                'on-success': [
                    'succeed'
                ]
            }
        }

    @staticmethod
    def __task_session_publish():
        return {
            'session.publish': {
                'action': 'std.http',
                'input': {
                    'url': 'http://172.20.0.1:8000/api/v1/sessions/<% $.session %>/write/',
                    'method': 'POST',
                    'body': '<% $.value %>',
                    'headers': {
                        'Content-Type': 'application/json',
                        'Key': '<% $.key %>'
                    }
                }
            }
        }

    @staticmethod
    def __task_session_fetch():
        return {
            'session.fetch': {
                'action': 'std.http',
                'input': {
                    'url': 'http://172.20.0.1:8000/api/v1/sessions/<% $.session %>/read/',
                    'method': 'POST',
                    'body': '<% $.value %>',
                    'headers': {
                        'Content-Type': 'application/json',
                        'Key': '<% $.key %>'
                    }
                }
            }
        }
