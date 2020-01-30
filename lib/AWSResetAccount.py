import importlib
import os
import yaml
import boto3

class AWSResetAccount:
    config_file = None
    configuration = None

    resource_classes = {}

    def __init__(self, config_file):
        self.config_file = config_file
        self.load_configuration()

    def load_configuration(self):
        with open(self.config_file) as fh:
            self.configuration = yaml.load(fh, Loader=yaml.FullLoader)

    def delete_resources(self):
        print("ok")
        pass

    def list_resources(self):
        ids= []
        resources = list(self.configuration.keys())
        for resource_type in resources:
            print(resource_type)
            self_path = os.path.dirname(__file__)
            resource_path = os.path.join(self_path, 'modules', f'{resource_type}.py')
            if not os.path.exists(resource_path):
                print(f'{resource_type} has not been implemented.')
                continue

            module_name = ".".join(['lib','modules',resource_type])
            module = importlib.import_module(module_name)
            resource_class = getattr(module, 'Resource')
            try:
                resource = resource_class()
            except TypeError as error:
                print(f'Error instantiating class {module_name}: {error.args[0]}')

                continue

            self.resource_classes[resource_type] = resource

            ids = resource.get_resources()

        print(ids)
