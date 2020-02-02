from ..BaseResource import BaseResource
import boto3

class Resource(BaseResource):
    name = 'aws_kms'
    type = 'kms'
    client = None
    dry_run = True
    configuration = {}
    resources = []

    def __init__(self):
        self.client = boto3.client(self.type)

    def get_resources(self):
        client = self.client
        resources = client.list_aliases()
        ids = []
        for resource in resources['Aliases']:
            # for instance in page['Reservations']:
                self.resources.append({
                    "AliasArn": resource['AliasArn'],
                })

        return self.resources

    def list_resources(self):
        pprint(self.resources)

    def delete_resources(self, resources, options={}):
        print('not implemented')

