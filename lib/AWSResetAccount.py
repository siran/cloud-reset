"""
Reset an AWS account by deleting all resources specified
in a YAML configuration file
"""

import importlib
import os
import yaml
import boto3
import warnings
from pprint import pprint

class AWSResetAccount:
    """ Reset an AWS account by deleting all resources specified
    in a YAML configuration file
    """
    config_file = None
    configuration = None

    resource_instances = {}
    resource_ids = {}

    def __init__(self, config_file):
        self.config_file = config_file
        self.load_configuration()

    def load_configuration(self):
        """ loads the .yml file where resources to be deleted are defined """
        with open(self.config_file) as fh:
            self.configuration = yaml.load(fh, Loader=yaml.FullLoader)

    def get_resources_by_type(self, resource_type):
        """ Gets all the resource ids for a given type of resource """

        module_name = ".".join(['lib','modules',resource_type])
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            warnings.warn(f'{resource_type} has not been implemented.')
            return

        resource_class = getattr(module, 'Resource')
        try:
            resource_instance = resource_class()
        except TypeError as error:
            print(f'Error instantiating class {module_name}: {error.args[0]}')
            return

        self.resource_instances[resource_type] = resource_instance
        ids = resource_instance.get_resources()
        self.resource_ids[resource_type] = ids
        return ids

    def get_resources(self):
        """ Gets all the resource ids defined in the configuration file"""

        resources = list(self.configuration.keys())
        for resource_type in resources:
            print(resource_type)
            ids = self.get_resources_by_type(resource_type) or []

    def list_resources(self):
        """ Pretty print the resource ids that would be deleted """

        self.get_resources()
        pprint(self.resource_ids)

    def delete_resources(self):
        """ Deletes the resource ids """
        self.get_resources()
        print('Resources to be deleted')
        pprint(self.resource_ids)
