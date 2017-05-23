import requests

from asap.core.workflow import MistralWorkflowBuilder


class RuntimeWorkflowBuilder(MistralWorkflowBuilder):
    def __init__(self, runtime, *args, **kwargs):
        super(RuntimeWorkflowBuilder, self).__init__(*args, **kwargs)
        self.runtime = runtime

    def get_workflow_name(self):
        return 'runtime_{runtime}'.format(runtime=self.uuid)

    def get_workflow_description(self):
        return self.runtime.description

    def get_workflow_type(self):
        return 'reverse'

    def get_tasks(self):
        tasks = {
            self.widget_workflow_task_name(_):
                self.__task_widget(_) for _ in self.widgets
        }
        publish_tasks = {
            self.publish_widget_workflow_task_name(_):
                self.__task_publish_widget_status(_) for _ in self.widgets
        }

        tasks.update(**publish_tasks)
        tasks.update({
            'wait_for_widgets': {
                'requires': [self.publish_widget_workflow_task_name(_) for _ in self.widgets]
            }
        })
        return tasks

    def get_workflow_inputs(self):
        return [
            'session'
        ]

    @property
    def uuid(self):
        return self.runtime.uuid

    @property
    def widget_locker_uuid(self):
        return self.runtime.widget_locker_uuid

    @property
    def widgets(self):
        # FIXME
        # noinspection PyPep8Naming
        WidgetLocker_URL = 'http://172.20.0.1:8000/api/v1/widget-lockers/{wl_uuid}/widgets/'
        response = requests.get(WidgetLocker_URL.format(wl_uuid=self.widget_locker_uuid))

        # move these lame tasks to some place else
        # and make these smart
        return response.json().get('results')

    @staticmethod
    def get_widget_id(widget):
        return widget.get('uuid')[:6]

    @staticmethod
    def widget_workflow_name(widget):
        return 'widget_{widget}'.format(widget=widget.get('uuid'))

    @staticmethod
    def widget_workflow_task_name(widget):
        return 'wait_for_{widget_workflow}'.format(
            widget_workflow=RuntimeWorkflowBuilder.widget_workflow_name(widget)[:13]
        )

    @staticmethod
    def publish_widget_workflow_task_name(widget):
        return 'publish_{widget_workflow}'.format(
            widget_workflow=RuntimeWorkflowBuilder.widget_workflow_name(widget)[:13]
        )

    @staticmethod
    def __task_widget(widget):
        return {
            'workflow': RuntimeWorkflowBuilder.widget_workflow_name(widget),
            'input': {
                'session': '<% $.session %>'
            },
            'publish': {
                'result': '<% task({widget_workflow}).result %>'.format(
                    widget_workflow=RuntimeWorkflowBuilder.widget_workflow_task_name(widget)
                )
            },
            'publish-on-error': {
                'result': '<% task({widget_workflow}).result %>'.format(
                    widget_workflow=RuntimeWorkflowBuilder.widget_workflow_task_name(widget)
                )
            }
        }

    @staticmethod
    def __task_publish_widget_status(widget):
        from asap.apps.widget.views.process_service import KEYSTORE_SERVER
        return {
            'action': 'std.http',
            'input': {
                'method': 'post',
                'url': '{store}/<% $.session %>/set/'.format(
                    store=KEYSTORE_SERVER
                ),
                'body': '<% task({widget_workflow}).result %>'.format(
                    widget_workflow=RuntimeWorkflowBuilder.widget_workflow_task_name(widget)
                ),
                'headers': {
                    'Process': widget.get('uuid'),
                    'Content-Type': 'application/json'
                }
            },
            'requires': [RuntimeWorkflowBuilder.widget_workflow_task_name(widget)]
        }
