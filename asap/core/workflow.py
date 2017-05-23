from abc import ABC, abstractmethod


class WorkflowBuilder(ABC):
    """
    Abstract class for all Workflows.
    A Workflow will always have these attributes.
    
     - Version: 
        We may want to change the execution environment, 
        a different parser or maybe a whole new engine like Conductor,
        totally abandoning Mistral.
     - Name
     - Description
     - Type:
        Fork/Join or Direct/Reverse
     - Tasks:
        List of all tasks in the workflow.
        
    FIXME:
        - Currently our terminology/data-structure/... resembles a lot with Mistral, 
        and needs to be generic enough, but not our priority.
        - Also these are being generated directly, 
        there should be an intermediate abstraction.
    """

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_workflow_version(self):
        pass

    @abstractmethod
    def get_workflow_name(self):
        pass

    @abstractmethod
    def get_workflow_description(self):
        pass

    @abstractmethod
    def get_workflow_type(self):
        pass

    @abstractmethod
    def get_workflow_inputs(self):
        pass

    @abstractmethod
    def get_tasks(self):
        pass


class MistralWorkflowBuilder(WorkflowBuilder):
    def __init__(self, *args, **kwargs):
        super(MistralWorkflowBuilder, self).__init__(*args, **kwargs)

    def get_workflow_version(self):
        return '2.0'


class Workflow(object):
    def __init__(self, builder):
        assert isinstance(builder, WorkflowBuilder), \
            'builder must be instance of workflow builder'
        self.builder = builder


class MistralWorkflow(Workflow):
    def __init__(self, builder):
        super(MistralWorkflow, self).__init__(builder)
        assert isinstance(builder, MistralWorkflowBuilder), \
            'builder must be instance of MistralWorkflowBuilder'

    def get_json(self):
        return {
            'version': self.builder.get_workflow_version(),
            self.builder.get_workflow_name(): {
                'description': self.builder.get_workflow_description(),
                'type': self.builder.get_workflow_type(),
                'input': self.builder.get_workflow_inputs(),
                'tasks': self.builder.get_tasks()
            }
        }

    @property
    def json(self):
        import json
        return json.dumps(self.get_json())

    @property
    def yaml(self):
        import yaml
        return yaml.dump(self.get_json())
