from ..BaseResource import BaseResource
import boto3

class Resource(BaseResource):
    name = 's3'
    type = 's3'
    client = None
    dry_run = True
    configuration = {}
    resources = []

    def __init__(self):
        self.client = boto3.client(self.type)

    def get_resources(self):
        client = self.client
        response = client.list_buckets()
        for resource in response['Buckets']:
            # for instance in page['Reservations']:
                self.resources.append({
                    "Name": resource['Name'],
                })

        return self.resources

    def list_resources(self):
        pprint(self.resources)

    def delete_resources(self, resources):
        for resource in resources:
            bucket_name = resource['Name']
            print(f"Delete {bucket_name}")
            response = self.client.delete_bucket(Bucket=bucket_name)
