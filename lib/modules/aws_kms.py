from ..BaseResource import BaseResource
import boto3

class Resource(BaseResource):
    name = 'aws_kms'
    type = 'kms'
    client = None
    ids = []

    def __init__(self):
        self.client = boto3.client(self.type)

    def get_resources(self):
        client = self.client
        resources = client.list_aliases()
        ids = []
        for resource in resources['Aliases']:
            # for instance in page['Reservations']:
                self.ids.append(resource['AliasArn'])

        return self.ids

    def list_resources(self):
        pprint()

    def delete_resources(self, ids):
        print('not implemented')

