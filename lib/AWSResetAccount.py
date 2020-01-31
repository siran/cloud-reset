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

    # set to True for security
    dry_run = True

    def __init__(self, config_file):
        self.config_file = config_file
        self.load_configuration()

    def load_configuration(self):
        """ loads the .yml file where resources to be deleted are defined """

        with open(self.config_file) as fh:
            self.configuration = yaml.load(fh, Loader=yaml.FullLoader)

    def instantiate_resource(self, resource_type):
        """ Instantiate the class that manages a certain resource type """

        module_name = ".".join(['lib','modules',resource_type])
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            warnings.warn(f'{resource_type} has not been implemented.')
            return

        resource_class = getattr(module, 'Resource')
        try:
            resource_instance = resource_class()
            resource_instance.dry_run = self.dry_run
        except TypeError as error:
            print(f'Error instantiating class {module_name}: {error.args[0]}')
            return

        self.resource_instances[resource_type] = resource_instance
        return resource_instance

    def get_resources_by_type(self, resource_type):
        """ Gets all the resource ids for a given type of resource """

        if not self.resource_instances.get(resource_type):
            self.instantiate_resource(resource_type)

        resource_instance = self.resource_instances.get(resource_type)
        if not resource_instance:
            return

        resource_instance.get_resources()
        self.resource_ids[resource_type] = resource_instance.ids or []

        return resource_instance.ids or []

    def get_resources(self):
        """ Gets all the resource ids defined in the configuration file"""

        resources = list(self.configuration.keys())
        for resource_type in resources:
            print(f'Loading {resource_type}...')
            if not self.get_resources_by_type(resource_type):
                print(f'Resources of type {resource_type} could not be loaded')

    def list_resources(self):
        """ Pretty print the resource ids that would be deleted """

        self.get_resources()
        pprint(self.resource_ids)

    def confirm(self):
        while True:
            ans = input('Are you sure you want to continue? y/[N]:') or 'N'

            if ans.lower() in ['y', 'n']:
                print(f'You answered {ans}')
                return ans.lower() == 'y'
                break

    def delete_resources_by_type(self, resource_type):
        """ Deletes the resource ids """

        self.get_resources_by_type(resource_type)
        resource_instance = self.resource_instances[resource_type]
        print('Resources to be deleted')
        pprint(self.resource_ids[resource_type])
        if self.confirm():
            resource_instance.delete_resources(
                self.resource_ids[resource_type]
            )
        else:
            print(f'Not deleting {resource_type}...')

    def delete_resources(self):
        resources = list(self.configuration.keys())
        for resource_type in resources:
            self.delete_resources_by_type(resource_type)