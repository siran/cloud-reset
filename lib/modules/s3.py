from ..BaseResource import BaseResource
import boto3

class Resource(BaseResource):
    name = 's3'
    type = 's3'
    client = None
    dry_run = True
    configuration = {}
    ids = []
    resources = []

    def __init__(self):
        self.client = boto3.client(self.type)

    def get_resources(self):
        client = self.client
        response = client.list_buckets()
        for resource in response['Buckets']:
            # for instance in page['Reservations']:
                self.ids.append(resource['Name'])
                self.resources.append({
                    "Name": resource['Name'],
                })

        return self.resources

    def list_resources(self):
        pprint()

    def delete_resources(self, ids):
        print(self.configuration)
        for resource_id in self.ids:
            print(f'Delete {resource_id}')
