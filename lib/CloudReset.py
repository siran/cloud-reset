"""
Reset an AWS account by deleting all resources specified
in a YAML configuration file
"""

import functools
import importlib
import os
import yaml
import boto3
import re
import sys
import warnings
from pprint import pprint

class CloudReset:
    """ Reset an AWS account by deleting all resources specified
    in a YAML configuration file
    """
    config_file = None
    configuration = None

    resource_instances = {}
    resources = {}

    # set to True for security
    dry_run = True

    def __init__(self, config_file, args=None):
        if not args.profile:
            if (   not os.environ.get("AWS_PROFILE")
                or os.environ["AWS_PROFILE"] == 'default'
                or not re.search('^sandbox', os.environ["AWS_PROFILE"])
            ):
                print("Refusing to run with an empty or default AWS_PROFILE environment variable.")
                print("Please specify a value fot the AWS_PROFILE that will be used to delete resources.")
                print("The profile name must start with the string 'sandbox'.")
                sys.exit(1)

        self.config_file = config_file
        self.load_configuration()

    def load_configuration(self):
        """ Loads the .yml file where resources to be deleted are defined """

        with open(self.config_file) as fh:
            self.configuration = yaml.load(fh, Loader=yaml.FullLoader)

    def run(self):
        """ Run the configuration """

        for block in self.configuration:
            resource_type, options = list(block.items())[0]
            options = options or {}
            self.delete_resources_by_type(resource_type, options)

        print('Finished run!')

    def get_resource_instance(self, resource_type):
        """ Instantiate the class that manages a certain resource type """

        if self.resource_instances.get(resource_type):
            return self.resource_instances.get(resource_type)

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

    def get_resources_by_type(self, resource_type, options = {}):
        """ Gets resources of a given type and applies filters and other options """

        resource_instance = self.get_resource_instance(resource_type)
        if not resource_instance:
            return

        resource_instance.get_resources()

        self.resources = resource_instance.resources
        if options:
            self.filter_resources(options)

    def get_resources(self):
        """ Gets all the resource ids defined in the configuration file"""

        resources_config = list(self.configuration.keys())
        for resource_type in resources_config:
            print(f'Loading {resource_type}...')
            resources = self.get_resources_by_type(resource_type)
            if not resources:
                print(f'Resources of type {resource_type} could not be loaded')

    def filter_resources(self, filter_obj={}):
        """ Calls filter functions for resources of type"""

        resources = self.resources
        filter_types = ['exclude']
        for filter_type in filter_types:
            filters = filter_obj.get(filter_type)
            if not filters:
                continue
            filter_fn = f"filter_{filter_type}"
            if not hasattr(self, filter_fn):
                raise NotImplementedError(f"Filter of type {filter_type} has not been implemented.")
            for filter_expr in filters:
                resources = getattr(self, filter_fn)(resources = resources, filter_expr = filter_expr)

        self.resources = resources

    def filter_exclude(self, filter_expr, resources):
        """ excludes resources by filter options """

        for filter_key, filter_value in filter_expr.items():
            # self.exclude_by_name(filter_value, resources)/
            filter_field = filter_key
            filter_fn = functools.partial(
                getattr(self, f"filter_by"),
                filter_value=filter_value,
                filter_field = filter_field)

            resources = list(filter(filter_fn, resources))

        return resources

    def filter_by(self, resource, filter_value, filter_field):
        """ Returns True/False if resource[filter_field] matches regex `filter_value`. """

        if filter_field == "Name":
            return not self.match_values(expr, resource['Name'])
        elif resource.get("Tags") and filter_field == 'Tag':
            for tag in resource["Tags"]:
                tag_key = tag["Key"]
                tag_value = tag["Value"]
                if filter_value["Key"] == tag_key:
                    return not self.match_values(filter_value["Value"], tag_value)
            return False

    def match_values(self, expression, value):
        """
        Return True if expression == value
            expression (str): if enclosed buy "/" it's interpreted as regex
            value (str): value to compare with
        """
        if expression[0] == '/' and expression[-1] == '/':
            expr = expression[1:-1]
            return bool(re.search(expr, value))
        else:
            return expr == value

    def list_resources(self):
        """ Pretty print the resource ids that would be deleted """

        self.get_resources()
        pprint(self.resources)

    def confirm(self):
        while True:
            ans = input('Are you sure you want to continue? y/[N]:') or 'N'

            if ans.lower() in ['y', 'n']:
                print(f'You answered {ans}')
                return ans.lower() == 'y'
                break

    def delete_resources_by_type(self, resource_type, options={}):
        """ Trigger the deletion of the `resource_type` """

        self.get_resources_by_type(resource_type, options)
        resource_instance = self.resource_instances[resource_type]
        if len(self.resources) == 0:
            print(f'{resource_type}: No resources to be deleted')
            return

        print(f'{resource_type}: Resources to be deleted:')
        pprint(self.resources)
        if not self.dry_run:
            if self.confirm():
                resource_instance.delete_resources(
                    resources=self.resources,
                    options = options.get('options')
                )
            else:
                print(f'Not deleting {resource_type}...')
        else:
            print('Dry run flag set. Not deleting anything.')

    # def delete_resources(self):
    #     resources = list(self.configuration.keys())
    #     for resource_type in resources:
    #         self.delete_resources_by_type(resource_type)