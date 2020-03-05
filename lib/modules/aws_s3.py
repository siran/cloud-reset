from ..BaseResource import BaseResource
import boto3

class Resource(BaseResource):
    name = 'aws_s3'
    type = 's3'
    client = None
    dry_run = True
    configuration = {}
    resources = []

    def __init__(self):
        self.client = boto3.client(self.type)
        self.resource = boto3.resource(self.type)

    def get_resources(self):
        """ Gets list of S3 buckets """
        client = self.client
        if self.resources:
            return self.resources

        response = client.list_buckets()
        for resource in response['Buckets']:
            resource_name = resource['Name']
            tags = client.get_bucket_tagging(
                Bucket=resource_name
            )
            self.resources.append({
                "Name": resource_name,
                "Tags": tags.get("TagSet")
            })

        return self.resources

    def list_resources(self):
        pprint(self.resources)

    def delete_bucket_contents(self, bucket):
        if self.check_dry_run():
            return True
        bucket = self.resource.Bucket(bucket)
        bucket.objects.all().delete()
        return True

    def delete_resources(self, resources, options={}):
        for resource in resources:
            bucket_name = resource['Name']
            try:
                if options['force']:
                    self.delete_bucket_contents(bucket_name)
                self.client.delete_bucket(Bucket=bucket_name)
                print(f"Bucket {bucket_name} deleted.")
            except Exception as error:
                if hasattr(error, 'response') and error.response['Error']['Code'] == 'BucketNotEmpty':
                    warning.warn('Bucket not empty and force flag not set.')
                else:
                    raise(error)

