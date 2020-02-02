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
        """ Gets list of S3 buckets """
        client = self.client
        if self.resources:
            return self.resources

        response = client.list_buckets()
        for resource in response['Buckets']:
            # for instance in page['Reservations']:
                self.resources.append({
                    "Name": resource['Name'],
                })

        return self.resources

    def list_resources(self):
        pprint(self.resources)

    def delete_resources(self, resources, options={}):
        for resource in resources:
            bucket_name = resource['Name']
            print(f"Delete {bucket_name}")
            try:
                response = self.client.delete_bucket(Bucket=bucket_name)
            except Exception as error:
                if error.response['Error']['Code'] == 'BucketNotEmpty':
                    if options['force']:
                        print('WIP: delete bucket contents first.')
                    else:
                        warning.warn('Bucket not empty and force flag not set.')

